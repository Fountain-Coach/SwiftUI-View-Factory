import json
from app.services.codegen import generate_swift
from app.models.layout import LayoutNode


def test_mockup6_textfield_state_binding():
    with open("examples/mockup6.layout.json") as f:
        layout = LayoutNode(**json.load(f))

    output = generate_swift(layout)

    assert '@State private var emailInput: String = ""' in output
    assert 'TextField("Email", text: $emailInput)' in output
