#!/bin/bash
set -euo pipefail

# Generate layout JSON and Swift views for images in the Images directory.
# Requires the API server to be running and OPENAI_API_KEY if using OpenAI.

if [ "${1:-}" = "--latest" ]; then
  img=$(ls -1t Images/*.{png,jpg,jpeg,JPG,JPEG,PNG} 2>/dev/null | head -n 1 || true)
  if [ -z "$img" ]; then
    echo "No images found" >&2
    exit 0
  fi
  images=("$img")
elif [ "$#" -gt 0 ]; then
  images=("$@")
else
  images=(Images/*.{png,jpg,jpeg,JPG,JPEG,PNG})
fi

for img in "${images[@]}"; do
  [ -e "$img" ] || continue
  base=$(basename "$img")
  name="${base%.*}"
  layout="Layouts/${name}.layout.json"
  view="${name}.swift"

  if [ ! -f "$layout" ]; then
    echo "Interpreting $img"
    if ! python cli/vi.py interpret "$img" > "$layout"; then
      echo "Failed interpreting $img" >&2
      rm -f "$layout"
      continue
    fi
  fi

  if [ ! -f "$view" ]; then
    echo "Generating Swift for $layout"
    if ! python cli/vi.py generate "$layout"; then
      echo "Failed generating Swift for $layout" >&2
      rm -f "$view" GeneratedView.swift 2>/dev/null || true
      continue
    fi
    if [ -f GeneratedView.swift ]; then
      mv GeneratedView.swift "$view"
    fi
  fi

done

# Commit generated files if anything changed
changes=$(git status --porcelain Layouts *.swift 2>/dev/null | wc -l || true)
if [ "$changes" -gt 0 ]; then
  git add Layouts/*.layout.json 2>/dev/null || true
  git add *.swift 2>/dev/null || true
  git commit -m "chore: generate layouts and views from new images"
  git push
fi
