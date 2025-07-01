# CLI Enhancements and Cross-Platform Samples

1. Extend `cli/vi.py generate` with options to set `--name`, `--backend-hooks`, and style flags (`--font`, `--color`, `--spacing`, `--indent`, `--no-header`).
2. Pass the new options to `/factory/generate` so generated code respects them.
3. Document the additional CLI flags in `USAGE.md` with example commands.
4. Add unit tests under `tests/unit` to ensure CLI arguments are parsed and the request payload is correct.
5. Introduce new golden layouts showcasing `List` and `NavigationStack` under `examples/` and update README references.
6. Create minimal iOS and visionOS demo apps alongside `DragAndDropApp` demonstrating the generated views.
7. Update `docs/test_strategy.md` with build instructions for all sample apps.
