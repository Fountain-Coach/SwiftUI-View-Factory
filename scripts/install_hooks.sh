#!/bin/bash
set -euo pipefail
HOOK_DIR=".git/hooks"
mkdir -p "$HOOK_DIR"
HOOK_PATH="$HOOK_DIR/post-commit"
cat <<'EOL' > "$HOOK_PATH"
#!/bin/bash
scripts/store_logs.sh >/dev/null 2>&1
EOL
chmod +x "$HOOK_PATH"
echo "Post-commit hook installed to capture docker logs."

