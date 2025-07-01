from pydantic import BaseModel
from typing import Optional, List


class LayoutNode(BaseModel):
    type: str
    text: Optional[str] = None
    children: Optional[List['LayoutNode']] = None

LayoutNode.update_forward_refs()


class LayoutInterpretationResponse(BaseModel):
    """Response returned from the image interpreter."""

    structured: LayoutNode
    description: Optional[str] = None
    version: str = "layout-v1"

