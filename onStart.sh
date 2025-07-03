#!/bin/bash
set -euo pipefail

# === 🧩 Configuration ===
: "${HETZNER_USER:=codex}"
: "${HETZNER_IP:?❌ ERROR: You must set HETZNER_IP in Codex secrets}"
: "${REMOTE_PATH:=/home/codex/SwiftUI-View-Factory}"
: "${REPO_URL:=https://github.com/Fountain-Coach/SwiftUI-View-Factory.git}"
KEY_PATH="$HOME/.ssh/id_codex"
KNOWN_HOSTS="$HOME/.ssh/known_hosts"
# =========================

# ✅ Export Codex secrets so they're inherited by all shells
export HETZNER_IP

echo "🔐 **[1/6] Generating ephemeral SSH key**"
ssh-keygen -t ed25519 -N "" -f "$KEY_PATH" <<< y >/dev/null 2>&1

echo "🔒 **[2/6] Adding Hetzner to known_hosts**"
ssh-keyscan -H "$HETZNER_IP" >> "$KNOWN_HOSTS" 2>/dev/null

echo "🚪 **[3/6] Injecting SSH public key into Hetzner authorized_keys**"
ssh-copy-id -i "${KEY_PATH}.pub" "$HETZNER_USER@$HETZNER_IP"

echo "📡 **[4/6] Connecting to Hetzner and preparing workspace**"
ssh -i "$KEY_PATH" "$HETZNER_USER@$HETZNER_IP" bash <<EOF
set -e

echo "📁 Checking repo path: $REMOTE_PATH"
if [ ! -d "$REMOTE_PATH" ]; then
  echo "🆕 Cloning repo: $REPO_URL"
  git clone "$REPO_URL" "$REMOTE_PATH"
else
  echo "🔄 Pulling latest from main branch..."
  cd "$REMOTE_PATH"
  git reset --hard
  git pull origin main
fi

cd "$REMOTE_PATH"
echo "🐳 Running docker compose..."
docker compose up -d --build

echo "✅ Remote Hetzner setup complete."
EOF

echo "🎉 **[6/6] Hetzner is live. You may now run ./check_hetzner_health.sh to verify.**"
