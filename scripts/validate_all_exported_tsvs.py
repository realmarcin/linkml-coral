#!/usr/bin/env python3
"""
Batch validation script for all exported ENIGMA TSV files.

This script validates all TSV files in the data/export/exported_tsvs/ directory
against the CORAL LinkML schema with comprehensive enum, FK, and quality validation.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple


def find_tsv_files(directory: Path, exclude_patterns: List[str] = None) -> List[Path]:
    """
    Find all TSV files in a directory.

    Args:
        directory: Directory to search
        exclude_patterns: List of filename patterns to exclude

    Returns:
        List of TSV file paths
    """
    if exclude_patterns is None:
        exclude_patterns = ['ASV_count']  # Measurement tables without direct class mapping

    tsv_files = []
    for tsv_file in directory.glob('*.tsv'):
        # Check if file should be excluded
        should_exclude = any(pattern in tsv_file.name for pattern in exclude_patterns)
        if not should_exclude:
            tsv_files.append(tsv_file)

    return sorted(tsv_files)


def run_validation(
    tsv_files: List[Path],
    tsv_dir: Path,
    enable_enum: bool = True,
    enable_fk: bool = True,
    enable_quality: bool = True,
    report_format: str = 'all',
    output_dir: Path = None,
    verbose: bool = False
) -> Tuple[int, str]:
    """
    Run validation on TSV files.

    Args:
        tsv_files: List of TSV files to validate
        tsv_dir: Directory containing TSV files (for FK index)
        enable_enum: Enable enum validation
        enable_fk: Enable FK validation
        enable_quality: Enable quality metrics
        report_format: Report format (console, json, csv, all)
        output_dir: Output directory for reports
        verbose: Verbose output

    Returns:
        Tuple of (return_code, output)
    """
    # Build command
    cmd = [
        'uv', 'run', 'python', 'validate_tsv_linkml.py'
    ]

    # Add TSV files
    cmd.extend([str(f) for f in tsv_files])

    # Add validation options
    if enable_enum:
        cmd.append('--enum-validate')

    if enable_fk:
        cmd.extend(['--fk-validate', '--tsv-dir', str(tsv_dir)])

    if enable_quality:
        cmd.append('--quality-metrics')

    # Add reporting options
    cmd.extend(['--report-format', report_format])

    if output_dir:
        cmd.extend(['--output-dir', str(output_dir)])

    if verbose:
        cmd.append('--verbose')

    # Run validation
    print(f"Running validation command:")
    print(f"  {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )

        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        return result.returncode, result.stdout

    except subprocess.TimeoutExpired:
        error_msg = "❌ Validation timed out after 1 hour"
        print(error_msg, file=sys.stderr)
        return 1, error_msg
    except Exception as e:
        error_msg = f"❌ Error running validation: {e}"
        print(error_msg, file=sys.stderr)
        return 1, error_msg


def main():
    parser = argparse.ArgumentParser(
        description='Batch validate all exported ENIGMA TSV files'
    )
    parser.add_argument('--tsv-dir',
                       default='data/export/exported_tsvs',
                       help='Directory containing TSV files (default: data/export/exported_tsvs)')
    parser.add_argument('--output-dir',
                       help='Output directory for reports (default: validation_reports/)')
    parser.add_argument('--no-enum', action='store_true',
                       help='Disable enum validation')
    parser.add_argument('--no-fk', action='store_true',
                       help='Disable FK validation')
    parser.add_argument('--no-quality', action='store_true',
                       help='Disable quality metrics')
    parser.add_argument('--report-format', choices=['console', 'json', 'csv', 'all'],
                       default='all',
                       help='Report format (default: all)')
    parser.add_argument('--exclude',
                       nargs='+',
                       help='Filename patterns to exclude')
    parser.add_argument('--include',
                       nargs='+',
                       help='Only validate files matching these patterns')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    # Check TSV directory
    tsv_dir = Path(args.tsv_dir)
    if not tsv_dir.exists():
        print(f"Error: TSV directory not found: {tsv_dir}", file=sys.stderr)
        sys.exit(1)

    # Setup output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = Path(f'validation_reports/batch_{timestamp}')

    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("ENIGMA TSV Batch Validation")
    print("="*70)
    print(f"TSV directory: {tsv_dir}")
    print(f"Output directory: {output_dir}")
    print()

    # Find TSV files
    exclude_patterns = args.exclude if args.exclude else ['ASV_count']
    all_tsv_files = find_tsv_files(tsv_dir, exclude_patterns)

    # Filter by include patterns if specified
    if args.include:
        filtered_files = []
        for tsv_file in all_tsv_files:
            if any(pattern in tsv_file.name for pattern in args.include):
                filtered_files.append(tsv_file)
        tsv_files = filtered_files
    else:
        tsv_files = all_tsv_files

    if not tsv_files:
        print("No TSV files found to validate", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(tsv_files)} TSV files to validate:")
    for tsv_file in tsv_files:
        print(f"  - {tsv_file.name}")
    print()

    # Validation settings
    print("Validation settings:")
    print(f"  Enum validation: {'enabled' if not args.no_enum else 'disabled'}")
    print(f"  FK validation: {'enabled' if not args.no_fk else 'disabled'}")
    print(f"  Quality metrics: {'enabled' if not args.no_quality else 'disabled'}")
    print(f"  Report format: {args.report_format}")
    print()

    # Run validation
    return_code, output = run_validation(
        tsv_files=tsv_files,
        tsv_dir=tsv_dir,
        enable_enum=not args.no_enum,
        enable_fk=not args.no_fk,
        enable_quality=not args.no_quality,
        report_format=args.report_format,
        output_dir=output_dir,
        verbose=args.verbose
    )

    # Final summary
    print()
    print("="*70)
    if return_code == 0:
        print("✅ Batch validation completed successfully")
        print(f"📁 Reports saved to: {output_dir}")
    else:
        print("⚠️  Batch validation completed with errors")
        print(f"📁 Reports saved to: {output_dir}")
    print("="*70)

    sys.exit(return_code)


if __name__ == "__main__":
    main()
