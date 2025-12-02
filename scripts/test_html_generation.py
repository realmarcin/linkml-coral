#!/usr/bin/env python3
"""Test the HTML generation fix."""

import subprocess
import shutil
from pathlib import Path

# Clean up old diagrams
schema_dir = Path("schema_diagrams")
if schema_dir.exists():
    shutil.rmtree(schema_dir)

print("Testing fixed HTML generation...")

# Run the visualization with the fixed code
result = subprocess.run([
    'uv', 'run', 'python', 'visualize_schema.py',
    '--no-attributes',
    '--output-dir', 'schema_diagrams'
], capture_output=True, text=True)

print(f"Generation result: {result.returncode}")
if result.returncode != 0:
    print(f"Error: {result.stderr}")
    exit(1)

# Check the results
print("\n📁 Generated files:")
for file in schema_dir.glob("*"):
    print(f"  - {file.name}")

# Check if clean files were created
clean_files = list(schema_dir.glob("*.clean.mmd"))
print(f"\n🧹 Clean files for HTML: {len(clean_files)}")

# Check the HTML content
html_file = schema_dir / "schema_visualization.html"
if html_file.exists():
    content = html_file.read_text()
    
    # Check for problematic content
    has_comments = "%%" in content
    has_markdown = "```mermaid" in content
    
    print(f"\n📄 HTML file analysis:")
    print(f"  - Contains %% comments: {has_comments}")
    print(f"  - Contains markdown blocks: {has_markdown}")
    print(f"  - File size: {len(content)} characters")
    
    if not has_comments and not has_markdown:
        print("  ✅ HTML file looks clean!")
    else:
        print("  ❌ HTML file still has issues")
        
        # Show first occurrence
        if has_comments:
            idx = content.find("%%")
            print(f"    Comment found at position {idx}")
        if has_markdown:
            idx = content.find("```mermaid")
            print(f"    Markdown found at position {idx}")
else:
    print("❌ HTML file not found")

print("\n🔧 Fix applied to visualize_schema.py code generation")