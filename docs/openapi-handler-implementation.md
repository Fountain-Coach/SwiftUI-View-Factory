# Example: OpenAPI Handlers Using the OpenAI API

This document demonstrates how the handler scripts implement the
[OpenAPI handler proposal](openapi-handler-proposal.md). The latest
handlers call the OpenAI API directly instead of routing through a
controller service.

## Handler Registry

`handlers/index.yml` lists the available kinds:

```yaml
deploy: handlers/deploy.sh
backup: handlers/backup.py
interpretLayoutV13: handlers/interpretLayoutV13.py
generateSwiftUIView: handlers/generateSwiftUIView.py
getOpenAIKey: handlers/getOpenAIKey.py
```

## `handlers/interpretLayoutV13.py`

Uploads a mockup image and uses the OpenAI vision model to return a
structured layout tree.

```python
#!/usr/bin/env python3
import os
import sys
import yaml
import json
import base64
import openai

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(request_file) as f:
    data = yaml.safe_load(f)

file_path = data.get('spec', {}).get('file')
openai.api_key = os.getenv('OPENAI_API_KEY')

with open(file_path, 'rb') as fp:
    encoded = base64.b64encode(fp.read()).decode('utf-8')

resp = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Return JSON with keys 'structured' and 'description'."},
        {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}}]}
    ],
)

with open(os.path.join(log_dir, 'interpretLayoutV13_response.json'), 'w') as f:
    json.dump(json.loads(resp.choices[0].message.content), f, indent=2)
```

## `handlers/generateSwiftUIView.py`

Generates SwiftUI code from a layout tree by invoking the OpenAI API.

```python
#!/usr/bin/env python3
import os
import sys
import yaml
import json
import openai

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(request_file) as f:
    data = yaml.safe_load(f)

spec = data.get('spec', {})
openai.api_key = os.getenv('OPENAI_API_KEY')

resp = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Produce SwiftUI code for this layout."},
        {"role": "user", "content": json.dumps(spec)}
    ],
)

with open(os.path.join(log_dir, 'generateSwiftUIView_response.json'), 'w') as f:
    json.dump({"swift": resp.choices[0].message.content}, f, indent=2)
```

## `handlers/getOpenAIKey.py`

Returns the API key from the environment and saves it to the log
directory.

```python
#!/usr/bin/env python3
import os
import sys
import json

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(os.path.join(log_dir, 'getOpenAIKey_response.json'), 'w') as f:
    json.dump({"api_key": os.getenv('OPENAI_API_KEY')}, f, indent=2)
```

All handlers require the OPENAI_API_KEY environment variable.

## `handlers/buildSwiftProject.py`

Runs `xcodebuild` with parameters from the request. It must be executed on
macOS with Xcode installed. Build output is saved to `xcodebuild.log` and the
handler reports success or failure via `status.yml`.

## `handlers/packageSwiftUIView.py`

Prepares a Swift package from loose `.swift` files and archives it as
`<package_name>.package`. The archive can then be built on macOS using the
`buildSwiftProject` handler.

