#!/usr/bin/env python3
"""Test gen-erdiagram output to debug the markdown issue."""

import subprocess
import sys

# Run gen-erdiagram and capture output
result = subprocess.run([
    'uv', 'run', 'gen-erdiagram', 
    'src/linkml_coral/schema/linkml_coral.yaml',
    '--exclude-attributes'
], capture_output=True, text=True)

print("Exit code:", result.returncode)
print("\n--- STDOUT ---")
print(repr(result.stdout))  # Using repr to see actual characters

print("\n--- STDERR ---")
print(result.stderr)

# Check the last few lines
lines = result.stdout.split('\n')
print(f"\n--- LAST 5 LINES ---")
for i, line in enumerate(lines[-5:]):
    print(f"{len(lines)-5+i}: {repr(line)}")