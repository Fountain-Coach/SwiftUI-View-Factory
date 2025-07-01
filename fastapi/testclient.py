import asyncio
import inspect
from typing import Any, Dict

from . import UploadFile


class Response:
    def __init__(self, status_code: int, data: Any = None) -> None:
        self.status_code = status_code
        self._data = data

    def json(self) -> Any:
        if hasattr(self._data, "dict"):
            return self._data.dict()
        return self._data


class TestClient:
    def __init__(self, app) -> None:
        self.app = app

    def _call(
        self,
        method: str,
        path: str,
        json: Dict | None = None,
        files: Dict | None = None,
    ):
        func = self.app.routes.get((method, path))
        if func is None:
            return Response(404, None)

        kwargs = {}
        sig = inspect.signature(func)
        params = list(sig.parameters.values())
        if files:
            filename, fileobj, content_type = files["file"]
            upload = UploadFile(filename, fileobj, content_type)
            kwargs[params[0].name] = upload
        elif json is not None:
            ann = params[0].annotation
            if hasattr(ann, "parse_obj"):
                kwargs[params[0].name] = ann.parse_obj(json)
            else:
                kwargs[params[0].name] = json

        if asyncio.iscoroutinefunction(func):
            result = asyncio.run(func(**kwargs))
        else:
            result = func(**kwargs)
        return Response(200, result)

    def get(self, path: str):
        return self._call("GET", path)

    def post(self, path: str, *, json: Dict | None = None, files: Dict | None = None):
        return self._call("POST", path, json=json, files=files)
