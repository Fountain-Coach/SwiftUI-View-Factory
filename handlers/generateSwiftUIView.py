#!/usr/bin/env python3
import os
import sys
import json
import yaml
import openai

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(request_file) as f:
    data = yaml.safe_load(f)

spec = data.get('spec', {})
layout = spec.get('layout')
name = spec.get('name', 'GeneratedView')
style = spec.get('style', {})
backend_hooks = spec.get('backend_hooks', False)
model = spec.get('gpt_model', 'gpt-4o')

response_file = os.path.join(log_dir, 'generateSwiftUIView_response.json')
status_file = os.path.join(log_dir, 'status.yml')

try:
    openai.api_key = os.getenv('OPENAI_API_KEY')
    prompt_data = {
        "layout": layout,
        "name": name,
        "style": style,
        "backend_hooks": backend_hooks
    }
    messages = [
        {"role": "system", "content": "Generate SwiftUI code from the provided layout JSON. Return only the code."},
        {"role": "user", "content": json.dumps(prompt_data)}
    ]
    resp = openai.ChatCompletion.create(model=model, messages=messages)
    swift_code = resp.choices[0].message.content.strip()
    result = {"swift": swift_code, "log": json.dumps(resp, default=str)}
    with open(response_file, 'w') as f:
        json.dump(result, f, indent=2)
    status = 'success'
except Exception as e:
    with open(os.path.join(log_dir, 'error.log'), 'w') as f:
        f.write(str(e))
    status = 'error'

with open(status_file, 'w') as f:
    f.write(f'status: {status}\n')
