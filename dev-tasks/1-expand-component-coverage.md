# Expand Component Coverage

1. Update `app/models/layout.py` to include additional SwiftUI component types: `List`, `Section`, `NavigationStack`, etc.
2. Modify the OpenAPI spec at `api/openapi.yml` so clients know these components are supported.
3. Extend `generate_swift` in `app/services/codegen.py` to handle the new component types.
4. Write unit tests under `tests/unit` verifying code generation for each new component.
5. Add integration tests ensuring `/factory/generate` correctly handles layouts that include the new components.
