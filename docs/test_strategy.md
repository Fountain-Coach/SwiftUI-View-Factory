# Xcode Test Strategy

This repository includes Swift packages that build macOS and iOS user interfaces with AppKit or UIKit. To verify they compile correctly, we rely on **xcodebuild**. The build is scripted so that automation tools can inspect compiler results.

## Goals

1. Validate Swift packages compile without errors.
2. Surface compiler diagnostics in CI or local scripts.
3. Keep the process fully local without external dependencies beyond Xcode.

## Running Tests

Use `xcodebuild` directly to build the demo packages. Example invocations:

```bash
xcodebuild \
  -scheme DragAndDropApp \
  -configuration Debug \
  -destination 'platform=macOS' \
  build 2>&1 | tee build.log

xcodebuild \
  -scheme iOSDemoApp \
  -configuration Debug \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  build 2>&1 | tee build.log

xcodebuild \
  -scheme VisionDemoApp \
  -configuration Debug \
  -destination 'platform=visionOS Simulator,name=Apple Vision Pro' \
  build 2>&1 | tee build.log
```

The command pipes all compiler output to `build.log`. The exit code of `xcodebuild` indicates success or failure. Review the log for warnings or errors.

## Automating with a Script

For convenience, create a small script (e.g. `scripts/build_app.sh`). It scans
the `SDK` directory for local Swift packages, builds them first, then builds the
demo applications:

```bash
#!/bin/bash
set -euo pipefail
LOG="build.log"
rm -f "$LOG"

# Build SDK packages
if [ -d "SDK" ]; then
  for dir in SDK/*; do
    [ -f "$dir/Package.swift" ] || continue
    name=$(basename "$dir")
    (cd "$dir" && xcodebuild -scheme "$name" -configuration Debug build 2>&1 | tee -a ../"$LOG")
  done
fi

# Build the demo apps
xcodebuild -scheme DragAndDropApp -configuration Debug -destination 'platform=macOS' build 2>&1 | tee -a "$LOG"
xcodebuild -scheme iOSDemoApp -configuration Debug -destination 'platform=iOS Simulator,name=iPhone 15' build 2>&1 | tee -a "$LOG"
xcodebuild -scheme VisionDemoApp -configuration Debug -destination 'platform=visionOS Simulator,name=Apple Vision Pro' build 2>&1 | tee -a "$LOG"
```

Run the script locally or within your CI pipeline. The output file `build.log` will contain compiler diagnostics. Any build failure stops the script due to `set -e`.

## Interpreting Results

1. **Success** – `xcodebuild` exits with code `0`. Review `build.log` for warnings.
2. **Failure** – a non-zero exit code indicates a compiler error. The offending lines appear in the log.

This approach tests that your AppKit or UIKit code compiles on Apple platforms and provides a machine-readable log for further analysis.
