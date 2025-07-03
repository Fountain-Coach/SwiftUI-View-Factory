#!/bin/bash
set -euo pipefail

# === 🌐 Auto-load environment ===
# Ensure Codex-exported secrets are loaded in any new shell context
if [[ -f ~/.bashrc ]]; then source ~/.bashrc; fi
if [[ -f ~/.profile ]]; then source ~/.profile; fi
if [[ -f ~/.zshrc ]]; then source ~/.zshrc; fi

# === 🧩 Configuration ===
: "${HETZNER_IP:?❌ ERROR: HETZNER_IP is not set. Make sure it's a Codex secret or shell export.}"
: "${HETZNER_PORT:=8000}"
: "${HETZNER_HEALTH_PATH:=/health}"
MAX_RETRIES=10
WAIT_SECONDS=2

SERVICE_URL="http://${HETZNER_IP}:${HETZNER_PORT}${HETZNER_HEALTH_PATH}"
echo "🩺 Checking Hetzner health at: $SERVICE_URL"

# === 🔁 Retry loop ===
for i in $(seq 1 $MAX_RETRIES); do
  if curl -sSf "$SERVICE_URL" > /dev/null; then
    echo "✅ Hetzner service is UP and responding at $SERVICE_URL"
    exit 0
  else
    echo "⏳ Waiting... ($i/$MAX_RETRIES)"
    sleep $WAIT_SECONDS
  fi
done

# === ❌ Timeout failure ===
echo "❌ ERROR: Hetzner service did not respond after $MAX_RETRIES attempts."
exit 1
