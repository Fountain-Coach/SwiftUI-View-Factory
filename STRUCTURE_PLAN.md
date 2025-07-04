# Repository Structure Plan

This plan is based on the guidance from the PDF documents in `docs/`:
- **dispatcher_right.pdf** – outlines a checklist & blueprint for a robust dispatcher loop
- **how-codex-acts-like-a-compiler.pdf** – describes a Git-based orchestration model
- **Is "How Codex Acts Like a Compiler" a Hard-Wired Demo or a Generic Repository Blueprint?.pdf** – clarifies that the pattern is intended to be reusable

## Goals
1. Provide a deterministic Git-driven workflow where requests are merged to `main` and executed by a dispatcher on a target machine.
2. Capture execution output in a structured, machine-readable way.
3. Keep the repository extensible so new request types and handlers can be added without rewriting the dispatcher.

## Top-level Layout
```
/                      # Root of the repo
├── api/               # OpenAPI specification for the SwiftUI View Factory service
├── docs/              # Reference PDFs and additional documentation
├── requests/          # Inbox for Codex-written request files
├── processed/         # Archive for handled requests
├── logs/              # Structured execution logs
├── scripts/           # Helper scripts invoked by the dispatcher
├── handlers/          # Individual request handlers (shell or Python)
├── codex.repo.yaml    # Declarative config describing the orchestration contract
└── README.codex.md    # Human & Codex-readable overview of the system
```

## Request Contract
- **Inbox**: `requests/` – each file contains YAML describing an action. Once read, the dispatcher moves the file into `processed/` (or embeds a UUID).
- **Outbox**: `logs/` – each execution produces a JSON Lines log and a small status file. These artifacts are committed back to `main`.

Example constants from *dispatcher_right.pdf*:
```bash
INBOX="requests"
OUTBOX="logs"
DONE="processed"
```

## Dispatcher Outline
Following the checklist in *dispatcher_right.pdf*, the dispatcher should:
1. **Parse** request files into a canonical structure (start with YAML; validate with `jsonschema`).
2. **Route** the request `kind` to a handler in `handlers/`. The mapping is discoverable at runtime (e.g., via `handlers/index.yml`).
3. **Execute** the handler in a sandboxed environment (non-root user, bounded by `timeout` or containers). Pass secrets via environment variables or mounted files.
4. **Ensure Idempotence** – serialize by resource using `flock` on a resource ID and make handlers safely re-runnable.
5. **Log** structured output (`JSONL`) and human-readable summaries. Use an exit trap to record failures and bump Prometheus counters.
6. **Commit & Push** the log and status file back to `main` in a back-off loop.
7. **Expose Health** via `--version` and `--selftest`; optionally run under `systemd` or a Kubernetes probe.
8. **Allow Extensibility** – new handlers are dropped in `handlers/` and referenced in the router table without modifying dispatcher logic.

## codex.repo.yaml Example
As suggested in *how-codex-acts-like-a-compiler.pdf*:
```yaml
repo:
  purpose: infrastructure-orchestration
  strategy: git-merge-execution
codex:
  deploy_trigger_path: requests/
  deploy_output_path: logs/
  mainline_branch: main
  enforce_merge_before_execution: true
  cleanup_after_success: true
```

## README.codex.md Checklist
- Document the role of each folder (`requests/`, `logs/`, `processed/`, etc.).
- Explain how to run the dispatcher loop on the execution host.
- Describe how Codex should format request files and where it can find logs.
- Provide instructions for adding new handlers or adjusting `codex.repo.yaml`.

## Next Steps
1. Create the directories and placeholder `.gitkeep` files so the structure is visible in Git.
2. Add a minimal dispatcher script under `scripts/dispatch.sh` implementing the steps above.
3. Populate `handlers/` with example handlers (e.g., `deploy.sh`, `backup.py`).
4. Commit an initial `codex.repo.yaml` and `README.codex.md` detailing the workflow.

