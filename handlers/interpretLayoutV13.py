#!/usr/bin/env python3
import os
import sys
import json
import yaml
import base64
import openai

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(request_file) as f:
    data = yaml.safe_load(f)

spec = data.get('spec', {})
file_path = spec.get('file')
model = spec.get('gpt_model', 'gpt-4o')

response_file = os.path.join(log_dir, 'interpretLayoutV13_response.json')
status_file = os.path.join(log_dir, 'status.yml')

try:
    openai.api_key = os.getenv('OPENAI_API_KEY')
    with open(file_path, 'rb') as fp:
        encoded = base64.b64encode(fp.read()).decode('utf-8')

    messages = [
        {
            "role": "system",
            "content": "You interpret UI mockup images into a JSON layout tree. Respond strictly with JSON containing keys 'structured' and 'description'."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Interpret this mockup"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}}
            ]
        }
    ]

    resp = openai.ChatCompletion.create(model=model, messages=messages)
    content = resp.choices[0].message.content
    result = json.loads(content)
    result.setdefault('version', 'layout-v1')
    result['log'] = json.dumps(resp, default=str)

    with open(response_file, 'w') as f:
        json.dump(result, f, indent=2)
    status = 'success'
except Exception as e:
    with open(os.path.join(log_dir, 'error.log'), 'w') as f:
        f.write(str(e))
    status = 'error'

with open(status_file, 'w') as f:
    f.write(f'status: {status}\n')
