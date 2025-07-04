# Running Xcode Builds via Git Orchestration

SwiftUI code requires Apple's proprietary toolchain to compile, which is only
available on macOS. The repository follows a Git-driven dispatcher model where
request files are placed under `requests/` and handler output is committed to
`logs/`. This document explains how the same pattern works for Xcode builds.

## Problem

Xcode and the SwiftUI compiler are closed source and macOS-only. To get real
compiler feedback we must run the build tools on a Mac while still using the
Git orchestrated workflow.

## Solution Strategy

1. **Git-based Orchestration**
   - Requests describing build actions are merged to `main` under `requests/`.
   - Handler output is written to `logs/` and committed back for review.

2. **Local macOS Clone with Xcode**
   - A Mac machine with Xcode installed clones the repository and runs
     `scripts/dispatch.sh` just like any other execution host.
   - The dispatcher processes incoming requests and invokes macOS-specific
     handlers.

3. **Scripted Xcode Build**
   - Handlers use `xcodebuild` (or `swift build`) to compile SwiftUI projects.
     Build logs are captured and stored under `logs/` so the compiler output is
     versioned in Git.

4. **Managing Closed-Source Tools**
   - Although Xcode itself is proprietary, its command-line interface can be
     scripted. The repository does not contain Xcode; it simply triggers the
     tools that are already installed on the Mac runner.

5. **Benefits of the Git Workflow**
   - Compiler warnings and errors are persisted in Git history.
   - Multiple machines can reproduce builds by checking out the same commit and
     running the dispatcher.

## `buildSwiftProject` Handler

A new handler `handlers/buildSwiftProject.py` encapsulates the Xcode invocation.
Requests of `kind: buildSwiftProject` should include a `spec` section with
optional fields:

```yaml
kind: buildSwiftProject
spec:
  workspace: MyApp.xcworkspace   # optional
  project: MyApp.xcodeproj       # optional if workspace is used
  scheme: MyApp                  # Xcode scheme to build
  sdk: macosx                    # or iphonesimulator
  destination: 'generic/platform=macOS'  # passed to xcodebuild
```

The handler composes the appropriate `xcodebuild` command and writes
`xcodebuild.log` and `status.yml` in the log directory.

Run the dispatcher on a Mac with Xcode installed to process such requests and
commit the resulting build logs back to the repository.

## `packageSwiftUIView` Handler

Use this handler to convert loose `.swift` files into a Swift package that can
be opened in Xcode. It runs `swift package init`, copies the specified files,
and archives the directory to `<package_name>.package` in the log folder.

