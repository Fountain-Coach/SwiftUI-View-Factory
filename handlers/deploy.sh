#!/usr/bin/env bash
set -euo pipefail
request_file="$1"
log_dir="$2"

echo "Deploy handler executed for $request_file" >> "$log_dir/deploy.log"
