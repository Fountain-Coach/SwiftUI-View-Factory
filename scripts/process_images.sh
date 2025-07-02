#!/bin/bash
set -euo pipefail

# Generate layout JSON and Swift views for images in the Images directory using
# the FastAPI service. Set ``API_URL`` if the service isn't available at the
# default ``http://localhost:8000``.

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
    if ! python - "$img" "$layout" <<'PY'
import json, pathlib, requests, sys, os
img, layout = sys.argv[1:3]
url = os.environ.get('API_URL', 'http://localhost:8000').rstrip('/') + '/factory/interpret'
with open(img, 'rb') as f:
    try:
        r = requests.post(url, files={'file': f}, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        raise SystemExit(1)
data = r.json()
log = data.pop('log', None)
if log:
    pathlib.Path('Layouts').mkdir(exist_ok=True)
    log_path = pathlib.Path('Layouts') / (pathlib.Path(img).stem + '.openai.log')
    log_path.write_text(log)
with open(layout, 'w') as fh:
    json.dump(data, fh, indent=2)
PY
    then
      echo "Failed interpreting $img" >&2
      rm -f "$layout"
      continue
    fi
  fi

  if [ ! -f "$view" ]; then
    echo "Generating Swift for $layout"
    if ! python - "$layout" "$view" <<'PY'
import json, pathlib, requests, sys, os
layout_file, swift_out = sys.argv[1:3]
url = os.environ.get('API_URL', 'http://localhost:8000').rstrip('/') + '/factory/generate'
try:
    with open(layout_file) as f:
        data = json.load(f)
    if isinstance(data, dict) and 'structured' in data:
        layout = data['structured']
    else:
        layout = data
    r = requests.post(url, json={'layout': layout}, timeout=30)
    r.raise_for_status()
    swift = r.json().get('swift', '')
except Exception as e:
    print(f"Request failed: {e}", file=sys.stderr)
    raise SystemExit(1)
pathlib.Path(swift_out).write_text(swift)
PY
    then
      echo "Failed generating Swift for $layout" >&2
      rm -f "$view" 2>/dev/null || true
      continue
    fi
  fi

done

# Commit generated files if anything changed
changes=$(git status --porcelain Layouts *.swift 2>/dev/null | wc -l || true)
if [ "$changes" -gt 0 ]; then
  git add Layouts/*.layout.json 2>/dev/null || true
  git add Layouts/*.openai.log 2>/dev/null || true
  git add Layouts/*.error.log 2>/dev/null || true
  git add *.swift 2>/dev/null || true
  git commit -m "chore: generate layouts, views, and logs from new images"
  git push
fi
