#!/bin/bash
set -euo pipefail

# === 🧩 CONFIGURATION ===
: "${HETZNER_USER:=codex}"
: "${REMOTE_PATH:=/home/codex/SwiftUI-View-Factory}"
: "${REPO_URL:=https://github.com/Fountain-Coach/SwiftUI-View-Factory.git}"
: "${HETZNER_PORT:=8000}"
: "${HETZNER_HEALTH_PATH:=/health}"
KEY_PATH="$HOME/.ssh/id_codex"
KNOWN_HOSTS="$HOME/.ssh/known_hosts"
MAX_RETRIES=10
WAIT_SECONDS=2

# === ✅ Check for HETZNER_IP safely (no crash) ===
if [[ -z "${HETZNER_IP:-}" ]]; then
  echo "❌ ERROR: HETZNER_IP is not set. You must define it as a Codex secret."
  exit 1
fi

# === 🔐 EXPORT HETZNER_IP FOR ALL FUTURE SHELLS ===
echo "💾 Exporting HETZNER_IP to shell profiles..."
for file in ~/.bashrc ~/.profile ~/.zshrc; do
  if [[ -f "$file" ]]; then
    sed -i '/^export HETZNER_IP=/d' "$file" || true
  fi
  echo "export HETZNER_IP=$HETZNER_IP" >> "$file"
done
export HETZNER_IP

# === 🔑 Generate ephemeral SSH key ===
echo "🔐 [1/6] Generating SSH key..."
ssh-keygen -t ed25519 -N "" -f "$KEY_PATH" <<< y >/dev/null 2>&1

# === 🧾 Add Hetzner to known_hosts ===
echo "🔒 [2/6] Adding Hetzner to known_hosts..."
ssh-keyscan -H "$HETZNER_IP" >> "$KNOWN_HOSTS" 2>/dev/null

# === 🪪 Inject SSH key to Hetzner ===
echo "🚪 [3/6] Copying public key to Hetzner authorized_keys..."
ssh-copy-id -i "${KEY_PATH}.pub" "$HETZNER_USER@$HETZNER_IP"

# === 🛰️ Connect to Hetzner & sync code ===
echo "📡 [4/6] Connecting to Hetzner to clone/pull repo..."
ssh -i "$KEY_PATH" "$HETZNER_USER@$HETZNER_IP" bash <<EOF
set -e

if [ ! -d "$REMOTE_PATH" ]; then
  echo "🆕 Cloning repository from $REPO_URL"
  git clone "$REPO_URL" "$REMOTE_PATH"
else
  echo "🔄 Pulling latest updates from main..."
  cd "$REMOTE_PATH"
  git reset --hard
  git pull origin main
fi

cd "$REMOTE_PATH"
echo "🐳 Running Docker Compose..."
docker compose up -d --build

echo "✅ Hetzner remote environment is live."
EOF

# === 🩺 HEALTH CHECK (curl-based) ===
echo "🩺 [5/6] Checking health of service..."

SERVICE_URL="http://${HETZNER_IP}:${HETZNER_PORT}${HETZNER_HEALTH_PATH}"

for i in $(seq 1 $MAX_RETRIES); do
  if curl -sSf "$SERVICE_URL" > /dev/null; then
    echo "✅ Service is up at $SERVICE_URL"
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
echo "🎉 [6/6] All systems go. Hetzner is synced, running, and healthy."
