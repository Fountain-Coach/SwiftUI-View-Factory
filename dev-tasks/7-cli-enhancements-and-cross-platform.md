# API Enhancements and Cross-Platform Samples

1. Expand `/factory/generate` with options for `name`, `backend_hooks`, and style flags (`font`, `color`, `spacing`, `indent`, `header_comment`).
2. Document these payload fields in `USAGE.md` with example `curl` commands.
3. Add integration tests ensuring the API accepts the parameters and produces the expected Swift.
5. Introduce new golden layouts showcasing `List` and `NavigationStack` under `examples/` and update README references.
6. Create minimal iOS and visionOS demo apps alongside `DragAndDropApp` demonstrating the generated views.
7. Update `docs/test_strategy.md` with build instructions for all sample apps.
