# Usage: From Prompt to Handler

This document explains how a natural language request is transformed into a structured YAML file and ultimately executed by a handler script. The process follows the "compiler" model outlined in the repository.

## 1. Write a Prompt
A user starts by writing a prompt describing an action or change. For example:

```text
Generate a SwiftUI view that displays a list of users with avatars and names.
```

## 2. Codex Compiles the Prompt
Codex interprets the prompt and creates a YAML request file in `requests/`. A typical request might look like:

```yaml
kind: deploy
spec:
  template: UserList
  data: users.json
```

The `kind` field selects a handler. Additional fields under `spec` provide parameters for that handler.

## 3. Dispatcher Processes Requests
The dispatcher script `scripts/dispatch.sh` scans the `requests/` directory. For each request file:

1. It extracts `kind:` from the YAML.
2. It looks up the matching handler in `handlers/index.yml`.
3. The handler path is executed with the request file and a dedicated log directory under `logs/`.

```
logs/
  <uuid>/
    dispatch.log
    handler.log
    status.yml
```

After execution, the request file is moved to `processed/`.

## 4. Adding New Handlers
If a request uses a `kind` that is not listed in `handlers/index.yml`, you can create a new handler:

1. Place an executable script under `handlers/` (e.g., `handlers/mytask.sh`).
2. Register it in `handlers/index.yml`:

```yaml
mytask: handlers/mytask.sh
```

3. Commit the new script and index entry. The dispatcher will then route future requests with `kind: mytask` to this handler.

## 5. Handler Responsibilities
Handlers receive the request path and log directory as arguments. They must record output in their log file and set an overall status in `status.yml` (either `success`, `failure`, or `error`). See `handlers/deploy.sh` for a simple example.

## Summary
The repository treats Codex like a compiler: natural language prompts are compiled into YAML instructions, which are executed deterministically by handler scripts. You can extend the system by adding new handlers and updating `handlers/index.yml`.
