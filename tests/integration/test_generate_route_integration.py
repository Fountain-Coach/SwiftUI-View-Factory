import json
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app


def test_generate_endpoint():
    client = TestClient(app)
    layout = json.loads(Path("examples/mockup1.layout.json").read_text())
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
