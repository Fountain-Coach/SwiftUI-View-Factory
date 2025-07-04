# Packaging SwiftUI Views into a .package

The generated SwiftUI source files need to live in a valid Swift package so Xcode can open and build them. The repository provides the `packageSwiftUIView` handler to automate this step.

## Problem

`xcodebuild` expects a complete Xcode project or Swift Package. The view factory only returns loose `.swift` files. Without a package, the macOS build host has nothing to compile.

## Solution

`packageSwiftUIView` creates a Swift package and archives it as `<name>.package`. The archive can be opened in Xcode on macOS and then compiled using the `buildSwiftProject` handler.

### Request Format

```yaml
kind: packageSwiftUIView
spec:
  package_name: ExampleApp
  files:
    - Logs/request-123/MyView.swift
```

The handler performs these steps:

1. Runs `swift package init --name <package_name> --type executable` in the log directory.
2. Copies each listed Swift file into `Sources/<package_name>/`.
3. Zips the package directory to `<package_name>.package`.
4. Writes `status.yml` with `success` or `failure`.

Use the resulting `.package` file with the `buildSwiftProject` handler on a macOS machine to obtain real compiler feedback.
