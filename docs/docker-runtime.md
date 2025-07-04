# Dockerized Runtime for Cross-Platform Consistency

The Python handlers in this repository rely on a specific runtime and external
dependencies. When the dispatcher runs directly on different operating systems,
results can vary or fail altogether.

## Problem

Contributors may execute the factory on Windows, macOS or Linux machines with
varying Python versions. Some handlers also expect additional tools. These
environment differences make it hard to reproduce results and can lead to
execution errors.

## Solution

Use a Docker container to provide a known-good Python environment. The wrapper
script `scripts/docker_dispatch.sh` locates the repository root using
`git rev-parse` so the clone can live anywhere on the host. It mounts the root
at `/repo` inside the container and runs `scripts/dispatch.sh` there. The
container image defaults to `python:3.11-slim` but can be overridden with the
`DOCKER_IMAGE` environment variable.

## Usage

Run the wrapper instead of `dispatch.sh`:

```bash
scripts/docker_dispatch.sh
```

Any arguments are forwarded to the dispatcher. Environment variables such as
`OPENAI_API_KEY` are passed through so handlers behave exactly as they do on the
host machine.
