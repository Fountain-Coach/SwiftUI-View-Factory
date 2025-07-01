import json
from app.services.codegen import generate_swift
from app.models.layout import LayoutNode


def test_mockup2_generates_enriched_swift():
    with open("examples/mockup2.layout.json") as f:
        layout = LayoutNode(**json.load(f))

    output = generate_swift(layout)

    # Check semantic styling is reflected
    assert 'Text("Welcome Back")' in output
    assert ".foregroundColor(.gray)" in output

    assert 'Button("Submit")' in output
    assert ".buttonStyle(.borderedProminent)" in output
