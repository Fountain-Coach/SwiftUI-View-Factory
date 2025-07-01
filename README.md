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

## 🧪 Golden Examples
- **mockup1** – `VStack` with welcome text, logo image and a button
- **mockup2** – `VStack` showing `role` and `tag` metadata on text and button
- **mockup3** – conditional rendering based on `userIsLoggedIn`
- **mockup4** – `ScrollView` listing three text items
- **mockup5** – `ZStack` with a background image and overlay text
- **mockup6** – single `TextField` bound to a state variable
- **mockup7** – grouped input fields inside a `Form`
- **mockup8** – demonstrates backend hooks via `onAppear`

## 🚀 Getting Started
### CLI
```bash
pip install -r requirements.txt
python cli/vi.py interpret path/to/mockup.png
python cli/vi.py generate examples/mockup1.layout.json
python cli/vi.py test GeneratedView.swift
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
    "spacing": 8
  }
}
```

`font` and `color` apply to `Text` and `Button` views while `spacing` controls
stack spacing. All fields are optional.

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

## Docker Support
Build the container image:

```bash
docker build -t swiftui-factory .
```

Run the CLI using Docker:

```bash
docker run --rm -v $PWD:/app -e OPENAI_API_KEY=... swiftui-factory interpret examples/mockup1.jpeg
```

Run the FastAPI server:

```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=... swiftui-factory uvicorn app.main:app --host 0.0.0.0 --port 8000
```

See [USAGE.md](USAGE.md) for more details.

## ✅ CI
- ![CI Status](https://github.com/yourname/SwiftUI-View-Factory/actions/workflows/ci.yml/badge.svg)
- Python 3.11
- Formatter: [black](https://github.com/psf/black)

