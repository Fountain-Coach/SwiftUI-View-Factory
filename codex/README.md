# Codex Automation Tasks

This directory contains formal task descriptions for Codex to automate.

## Tasks

### test-openapi.codex.yml

Checks that `/openapi.json` returns a valid OpenAPI schema. It uses `TestClient` to ensure the FastAPI service is operational and responds correctly.

### Docker Integration

You can optionally bring up the FastAPI app in a container:

```bash
docker compose up -d fastapi-app
```

This ensures endpoint availability for integration tests.

---
To run a Codex task, pass the `.codex.yml` to your Codex interpreter or agent.
