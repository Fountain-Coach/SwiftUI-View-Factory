import json
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app


def test_generate_endpoint():
    client = TestClient(app)
    layout = json.loads(Path("Layouts/example_app.layout.json").read_text())
    resp = client.post("/factory/generate", json={"layout": layout})
    assert resp.status_code == 200
    swift = resp.json()["swift"]
    assert "struct GeneratedView" in swift
    assert 'Button("Get Started")' in swift


def test_generate_endpoint_new_components():
    client = TestClient(app)
    layout = {
        "type": "NavigationStack",
        "children": [
            {
                "type": "List",
                "children": [
                    {
                        "type": "Section",
                        "text": "Header",
                        "children": [{"type": "Text", "text": "Row1"}],
                    }
                ],
            }
        ],
    }

    resp = client.post("/factory/generate", json={"layout": layout})
    assert resp.status_code == 200
    swift = resp.json()["swift"]
    assert "NavigationStack {" in swift
    assert "List {" in swift
    assert 'Section(header: Text("Header"))' in swift


def test_generate_endpoint_with_style():
    client = TestClient(app)
    layout = {"type": "VStack", "children": [{"type": "Text", "text": "Hello"}]}
    resp = client.post(
        "/factory/generate",
        json={
            "layout": layout,
            "style": {"font": "title", "color": "red", "spacing": 5},
        },
    )
    assert resp.status_code == 200
    swift = resp.json()["swift"]
    assert "VStack(spacing: 5)" in swift
    assert ".font(.title)" in swift
    assert ".foregroundColor(.red)" in swift


def test_generate_endpoint_extra_style():
    client = TestClient(app)
    layout = {"type": "Text", "text": "Styled"}
    resp = client.post(
        "/factory/generate",
        json={
            "layout": layout,
            "style": {
                "bold": True,
                "italic": True,
                "padding": 8,
                "background_color": "green",
                "corner_radius": 4,
            },
        },
    )
    assert resp.status_code == 200
    swift = resp.json()["swift"]
    assert ".bold()" in swift
    assert ".italic()" in swift
    assert ".padding(8)" in swift
    assert ".background(Color.green)" in swift
    assert ".cornerRadius(4)" in swift


def test_generate_endpoint_backend_hooks():
    client = TestClient(app)
    layout = {"type": "Text", "text": "Hi"}
    resp = client.post(
        "/factory/generate",
        json={"layout": layout, "backend_hooks": True},
    )
    assert resp.status_code == 200
    swift = resp.json()["swift"]
    assert ".onAppear {" in swift
    assert 'print("Analytics event")' in swift


def test_generate_endpoint_backend_hooks_disabled():
    client = TestClient(app)
    layout = {"type": "Text", "text": "Hi"}
    resp = client.post("/factory/generate", json={"layout": layout})
    assert resp.status_code == 200
    swift = resp.json()["swift"]
    assert ".onAppear {" not in swift


def test_generate_endpoint_scrollview():
    client = TestClient(app)
    layout = {
        "type": "ScrollView",
        "children": [
            {"type": "Text", "text": "Item 1"},
            {"type": "Text", "text": "Item 2"},
        ],
    }
    resp = client.post("/factory/generate", json={"layout": layout})
    assert resp.status_code == 200
    swift = resp.json()["swift"]
    assert "ScrollView {" in swift
    assert 'Text("Item 1")' in swift
    assert 'Text("Item 2")' in swift


def test_generate_endpoint_form():
    client = TestClient(app)
    layout = {
        "type": "Form",
        "children": [
            {"type": "TextField", "text": "Name", "id": "name"},
            {"type": "TextField", "text": "Email", "id": "email"},
        ],
    }
    resp = client.post("/factory/generate", json={"layout": layout})
    assert resp.status_code == 200
    swift = resp.json()["swift"]
    assert "Form {" in swift
    assert 'TextField("Name", text: $name)' in swift
    assert 'TextField("Email", text: $email)' in swift


def test_generate_endpoint_indent_and_header():
    client = TestClient(app)
    layout = {"type": "VStack", "children": [{"type": "Text", "text": "Hi"}]}
    resp = client.post(
        "/factory/generate",
        json={"layout": layout, "style": {"indent": 4, "header_comment": False}},
    )
    assert resp.status_code == 200
    swift = resp.json()["swift"]
    lines = swift.splitlines()
    assert lines[0] == "import SwiftUI"
    assert lines[1].startswith("struct GeneratedView")
    assert lines[2].startswith("    var body")
