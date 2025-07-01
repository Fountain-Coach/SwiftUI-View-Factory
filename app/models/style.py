from pydantic import BaseModel
from typing import Optional


class StyleOptions(BaseModel):
    """Styling preferences for code generation."""

    indent: int = 2
    header_comment: bool = True
    font: Optional[str] = None
    color: Optional[str] = None
    spacing: Optional[int] = None
