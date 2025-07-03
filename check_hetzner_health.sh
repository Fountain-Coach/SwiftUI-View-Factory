#!/bin/bash
set -euo pipefail

# === 🧩 Configuration ===
: "${HETZNER_PORT:=8000}"
: "${HETZNER_HEALTH_PATH:=/health}"
MAX_RETRIES=10
WAIT_SECONDS=2
# ========================

# === 🌐 Resolve HETZNER_IP ===
if [[ -z "${HETZNER_IP:-}" ]]; then
  echo "⚠️  Environment variable HETZNER_IP not set."
  read -rp "👉 Please enter your Hetzner IP: " HETZNER_IP
fi

SERVICE_URL="http://${HETZNER_IP}:${HETZNER_PORT}${HETZNER_HEALTH_PATH}"
echo "🩺 Checking Hetzner health at: $SERVICE_URL"

# === ⏱️ Wait for service to come online ===
for i in $(seq 1 $MAX_RETRIES); do
  if curl -sSf "$SERVICE_URL" > /dev/null; then
    echo "✅ Hetzner service is UP and responding at $SERVICE_URL"
    exit 0
  else
    echo "⏳ Waiting... ($i/$MAX_RETRIES)"
    sleep $WAIT_SECONDS
  fi
done

# === ❌ Fail if unreachable ===
echo "❌ ERROR: Hetzner service did not respond after $MAX_RETRIES attempts."
exit 1
