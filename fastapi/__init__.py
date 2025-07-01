from typing import Any, Callable, Dict, Tuple
import inspect
import asyncio


class UploadFile:
    def __init__(self, filename: str, file, content_type: str | None = None):
        self.filename = filename
        self.file = file
        self.content_type = content_type

    async def read(self) -> bytes:
        return self.file.read()


def File(default: Any = None):
    return default


class APIRouter:
    def __init__(self) -> None:
        self.routes: Dict[Tuple[str, str], Callable] = {}

    def post(self, path: str):
        def decorator(func: Callable):
            self.routes[("POST", path)] = func
            return func

        return decorator

    def get(self, path: str):
        def decorator(func: Callable):
            self.routes[("GET", path)] = func
            return func

        return decorator


class FastAPI:
    def __init__(self, title: str | None = None) -> None:
        self.title = title
        self.routes: Dict[Tuple[str, str], Callable] = {}
        # minimal openapi endpoint
        @self.get("/openapi.json")
        def _openapi():
            return {"paths": {p: {} for (_, p) in self.routes}}

    def post(self, path: str):
        def decorator(func: Callable):
            self.routes[("POST", path)] = func
            return func

        return decorator

    def get(self, path: str):
        def decorator(func: Callable):
            self.routes[("GET", path)] = func
            return func

        return decorator

    def include_router(self, router: APIRouter, prefix: str = "") -> None:
        for (method, path), func in router.routes.items():
            self.routes[(method, prefix + path)] = func


# testclient is a submodule
from .testclient import TestClient
