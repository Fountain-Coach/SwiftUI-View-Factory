from pydantic import BaseModel
from typing import Optional, List


class LayoutNode(BaseModel):
    """Node in a layout tree."""

    id: Optional[str] = None
    role: Optional[str] = None
    tag: Optional[str] = None
    type: str
    text: Optional[str] = None
    children: Optional[List['LayoutNode']] = None
    # Conditional layout support
    condition: Optional[str] = None
    then: Optional['LayoutNode'] = None
    else_: Optional['LayoutNode'] = None

    def __init__(self, **data):
        # Map reserved keyword 'else' to 'else_'
        if 'else' in data and 'else_' not in data:
            data['else_'] = data.pop('else')

        children = data.get('children')
        if isinstance(children, list):
            data['children'] = [c if isinstance(c, LayoutNode) else LayoutNode(**c) for c in children]

        then = data.get('then')
        if isinstance(then, dict):
            data['then'] = LayoutNode(**then)

        else_branch = data.get('else_')
        if isinstance(else_branch, dict):
            data['else_'] = LayoutNode(**else_branch)

        super().__init__(**data)

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if 'else_' in data:
            data['else'] = data.pop('else_')
        return data

LayoutNode.update_forward_refs()


class LayoutInterpretationResponse(BaseModel):
    """Response returned from the image interpreter."""

    structured: LayoutNode
    description: Optional[str] = None
    version: str = "layout-v1"

