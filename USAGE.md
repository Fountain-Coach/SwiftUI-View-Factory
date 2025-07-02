# Usage

## CLI
Run CLI commands locally after installing dependencies:

```bash
pip install -r requirements.txt
python cli/vi.py interpret Images/example_app_mockup.jpeg > Layouts/example_app.layout.json
python cli/vi.py generate Layouts/example_app.layout.json
python cli/vi.py test GeneratedView.swift
```

The `generate` command accepts additional flags to customize the output:

```bash
python cli/vi.py generate Layouts/example_app.layout.json \
  --name HomeView \
  --font title --color blue --spacing 8 \
  --indent 4 --no-header --backend-hooks
```

Add `--verify-build` to compile the generated code before saving:

```bash
python cli/vi.py generate Layouts/example_app.layout.json --verify-build
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
docker run --rm -v $PWD:/app -e OPENAI_API_KEY=... swiftui-factory interpret Images/example_app_mockup.jpeg
```

### FastAPI
```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=... swiftui-factory uvicorn app.main:app --host 0.0.0.0 --port 8000
```
