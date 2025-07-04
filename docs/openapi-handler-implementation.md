# Example: OpenAPI Handlers Using Direct HTTP Calls

This document demonstrates a concrete implementation of the
[OpenAPI handler proposal](openapi-handler-proposal.md). Each handler
invokes the SwiftUI View Factory API defined in `api/openapi.yml` using
plain HTTP requests.

## Handler Registry

`handlers/index.yml` lists the available kinds:

```yaml
deploy: handlers/deploy.sh
backup: handlers/backup.py
interpret: handlers/interpret.py
generate: handlers/generate.py
secret: handlers/secret.py
```

## `handlers/interpret.py`

Uploads a mockup image to `/factory/interpret` and stores the JSON
response in the log directory.

```python
#!/usr/bin/env python3
import os
import sys
import yaml
import requests

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(request_file) as f:
    data = yaml.safe_load(f)

spec = data.get('spec', {})
file_path = spec.get('file')

base_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
url = f"{base_url}/factory/interpret"

response_file = os.path.join(log_dir, 'interpret_response.json')
status_file = os.path.join(log_dir, 'status.yml')

try:
    with open(file_path, 'rb') as fp:
        files = {'file': fp}
        resp = requests.post(url, files=files)
    with open(response_file, 'w') as f:
        f.write(resp.text)
    if resp.ok:
        with open(status_file, 'w') as f:
            f.write('status: success\n')
    else:
        with open(status_file, 'w') as f:
            f.write('status: failure\n')
except Exception as e:
    with open(os.path.join(log_dir, 'error.log'), 'w') as f:
        f.write(str(e))
    with open(status_file, 'w') as f:
        f.write('status: error\n')
```

## `handlers/generate.py`

Posts a layout tree to `/factory/generate` and writes the resulting
Swift code JSON to the logs.

```python
#!/usr/bin/env python3
import os
import sys
import yaml
import requests

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(request_file) as f:
    data = yaml.safe_load(f)

spec = data.get('spec', {})

base_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
url = f"{base_url}/factory/generate"

response_file = os.path.join(log_dir, 'generate_response.json')
status_file = os.path.join(log_dir, 'status.yml')

try:
    resp = requests.post(url, json=spec)
    with open(response_file, 'w') as f:
        f.write(resp.text)
    if resp.ok:
        with open(status_file, 'w') as f:
            f.write('status: success\n')
    else:
        with open(status_file, 'w') as f:
            f.write('status: failure\n')
except Exception as e:
    with open(os.path.join(log_dir, 'error.log'), 'w') as f:
        f.write(str(e))
    with open(status_file, 'w') as f:
        f.write('status: error\n')
```

## `handlers/secret.py`

Calls `/secret` to retrieve the API key. The response body is saved in
the log directory.

```python
#!/usr/bin/env python3
import os
import sys
import requests

request_file = sys.argv[1]
log_dir = sys.argv[2]

base_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
url = f"{base_url}/secret"

response_file = os.path.join(log_dir, 'secret_response.json')
status_file = os.path.join(log_dir, 'status.yml')

try:
    resp = requests.get(url)
    with open(response_file, 'w') as f:
        f.write(resp.text)
    if resp.ok:
        with open(status_file, 'w') as f:
            f.write('status: success\n')
    else:
        with open(status_file, 'w') as f:
            f.write('status: failure\n')
except Exception as e:
    with open(os.path.join(log_dir, 'error.log'), 'w') as f:
        f.write(str(e))
    with open(status_file, 'w') as f:
        f.write('status: error\n')
```

All handlers rely on the `API_BASE_URL` environment variable. If it is
not set, they default to `http://localhost:8000` as defined in the
OpenAPI spec.

