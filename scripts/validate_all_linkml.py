#!/usr/bin/env python3
"""
Batch validate all TSV files in ENIGMA_ASV_export directory using linkml-validate.
"""

import subprocess
import sys
import time
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
    
    print(f"🔍 Found {len(tsv_files)} TSV files to validate")
    print(f"📁 Directory: {tsv_dir}")
    print(f"🚀 Starting batch validation with linkml-validate...")
    print("="*80)
    
    # Build command with all TSV file paths
    cmd = [
        "uv", "run", "python", "validate_tsv_linkml.py",
        "--max-errors", "5",
        "--save-yaml", "batch_validation_yaml"
    ]
    
    # Add all TSV file paths
    for tsv_file in sorted(tsv_files):
        cmd.append(str(tsv_file))
    
    start_time = time.time()
    
    try:
        # Run the validation
        result = subprocess.run(
            cmd,
            cwd=Path(__file__).parent,
            timeout=1800  # 30 minute timeout for all files
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("="*80)
        print(f"⏱️  Total validation time: {duration:.1f} seconds")
        
        if result.returncode == 0:
            print("🎉 Batch validation completed successfully!")
        else:
            print("⚠️  Batch validation completed with errors")
            
        sys.exit(result.returncode)
        
    except subprocess.TimeoutExpired:
        print("❌ Validation timed out after 30 minutes")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⛔ Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running validation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()