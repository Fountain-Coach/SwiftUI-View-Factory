# SwiftUI View Factory

[![CI](https://github.com/yourname/SwiftUI-View-Factory/actions/workflows/ci.yml/badge.svg)](https://github.com/yourname/SwiftUI-View-Factory/actions/workflows/ci.yml)

SwiftUI View Factory converts UI mockups or structured layout trees into production-ready SwiftUI code.

## ✅ Capabilities
- Convert UI mockup images to structured layout trees using GPT-4o
- Generate SwiftUI code from layout trees with metadata and state handling
- Validate generated Swift code builds successfully
- Supports CLI interface: `vi interpret`, `vi generate`, `vi test`
- Includes golden test suite for reproducibility
- Designed for Codex orchestration with behavior-driven examples

## Input Directories
UI mockups belong in the `Images/` folder while structured layout JSON files
reside in `Layouts/`. The CLI commands shown below reference these locations.

Whenever the Factory interacts with OpenAI, the raw request and response are
written to `Layouts/<name>.openai.log`. Any validation failures produce a
corresponding `<name>.error.log` file.

## Supported SwiftUI Components
SwiftUI View Factory focuses on a curated subset of the framework. Only the
following component types are recognized when interpreting or generating layout
trees:

```
VStack
HStack
Text
Image
Button
Spacer
ScrollView
ZStack
Conditional
TextField
Form
List
Section
NavigationStack
```
This list matches the `LayoutNode.type` enumeration in the API schema. Views
outside this set are ignored.

## 🧪 Example App
The repository ships with a single example workflow. A demo mockup image lives
under `Images/`. Use the CLI to interpret the image and generate the SwiftUI
view. The resulting `GeneratedView` is displayed inside the `ExampleApp` Xcode
project.

## 🚀 Getting Started
### CLI
```bash
pip install -r requirements.txt
python cli/vi.py interpret Images/example_app_mockup.jpeg > Layouts/example_app.layout.json
python cli/vi.py generate Layouts/example_app.layout.json
python cli/vi.py test GeneratedView.swift
```
Add `--verify-build` when generating to ensure the Swift code compiles:
```bash
python cli/vi.py generate Layouts/example_app.layout.json --verify-build
```

### Local FastAPI launch
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Visit http://localhost:8000/docs for interactive API docs.

### Styling options
The `/factory/generate` endpoint accepts a `style` object to customize
generated SwiftUI code. Example payload:

```json
{
  "layout": {"type": "VStack", "children": [{"type": "Text", "text": "Hello"}]},
  "style": {
    "indent": 4,
    "header_comment": false,
    "font": "title",
    "color": "red",
    "spacing": 8,
    "bold": true,
    "italic": true,
    "padding": 4,
    "background_color": "blue",
    "corner_radius": 6
  }
}
```

`font` and `color` apply to `Text` and `Button` views while `spacing` controls
stack spacing. Additional options like `bold`, `italic`, `padding`,
`background_color`, and `corner_radius` modify leaf views. All fields are
optional.

### Backend hooks
Enable `backend_hooks` to insert an `.onAppear` block for analytics or network
calls:

```json
{
  "layout": {"type": "Text", "text": "Hello"},
  "backend_hooks": true
}
```
The generated SwiftUI view will contain an `onAppear` modifier with a placeholder
`print` statement so you can wire up your backend SDK.

### Running tests
```bash
pytest
```

### Client SDKs
SwiftUI View Factory looks for Swift packages under the `SDK` directory. Any
package found there is built before the demo applications when running
`scripts/build_app.sh`. Use conditional imports (`#if canImport(...)`) within the
apps to access your SDK at runtime. Compiler diagnostics from these builds are
appended to `build.log` for review.

## Docker Support
Build the container image:

```bash
docker build -t swiftui-factory .
```

Run the CLI using Docker:

```bash
docker run --rm -v $PWD:/app -e OPENAI_API_KEY=... swiftui-factory interpret Images/example_app_mockup.jpeg > Layouts/example_app.layout.json
```

Run the FastAPI server:

```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=... swiftui-factory uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### OpenAI Secret Service

For local development the `docker-compose.yml` file spins up two containers:
the main Factory API and an **OpenAI Secret Service** responsible for
providing the `OPENAI_API_KEY` at runtime. Populate `.env` with your key before
running:

```bash
cp .env.example .env  # edit with your key
docker compose up
```
The Factory container retrieves the key from `http://secret-service:8001/secret`.

Ensure `OPENAI_API_KEY` is set either in `.env` or served from the secret
service so the interpreter can communicate with the real OpenAI API.

See [USAGE.md](USAGE.md) for more details.

## ✅ CI
- ![CI Status](https://github.com/yourname/SwiftUI-View-Factory/actions/workflows/ci.yml/badge.svg)
- Python 3.11
- Formatter: [black](https://github.com/psf/black)
- Automatic image processing: pushes to `Images/` trigger a workflow that
  interprets new mockups into `Layouts/` JSON files and generates Swift views.

