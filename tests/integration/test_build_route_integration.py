import subprocess
from fastapi.testclient import TestClient
from app.main import app


def test_build_endpoint_error(monkeypatch):
    def fake_run(cmd, capture_output, text):
        class Result:
            returncode = 1
            stdout = ""
            stderr = "error: expected '}' in body of function"

        return Result()

    monkeypatch.setattr(subprocess, "run", fake_run)
    client = TestClient(app)
    resp = client.post("/factory/test-build", json={"swift": "broken"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is False
    assert "error:" in data["log"]
