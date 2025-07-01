#!/bin/bash
set -euo pipefail
xcodebuild -scheme DragAndDropApp -configuration Debug -destination 'platform=macOS' build 2>&1 | tee build.log

if ! git diff --quiet build.log; then
  git add build.log
  git commit -m "chore: update build log from latest Xcode build"
  git push origin main
fi
