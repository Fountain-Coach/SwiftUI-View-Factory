import json
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app


def test_generate_endpoint():
    client = TestClient(app)
    layout = json.loads(Path("examples/mockup1.layout.json").read_text())
    resp = client.post("/factory/generate", json=layout)
    assert resp.status_code == 200
    swift = resp.json()["swift"]
    assert "struct GeneratedView" in swift
    assert 'Button("Get Started")' in swift
