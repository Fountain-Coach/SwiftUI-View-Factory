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
