import json
from app.services.codegen import generate_swift
from app.models.layout import LayoutNode


def test_mockup4_scrollview_output():
    with open("examples/mockup4.layout.json") as f:
        layout = LayoutNode(**json.load(f))

    output = generate_swift(layout)
    lines = output.splitlines()
    # Ensure ScrollView block is emitted
    assert any(line.strip().startswith("ScrollView") for line in lines)
    assert "Text(\"Item 1\")" in output
    assert "Text(\"Item 2\")" in output
