#!/usr/bin/env python3
"""Generate a Swift package using swift-openapi-generator."""
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
package_name = spec.get('package_name', 'OpenAPIClient')
module_name = spec.get('module_name', package_name)
openapi_path = spec.get('openapi', 'api/openapi.yml')
generator_version = spec.get('generator_version', '1.6.0')
runtime_version = spec.get('runtime_version', '1.7.0')
transport_version = spec.get('transport_version', '1.0.0')

package_dir = os.path.join(log_dir, package_name)
os.makedirs(package_dir, exist_ok=True)

# Initialize the Swift package
subprocess.check_call(['swift', 'package', 'init', '--name', package_name, '--type', 'executable'], cwd=package_dir)

package_swift = f"""// swift-tools-version: 6.1
import PackageDescription

let package = Package(
    name: \"{package_name}\",
    platforms: [.macOS(.v10_15)],
    dependencies: [
        .package(url: \"https://github.com/apple/swift-openapi-generator.git\", from: \"{generator_version}\"),
        .package(url: \"https://github.com/apple/swift-openapi-runtime.git\", from: \"{runtime_version}\"),
        .package(url: \"https://github.com/apple/swift-openapi-urlsession.git\", from: \"{transport_version}\"),
    ],
    targets: [
        .executableTarget(
            name: \"{module_name}\",
            dependencies: [
                .product(name: \"OpenAPIRuntime\", package: \"swift-openapi-runtime\"),
                .product(name: \"OpenAPIURLSession\", package: \"swift-openapi-urlsession\"),
            ],
            plugins: [.plugin(name: \"OpenAPIGenerator\", package: \"swift-openapi-generator\")]
        )
    ]
)
"""

with open(os.path.join(package_dir, 'Package.swift'), 'w') as f:
    f.write(package_swift)

# Copy OpenAPI document into the target directory so the plugin can access it
target_dir = os.path.join(package_dir, 'Sources', module_name)
os.makedirs(target_dir, exist_ok=True)
shutil.copy(openapi_path, os.path.join(target_dir, 'openapi.yml'))

status = 'success'
with open(os.path.join(log_dir, 'build.log'), 'w') as build_log:
    try:
        subprocess.check_call(['swift', 'build'], cwd=package_dir, stdout=build_log, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        status = 'failure'

# Archive the package
archive = os.path.join(log_dir, f"{package_name}.package")
subprocess.check_call(['zip', '-r', archive, package_name], cwd=log_dir)

with open(os.path.join(log_dir, 'status.yml'), 'w') as f:
    f.write(f'status: {status}\n')
