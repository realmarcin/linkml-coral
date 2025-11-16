#!/usr/bin/env python3
"""
Validate TSV files and generate detailed reports.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Import from our validation script
import subprocess

def run_validation_with_report(tsv_files, output_dir="validation_reports"):
    """Run validation and create detailed reports."""
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Create timestamp for this validation run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Results summary
    results = {
        "timestamp": timestamp,
        "files_validated": [],
        "total_errors": 0,
        "summary": {}
    }
    
    print(f"Starting validation run at {timestamp}")
    print(f"Reports will be saved to: {output_path}")
    print("="*60)
    
    for tsv_file in tsv_files:
        tsv_path = Path(tsv_file)
        if not tsv_path.exists():
            print(f"❌ File not found: {tsv_file}")
            continue
            
        print(f"\nValidating {tsv_path.name}...")
        
        # Run validation and capture output
        try:
            result = subprocess.run(
                ["uv", "run", "python", "validate_tsv.py", str(tsv_path), "--verbose"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            
            # Create individual file report
            file_report = {
                "file": str(tsv_path),
                "filename": tsv_path.name,
                "validation_time": datetime.now().isoformat(),
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
            
            # Save individual report
            report_file = output_path / f"{tsv_path.stem}_validation_{timestamp}.txt"
            with open(report_file, 'w') as f:
                f.write(f"Validation Report for {tsv_path.name}\n")
                f.write(f"Generated: {datetime.now()}\n")
                f.write("="*60 + "\n\n")
                f.write("STDOUT:\n")
                f.write(result.stdout)
                if result.stderr:
                    f.write("\nSTDERR:\n")
                    f.write(result.stderr)
            
            # Update summary
            results["files_validated"].append(file_report)
            if result.returncode != 0:
                results["total_errors"] += 1
                
            # Extract validation info from output
            if "All" in result.stdout and "records are valid" in result.stdout:
                # Parse number of records
                for line in result.stdout.split('\n'):
                    if "Read" in line and "records" in line:
                        try:
                            record_count = int(line.split()[1])
                            results["summary"][tsv_path.name] = {
                                "status": "valid",
                                "records": record_count,
                                "errors": 0
                            }
                        except:
                            pass
                print(f"  ✅ Validation successful - report saved to {report_file}")
            else:
                # Count errors
                error_count = result.stdout.count("validation errors:")
                results["summary"][tsv_path.name] = {
                    "status": "invalid", 
                    "errors": error_count
                }
                print(f"  ❌ Validation failed - report saved to {report_file}")
                
        except Exception as e:
            print(f"  ❌ Error running validation: {e}")
            results["total_errors"] += 1
    
    # Create summary report
    summary_file = output_path / f"validation_summary_{timestamp}.json"
    with open(summary_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Create human-readable summary
    summary_txt_file = output_path / f"validation_summary_{timestamp}.txt"
    with open(summary_txt_file, 'w') as f:
        f.write(f"Validation Summary Report\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"Files validated: {len(results['files_validated'])}\n")
        f.write(f"Total errors: {results['total_errors']}\n\n")
        
        f.write("Results by file:\n")
        f.write("-" * 40 + "\n")
        for filename, info in results["summary"].items():
            status_icon = "✅" if info["status"] == "valid" else "❌"
            if info["status"] == "valid":
                f.write(f"{status_icon} {filename}: {info['records']} records valid\n")
            else:
                f.write(f"{status_icon} {filename}: {info['errors']} errors\n")
    
    print("\n" + "="*60)
    print(f"Validation complete!")
    print(f"Summary report: {summary_txt_file}")
    print(f"Detailed JSON: {summary_file}")
    print(f"Individual reports: {output_path}/*_validation_{timestamp}.txt")
    
    return results["total_errors"] == 0

def main():
    parser = argparse.ArgumentParser(description='Validate TSV files and generate reports')
    parser.add_argument('tsv_files', nargs='+', help='TSV files to validate')
    parser.add_argument('--output-dir', default='validation_reports',
                       help='Directory to save validation reports')
    
    args = parser.parse_args()
    
    success = run_validation_with_report(args.tsv_files, args.output_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()