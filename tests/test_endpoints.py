import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


def test_placeholder():
    assert True


def test_interpret_mockup1(monkeypatch):
    """Interpretation of mockup1.jpeg should produce expected layout."""

    image_path = Path("examples/mockup1.jpeg")
    if not image_path.is_file():
        pytest.skip("mockup1.jpeg not available")

    # Ensure an 'openai' module is present and patch ChatCompletion.acreate
    import sys
    import types

    if "openai" not in sys.modules:
        sys.modules["openai"] = types.SimpleNamespace(
            api_key=None, ChatCompletion=types.SimpleNamespace()
        )

    import openai

    from app.main import app

    async def fake_acreate(*args, **kwargs):
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "structured": {
                                    "type": "VStack",
                                    "children": [
                                        {"type": "Text", "text": "Welcome"},
                                        {"type": "Button", "text": "Get Started"},
                                    ],
                                },
                                "version": "layout-v1",
                            }
                        )
                    }
                }
            ]
        }

    monkeypatch.setattr(openai.ChatCompletion, "acreate", fake_acreate, raising=False)

    client = TestClient(app)
    with image_path.open("rb") as f:
        response = client.post("/factory/interpret", files={"file": ("mockup1.jpeg", f, "image/jpeg")})

    assert response.status_code == 200
    data = response.json()
    assert data["structured"]["type"] == "VStack"
    children = data["structured"].get("children", [])

    assert any(child["type"] == "Text" and child.get("text") == "Welcome" for child in children)
    assert any(child["type"] == "Button" and child.get("text") == "Get Started" for child in children)
