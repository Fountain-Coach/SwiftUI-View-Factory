import json
import sys
import types
from pathlib import Path
import subprocess

from fastapi.testclient import TestClient
from app.main import app


def test_mockup1_full_flow(monkeypatch):
    # prepare openai patch
    if "openai" not in sys.modules:
        sys.modules["openai"] = types.SimpleNamespace(
            api_key=None, ChatCompletion=types.SimpleNamespace()
        )
    import openai

    layout_json = json.loads(Path("Layouts/demo_app.layout.json").read_text())

    async def fake_acreate(*args, **kwargs):
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {"structured": layout_json, "version": "layout-v1"}
                        )
                    }
                }
            ]
        }

    monkeypatch.setattr(openai.ChatCompletion, "acreate", fake_acreate, raising=False)

    def fake_run(cmd, capture_output, text):
        class Result:
            returncode = 0
            stdout = "ok"
            stderr = ""

        return Result()

    monkeypatch.setattr(subprocess, "run", fake_run)

    client = TestClient(app)
    with Path("Images/demo_mockup.jpeg").open("rb") as f:
        resp = client.post(
            "/factory/interpret", files={"file": ("demo_mockup.jpeg", f, "image/jpeg")}
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
