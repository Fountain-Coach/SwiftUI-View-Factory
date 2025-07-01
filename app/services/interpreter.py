# service/interpreter.py
from fastapi import UploadFile
from app.models.layout import LayoutNode

async def interpret_image(file: UploadFile) -> dict:
    # Stub: replace with OpenAI API call to interpret layout
    return {
        "structured": {
            "type": "VStack",
            "children": [{"type": "Text", "text": "Hello"}]
        },
        "description": "Simple VStack with Hello text",
        "version": "layout-v1"
    }
