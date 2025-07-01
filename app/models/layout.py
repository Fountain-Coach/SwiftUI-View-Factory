from pydantic import BaseModel
from typing import Optional, List

class LayoutNode(BaseModel):
    type: str
    text: Optional[str] = None
    children: Optional[List['LayoutNode']] = None

LayoutNode.update_forward_refs()
