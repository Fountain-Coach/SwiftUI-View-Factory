# service/interpreter.py
from fastapi import UploadFile
from app.models import LayoutNode, LayoutInterpretationResponse, ErrorResponse
from pathlib import Path
import openai
import base64
import json
import os
import traceback
from dotenv import load_dotenv
import requests

load_dotenv()

# Ensure API key is loaded from environment if available
openai.api_key = os.getenv("OPENAI_API_KEY")
SECRET_SERVICE_URL = os.getenv("OPENAI_SECRET_SERVICE_URL")

def _fetch_api_key() -> str | None:
    if not SECRET_SERVICE_URL:
        return None
    try:
        resp = requests.get(f"{SECRET_SERVICE_URL}/secret", timeout=5)
        if resp.status_code == 200:
            return resp.json().get("api_key")
    except Exception:
        return None
    return None


async def interpret_image(file: UploadFile) -> LayoutInterpretationResponse | ErrorResponse:
    """Interpret an uploaded UI mockup image into a layout tree.

    The function attempts to use GPT-4 via the OpenAI API to analyse the
    screenshot and return a JSON response matching the
    ``LayoutInterpretationResponse`` schema. If anything fails (e.g. API key is
    missing or the response cannot be parsed) a simple fallback layout is
    returned instead.
    """

    fallback = LayoutInterpretationResponse(
        structured=LayoutNode(
            type="VStack",
            children=[LayoutNode(type="Text", text="Hello")],
        ),
        description="Simple VStack with Hello text",
        version="layout-v1",
    )

    log_data = {}
    try:
        if not openai.api_key:
            openai.api_key = _fetch_api_key() or None
        if not openai.api_key:
            if SECRET_SERVICE_URL:
                hint = (
                    "OPENAI_API_KEY is not set. Tried fetching from "
                    f"{SECRET_SERVICE_URL}/secret but no key was returned. "
                    "Ensure the secret service is running and accessible."
                )
            else:
                hint = (
                    "OPENAI_API_KEY is not set. Provide the key via the "
                    "environment variable or configure OPENAI_SECRET_SERVICE_URL."
                )
            raise RuntimeError(hint)

        # Read and base64 encode the uploaded image for GPT-4 vision models
        content = await file.read()
        encoded = base64.b64encode(content).decode("utf-8")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a service that converts UI screenshots into a JSON layout tree "
                    "matching the LayoutNode schema. Respond only with JSON conforming to "
                    "LayoutInterpretationResponse {structured: LayoutNode, description?: string, version: string}."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Convert this image into a layout tree."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{file.content_type};base64,{encoded}"
                        },
                    },
                ],
            },
        ]
        log_data["request"] = messages

        # Call OpenAI asynchronously; surface errors if any
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
        )
        log_data["response"] = response
        content = response["choices"][0]["message"]["content"]
    except Exception as exc:
        log_data["error"] = str(exc)
        log_json = json.dumps(log_data, indent=2, default=str)
        Path("Layouts").mkdir(exist_ok=True)
        log_path = Path("Layouts") / f"{Path(file.filename).stem}.openai.log"
        log_path.write_text(log_json)
        return ErrorResponse(
            code="openai_error",
            message=f"OpenAI API error: {exc}",
            detail=traceback.format_exc(),
            log=log_json,
        )

    try:
        # The model should return JSON. Attempt to parse it.
        data = json.loads(content)

        layout = LayoutNode.parse_obj(data.get("structured", {}))
        description = data.get("description")
        version = data.get("version", "layout-v1")

        log_json = json.dumps(log_data, indent=2, default=str)
        Path("Layouts").mkdir(exist_ok=True)
        log_path = Path("Layouts") / f"{Path(file.filename).stem}.openai.log"
        log_path.write_text(log_json)

        return LayoutInterpretationResponse(
            structured=layout,
            description=description,
            version=version,
            log=log_json,
        )

    except json.JSONDecodeError as exc:
        log_data["response"] = content
        log_json = json.dumps(log_data, indent=2, default=str)
        Path("Layouts").mkdir(exist_ok=True)
        log_path = Path("Layouts") / f"{Path(file.filename).stem}.openai.log"
        log_path.write_text(log_json)
        return ErrorResponse(
            code="invalid_response",
            message="Failed to parse response from OpenAI",
            detail=str(exc),
            log=log_json,
        )
    except Exception:
        # If anything goes wrong (no API key, parse error, etc.) return fallback
        return fallback
