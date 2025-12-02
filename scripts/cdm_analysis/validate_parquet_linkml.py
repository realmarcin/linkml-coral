#!/usr/bin/env python3
"""
Validate CDM parquet files against LinkML schema.

This script validates parquet files from the KBase CDM database against the
CDM LinkML schema. Since linkml-validate doesn't natively support parquet,
this converts parquet → YAML → validates with linkml-validate.

Usage:
    python validate_parquet_linkml.py <parquet_file> --class <class_name>
    python validate_parquet_linkml.py /path/to/sdt_sample.parquet --class Sample
    python validate_parquet_linkml.py /path/to/*.parquet --batch
"""

import argparse
import sys
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import yaml

try:
    import pandas as pd
except ImportError:
    print("Error: pandas not installed. Run: uv pip install pandas")
    sys.exit(1)

try:
    import pyarrow.parquet as pq
except ImportError:
    print("Error: pyarrow not installed. Run: uv pip install pyarrow")
    sys.exit(1)


# CDM Schema path (relative to script location)
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
CDM_SCHEMA = REPO_ROOT / "src/linkml_coral/schema/cdm/linkml_coral_cdm.yaml"


# Mapping from CDM table names to LinkML class names
TABLE_TO_CLASS = {
    "sdt_location": "Location",
    "sdt_sample": "Sample",
    "sdt_community": "Community",
    "sdt_reads": "Reads",
    "sdt_assembly": "Assembly",
    "sdt_bin": "Bin",
    "sdt_genome": "Genome",
    "sdt_gene": "Gene",
    "sdt_strain": "Strain",
    "sdt_taxon": "Taxon",
    "sdt_asv": "ASV",
    "sdt_protocol": "Protocol",
    "sdt_image": "Image",
    "sdt_condition": "Condition",
    "sdt_dubseq_library": "DubSeqLibrary",
    "sdt_tnseq_library": "TnSeqLibrary",
    "sdt_enigma": "ENIGMA",
    "sys_typedef": "SystemTypedef",
    "sys_ddt_typedef": "SystemDDTTypedef",
    "sys_oterm": "SystemOntologyTerm",
    "sys_process": "SystemProcess",
    "sys_process_input": "SystemProcessInput",
    "sys_process_output": "SystemProcessOutput",
    "ddt_ndarray": "DynamicDataArray",
}


def get_class_from_table(table_name: str) -> Optional[str]:
    """
    Infer LinkML class name from parquet table/file name.

    Args:
        table_name: Name like "sdt_sample" or path like "/path/to/sdt_sample.parquet"

    Returns:
        Class name like "Sample" or None if not found
    """
    # Extract base name without extension
    base_name = Path(table_name).stem.lower()

    # Try exact match
    if base_name in TABLE_TO_CLASS:
        return TABLE_TO_CLASS[base_name]

    # Try removing common prefixes/suffixes
    for prefix in ["", "ddt_brick"]:
        test_name = base_name.replace(prefix, "").strip("_")
        if test_name in TABLE_TO_CLASS:
            return TABLE_TO_CLASS[test_name]

    return None


def read_parquet_sample(
    parquet_path: Path,
    max_rows: Optional[int] = None,
    offset: int = 0
) -> pd.DataFrame:
    """
    Read parquet file with optional row limits.

    Args:
        parquet_path: Path to parquet file or directory
        max_rows: Maximum rows to read (None = all)
        offset: Number of rows to skip

    Returns:
        DataFrame with parquet data
    """
    if parquet_path.is_dir():
        # Delta Lake format - read all parquet files in directory
        parquet_files = list(parquet_path.glob("*.parquet"))
        if not parquet_files:
            raise ValueError(f"No parquet files found in {parquet_path}")

        # Read first file for schema
        df = pd.read_parquet(parquet_files[0])

        # Read remaining files if needed
        if max_rows is None or len(df) < max_rows:
            for pf in parquet_files[1:]:
                chunk = pd.read_parquet(pf)
                df = pd.concat([df, chunk], ignore_index=True)
                if max_rows and len(df) >= max_rows:
                    break
    else:
        # Single parquet file
        df = pd.read_parquet(parquet_path)

    # Apply offset and limit
    if offset > 0:
        df = df.iloc[offset:]
    if max_rows is not None:
        df = df.head(max_rows)

    return df


def get_parquet_row_count(parquet_path: Path) -> int:
    """Get total row count without loading entire file."""
    if parquet_path.is_dir():
        # Delta Lake - sum all parquet files
        total = 0
        for pf in parquet_path.glob("*.parquet"):
            parquet_file = pq.ParquetFile(pf)
            total += parquet_file.metadata.num_rows
        return total
    else:
        parquet_file = pq.ParquetFile(parquet_path)
        return parquet_file.metadata.num_rows


