#!/usr/bin/env python3
"""Test gen-erdiagram output format."""

import subprocess

print("Testing raw gen-erdiagram output...")

# Test basic command
result = subprocess.run([
    'uv', 'run', 'gen-erdiagram', 
    'src/linkml_coral/schema/linkml_coral.yaml',
    '--exclude-attributes'
], capture_output=True, text=True)

print(f"Exit code: {result.returncode}")
if result.returncode == 0:
    output = result.stdout
    print(f"Output length: {len(output)} characters")
    print("\nFirst 200 characters:")
    print(repr(output[:200]))
    print("\nLast 200 characters:")
    print(repr(output[-200:]))
    
    # Check format
    if output.startswith('```mermaid'):
        print("\n✅ Output is in markdown format")
    elif output.startswith('erDiagram'):
        print("\n✅ Output is pure Mermaid format")
    else:
        print("\n❓ Unknown format")
else:
    print(f"❌ Error: {result.stderr}")