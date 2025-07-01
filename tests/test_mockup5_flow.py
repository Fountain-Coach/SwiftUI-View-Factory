import json
from app.services.codegen import generate_swift
from app.models.layout import LayoutNode


def test_mockup5_zstack():
    with open("examples/mockup5.layout.json") as f:
        layout = LayoutNode(**json.load(f))

    output = generate_swift(layout)

    assert "ZStack" in output
    assert 'Image("background")' in output
    assert 'Text("Overlay")' in output
