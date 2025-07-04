#!/usr/bin/env bash
set -euo pipefail
# Locate repository root independent of invocation path
REPO_ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
IMAGE="${DOCKER_IMAGE:-python:3.11-slim}"

# Propagate relevant env vars (OPENAI_API_KEY used by handlers)
ENV_VARS=""
if [[ -n "${OPENAI_API_KEY:-}" ]]; then
  ENV_VARS="-e OPENAI_API_KEY=$OPENAI_API_KEY"
fi

# Execute dispatcher inside container
exec docker run --rm \
    -v "$REPO_ROOT":/repo \
    -w /repo \
    $ENV_VARS \
    "$IMAGE" \
    bash scripts/dispatch.sh "$@"
