import json
from app.models.layout import LayoutNode


def test_parse_layout_json():
    with open("examples/mockup1.layout.json") as f:
        data = json.load(f)
    layout = LayoutNode(**data)
    assert layout.type == "VStack"
    assert len(layout.children or []) == 3
    assert layout.children[0].type == "Text"


def test_else_alias_handling():
    data = {
        "type": "Conditional",
        "condition": "flag",
        "then": {"type": "Text", "text": "Yes"},
        "else": {"type": "Text", "text": "No"},
    }
    layout = LayoutNode(**data)
    assert getattr(layout, "else_").type == "Text"
    out = layout.dict()
    assert out.get("else", {}).get("text") == "No"
