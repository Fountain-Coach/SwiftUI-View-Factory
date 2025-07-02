import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from pathlib import Path
import subprocess

from fastapi.testclient import TestClient
from app.main import app
import openai


def _start_fake_openai(layout_data):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path == "/v1/chat/completions":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                resp = {"choices": [{"message": {"content": json.dumps(layout_data)}}]}
                self.wfile.write(json.dumps(resp).encode())
            else:
                self.send_response(404)
                self.end_headers()

    server = HTTPServer(("localhost", 0), Handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server, thread


def test_mockup1_full_flow(monkeypatch):
    layout_data = json.loads(Path("Layouts/example_app.layout.json").read_text())
    server, thread = _start_fake_openai(layout_data)
    openai.api_key = "test"
    openai.base_url = f"http://localhost:{server.server_port}/v1"

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
            "/factory/interpret", files={"file": ("example_app_mockup.jpeg", f, "image/jpeg")}
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

    server.shutdown()
    thread.join()
