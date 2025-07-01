# Implement Backend Hooks

1. Activate the `backend_hooks` flag in `api/openapi.yml` and document its behavior.
2. Modify `generate_swift` so when `backend_hooks` is true, it injects hooks for analytics or network calls using SwiftUI lifecycle events.
3. Ensure that generated code does not change when the flag is omitted or false.
4. Add examples and unit tests demonstrating backend hook insertion.
