import json
import sys
import types
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app


def test_interpret_endpoint(monkeypatch):
    if "openai" not in sys.modules:
        sys.modules["openai"] = types.SimpleNamespace(
            api_key=None, ChatCompletion=types.SimpleNamespace()
        )
    import openai
    openai.api_key = "test"

    layout_data = {
        "structured": {
            "type": "VStack",
            "children": [
                {"type": "Text", "text": "Welcome"},
                {"type": "Button", "text": "Get Started"},
            ],
        },
        "version": "layout-v1",
    }

    async def fake_acreate(*args, **kwargs):
        return {"choices": [{"message": {"content": json.dumps(layout_data)}}]}

    monkeypatch.setattr(openai.ChatCompletion, "acreate", fake_acreate, raising=False)

    client = TestClient(app)
    with Path("Images/example_app_mockup.jpeg").open("rb") as f:
        resp = client.post(
            "/factory/interpret", files={"file": ("example_app_mockup.jpeg", f, "image/jpeg")}
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["structured"]["type"] == "VStack"
    assert any(c.get("type") == "Text" for c in data["structured"].get("children", []))


def test_interpret_openai_error(monkeypatch):
    if "openai" not in sys.modules:
        sys.modules["openai"] = types.SimpleNamespace(
            api_key=None, ChatCompletion=types.SimpleNamespace()
        )
    import openai
    openai.api_key = "test"

    async def fake_acreate(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(openai.ChatCompletion, "acreate", fake_acreate, raising=False)

    client = TestClient(app)
    with Path("Images/example_app_mockup.jpeg").open("rb") as f:
        resp = client.post(
            "/factory/interpret", files={"file": ("example_app_mockup.jpeg", f, "image/jpeg")}
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == "openai_error"
    assert "boom" in data["message"]
    assert "RuntimeError" in data["detail"]
