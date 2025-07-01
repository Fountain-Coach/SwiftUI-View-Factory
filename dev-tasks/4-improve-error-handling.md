# Improve Error Handling

1. Enhance `app/services/interpreter.py` to surface specific OpenAI API errors with structured messages.
2. Update `app/services/build.py` so `test_build` returns detailed Swift compiler errors instead of only a success flag.
3. Add integration tests verifying that error messages propagate through the `/factory/test-build` endpoint.
