#!/usr/bin/env python3
"""Generate SwiftUI views from UI mockup images."""
import mimetypes
import os
from pathlib import Path

import httpx

API_URL = os.environ.get("FACTORY_URL", "http://localhost:8000")


def process_image(path: Path, output_dir: Path) -> None:
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with path.open("rb") as f:
        resp = httpx.post(
            f"{API_URL}/factory/interpret", files={"file": (path.name, f, mime)}
        )
    resp.raise_for_status()
    layout = resp.json()["structured"]

    resp = httpx.post(
        f"{API_URL}/factory/generate",
        json={"layout": layout, "name": path.stem},
    )
    resp.raise_for_status()
    swift = resp.json()["swift"]

    output_path = output_dir / f"{path.stem}.swift"
    output_path.write_text(swift)


def main(upload_dir: str = "upload", download_dir: str = "download") -> None:
    upload_path = Path(upload_dir)
    download_path = Path(download_dir)
    download_path.mkdir(parents=True, exist_ok=True)

    for file_path in upload_path.iterdir():
        if file_path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            process_image(file_path, download_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate SwiftUI views")
    parser.add_argument("--upload", default="upload", help="Input directory")
    parser.add_argument("--download", default="download", help="Output directory")
    args = parser.parse_args()
    main(args.upload, args.download)
