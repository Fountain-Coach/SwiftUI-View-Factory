# service/interpreter.py
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool
from app.models.layout import LayoutNode
import openai
import base64
import json
from typing import Any, Dict

# Ensure API key is loaded from environment if available
openai.api_key = openai.api_key

async def interpret_image(file: UploadFile) -> Dict[str, Any]:
    """Interpret an uploaded UI mockup image into a layout tree.

    The function attempts to use GPT-4 via the OpenAI API to analyse the
    screenshot and return a JSON response matching the
    ``LayoutInterpretationResponse`` schema. If anything fails (e.g. API key is
    missing or the response cannot be parsed) a simple fallback layout is
    returned instead.
    """

    fallback = {
        "structured": {
            "type": "VStack",
            "children": [{"type": "Text", "text": "Hello"}],
        },
        "description": "Simple VStack with Hello text",
        "version": "layout-v1",
    }

    try:
        # Read and base64 encode the uploaded image for GPT-4 vision models
        content = await file.read()
        encoded = base64.b64encode(content).decode("utf-8")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a service that converts UI screenshots into a JSON layout\n"
                    "tree. Respond only with JSON that conforms to the following\n"
                    "LayoutInterpretationResponse schema:\n"
                    "{structured: LayoutNode, description?: string, version: string}.\n"
                    "LayoutNode fields: {type, text?, children?}."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Interpret this UI mockup into a layout tree.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{file.content_type};base64,{encoded}"},
                    },
                ],
            },
        ]

        # Call OpenAI asynchronously; fall back on error
        response = await openai.ChatCompletion.acreate(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=500,
        )

        content = response["choices"][0]["message"]["content"]

        # The model should return JSON. Attempt to parse it.
        data = json.loads(content)

        # Validate basic structure using LayoutNode
        LayoutNode.parse_obj(data.get("structured", {}))

        # Ensure mandatory fields
        data.setdefault("version", "layout-v1")

        return data

    except Exception:
        # If anything goes wrong (no API key, parse error, etc.) return fallback
        return fallback
