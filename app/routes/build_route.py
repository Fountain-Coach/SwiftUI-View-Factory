from fastapi import APIRouter
from pydantic import BaseModel
from app.services.build import test_build

router = APIRouter()


class BuildRequest(BaseModel):
    swift: str
    output_binary: bool = False


@router.post("/test-build")
async def build(req: BuildRequest):
    result = test_build(req.swift, output_binary=req.output_binary)

    if req.output_binary and result[0]:
        success, log, artifact = result  # type: ignore[misc]
        return {"success": success, "log": log, "artifact": artifact}

    success, log = result[:2]
    return {"success": success, "log": log}
