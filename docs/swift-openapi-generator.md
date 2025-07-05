# Using Apple's Swift OpenAPI Generator

This repository can generate Swift client libraries from the API description
`api/openapi.yml`. The recommended tool is [apple/swift-openapi-generator](https://github.com/apple/swift-openapi-generator), which plugs into the Swift Package Manager.

## Prerequisites

- A macOS or Linux machine with the Swift toolchain installed
- The `swift-openapi-generator` package checked out or accessible via SwiftPM

## Handler: `generateSwiftClient`

The repository includes a Python handler `generateSwiftClient.py` that prepares
a Swift package using the `swift-openapi-generator` plugin. The handler copies
`api/openapi.yml` into the target's source directory, writes a `Package.swift`
with the required dependencies and plugin, runs `swift build` for immediate
compiler feedback, and finally archives the directory as `<package_name>.package`.

Example request:

```yaml
kind: generateSwiftClient
spec:
  package_name: HelloClient
  module_name: HelloClient
  generator_version: 1.6.0
```

The build output is saved to `build.log` and `status.yml` indicates `success` or
`failure`. The resulting package can be compiled on macOS or Linux where the
plugin resolves the OpenAPI document during the build.

