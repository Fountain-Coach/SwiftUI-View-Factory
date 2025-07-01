# Docker Guide

Run locally with:

```bash
docker compose up --build
```

Then visit http://localhost:8000/docs to view the API.

The service expects an `OPENAI_API_KEY` either in your shell or in a `.env` file.

You can also use this docker-compose.yml in CI for headless testing.
