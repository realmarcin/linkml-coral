#!/usr/bin/env python3
"""Test the fixed gen-erdiagram command."""

import subprocess

# Test the command structure that works in the shell script
schema_path = "src/linkml_coral/schema/linkml_coral.yaml"

print("Testing gen-erdiagram with correct syntax...")
cmd = ['uv', 'run', 'gen-erdiagram', schema_path, '--classes', 'Sample', 'Location']

print(f"Command: {' '.join(cmd)}")
result = subprocess.run(cmd, capture_output=True, text=True)

print(f"Exit code: {result.returncode}")
if result.returncode == 0:
    print(f"✅ Success! Generated {len(result.stdout.splitlines())} lines of output")
    print("First few lines:")
    print('\n'.join(result.stdout.splitlines()[:5]))
else:
    print(f"❌ Failed: {result.stderr}")