from fastapi import APIRouter
from app.services.codegen import generate_swift
from app.models.layout import LayoutNode

router = APIRouter()

@router.post("/generate")
async def generate(layout: LayoutNode):
    return {"swift": generate_swift(layout)}
