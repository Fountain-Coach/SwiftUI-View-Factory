# SwiftUI View Factory Workflow

This repository is a practical blueprint for running Codex-managed tasks on your local machine. It started as a **SwiftUI View Factory** – an API that turns UI mockups into Swift code – and evolved into a generalized workflow pattern. Any service described with OpenAPI can plug into the same infrastructure.

The factory exposes endpoints defined in [`api/openapi.yml`](api/openapi.yml). Handlers under `handlers/` call these endpoints or speak directly to OpenAI based on request files committed to `requests/`. The dispatcher script processes those files and saves results to `logs/` before archiving them in `processed/`.

While the example API focuses on SwiftUI generation, the workflow is not limited to Swift. You can adapt the same dispatcher and handler pattern to automate other domains by supplying a different OpenAPI spec and implementing matching handlers.

## Repository Layout

```text
/                   # Repository root
├── api/            # OpenAPI specification(s)
├── docs/           # Reference guides and PDFs
├── handlers/       # Request handlers registered in `handlers/index.yml`
├── scripts/        # Dispatcher and helper scripts
├── requests/       # Inbox for Codex-written request YAML
├── processed/      # Archive for handled requests
├── logs/           # Structured execution logs
├── image-upload/   # Source images for interpretation
├── api-versioning/ # Alternate API versions and critiques
└── codex.repo.yaml # Orchestration configuration
```

## Using the Workflow

1. Place a request file under `requests/` describing a handler `kind` and parameters.
2. Run `scripts/dispatch.sh` (or `scripts/docker_dispatch.sh` for a containerized runtime). Each request is routed to the appropriate handler and logged under `logs/`.
3. Review the log output and status files committed back to the repository.

Detailed instructions and examples are available in the [usage guide](docs/USAGE.md). The [OpenAPI handler proposal](docs/openapi-handler-proposal.md) and [implementation notes](docs/openapi-handler-implementation.md) explain how handlers use the API spec. For running the dispatcher continuously or inside Docker, see [daemonizing-dispatcher](docs/daemonizing-dispatcher.md) and [docker-runtime](docs/docker-runtime.md).

## Why a Generalized Tool?

The same Git-driven workflow works for any OpenAPI-described service. By swapping out the spec in `api/` and adding new handlers, Codex can orchestrate a variety of local tasks – from building Swift projects on macOS ([macOS Xcode workflow](docs/macos-xcode-workflow.md)) to packaging generated client libraries ([swift-openapi-generator](docs/swift-openapi-generator.md)).

This repository demonstrates how Codex acts like a compiler: prompts become structured request files, handlers perform reproducible work, and logs provide a deterministic audit trail. For more background, see [how-codex-acts-like-a-compiler.pdf](docs/how-codex-acts-like-a-compiler.pdf) and [dispatcher_right.pdf](docs/dispatcher_right.pdf).

For a deeper walkthrough of the repository structure and dispatcher checklist, see [README.codex.md](README.codex.md).
