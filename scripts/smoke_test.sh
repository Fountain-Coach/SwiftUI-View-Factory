#!/bin/bash
set -euo pipefail
export OPENAI_API_KEY=${OPENAI_API_KEY:-test}
# Start the app
container_id=$(docker run -d -p 8000:8000 -e OPENAI_API_KEY="$OPENAI_API_KEY" $(docker build -q .))
# Wait for the app to be up
attempts=0
until curl -sf http://localhost:8000/secret >/dev/null || [ $attempts -ge 10 ]; do
  sleep 2
  attempts=$((attempts+1))
  echo "Waiting for app..."
done
# Call endpoints
curl -s -H "Authorization: Bearer $OPENAI_API_KEY" http://localhost:8000/secret > ci-logs/smoke_secret.json
curl -s -X POST http://localhost:8000/factory/generate -H 'Content-Type: application/json' -d '{"layout": {"type": "Text", "text": "Hi"}}' > ci-logs/smoke_generate.json
# Stop container
docker stop "$container_id"
