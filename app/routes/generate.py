from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.codegen import generate_swift
from app.models.layout import LayoutNode
from app.models.style import StyleOptions

router = APIRouter()


class GenerateRequest(BaseModel):
    """Request model for the ``/generate`` endpoint.

    ``layout`` is accepted as a raw dictionary so that invalid layouts do not
    cause automatic request validation errors.  They can then be handled
    gracefully within the route handler.
    """

    layout: dict
    name: Optional[str] = None
    style: Optional[StyleOptions] = None
    backend_hooks: bool = False


@router.post("/generate")
async def generate(req: GenerateRequest):
    try:
        layout = LayoutNode(**req.layout)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid layout: {exc}")

    style = req.style or StyleOptions()
    if isinstance(style, dict):
        style = StyleOptions(**style)

    return {
        "swift": generate_swift(
            layout,
            style=style.__dict__,
            backend_hooks=req.backend_hooks,
        )
    }
