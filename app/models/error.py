from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    code: str
    message: str
    detail: Optional[str] = None
    log: Optional[str] = None
