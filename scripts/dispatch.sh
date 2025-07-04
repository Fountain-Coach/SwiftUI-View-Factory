#!/usr/bin/env bash
set -euo pipefail

INBOX="requests"
OUTBOX="logs"
DONE="processed"
HANDLER_INDEX="handlers/index.yml"
VERSION="0.1.0"

if [[ "${1:-}" == "--version" ]]; then
  echo "$VERSION"
  exit 0
fi

if [[ "${1:-}" == "--selftest" ]]; then
  echo "Dispatcher OK"
  exit 0
fi

mkdir -p "$OUTBOX" "$DONE"

shopt -s nullglob
for req in "$INBOX"/*.yml "$INBOX"/*.yaml; do
  [ -e "$req" ] || continue
  uuid=$(basename "$req")
  base="${uuid%.*}"
  log_dir="$OUTBOX/$base"
  mkdir -p "$log_dir"
  kind=$(grep '^kind:' "$req" | awk '{print $2}')
  handler=$(grep "^$kind:" "$HANDLER_INDEX" | awk '{print $2}')
  if [[ -z "$handler" || ! -x "$handler" ]]; then
    echo "Unknown handler for kind $kind" | tee "$log_dir/error.log"
    echo "status: error" > "$log_dir/status.yml"
    mv "$req" "$DONE/"
    continue
  fi
  echo "Processing $req with $handler" | tee "$log_dir/dispatch.log"
  if "$handler" "$req" "$log_dir" >> "$log_dir/handler.log" 2>&1; then
    echo "status: success" > "$log_dir/status.yml"
  else
    echo "status: failure" > "$log_dir/status.yml"
  fi
  mv "$req" "$DONE/"

done
