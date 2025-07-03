#!/bin/bash
set -euo pipefail

# === 🧩 CONFIGURATION ===
: "${HETZNER_USER:=codex}"
: "${HETZNER_IP:?❌ ERROR: You must set HETZNER_IP as a Codex secret}"
: "${REMOTE_PATH:=/home/codex/SwiftUI-View-Factory}"
: "${REPO_URL:=https://github.com/Fountain-Coach/SwiftUI-View-Factory.git}"
KEY_PATH="$HOME/.ssh/id_codex"
KNOWN_HOSTS="$HOME/.ssh/known_hosts"
# =========================

# === 🔐 EXPORT HETZNER_IP FOR ALL FUTURE SHELLS ===
echo "💾 Exporting HETZNER_IP globally..."
echo "export HETZNER_IP=$HETZNER_IP" >> ~/.bashrc
echo "export HETZNER_IP=$HETZNER_IP" >> ~/.profile
echo "export HETZNER_IP=$HETZNER_IP" >> ~/.zshrc 2>/dev/null || true
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

# === 🛰️ Connect to Hetzner & bootstrap the service ===
echo "📡 [4/6] Connecting to Hetzner and preparing project repo..."
ssh -i "$KEY_PATH" "$HETZNER_USER@$HETZNER_IP" bash <<EOF
set -e

echo "📁 Checking project directory: $REMOTE_PATH"
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

echo "✅ Hetzner remote environment is ready."
EOF

# === ✅ All Done ===
echo "🎉 [6/6] DONE: Hetzner is live and synced. Run ./check_hetzner_health.sh to verify."
