#!/usr/bin/env python3
import sys, os

request_file = sys.argv[1]
log_dir = sys.argv[2]

with open(os.path.join(log_dir, "backup.log"), "a") as f:
    f.write(f"Backup handler executed for {request_file}\n")
