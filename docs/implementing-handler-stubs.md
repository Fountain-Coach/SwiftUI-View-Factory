# Implementing Stub Handlers

When Codex encounters a request `kind` with no matching handler, the dispatcher logs an error. A maintenance job can read these logs and automatically create placeholder scripts and registry entries so the system "knows" about the new kind. These placeholders are stubs—you still need to implement the logic.

This guide walks through the steps to turn those stubs into working handlers.

## 1. Locate the Stub

New handlers are registered in `handlers/index.yml`. Each entry maps a `kind` to an executable script path:

```yaml
mytask: handlers/mytask.sh
```

Stub scripts are created under `handlers/` and usually contain a simple message like:

```bash
#!/usr/bin/env bash
# TODO: implement mytask handler
```

## 2. Understand the Contract

Handlers are executed by `scripts/dispatch.sh` with two arguments:

1. **Request file path** – YAML describing the action.
2. **Log directory** – where the handler should write logs and status files.

A minimal handler must append messages to a log file and write a `status.yml` file with one of `success`, `failure`, or `error`.

Example from `handlers/deploy.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
request_file="$1"
log_dir="$2"

echo "Deploy handler executed for $request_file" >> "$log_dir/deploy.log"
```

## 3. Add Real Logic

Edit the stub script to perform its task. Use the request YAML as input and write any output to the log directory. Be sure to exit non-zero if something fails—the dispatcher records this and sets `status: failure`.

For Python handlers, follow the pattern in `handlers/backup.py`:

```python
#!/usr/bin/env python3
import sys, os

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(os.path.join(log_dir, "backup.log"), "a") as f:
    f.write(f"Backup handler executed for {request_file}\n")
```

Replace the body with your actual implementation.

## 4. Test Locally

Run `scripts/dispatch.sh --selftest` to ensure the dispatcher works. Then place a sample request file in `requests/` with `kind: mytask` and run the dispatcher to test your handler end-to-end. Check the generated logs under `logs/` for success or failure.

## 5. Commit and Push

Once the handler performs correctly, commit the updated script and any additional files. The system now has a fully implemented handler for the previously unknown `kind`.

