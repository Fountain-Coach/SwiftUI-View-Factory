from app.models.layout import LayoutNode
from app.services.codegen import generate_swift


def test_generate_swift_simple():
    layout = LayoutNode(type="VStack", children=[LayoutNode(type="Text", text="Hello")])
    swift = generate_swift(layout)
    # Expect struct and Text line present
    assert "struct GeneratedView" in swift
    assert 'Text("Hello")' in swift
    # Check indentation 2 spaces for Text line (struct line etc). Find the line with Text
    lines = swift.splitlines()
    for line in lines:
        if 'Text("Hello")' in line:
            assert line.startswith(' ' * 4)  # two indentation levels => 4 spaces
            break
    else:
        assert False, "Text line not found"


def test_header_comment_included():
    layout = LayoutNode(type="Text", text="Hi")
    swift = generate_swift(layout)
    assert swift.splitlines()[0].startswith("// Generated")


def test_button_role_submit():
    layout = LayoutNode(type="Button", text="Save", role="submit")
    swift = generate_swift(layout)
    assert 'Button("Save") {}.buttonStyle(.borderedProminent)' in swift


def test_text_readonly_tag():
    layout = LayoutNode(type="Text", text="Readonly", tag="readOnly")
    swift = generate_swift(layout)
    assert 'Text("Readonly").foregroundColor(.gray)' in swift


def test_id_comment_present():
    layout = LayoutNode(type="Text", text="ID", id="node1")
    swift = generate_swift(layout)
    lines = swift.splitlines()
    for i, line in enumerate(lines):
        if 'Text("ID")' in line:
            assert lines[i - 1].strip() == "// id: node1"
            break
    else:
        assert False, "id comment missing"


def test_conditional_node():
    layout = LayoutNode(
        type="Conditional",
        condition="flag",
        then=LayoutNode(type="Text", text="Yes"),
        **{"else": LayoutNode(type="Text", text="No")}
    )
    swift = generate_swift(layout)
    assert "if flag {" in swift
    assert 'Text("Yes")' in swift
    assert '} else {' in swift
    assert 'Text("No")' in swift
