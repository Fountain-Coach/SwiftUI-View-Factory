# service/interpreter.py
from fastapi import UploadFile
from app.models.layout import LayoutNode, LayoutInterpretationResponse
import openai
import base64
import json
import os

# Ensure API key is loaded from environment if available
openai.api_key = os.getenv("OPENAI_API_KEY", openai.api_key)

async def interpret_image(file: UploadFile) -> LayoutInterpretationResponse:
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

    try:
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
                        "image_url": {"url": f"data:{file.content_type};base64,{encoded}"},
                    },
                ],
            },
        ]

        # Call OpenAI asynchronously; fall back on error
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
        )

        content = response["choices"][0]["message"]["content"]

        # The model should return JSON. Attempt to parse it.
        data = json.loads(content)

        layout = LayoutNode.parse_obj(data.get("structured", {}))
        description = data.get("description")
        version = data.get("version", "layout-v1")

        return LayoutInterpretationResponse(
            structured=layout,
            description=description,
            version=version,
        )

    except Exception:
        # If anything goes wrong (no API key, parse error, etc.) return fallback
        return fallback
