from fastapi import APIRouter
from app.services.build import test_build

router = APIRouter()

@router.post("/test-build")
async def build(swift: str):
    success, log = test_build(swift)
    return {"success": success, "log": log}
