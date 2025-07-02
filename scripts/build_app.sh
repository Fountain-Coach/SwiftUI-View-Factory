#!/bin/bash
set -euo pipefail

LOG="build.log"
rm -f "$LOG"

# Build any SDK packages first
if [ -d "SDK" ]; then
  for dir in SDK/*; do
    [ -f "$dir/Package.swift" ] || continue
    name=$(basename "$dir")
    echo "Building $name" | tee -a "$LOG"
    (cd "$dir" && xcodebuild -scheme "$name" -configuration Debug build 2>&1 | tee -a ../"$LOG")
  done
fi

# Build the ExampleApp
xcodebuild -scheme ExampleApp -configuration Debug -destination 'platform=iOS Simulator,name=iPhone 15' build 2>&1 | tee -a "$LOG"

# Commit updated build log if it changed
if [ -n "$(git status --porcelain $LOG)" ]; then
  git add "$LOG"
  git commit -m "chore: update build log from latest Xcode build"
  git push origin main
fi
