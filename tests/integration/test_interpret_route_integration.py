import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app
import openai
import importlib


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


def test_interpret_endpoint_success(monkeypatch):
    layout_data = {
        "structured": {"type": "VStack", "children": [{"type": "Text", "text": "Welcome"}]},
        "version": "layout-v1",
    }
    server, thread = _start_fake_openai(layout_data)
    openai.api_key = "test"
    openai.base_url = f"http://localhost:{server.server_port}/v1"

    client = TestClient(app)
    with Path("Images/example_app_mockup.jpeg").open("rb") as f:
        resp = client.post(
            "/factory/interpret",
            files={"file": ("example_app_mockup.jpeg", f, "image/jpeg")},
        )

    server.shutdown()
    thread.join()

    assert resp.status_code == 200
    data = resp.json()
    assert data["structured"]["type"] == "VStack"
    log_path = Path("Layouts/example_app_mockup.openai.log")
    assert log_path.exists()


def test_interpret_endpoint_missing_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_SECRET_SERVICE_URL", raising=False)
    openai.api_key = None
    import app.services.interpreter as interpreter
    interpreter.SECRET_SERVICE_URL = None
    importlib.reload(interpreter)

    client = TestClient(app)
    with Path("Images/example_app_mockup.jpeg").open("rb") as f:
        resp = client.post(
            "/factory/interpret",
            files={"file": ("example_app_mockup.jpeg", f, "image/jpeg")},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == "openai_error"
    assert "OPENAI_API_KEY is not set" in data["message"]
