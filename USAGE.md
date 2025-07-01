# Usage

## CLI
Run CLI commands locally after installing dependencies:

```bash
pip install -r requirements.txt
python cli/vi.py interpret path/to/mockup.png
python cli/vi.py generate examples/mockup1.layout.json
python cli/vi.py test GeneratedView.swift
```

## FastAPI
Launch the API locally with Uvicorn:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running via Docker

### CLI
```bash
docker run --rm -v $PWD:/app -e OPENAI_API_KEY=... swiftui-factory interpret examples/mockup1.jpeg
```

### FastAPI
```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=... swiftui-factory uvicorn app.main:app --host 0.0.0.0 --port 8000
```
