#!/bin/bash
set -euo pipefail
xcodebuild -scheme DragAndDropApp -configuration Debug -destination 'platform=macOS' build 2>&1 | tee build.log
