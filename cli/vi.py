#!/usr/bin/env python3
import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('image')
def interpret(image):
    print(f"[stub] Interpret image: {image}")

@cli.command()
@click.argument('layout_json')
def generate(layout_json):
    print(f"[stub] Generate SwiftUI code from: {layout_json}")

@cli.command()
@click.argument('swift_file')
def test(swift_file):
    print(f"[stub] Test Swift code: {swift_file}")

if __name__ == '__main__':
    cli()
