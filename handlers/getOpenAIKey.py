#!/usr/bin/env python3
import os
import sys
import json

from client.swift_ui_view_factory_api_client import Client
from client.swift_ui_view_factory_api_client.api.secrets import get_open_ai_key

request_file = sys.argv[1]
log_dir = sys.argv[2]

base_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
client = Client(base_url=base_url)

response_file = os.path.join(log_dir, 'getOpenAIKey_response.json')
status_file = os.path.join(log_dir, 'status.yml')

try:
    resp = get_open_ai_key.sync(client=client)
    with open(response_file, 'w') as f:
        json.dump(resp.to_dict() if hasattr(resp, 'to_dict') else None, f, indent=2)
    status = 'success'
except Exception as e:
    with open(os.path.join(log_dir, 'error.log'), 'w') as f:
        f.write(str(e))
    status = 'error'

with open(status_file, 'w') as f:
    f.write(f'status: {status}\n')
