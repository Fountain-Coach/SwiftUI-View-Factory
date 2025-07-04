# Extending the Handler Registry from Logs

This document describes how Codex and human operators can use the logs produced by `scripts/dispatch.sh` to discover new request kinds and grow the handler registry.

## Background

The dispatcher reads YAML request files from `requests/` and routes each file by its `kind` field using `handlers/index.yml`. When a request uses a kind that isn't in the index, the dispatcher writes an error to the log directory:

```
Unknown handler for kind <kind>
```

This message is recorded in `error.log` alongside a `status.yml` file containing `status: error`. The request file is moved to `processed/` so it won't be retried.

Relevant code snippet from `scripts/dispatch.sh`:

```bash
kind=$(grep '^kind:' "$req" | awk '{print $2}')
handler=$(grep "^$kind:" "$HANDLER_INDEX" | awk '{print $2}')
if [[ -z "$handler" || ! -x "$handler" ]]; then
  echo "Unknown handler for kind $kind" | tee "$log_dir/error.log"
  echo "status: error" > "$log_dir/status.yml"
  mv "$req" "$DONE/"
  continue
fi
```

## Learning from Logs

Because all log files are committed to `logs/`, both Codex and humans can scan them for messages about unknown handlers. The typical workflow is:

1. **Collect logs** – Each run of the dispatcher creates a subdirectory under `logs/` containing `dispatch.log`, `handler.log`, and `status.yml`.
2. **Search for errors** – A maintenance script or Codex job reads all `error.log` files and extracts the missing `kind` values.
3. **Propose a handler** – For each new kind, create a placeholder script under `handlers/` and register it in `handlers/index.yml`. Codex can open a PR with these changes.
4. **Review and implement** – Human maintainers review the proposed handler stubs and implement the actual logic.

This feedback loop lets the system evolve organically based on real requests. Any unsupported kind becomes visible in the logs, prompting the creation of a new handler entry.

## Example Maintenance Script

A simple script to list unknown kinds might look like:

```bash
#!/usr/bin/env bash
find logs -name error.log -exec grep -h "Unknown handler" {} + | \
  awk '{print $NF}' | sort -u
```

Running this script prints each distinct kind that lacked a handler. Codex can use this list to generate new handler files and update `handlers/index.yml` accordingly.

## Conclusion

The repository treats logs as a discovery mechanism. By monitoring error messages about missing handlers, Codex learns which kinds to support next. Updating `handlers/index.yml` based on log feedback keeps the dispatcher minimal while allowing the system to grow over time.
