#!/usr/bin/env python3
"""
Batch validate all TSV files in ENIGMA_ASV_export directory.
"""

import subprocess
import sys
from pathlib import Path

def main():
    # Path to ENIGMA TSV files
    tsv_dir = Path("/Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export")
    
    if not tsv_dir.exists():
        print(f"Error: Directory not found: {tsv_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Find all TSV files
    tsv_files = list(tsv_dir.glob("*.tsv"))
    
    if not tsv_files:
        print(f"No TSV files found in {tsv_dir}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(tsv_files)} TSV files to validate:\n")
    
    # Validate each file
    total_errors = 0
    
    for tsv_file in sorted(tsv_files):
        print(f"Validating {tsv_file.name}...")
        
        try:
            result = subprocess.run(
                ["uv", "run", "python", "validate_tsv.py", str(tsv_file)],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            
            # Print result
            if result.returncode == 0:
                # Extract validation summary from output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if "All" in line and "records are valid" in line:
                        print(f"  ✅ {line.strip()}")
                        break
            else:
                print(f"  ❌ Validation failed")
                if result.stderr:
                    print(f"     Error: {result.stderr.strip()}")
                total_errors += 1
                
        except Exception as e:
            print(f"  ❌ Error running validation: {e}")
            total_errors += 1
    
    # Summary
    print(f"\n" + "="*50)
    if total_errors == 0:
        print("🎉 All TSV files validated successfully!")
    else:
        print(f"❌ {total_errors} files failed validation")
        sys.exit(1)

if __name__ == "__main__":
    main()