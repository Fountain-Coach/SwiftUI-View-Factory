# SwiftUI View Factory Orchestration

This repository follows the blueprint described in `STRUCTURE_PLAN.md`. The goal is to manage requests that trigger SwiftUI view generation and other tasks through a deterministic Git-based workflow.

## Repository Layout

```text
/                       # Root
├── api/                # OpenAPI specification for the service
├── docs/               # Reference PDFs and additional docs
├── requests/           # Inbox for Codex-written request files
├── processed/          # Archive for handled requests
├── logs/               # Structured execution logs
├── image-upload/       # Mockup images consumed by the factory
├── scripts/            # Dispatcher and helper scripts
├── handlers/           # Individual request handlers
├── codex.repo.yaml     # Orchestration contract
└── README.codex.md     # This file
```

The repository contains all of the directories above. Empty folders include a
`.gitkeep` placeholder so the structure is visible in Git.

## Request Contract

- **Inbox**: `requests/` – Codex places YAML files describing actions here. Each file is moved to `processed/` when handled.
- **Outbox**: `logs/` – Handlers write JSON Lines logs and status files here. These artifacts are committed back to `main`.

Example directory constants from `dispatcher_right.pdf`:

```bash
INBOX="requests"
OUTBOX="logs"
DONE="processed"
```

The dispatcher and Codex behavior are configured through `codex.repo.yaml` at
the repository root. Paths such as `requests/` and `logs/` can be adjusted
there if needed.

## Dispatcher Overview

The dispatcher loop should:

1. Parse request files (YAML validated via `jsonschema`).
2. Route by `kind` to a handler listed in `handlers/index.yml`.
3. Execute handlers in a sandboxed environment, passing secrets via environment variables or files.
4. Ensure idempotence by locking on resource IDs.
5. Log structured output and summaries; handle failures with an exit trap.
6. Commit results back to `main` with retries.
7. Expose `--version` and `--selftest` for health checks.
8. Allow new handlers without modifying the dispatcher.

For more details, see `docs/dispatcher_right.pdf` and `docs/how-codex-acts-like-a-compiler.pdf`.

## Usage

1. The directories above are present in Git with `.gitkeep` files. No setup is required.
2. Run `scripts/dispatch.sh` on the execution host to process requests. The script should watch `requests/` and place logs in `logs/`.
3. Codex writes request YAML files to `requests/` and later reads log files from `logs/`.
4. Place UI mockup images in `image-upload/` and create a request with `kind: processImageUploads` to interpret them.
5. Add new handlers under `handlers/` and update `handlers/index.yml` to register them.
6. Adjust `codex.repo.yaml` if the orchestration paths or policies change.
See `docs/USAGE.md` for a step-by-step overview.

## References

- `docs/dispatcher_right.pdf` – Dispatcher checklist and design notes.
- `docs/how-codex-acts-like-a-compiler.pdf` – Git-based orchestration model.
- `docs/Is “How Codex Acts Like a Compiler” a Hard-Wired Demo or a Generic Repository Blueprint?.pdf` – Discussion of this repository pattern.
