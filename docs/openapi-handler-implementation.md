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
interpretLayout: handlers/interpretLayout.py
generateSwiftUIView: handlers/generateSwiftUIView.py
getOpenAIKey: handlers/getOpenAIKey.py
```

## `handlers/interpretLayout.py`

Uploads a mockup image to `/factory/interpret` and stores the JSON
response in the log directory.

```python
#!/usr/bin/env python3
import os
import sys
import yaml
import json
from client.swift_ui_view_factory_api_client import Client
from client.swift_ui_view_factory_api_client.models import InterpretLayoutBody, File
from client.swift_ui_view_factory_api_client.api.factory import interpret_layout

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(request_file) as f:
    data = yaml.safe_load(f)

file_path = data.get('spec', {}).get('file')

client = Client(base_url=os.getenv('API_BASE_URL', 'http://localhost:8000'))

response_file = os.path.join(log_dir, 'interpretLayout_response.json')
status_file = os.path.join(log_dir, 'status.yml')

with open(file_path, 'rb') as fp:
    body = InterpretLayoutBody(file=File(payload=fp, file_name=os.path.basename(file_path)))
    resp = interpret_layout.sync(client=client, body=body)

with open(response_file, 'w') as f:
    json.dump(resp.to_dict(), f, indent=2)
with open(status_file, 'w') as f:
    f.write('status: success\n')
```

## `handlers/generateSwiftUIView.py`

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

client = Client(base_url=os.getenv('API_BASE_URL', 'http://localhost:8000'))

response_file = os.path.join(log_dir, 'generateSwiftUIView_response.json')
status_file = os.path.join(log_dir, 'status.yml')

body = GenerateSwiftUIViewBody.from_dict(spec)
resp = generate_swift_ui_view.sync(client=client, body=body)

with open(response_file, 'w') as f:
    json.dump(resp.to_dict(), f, indent=2)
with open(status_file, 'w') as f:
    f.write('status: success\n')
```

## `handlers/getOpenAIKey.py`

Calls `/secret` to retrieve the API key. The response body is saved in
the log directory.

```python
#!/usr/bin/env python3
import os
import sys
import json
from client.swift_ui_view_factory_api_client import Client
from client.swift_ui_view_factory_api_client.api.secrets import get_open_ai_key

request_file = sys.argv[1]
log_dir = sys.argv[2]

client = Client(base_url=os.getenv('API_BASE_URL', 'http://localhost:8000'))

response_file = os.path.join(log_dir, 'getOpenAIKey_response.json')
status_file = os.path.join(log_dir, 'status.yml')

resp = get_open_ai_key.sync(client=client)

with open(response_file, 'w') as f:
    json.dump(resp.to_dict(), f, indent=2)
with open(status_file, 'w') as f:
    f.write('status: success\n')
```

All handlers rely on the `API_BASE_URL` environment variable. If it is
not set, they default to `http://localhost:8000` as defined in the
OpenAPI spec.

