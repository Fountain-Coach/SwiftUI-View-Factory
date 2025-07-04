#!/usr/bin/env python3
"""Create a zipped Swift package containing generated SwiftUI files."""
import os
import sys
import yaml
import subprocess
import shutil

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(request_file) as f:
    data = yaml.safe_load(f)

spec = data.get('spec', {})
package_name = spec.get('package_name', 'GeneratedPackage')
files = spec.get('files', [])  # list of Swift file paths

package_dir = os.path.join(log_dir, package_name)
status_file = os.path.join(log_dir, 'status.yml')
log_file = os.path.join(log_dir, 'package.log')
os.makedirs(log_dir, exist_ok=True)

with open(log_file, 'w') as lf:
    try:
        # Initialize swift package
        subprocess.check_call([
            'swift', 'package', 'init', '--name', package_name, '--type', "executable"
        ], cwd=log_dir, stdout=lf, stderr=subprocess.STDOUT)
        sources_dir = os.path.join(package_dir, 'Sources', package_name)
        os.makedirs(sources_dir, exist_ok=True)
        for path in files:
            if os.path.isfile(path):
                shutil.copy(path, sources_dir)
            else:
                lf.write(f"WARNING: missing file {path}\n")
        # Archive to .package
        archive = os.path.join(log_dir, f"{package_name}.package")
        subprocess.check_call(['zip', '-r', archive, package_name], cwd=log_dir, stdout=lf, stderr=subprocess.STDOUT)
        status = 'success'
    except Exception as e:
        lf.write(f"\nERROR: {e}\n")
        status = 'failure'

with open(status_file, 'w') as sf:
    sf.write(f'status: {status}\n')
