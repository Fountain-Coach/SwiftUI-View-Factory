from fastapi import APIRouter, UploadFile, File
from app.services.interpreter import interpret_image

router = APIRouter()


@router.post("/interpret")
async def interpret(file: UploadFile = File(...)):
    return await interpret_image(file)
