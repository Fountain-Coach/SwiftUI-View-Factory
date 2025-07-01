import json
from app.services.codegen import generate_swift
from app.models.layout import LayoutNode


def test_mockup7_form_with_textfields():
    with open("examples/mockup7.layout.json") as f:
        layout = LayoutNode(**json.load(f))

    output = generate_swift(layout)

    assert "Form" in output
    assert 'TextField("Name", text: $nameInput)' in output
    assert 'TextField("Email", text: $emailInput)' in output
    assert '@State private var nameInput: String = ""' in output
    assert '@State private var emailInput: String = ""' in output
