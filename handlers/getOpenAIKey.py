#!/usr/bin/env python3
import os
import sys
import json

request_file = sys.argv[1]
log_dir = sys.argv[2]

response_file = os.path.join(log_dir, 'getOpenAIKey_response.json')
status_file = os.path.join(log_dir, 'status.yml')

try:
    key = os.getenv('OPENAI_API_KEY')
    resp = {"api_key": key}
    with open(response_file, 'w') as f:
        json.dump(resp, f, indent=2)
    status = 'success'
except Exception as e:
    with open(os.path.join(log_dir, 'error.log'), 'w') as f:
        f.write(str(e))
    status = 'error'

with open(status_file, 'w') as f:
    f.write(f'status: {status}\n')
