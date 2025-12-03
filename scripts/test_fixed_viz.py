#!/usr/bin/env python3
"""Test the fixed visualization script."""

import subprocess
from pathlib import Path

# Clean up old diagrams
import shutil
if Path("schema_diagrams").exists():
    shutil.rmtree("schema_diagrams")

print("Testing fixed visualization script...")

# Run the visualization script
result = subprocess.run([
    'uv', 'run', 'python', 'visualize_schema.py', 
    '--no-attributes', 
    '--output-dir', 'test_diagrams'
], capture_output=True, text=True)

print(f"Exit code: {result.returncode}")
if result.returncode == 0:
    print("✅ Visualization succeeded!")
    
    # Check the output
    test_dir = Path("test_diagrams")
    if test_dir.exists():
        mmd_files = list(test_dir.glob("*.mmd"))
        print(f"Generated {len(mmd_files)} diagram files:")
        
        for mmd_file in mmd_files:
            content = mmd_file.read_text()
            print(f"\n{mmd_file.name}:")
            print(f"  - Length: {len(content)} characters")
            print(f"  - Starts with: {content[:50]}...")
            
            # Check if it's proper Mermaid
            if content.startswith('%%') or content.startswith('erDiagram'):
                print("  - ✅ Proper Mermaid format")
            else:
                print("  - ❌ Still has markdown formatting")
else:
    print(f"❌ Failed: {result.stderr}")
    print(f"Stdout: {result.stdout}")