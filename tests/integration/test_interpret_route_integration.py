import json
import sys
import types
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app


def test_interpret_endpoint(monkeypatch):
    if "openai" not in sys.modules:
        sys.modules["openai"] = types.SimpleNamespace(AsyncOpenAI=None)
    import openai
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.delenv("OPENAI_SECRET_SERVICE_URL", raising=False)

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

    class FakeResponse:
        def __init__(self, content):
            self._content = content
            self.choices = [types.SimpleNamespace(message=types.SimpleNamespace(content=content))]

        def model_dump(self):
            return {"choices": [{"message": {"content": self._content}}]}

    async def fake_create(*args, **kwargs):
        return FakeResponse(json.dumps(layout_data))

    class FakeClient:
        def __init__(self, *a, **kw):
            self.chat = types.SimpleNamespace(completions=types.SimpleNamespace(create=fake_create))

    monkeypatch.setattr(openai, "AsyncOpenAI", lambda api_key=None: FakeClient(), raising=False)

    client = TestClient(app)
    with Path("Images/example_app_mockup.jpeg").open("rb") as f:
        resp = client.post(
            "/factory/interpret",
            files={"file": ("example_app_mockup.jpeg", f, "image/jpeg")},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["structured"]["type"] == "VStack"
    assert any(c.get("type") == "Text" for c in data["structured"].get("children", []))
    log_path = Path("Layouts/example_app_mockup.openai.log")
    assert log_path.exists()
    log = json.loads(log_path.read_text())
    assert "request" in log


def test_interpret_openai_error(monkeypatch):
    if "openai" not in sys.modules:
        sys.modules["openai"] = types.SimpleNamespace(AsyncOpenAI=None)
    import openai
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.delenv("OPENAI_SECRET_SERVICE_URL", raising=False)

    async def fake_create(*args, **kwargs):
        raise RuntimeError("boom")

    class FakeClient:
        def __init__(self, *a, **kw):
            self.chat = types.SimpleNamespace(completions=types.SimpleNamespace(create=fake_create))

    monkeypatch.setattr(openai, "AsyncOpenAI", lambda api_key=None: FakeClient(), raising=False)

    client = TestClient(app)
    with Path("Images/example_app_mockup.jpeg").open("rb") as f:
        resp = client.post(
            "/factory/interpret",
            files={"file": ("example_app_mockup.jpeg", f, "image/jpeg")},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == "openai_error"
    assert "boom" in data["message"]
    assert "RuntimeError" in data["detail"]
    log_path = Path("Layouts/example_app_mockup.openai.log")
    assert log_path.exists()
    log = json.loads(log_path.read_text())
    assert "error" in log
