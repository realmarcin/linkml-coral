#!/usr/bin/env python3
"""Test gen-erdiagram command syntax."""

import subprocess

# Test basic command
print("Testing basic gen-erdiagram...")
result = subprocess.run(['uv', 'run', 'gen-erdiagram', '--help'], capture_output=True, text=True)
print("Exit code:", result.returncode)
print("\nHelp output:")
print(result.stdout[:1000])

# Test with classes
print("\n\nTesting with multiple classes...")
cmd = ['uv', 'run', 'gen-erdiagram', 'src/linkml_coral/schema/linkml_coral.yaml', 
       '--classes', 'Sample', '--classes', 'Location', '--classes', 'Community']
result = subprocess.run(cmd, capture_output=True, text=True)
print("Exit code:", result.returncode)
if result.returncode == 0:
    print("Success! Output length:", len(result.stdout))
else:
    print("Error:", result.stderr)