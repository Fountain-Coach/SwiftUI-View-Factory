#!/usr/bin/env python3
"""Generate SwiftUI views by calling the running FastAPI service."""
import asyncio
import json
from pathlib import Path
import mimetypes

import httpx

API_URL = "http://localhost:8000"


async def interpret_image(client: httpx.AsyncClient, path: Path) -> dict:
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with path.open("rb") as f:
        files = {"file": (path.name, f, mime)}
        resp = await client.post(f"{API_URL}/factory/interpret", files=files)
    resp.raise_for_status()
    return resp.json()["structured"]


async def generate_swiftui(client: httpx.AsyncClient, layout: dict, name: str) -> str:
    payload = {"layout": layout, "name": name}
    resp = await client.post(f"{API_URL}/factory/generate", json=payload)
    resp.raise_for_status()
    return resp.json()["swift"]


async def process_file(client: httpx.AsyncClient, path: Path, output_dir: Path) -> None:
    if path.suffix.lower() == ".json":
        with path.open() as f:
            layout = json.load(f)
    else:
        layout = await interpret_image(client, path)
    swift = await generate_swiftui(client, layout, path.stem)
    output_path = output_dir / f"{path.stem}.swift"
    output_path.write_text(swift)


async def run(upload_dir: str = "upload", download_dir: str = "download") -> None:
    upload_path = Path(upload_dir)
    download_path = Path(download_dir)
    download_path.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient(base_url=API_URL) as client:
        for file_path in upload_path.iterdir():
            if file_path.suffix.lower() not in {
                ".json",
                ".png",
                ".jpg",
                ".jpeg",
                ".gif",
                ".webp",
            }:
                continue
            await process_file(client, file_path, download_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate SwiftUI views")
    parser.add_argument("--upload", default="upload", help="Input directory")
    parser.add_argument("--download", default="download", help="Output directory")
    args = parser.parse_args()
    asyncio.run(run(args.upload, args.download))
