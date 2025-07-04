# Codex Prompt Showcase: Implementing Handler Stubs

This short guide demonstrates how you can instruct Codex to implement a handler stub. The same pattern can be expanded to multiple stubs when they exist in the repository.

## 1. Identify the Stub

Stub handlers usually contain a `TODO` comment and are listed in `handlers/index.yml`. For example:

```bash
$ grep -n "TODO" handlers/*
handlers/mytask.sh:2:# TODO: implement mytask handler
```

## 2. Prompt Codex to Implement a Single Stub

Provide Codex with the path to the stub and a brief description of what the handler should do. Example prompt:

```text
Please implement the stub at `handlers/mytask.sh`. It should read the request YAML, perform the action, log to the provided directory, and write `status.yml` with `success` or `failure`.
```

Codex will open the file, replace the placeholder code, and commit the working handler.

## 3. Prompt Codex to Implement All Stubs

If several stub scripts are present, you can ask Codex to implement them all in one go. List the files and provide a high‑level instruction:

```text
Implement every handler script that still contains a TODO comment. Each handler receives the request path and log directory. Update `handlers/index.yml` if needed and ensure tests pass.
```

Codex iterates over each stub, fills in the logic, and runs programmatic checks such as `scripts/dispatch.sh --selftest` before creating a pull request.

## 4. Review and Merge

After Codex proposes the implementations, review the changes just like any other pull request. Once merged, the dispatcher will be able to run the new handlers automatically.

See `docs/implementing-handler-stubs.md` for more background on writing handlers.
