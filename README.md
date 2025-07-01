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

### Running tests
```bash
pytest
```

## ✅ CI
- ![CI Status](https://github.com/yourname/SwiftUI-View-Factory/actions/workflows/ci.yml/badge.svg)
- Python 3.11
- Formatter: [black](https://github.com/psf/black)

