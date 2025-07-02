#!/usr/bin/env python3
"""Generate SwiftUI views from layout JSON files in the upload directory."""
import asyncio
import json
from pathlib import Path

from app.main import GenerateRequest, LayoutNode, generate_swiftui_view


def process_file(path: Path, output_dir: Path) -> None:
    with path.open() as f:
        data = json.load(f)
    request = GenerateRequest(layout=LayoutNode(**data), name=path.stem)
    result = asyncio.run(generate_swiftui_view(request))
    output_path = output_dir / f"{path.stem}.swift"
    output_path.write_text(result["swift"])


def main(upload_dir: str = "upload", download_dir: str = "download") -> None:
    upload_path = Path(upload_dir)
    download_path = Path(download_dir)
    download_path.mkdir(parents=True, exist_ok=True)

    for file_path in upload_path.glob("*.json"):
        process_file(file_path, download_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate SwiftUI views")
    parser.add_argument("--upload", default="upload", help="Input directory")
    parser.add_argument("--download", default="download", help="Output directory")
    args = parser.parse_args()
    main(args.upload, args.download)
