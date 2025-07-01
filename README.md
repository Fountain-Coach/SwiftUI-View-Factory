# SwiftUI View Factory

[![CI](https://github.com/yourname/SwiftUI-View-Factory/actions/workflows/ci.yml/badge.svg)](https://github.com/yourname/SwiftUI-View-Factory/actions/workflows/ci.yml)

This service converts UI mockups or layout trees into SwiftUI `View` code.

## Run Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for the API documentation.

This repository is undergoing the final validation sweep for the **1.0** milestone.
