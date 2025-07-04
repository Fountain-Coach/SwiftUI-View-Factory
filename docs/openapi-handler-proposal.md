# Proposal: OpenAPI Handlers for the SwiftUI View Factory

This document outlines how to implement request handlers that call the
**SwiftUI View Factory** API described in `api/openapi.yml`. The same approach
applies to any OpenAPI specification.

## Current System Overview

- Requests are placed under `requests/` as YAML files. Each file has a `kind`
  field and arbitrary `spec` data.
- `scripts/dispatch.sh` routes each request to a handler listed in
  `handlers/index.yml`.
- Handlers receive the request path and a log directory. They write logs and a
  `status.yml` file before the dispatcher archives the request under
  `processed/`.

## Handler Strategy

1. **Generate an API client**
   - Use an OpenAPI code generator (e.g., `openapi-python-client`) to create a
     typed client for `api/openapi.yml`.
   - Commit the generated client under `handlers/client/` or vendor it with the
     repository.
   - Alternatively, call the endpoints using `curl` or `requests` with the base
     URL from an environment variable.

2. **Define request kinds**
   - Add new kinds such as `interpret` and `generate` to `handlers/index.yml`.
   - Each kind maps to a handler script (e.g., `handlers/interpret.py`).

3. **Implement the handler scripts**
   - Parse the YAML file to extract parameters.
   - Call the appropriate API endpoint using the generated client or raw HTTP
     requests. For example, `POST /factory/generate` converts a layout into
     SwiftUI code.
   - Capture the HTTP response and write both the raw output and a human summary
     to the log directory.
   - Set `status: success` on HTTP 200 responses; otherwise record `failure`.

4. **Sample request file**

   ```yaml
   kind: generate
   spec:
     layout:
       type: VStack
       children:
         - type: Text
           text: Hello
     name: HelloView
   ```

   Dispatching this file triggers `handlers/generate.py` which calls the
   `/factory/generate` endpoint and writes the resulting Swift code to the log.

## Generalizing to Other OpenAPIs

The same pattern works for any service description:

- Place the OpenAPI spec under `api/`.
- Generate or hand-write a client library.
- Create handler scripts that invoke the desired endpoints.
- Register the handlers in `handlers/index.yml` so the dispatcher can route
  requests by `kind`.

## Benefits

- **Consistency**: All API calls flow through the dispatcher and produce
  structured logs in `logs/`.
- **Extensibility**: Adding new endpoints only requires new handler scripts and
  index entries.
- **Security**: API keys are provided via environment variables so they never
  appear in the repository.

