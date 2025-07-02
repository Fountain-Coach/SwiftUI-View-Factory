import importlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

import openai

from app.services import interpreter


def _start_secret_service(api_key):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/secret":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(f'{{"api_key": "{api_key}"}}'.encode())
            else:
                self.send_response(404)
                self.end_headers()

    server = HTTPServer(("localhost", 0), Handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server, thread


def test_fetch_api_key(monkeypatch):
    server, thread = _start_secret_service("secret")
    url = f"http://localhost:{server.server_port}"
    monkeypatch.setenv("OPENAI_SECRET_SERVICE_URL", url)
    importlib.reload(interpreter)
    key = interpreter._fetch_api_key()
    server.shutdown()
    thread.join()
    assert key == "secret"


def test_ensure_api_key_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "envkey")
    monkeypatch.delenv("OPENAI_SECRET_SERVICE_URL", raising=False)
    openai.api_key = None
    importlib.reload(interpreter)
    key = interpreter.ensure_openai_api_key()
    assert key == "envkey"
    assert openai.api_key == "envkey"


def test_ensure_api_key_secret_service(monkeypatch):
    server, thread = _start_secret_service("sskey")
    url = f"http://localhost:{server.server_port}"
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_SECRET_SERVICE_URL", url)
    openai.api_key = None
    importlib.reload(interpreter)
    key = interpreter.ensure_openai_api_key()
    server.shutdown()
    thread.join()
    assert key == "sskey"
    assert openai.api_key == "sskey"


def test_ensure_api_key_missing(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_SECRET_SERVICE_URL", raising=False)
    openai.api_key = None
    importlib.reload(interpreter)
    try:
        interpreter.ensure_openai_api_key()
    except RuntimeError as exc:
        assert "OPENAI_API_KEY is not set" in str(exc)
    else:
        raise AssertionError("RuntimeError not raised")
