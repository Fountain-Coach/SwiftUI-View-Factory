# SwiftUI View Factory

This service converts UI mockups or layout trees into SwiftUI `View` code.

## Run Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for the API documentation.
