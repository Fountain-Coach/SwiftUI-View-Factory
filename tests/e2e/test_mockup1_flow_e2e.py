import json
import sys
import types
from pathlib import Path
import subprocess

from fastapi.testclient import TestClient
from app.main import app


def test_mockup1_full_flow(monkeypatch):
    if "openai" not in sys.modules:
        sys.modules["openai"] = types.SimpleNamespace(AsyncOpenAI=None)
    import openai
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.delenv("OPENAI_SECRET_SERVICE_URL", raising=False)

    layout_data = json.loads(Path("Layouts/example_app.layout.json").read_text())

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

    def fake_run(cmd, capture_output, text):
        class Result:
            returncode = 0
            stdout = "ok"
            stderr = ""

        return Result()

    monkeypatch.setattr(subprocess, "run", fake_run)

    client = TestClient(app)
    with Path("Images/example_app_mockup.jpeg").open("rb") as f:
        resp = client.post(
            "/factory/interpret",
            files={"file": ("example_app_mockup.jpeg", f, "image/jpeg")},
        )
    assert resp.status_code == 200
    layout = resp.json()["structured"]

    resp = client.post("/factory/generate", json={"layout": layout})
    swift = resp.json()["swift"]

    for snippet in ['Text("Welcome")', 'Image("logo")', 'Button("Get Started")']:
        assert snippet in swift

    resp = client.post("/factory/test-build", json={"swift": swift})
    assert resp.status_code == 200
    assert resp.json().get("success") is True
