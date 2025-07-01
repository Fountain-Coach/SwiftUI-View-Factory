## 🧠 Summary

<!-- Describe what this PR adds or changes. Be concise and clear. -->
This PR implements GPT-4 layout reasoning for the SwiftUI View Factory.

## ✅ Changes

- [x] Added `interpreter.py` logic using `openai.ChatCompletion`
- [x] Updated `/factory/interpret` endpoint
- [x] Included one test case under `tests/test_interpret.py`

## 🔁 Codex Integration

- [ ] Operation ID(s): `interpretLayout`, `generateSwiftUIView`
- [ ] CLI commands: `vi interpret examples/mockup.png`
- [ ] Behavior verified using local API + CLI

## 🧪 How to Test

```bash
uvicorn app.main:app --reload
curl -F 'file=@examples/mockup.png' http://localhost:8000/api/v1/factory/interpret
```

## 📎 Related Issues / Prompts
Closes #1
