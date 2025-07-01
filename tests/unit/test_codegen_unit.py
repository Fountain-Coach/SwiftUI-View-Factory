from app.models.layout import LayoutNode
from app.services.codegen import generate_swift


def test_generate_basic_vstack():
    layout = LayoutNode(type="VStack", children=[LayoutNode(type="Text", text="Hello")])
    swift = generate_swift(layout)
    assert "struct GeneratedView" in swift
    assert 'Text("Hello")' in swift


def test_generate_conditional():
    layout = LayoutNode(
        type="Conditional",
        condition="flag",
        then=LayoutNode(type="Text", text="Yes"),
        **{"else": LayoutNode(type="Text", text="No")}
    )
    swift = generate_swift(layout)
    assert "if flag {" in swift
    assert 'Text("Yes")' in swift
    assert "} else {" in swift
    assert 'Text("No")' in swift
