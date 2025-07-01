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


def test_generate_navigation_list_section():
    layout = LayoutNode(
        type="NavigationStack",
        children=[
            LayoutNode(
                type="List",
                children=[
                    LayoutNode(
                        type="Section",
                        text="Header",
                        children=[LayoutNode(type="Text", text="Row1")],
                    )
                ],
            )
        ],
    )

    swift = generate_swift(layout)
    assert "NavigationStack {" in swift
    assert "List {" in swift
    assert 'Section(header: Text("Header"))' in swift
    assert 'Text("Row1")' in swift
