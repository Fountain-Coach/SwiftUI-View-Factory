#!/usr/bin/env python3
import os
import sys
import json
import yaml
from pathlib import Path

from client.swift_ui_view_factory_api_client import Client
from client.swift_ui_view_factory_api_client.models import InterpretLayoutBody, File
from client.swift_ui_view_factory_api_client.api.factory import interpret_layout
from client.swift_ui_view_factory_api_client.models.error_response import ErrorResponse

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(request_file) as f:
    data = yaml.safe_load(f)

spec = data.get('spec', {})
file_path = spec.get('file')

base_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
client = Client(base_url=base_url)

response_file = os.path.join(log_dir, 'interpretLayout_response.json')
status_file = os.path.join(log_dir, 'status.yml')

try:
    with open(file_path, 'rb') as fp:
        body = InterpretLayoutBody(file=File(payload=fp, file_name=Path(file_path).name))
        resp = interpret_layout.sync(client=client, body=body)
    with open(response_file, 'w') as f:
        json.dump(resp.to_dict() if hasattr(resp, 'to_dict') else None, f, indent=2)
    if resp is not None and not isinstance(resp, ErrorResponse):
        status = 'success'
    else:
        status = 'failure'
except Exception as e:
    with open(os.path.join(log_dir, 'error.log'), 'w') as f:
        f.write(str(e))
    status = 'error'

with open(status_file, 'w') as f:
    f.write(f'status: {status}\n')