def validate_with_linkml(
    df: pd.DataFrame,
    class_name: str,
    schema_path: Path,
    verbose: bool = False
) -> Tuple[bool, str]:
    """
    Validate DataFrame against LinkML schema.

    Args:
        df: DataFrame with data to validate
        class_name: LinkML class name (e.g., "Sample")
        schema_path: Path to LinkML schema YAML
        verbose: Print detailed validation output

    Returns:
        Tuple of (success: bool, output: str)
    """
    # Convert DataFrame to list of dicts
    records = df.to_dict('records')

    # Handle NaN values (convert to None for YAML)
    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None

    # Convert to YAML
    yaml_data = yaml.dump(records, Dumper=yaml.SafeDumper, default_flow_style=False)

    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_data)
        temp_yaml = Path(f.name)

    try:
        # Run linkml-validate
        result = subprocess.run(
            [
                'linkml-validate',
                '-s', str(schema_path),
                '-C', class_name,
                str(temp_yaml)
            ],
            capture_output=True,
            text=True
        )

        success = result.returncode == 0
        output = result.stdout + result.stderr

        if verbose or not success:
            print(output)

        return success, output

    finally:
        # Cleanup temp file
        temp_yaml.unlink()


def validate_parquet_file(
    parquet_path: Path,
    class_name: Optional[str] = None,
    max_rows: Optional[int] = None,
    chunk_size: Optional[int] = None,
    verbose: bool = False,
    schema_path: Optional[Path] = None
) -> bool:
    """
    Validate a parquet file against CDM LinkML schema.

    Args:
        parquet_path: Path to parquet file or directory
        class_name: LinkML class name (auto-detected if None)
        max_rows: Maximum rows to validate (None = all)
        chunk_size: Validate in chunks (for large files)
        verbose: Print detailed output
        schema_path: Path to schema (default: CDM schema)

    Returns:
        True if validation passed
    """
    if schema_path is None:
        schema_path = CDM_SCHEMA

    if not schema_path.exists():
        print(f"Error: Schema not found at {schema_path}")
        return False

    # Auto-detect class name if not provided
    if class_name is None:
        class_name = get_class_from_table(parquet_path.name)
        if class_name is None:
            print(f"Error: Could not infer class name from {parquet_path.name}")
            print("Please specify --class explicitly")
            return False
        if verbose:
            print(f"Auto-detected class: {class_name}")

    # Get total row count
    total_rows = get_parquet_row_count(parquet_path)

    if verbose:
        print(f"\nValidating {parquet_path.name}")
        print(f"  Class: {class_name}")
        print(f"  Total rows: {total_rows:,}")
        if max_rows:
            print(f"  Validating: {min(max_rows, total_rows):,} rows")

    # Determine validation strategy
    if chunk_size:
        # Chunked validation for large files
        offset = 0
        all_success = True

        while offset < (max_rows or total_rows):
            rows_to_read = min(chunk_size, (max_rows or total_rows) - offset)

            if verbose:
                print(f"\n  Validating rows {offset:,} to {offset + rows_to_read:,}...")

            df = read_parquet_sample(parquet_path, max_rows=rows_to_read, offset=offset)

            if df.empty:
                break

            success, output = validate_with_linkml(df, class_name, schema_path, verbose=verbose)

            if not success:
                all_success = False
                print(f"  ❌ Validation failed for chunk at offset {offset}")
            elif verbose:
                print(f"  ✅ Chunk validated successfully")

            offset += len(df)

        return all_success

    else:
        # Single validation
        df = read_parquet_sample(parquet_path, max_rows=max_rows)

        if df.empty:
            print("Warning: Empty DataFrame")
            return True

        success, output = validate_with_linkml(df, class_name, schema_path, verbose=verbose)

        if success:
            if verbose:
                print(f"✅ Validation passed ({len(df):,} rows)")
        else:
            print(f"❌ Validation failed")

        return success


def main():
    parser = argparse.ArgumentParser(
        description="Validate CDM parquet files against LinkML schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate specific file with auto-detected class
  python validate_parquet_linkml.py /path/to/sdt_sample.parquet

  # Validate with explicit class name
  python validate_parquet_linkml.py /path/to/sdt_sample.parquet --class Sample

  # Validate first 1000 rows only
  python validate_parquet_linkml.py /path/to/sdt_sample.parquet --max-rows 1000

  # Validate in chunks (for large files)
  python validate_parquet_linkml.py /path/to/large_table.parquet --chunk-size 10000

  # Use custom schema
  python validate_parquet_linkml.py file.parquet --schema my_schema.yaml --class MyClass
        """
    )

    parser.add_argument(
        'parquet_file',
        type=Path,
        help='Path to parquet file or directory'
    )

    parser.add_argument(
        '--class', '-C',
        dest='class_name',
        help='LinkML class name (auto-detected if not specified)'
    )

    parser.add_argument(
        '--schema', '-s',
        type=Path,
        help=f'Path to LinkML schema (default: {CDM_SCHEMA.relative_to(REPO_ROOT)})'
    )

    parser.add_argument(
        '--max-rows',
        type=int,
        help='Maximum number of rows to validate (default: all)'
    )

    parser.add_argument(
        '--chunk-size',
        type=int,
        help='Validate in chunks of this size (for large files)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Print detailed validation output'
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.parquet_file.exists():
        print(f"Error: File not found: {args.parquet_file}")
        sys.exit(1)

    # Run validation
    try:
        success = validate_parquet_file(
            parquet_path=args.parquet_file,
            class_name=args.class_name,
            max_rows=args.max_rows,
            chunk_size=args.chunk_size,
            verbose=args.verbose,
            schema_path=args.schema
        )

        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"Error during validation: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
