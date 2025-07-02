#!/bin/bash
set -euo pipefail
LOG_DIR="ci-logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/test.log"
# Capture docker-compose logs
if [ -f docker-compose.yml ]; then
  docker-compose logs --no-color > "$LOG_FILE" || true
fi
# Configure git
git config user.name "github-actions"
git config user.email "github-actions@users.noreply.github.com"
# Commit and push logs
if [ -n "$(git status --porcelain $LOG_DIR)" ]; then
  git add "$LOG_DIR"
  git commit -m "Update CI logs" || true
  git push origin HEAD
fi
