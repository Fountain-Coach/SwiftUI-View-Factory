#!/bin/bash
set -euo pipefail

# === 🧩 Configuration ===
: "${HETZNER_USER:=codex}"
: "${HETZNER_IP:?You must set HETZNER_IP in Codex secrets.}"
: "${REMOTE_PATH:=/home/codex/SwiftUI-View-Factory}"
: "${REPO_URL:=https://github.com/Fountain-Coach/SwiftUI-View-Factory.git}"
KEY_PATH="$HOME/.ssh/id_codex"
KNOWN_HOSTS="$HOME/.ssh/known_hosts"
# =========================

echo "🔐 **[1/6] Generating SSH key for this Codex session**"
ssh-keygen -t ed25519 -N "" -f "$KEY_PATH" <<< y >/dev/null 2>&1

echo "🔒 **[2/6] Adding Hetzner to known_hosts**"
ssh-keyscan -H "$HETZNER_IP" >> "$KNOWN_HOSTS" 2>/dev/null

echo "🚪 **[3/6] Injecting public key into Hetzner authorized_keys**"
ssh-copy-id -i "${KEY_PATH}.pub" "$HETZNER_USER@$HETZNER_IP"

echo "📡 **[4/6] Connecting to Hetzner and preparing workspace...**"
ssh -i "$KEY_PATH" "$HETZNER_USER@$HETZNER_IP" bash <<EOF
set -e
echo "📁 Checking repo at $REMOTE_PATH..."

if [ ! -d "$REMOTE_PATH" ]; then
  echo "🆕 Cloning repository from $REPO_URL..."
  git clone "$REPO_URL" "$REMOTE_PATH"
else
  echo "🔄 Pulling latest code in $REMOTE_PATH..."
  cd "$REMOTE_PATH"
  git reset --hard
  git pull origin main
fi

cd "$REMOTE_PATH"

echo "🐳 Launching Docker Compose..."
docker compose up -d --build

echo "✅ Remote setup on Hetzner complete."
EOF

echo "🎉 **[6/6] Done! Hetzner environment is now live and serving your code.**"
