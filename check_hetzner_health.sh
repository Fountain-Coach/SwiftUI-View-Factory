#!/bin/bash
set -euo pipefail

: "${HETZNER_IP:?You must set HETZNER_IP in environment or secrets}"
SERVICE_URL="http://${HETZNER_IP}:8000/health"
MAX_RETRIES=10
WAIT_SECONDS=2

echo "🩺 Checking Hetzner health at $SERVICE_URL..."

for i in $(seq 1 $MAX_RETRIES); do
  if curl -sSf "$SERVICE_URL" > /dev/null; then
    echo "✅ Hetzner service is up and responding."
    exit 0
  else
    echo "⏳ Waiting... ($i/$MAX_RETRIES)"
    sleep $WAIT_SECONDS
  fi
done

echo "❌ ERROR: Hetzner service did not respond in time."
exit 1
