import json
from app.services.codegen import generate_swift
from app.models.layout import LayoutNode

def test_mockup1_generates_expected_swift():
    with open("examples/mockup1.layout.json") as f:
        layout = LayoutNode(**json.load(f))

    output = generate_swift(layout)
    assert "Text(\"Welcome\")" in output
    assert "Button(\"Get Started\")" in output
