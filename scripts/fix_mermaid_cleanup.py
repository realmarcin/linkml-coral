#!/usr/bin/env python3
"""
Fix for LinkML gen-erdiagram markdown cleanup issues.
This script directly tests and fixes the markdown cleanup.
"""

import subprocess
import re

def clean_mermaid_content(content: str) -> str:
    """
    Comprehensive cleanup of LinkML gen-erdiagram output.
    Removes all markdown artifacts that cause mermaid-cli parsing errors.
    """
    # Remove markdown code block markers
    content = re.sub(r'^```mermaid\s*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n```\s*$', '', content, flags=re.MULTILINE)
    
    # Remove any standalone ``` lines
    lines = content.split('\n')
    clean_lines = []
    
    for line in lines:
        stripped = line.strip()
        # Skip empty lines or lines that are just backticks
        if stripped and not re.match(r'^`{3,}', stripped):
            clean_lines.append(line)
    
    # Join and clean up whitespace
    result = '\n'.join(clean_lines).strip()
    
    # Final check - remove any trailing backticks that might remain
    result = re.sub(r'```+\s*$', '', result, flags=re.MULTILINE).strip()
    
    return result

def test_gen_erdiagram():
    """Test gen-erdiagram output and apply cleanup."""
    print("Testing gen-erdiagram output...")
    
    # Run gen-erdiagram
    result = subprocess.run([
        'uv', 'run', 'gen-erdiagram', 
        'src/linkml_coral/schema/linkml_coral.yaml',
        '--exclude-attributes'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running gen-erdiagram: {result.stderr}")
        return False
    
    print("Raw output (last 10 lines):")
    lines = result.stdout.split('\n')
    for i, line in enumerate(lines[-10:]):
        print(f"{len(lines)-10+i:3d}: {repr(line)}")
    
    # Apply cleanup
    clean_content = clean_mermaid_content(result.stdout)
    
    print("\nCleaned output (last 10 lines):")
    clean_lines = clean_content.split('\n')
    for i, line in enumerate(clean_lines[-10:]):
        print(f"{len(clean_lines)-10+i:3d}: {repr(line)}")
    
    # Save cleaned version
    with open('test_clean.mmd', 'w') as f:
        f.write(clean_content)
    
    print(f"\nSaved cleaned content to test_clean.mmd ({len(clean_content)} chars)")
    
    # Test with mermaid-cli if available
    try:
        test_result = subprocess.run([
            'mmdc', '-i', 'test_clean.mmd', '-o', 'test_clean.png'
        ], capture_output=True, text=True)
        
        if test_result.returncode == 0:
            print("✅ mermaid-cli conversion successful!")
        else:
            print(f"❌ mermaid-cli error: {test_result.stderr}")
    except FileNotFoundError:
        print("⚠️  mermaid-cli not found, skipping conversion test")
    
    return True

if __name__ == "__main__":
    test_gen_erdiagram()