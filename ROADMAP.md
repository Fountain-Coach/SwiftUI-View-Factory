# 🛣️ SwiftUI View Factory Roadmap

This document outlines the development milestones, features, and goals for the `swiftui-view-factory` service.

---

## ✅ Completed

- [x] OpenAPI spec finalized (`api/openapi.yml`)
- [x] FastAPI service scaffolded and running
- [x] GPT-4o integration for layout interpretation (`interpret_image`)
- [x] SwiftUI code generation with metadata support (`generate_swift`)
- [x] Build testing via `swiftc` (`test_build`)
- [x] CLI interface (`cli/vi.py`)
- [x] Golden test suite in `tests/`
- [x] Codex integration with `codex.yml`
- [x] Golden examples: mockup1–3

---

## 🟡 Milestone: 1.0 Stable Release

### 🔲 Layout Vocabulary
- [ ] Add support for `ZStack`
- [ ] Add support for `ScrollView`
- [ ] Add support for `TextField`, `Form`

### 🔲 Golden Examples
- [ ] Create `mockup4` with `ScrollView` + `TextField`
- [ ] Create `mockup5` with `ZStack` overlays

### 🔲 Robust Build Strategy
- [ ] Lock Swift version
- [ ] Confirm macOS/Linux toolchain compatibility
- [ ] Optional: emit compiled artifact path

### 🔲 Codex & Contributor Guidance
- [ ] Add `CONTRIBUTING.md` with test/golden guidelines
- [ ] Add `codex-instructions.md` to explain behavior contracts

### 🔲 Deployment
- [ ] Add `Dockerfile` and `Makefile` to run full pipeline
- [ ] Confirm GitHub Action for CI passes golden tests

---

## 🏁 1.0 Release Criteria

- `vi interpret | vi generate | vi test` flow works locally
- Golden tests pass
- Codex behavior is aligned with layout rules
- API is stable, layout schema is versioned

---

## 🔮 Future Ideas

- [ ] Component reuse with `id` and `tag` references
- [ ] Style themes and modifiers
- [ ] Backend-aware wiring using `role` hints
- [ ] Swift SDK client generation

---

