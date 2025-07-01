from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.codegen import generate_swift
from app.models.layout import LayoutNode
from app.models.style import StyleOptions

router = APIRouter()


class GenerateRequest(BaseModel):
    layout: LayoutNode
    name: Optional[str] = None
    style: StyleOptions = StyleOptions()
    backend_hooks: bool = False


@router.post("/generate")
async def generate(req: GenerateRequest):
    layout = req.layout
    if isinstance(layout, dict):
        layout = LayoutNode(**layout)

    style = req.style
    if isinstance(style, dict):
        style = StyleOptions(**style)

    return {
        "swift": generate_swift(
            layout,
            style=style.__dict__,
            backend_hooks=req.backend_hooks,
        )
    }
