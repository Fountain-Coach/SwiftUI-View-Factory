#!/bin/bash
set -euo pipefail

# === 🧩 CONFIGURATION (Public + Simple) ===
HETZNER_IP="120.148.95.115"  # ← your public Hetzner IP here
HETZNER_USER="codex"
REMOTE_PATH="/home/codex/SwiftUI-View-Factory"
REPO_URL="https://github.com/Fountain-Coach/SwiftUI-View-Factory.git"
HETZNER_PORT="8000"
HETZNER_HEALTH_PATH="/health"
KEY_PATH="$HOME/.ssh/id_codex"
KNOWN_HOSTS="$HOME/.ssh/known_hosts"
MAX_RETRIES=10
WAIT_SECONDS=2

# === 🔑 Generate ephemeral SSH key ===
echo "🔐 [1/6] Generating SSH key..."
ssh-keygen -t ed25519 -N "" -f "$KEY_PATH" <<< y >/dev/null 2>&1

# === 🧾 Add Hetzner to known_hosts ===
echo "🔒 [2/6] Adding Hetzner to known_hosts..."
ssh-keyscan -H "$HETZNER_IP" >> "$KNOWN_HOSTS" 2>/dev/null

# === 🪪 Inject SSH key to Hetzner ===
echo "🚪 [3/6] Copying public key to Hetzner authorized_keys..."
ssh-copy-id -i "${KEY_PATH}.pub" "$HETZNER_USER@$HETZNER_IP"

# === 🛰️ Sync Repo on Hetzner ===
echo "📡 [4/6] Connecting to Hetzner to update code..."
ssh -i "$KEY_PATH" "$HETZNER_USER@$HETZNER_IP" bash <<EOF
set -e

if [ ! -d "$REMOTE_PATH" ]; then
  echo "🆕 Cloning repo..."
  git clone "$REPO_URL" "$REMOTE_PATH"
else
  echo "🔄 Pulling latest changes..."
  cd "$REMOTE_PATH"
  git reset --hard
  git pull origin main
fi

cd "$REMOTE_PATH"
echo "🐳 Starting Docker Compose..."
docker compose up -d --build

echo "✅ Hetzner Docker environment is up."
EOF

# === 🩺 HEALTH CHECK ===
echo "🩺 [5/6] Checking health of service..."

SERVICE_URL="http://${HETZNER_IP}:${HETZNER_PORT}${HETZNER_HEALTH_PATH}"

for i in $(seq 1 $MAX_RETRIES); do
  if curl -sSf "$SERVICE_URL" > /dev/null; then
    echo "✅ Service is healthy at $SERVICE_URL"
    break
  else
    echo "⏳ Waiting... ($i/$MAX_RETRIES)"
    sleep $WAIT_SECONDS
  fi
done

if ! curl -sSf "$SERVICE_URL" > /dev/null; then
  echo "❌ ERROR: Service not available after $MAX_RETRIES attempts."
  exit 1
fi

# === ✅ DONE ===
echo "🎉 [6/6] Done! Hetzner is live, synced, running, and healthy."
