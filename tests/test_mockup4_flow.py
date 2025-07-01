import json
from app.services.codegen import generate_swift
from app.models.layout import LayoutNode

def test_mockup4_generates_scrollview():
    with open("examples/mockup4.layout.json") as f:
        layout = LayoutNode(**json.load(f))

    output = generate_swift(layout)

    assert "ScrollView" in output
    assert 'Text("Item 1")' in output
    assert 'Text("Item 2")' in output
    assert 'Text("Item 3")' in output
