#!/usr/bin/env python3
"""Command line interface for interacting with the SwiftUI View Factory API."""

import json
from pathlib import Path
from typing import Optional

import click
import requests

BASE_URL = "http://localhost:8000/api/v1"


@click.group()
@click.option(
    "--server",
    default=BASE_URL,
    show_default=True,
    help="Base URL of the SwiftUI View Factory API",
)
@click.pass_context
def cli(ctx: click.Context, server: str) -> None:
    """Parent CLI group setting the API server base URL."""
    ctx.obj = {"server": server.rstrip("/")}


@cli.command()
@click.argument("image")
@click.pass_obj
def interpret(obj: dict, image: str) -> None:
    """Send ``IMAGE`` to the ``/factory/interpret`` endpoint and print JSON."""

    server: str = obj.get("server", BASE_URL)

    try:
        with open(image, "rb") as f:
            files = {"file": f}
            resp = requests.post(f"{server}/factory/interpret", files=files, timeout=30)
        resp.raise_for_status()
        click.echo(json.dumps(resp.json(), indent=2))
    except FileNotFoundError:
        click.echo(f"File not found: {image}", err=True)
        raise SystemExit(1)
    except requests.RequestException as exc:
        click.echo(f"Request failed: {exc}", err=True)
        raise SystemExit(1)


@cli.command()
@click.argument("layout_json")
@click.option("--name", help="Name for the generated SwiftUI view")
@click.option("--backend-hooks", is_flag=True, help="Insert onAppear hooks")
@click.option("--font", help="Default font to apply")
@click.option("--color", help="Default foreground color")
@click.option("--spacing", type=int, help="Spacing for stack views")
@click.option("--indent", type=int, help="Indentation width")
@click.option("--no-header", is_flag=True, help="Omit header comment")
@click.option(
    "--verify-build",
    is_flag=True,
    help="Compile generated Swift code and only save on success",
)
@click.pass_obj
def generate(
    obj: dict,
    layout_json: str,
    name: Optional[str],
    backend_hooks: bool,
    font: Optional[str],
    color: Optional[str],
    spacing: Optional[int],
    indent: Optional[int],
    no_header: bool,
    verify_build: bool,
) -> None:
    """Load ``LAYOUT_JSON`` and generate SwiftUI code via the API."""

    server: str = obj.get("server", BASE_URL)
    try:
        data = json.loads(Path(layout_json).read_text())
        payload = {"layout": data}
        if name:
            payload["name"] = name

        style: dict = {}
        if font:
            style["font"] = font
        if color:
            style["color"] = color
        if spacing is not None:
            style["spacing"] = spacing
        if indent is not None:
            style["indent"] = indent
        if no_header:
            style["header_comment"] = False
        if style:
            payload["style"] = style
        if backend_hooks:
            payload["backend_hooks"] = True
    except FileNotFoundError:
        click.echo(f"File not found: {layout_json}", err=True)
        raise SystemExit(1)
    except json.JSONDecodeError as exc:
        click.echo(f"Invalid JSON: {exc}", err=True)
        raise SystemExit(1)

    try:
        resp = requests.post(f"{server}/factory/generate", json=payload, timeout=30)
        resp.raise_for_status()
        swift = resp.json().get("swift", "")

        if verify_build:
            try:
                build_resp = requests.post(
                    f"{server}/factory/test-build",
                    json={"swift": swift},
                    timeout=30,
                )
                build_resp.raise_for_status()
                build_data = build_resp.json()
                if not build_data.get("success"):
                    click.echo(build_data.get("log", ""), err=True)
                    raise SystemExit(1)
            except requests.RequestException as exc:
                click.echo(f"Build check failed: {exc}", err=True)
                raise SystemExit(1)

        # Write to root GeneratedView.swift
        Path("GeneratedView.swift").write_text(swift)
        click.echo("Saved GeneratedView.swift")
    except requests.RequestException as exc:
        click.echo(f"Request failed: {exc}", err=True)
        raise SystemExit(1)


@cli.command(name="test")
@click.argument("swift_file")
@click.pass_obj
def test_cmd(obj: dict, swift_file: str) -> None:
    """Send ``SWIFT_FILE`` contents to the ``/factory/test-build`` endpoint."""

    server: str = obj.get("server", BASE_URL)

    try:
        source = Path(swift_file).read_text()
    except FileNotFoundError:
        click.echo(f"File not found: {swift_file}", err=True)
        raise SystemExit(1)

    try:
        resp = requests.post(
            f"{server}/factory/test-build",
            json={"swift": source},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        click.echo(f"Success: {data.get('success')}")
        click.echo(data.get("log", ""))
    except requests.RequestException as exc:
        click.echo(f"Request failed: {exc}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    cli()
