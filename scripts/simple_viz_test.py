#!/usr/bin/env python3
"""Simple test for gen-erdiagram syntax."""

import subprocess
from pathlib import Path

schema_path = "src/linkml_coral/schema/linkml_coral.yaml"
output_dir = Path("test_output")
output_dir.mkdir(exist_ok=True)

# Test 1: Full schema
print("Test 1: Full schema")
cmd1 = ['uv', 'run', 'gen-erdiagram', schema_path]
result1 = subprocess.run(cmd1, capture_output=True, text=True)
print(f"Exit code: {result1.returncode}")
if result1.returncode == 0:
    (output_dir / "full.mmd").write_text(result1.stdout)
    print("✅ Full schema generated")
else:
    print(f"❌ Error: {result1.stderr}")

# Test 2: Selected classes
print("\nTest 2: Selected classes")
cmd2 = ['uv', 'run', 'gen-erdiagram', '--classes', 'Sample', 'Location', schema_path]
result2 = subprocess.run(cmd2, capture_output=True, text=True)
print(f"Exit code: {result2.returncode}")
if result2.returncode == 0:
    (output_dir / "selected.mmd").write_text(result2.stdout)
    print("✅ Selected classes generated")
else:
    print(f"❌ Error: {result2.stderr}")

print(f"\nOutputs saved to: {output_dir}/")