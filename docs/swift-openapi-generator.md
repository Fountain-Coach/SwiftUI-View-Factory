# Using Apple's Swift OpenAPI Generator

This repository can generate Swift client libraries from the API description
`api/openapi.yml`. The recommended tool is [apple/swift-openapi-generator](https://github.com/apple/swift-openapi-generator), which plugs into the Swift Package Manager.

## Prerequisites

- A macOS or Linux machine with the Swift toolchain installed
- The `swift-openapi-generator` package checked out or accessible via SwiftPM

## Handler Idea: `generateSwiftClient`

Add a new handler that invokes `swift-openapi-generator` and archives the
resulting Swift package. A minimal shell script might look like:

```bash
#!/usr/bin/env bash
set -euo pipefail
request_file="$1"
log_dir="$2"

spec="api/openapi.yml"
output_dir="$log_dir/Client"

mkdir -p "$output_dir"

swift run swift-openapi-generator generate "$spec" \
  --output-directory "$output_dir"

zip -r "$log_dir/SwiftClient.zip" "$output_dir"
```

Register the handler in `handlers/index.yml` under a new kind such as
`generateSwiftClient`. Dispatching a request with that kind produces a zipped
client library ready for Xcode or further packaging.

