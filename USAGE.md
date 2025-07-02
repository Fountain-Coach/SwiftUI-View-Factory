# Usage

## FastAPI
Launch the API locally with Uvicorn:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running via Docker
### FastAPI
```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=... swiftui-factory uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Process an image with ``curl`` once the server is running:

```bash
curl -f -F file=@Images/example_app_mockup.jpeg \
  http://localhost:8000/factory/interpret \
  > Layouts/example_app.layout.json
curl -f -H 'Content-Type: application/json' \
  -d @Layouts/example_app.layout.json \
  http://localhost:8000/factory/generate | jq -r .swift > GeneratedView.swift
```
