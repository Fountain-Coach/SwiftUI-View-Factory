#!/usr/bin/env python3
"""Bundle OpenAPI clients and SwiftUI sources into a single Swift package."""
import os
import sys
import yaml
import subprocess
import shutil
from glob import glob
from pathlib import Path

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(request_file) as f:
    data = yaml.safe_load(f)

spec = data.get('spec', {})
package_name = spec.get('package_name', 'APIClient')
module_name = spec.get('module_name', package_name)
openapi_dir = spec.get('openapi_dir', 'api')
swiftui_files = spec.get('swiftui_files', [])

def safe_module_name(path: str) -> str:
    name = Path(path).stem
    return name.replace('-', '_').replace('.', '_')

package_dir = os.path.join(log_dir, package_name)
os.makedirs(package_dir, exist_ok=True)

# Initialize base Swift package
subprocess.check_call(['swift', 'package', 'init', '--name', package_name], cwd=package_dir)

# Locate OpenAPI specs
openapi_paths = sorted(glob(os.path.join(openapi_dir, '*.yml')))
client_targets = []
for spec_path in openapi_paths:
    mod = safe_module_name(spec_path)
    target_dir = os.path.join(package_dir, 'Sources', mod)
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy(spec_path, os.path.join(target_dir, 'openapi.yml'))
    client_targets.append(mod)

# Copy SwiftUI view files
ui_target_dir = os.path.join(package_dir, 'Sources', module_name)
os.makedirs(ui_target_dir, exist_ok=True)
for path in swiftui_files:
    if os.path.isfile(path):
        shutil.copy(path, ui_target_dir)

# Compose Package.swift
products = ', '.join(f'"{n}"' for n in client_targets + [module_name])
client_target_defs = []
for mod in client_targets:
    client_target_defs.append(f"        .target(\n            name: \"{mod}\",\n            dependencies: [\n                .product(name: \"OpenAPIRuntime\", package: \"swift-openapi-runtime\"),\n                .product(name: \"OpenAPIURLSession\", package: \"swift-openapi-urlsession\")\n            ],\n            plugins: [.plugin(name: \"OpenAPIGenerator\", package: \"swift-openapi-generator\")]\n        )")
client_targets_str = ',\n'.join(client_target_defs)

package_swift = f"""// swift-tools-version: 6.1
import PackageDescription

let package = Package(
    name: \"{package_name}\",
    platforms: [.macOS(.v12)],
    products: [
        .library(name: \"{package_name}\", targets: [{products}])
    ],
    dependencies: [
        .package(url: \"https://github.com/apple/swift-openapi-generator.git\", from: \"1.6.0\"),
        .package(url: \"https://github.com/apple/swift-openapi-runtime.git\", from: \"1.7.0\"),
        .package(url: \"https://github.com/apple/swift-openapi-urlsession.git\", from: \"1.0.0\")
    ],
    targets: [
{client_targets_str},
        .target(
            name: \"{module_name}\",
            dependencies: []
        )
    ]
)
"""

with open(os.path.join(package_dir, 'Package.swift'), 'w') as f:
    f.write(package_swift)

status = 'success'
with open(os.path.join(log_dir, 'build.log'), 'w') as build_log:
    try:
        subprocess.check_call(['swift', 'build'], cwd=package_dir, stdout=build_log, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        status = 'failure'

archive = os.path.join(log_dir, f"{package_name}.package")
subprocess.check_call(['zip', '-r', archive, package_name], cwd=log_dir)

with open(os.path.join(log_dir, 'status.yml'), 'w') as f:
    f.write(f'status: {status}\n')
