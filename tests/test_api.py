import os
from fastapi.testclient import TestClient
import pytest

from app.main import app

client = TestClient(app)


def test_get_openai_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    response = client.get("/secret")
    assert response.status_code == 200
    assert response.json() == {"api_key": "test-key"}


def test_interpret_layout(tmp_path):
    file_path = tmp_path / "mock.png"
    file_path.write_bytes(b"fake")
    with file_path.open("rb") as f:
        response = client.post("/factory/interpret", files={"file": ("mock.png", f, "image/png")})
    assert response.status_code == 200
    data = response.json()
    assert data["structured"]["type"] == "VStack"


def test_generate_swiftui_view():
    payload = {
        "layout": {"type": "Text", "text": "Hello"},
        "name": "MyView"
    }
    response = client.post("/factory/generate", json=payload)
    assert response.status_code == 200
    assert "struct MyView" in response.json()["swift"]
