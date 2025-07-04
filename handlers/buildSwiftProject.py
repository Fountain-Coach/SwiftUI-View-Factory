#!/usr/bin/env python3
"""Build a Swift or Xcode project using xcodebuild.

This handler is intended to run on macOS with Xcode installed. It parses the
request YAML for a `spec` block containing `workspace`, `project`, `scheme`,
`sdk`, and `destination` fields. Any field may be omitted. The resulting build
log is written to `xcodebuild.log` in the log directory, and `status.yml`
records `success` or `failure`.
"""
import os
import sys
import yaml
import subprocess

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(request_file) as f:
    data = yaml.safe_load(f)

spec = data.get('spec', {})
workspace = spec.get('workspace')
project = spec.get('project')
scheme = spec.get('scheme')
sdk = spec.get('sdk')
destination = spec.get('destination')

cmd = ["xcodebuild"]
if workspace:
    cmd.extend(["-workspace", workspace])
if project:
    cmd.extend(["-project", project])
if scheme:
    cmd.extend(["-scheme", scheme])
if sdk:
    cmd.extend(["-sdk", sdk])
if destination:
    cmd.extend(["-destination", destination])

log_file = os.path.join(log_dir, 'xcodebuild.log')
status_file = os.path.join(log_dir, 'status.yml')

os.makedirs(log_dir, exist_ok=True)

with open(log_file, 'w') as lf:
    try:
        subprocess.check_call(cmd, stdout=lf, stderr=subprocess.STDOUT)
        status = 'success'
    except Exception as e:
        lf.write(f"\nERROR: {e}\n")
        status = 'failure'

with open(status_file, 'w') as sf:
    sf.write(f'status: {status}\n')
