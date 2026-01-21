#!/usr/bin/env python3
"""
Analyze ENIGMA CDM parquet files - extract structure, metadata, and descriptions.

This script examines all parquet files in the CDM database to extract:
- Table names and structure
- Column names, types, and descriptions
- Schema metadata (table descriptions, comments)
- Data statistics

The extracted metadata is crucial for:
- Updating the LinkML CDM schema
- Enabling rich metadata searches in DuckDB
- Documenting the data model
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

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


def analyze_parquet_table(table_path: Path, sample_rows: int = 5) -> Dict[str, Any]:
    """
    Analyze a single parquet table to extract metadata and structure.

    Args:
        table_path: Path to parquet file or directory (Delta Lake)
        sample_rows: Number of sample rows to include

    Returns:
        Dict with table metadata, schema, and sample data
    """
    table_name = table_path.name

    # Read parquet metadata
    parquet_files = list(table_path.glob("*.parquet"))
    if not parquet_files:
        return {"error": "No parquet files found"}

    # Get schema from first parquet file
    parquet_file = pq.ParquetFile(parquet_files[0])
    schema = parquet_file.schema_arrow
    metadata = parquet_file.metadata

    # Extract column information
    columns = []
    for i, field in enumerate(schema):
        col_info = {
            'name': field.name,
            'type': str(field.type),
            'nullable': field.nullable,
        }

        # Extract field metadata if available
        if field.metadata:
            col_info['metadata'] = {
                k.decode('utf-8'): v.decode('utf-8')
                for k, v in field.metadata.items()
            }

        columns.append(col_info)

    # Get table-level metadata
    table_metadata = {}
    if metadata.metadata:
        table_metadata = {
            k.decode('utf-8'): v.decode('utf-8')
            for k, v in metadata.metadata.items()
        }

    # Get row count
    total_rows = 0
    for pf in parquet_files:
        parquet_file = pq.ParquetFile(pf)
        total_rows += parquet_file.metadata.num_rows

    # Read sample data
    df = pd.read_parquet(parquet_files[0])
    sample_data = df.head(sample_rows).to_dict('records')

    return {
        'table_name': table_name,
        'num_parquet_files': len(parquet_files),
        'total_rows': total_rows,
        'num_columns': len(columns),
        'columns': columns,
        'table_metadata': table_metadata,
        'sample_data': sample_data[:sample_rows],
    }


def categorize_tables(db_path: Path) -> Dict[str, List[Path]]:
    """Categorize tables by type (static, system, dynamic)."""
    categories = {
        'static': [],
        'system': [],
        'dynamic': []
    }

    for table_dir in sorted(db_path.iterdir()):
        if not table_dir.is_dir():
            continue

        name = table_dir.name
        if name.startswith('sdt_'):
            categories['static'].append(table_dir)
        elif name.startswith('sys_'):
            categories['system'].append(table_dir)
        elif name.startswith('ddt_'):
            categories['dynamic'].append(table_dir)

    return categories


def extract_descriptions_from_metadata(table_info: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract human-readable descriptions from table and column metadata.

    Returns:
        Dict with 'table_description' and 'column_descriptions'
    """
    descriptions = {
        'table_description': None,
        'column_descriptions': {}
    }

    # Check table metadata for description
    table_meta = table_info.get('table_metadata', {})
    for key in ['description', 'comment', 'DESCRIPTION', 'COMMENT']:
        if key in table_meta:
            descriptions['table_description'] = table_meta[key]
            break

    # Extract column descriptions
    for col in table_info.get('columns', []):
        col_name = col['name']
        col_meta = col.get('metadata', {})

        for key in ['description', 'comment', 'DESCRIPTION', 'COMMENT']:
            if key in col_meta:
                descriptions['column_descriptions'][col_name] = col_meta[key]
                break

    return descriptions


def generate_schema_comparison(table_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generate schema information for comparison with LinkML schema."""
    columns_info = {}

    for col in table_info.get('columns', []):
        col_name = col['name']
        col_type = col['type']

        # Map Arrow types to LinkML/Python types
        linkml_type = map_arrow_type_to_linkml(col_type)

        columns_info[col_name] = {
            'parquet_type': col_type,
            'linkml_type': linkml_type,
            'nullable': col.get('nullable', True),
            'description': col.get('metadata', {}).get('description', ''),
        }

    return columns_info


def map_arrow_type_to_linkml(arrow_type: str) -> str:
    """Map Arrow/Parquet types to LinkML types."""
    type_map = {
        'int64': 'integer',
        'int32': 'integer',
        'double': 'float',
        'float': 'float',
        'string': 'string',
        'bool': 'boolean',
        'timestamp': 'datetime',
        'date32': 'date',
    }

    arrow_type_lower = arrow_type.lower()

    # Handle list types
    if 'list' in arrow_type_lower:
        return 'string'  # Will be multivalued in LinkML

    # Map basic types
    for key, value in type_map.items():
        if key in arrow_type_lower:
            return value

    return 'string'  # Default


def main():
    parser = argparse.ArgumentParser(
        description='Analyze ENIGMA CDM parquet files - extract metadata and descriptions',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'cdm_database',
        type=Path,
        default=Path('data/enigma_coral.db'),
        nargs='?',
        help='Path to CDM database directory (default: data/enigma_coral.db)'
    )

    parser.add_argument(
        '--output',
        type=Path,
        help='Output JSON file for full analysis (default: print to stdout)'
    )

    parser.add_argument(
        '--descriptions-only',
        action='store_true',
        help='Only extract and show descriptions (for schema updates)'
    )

    parser.add_argument(
        '--schema-comparison',
        action='store_true',
        help='Generate schema comparison for LinkML updates'
    )

    parser.add_argument(
        '--table',
        help='Analyze only this specific table'
    )

    parser.add_argument(
        '--category',
        choices=['static', 'system', 'dynamic', 'all'],
        default='all',
        help='Which table category to analyze (default: all)'
    )

    parser.add_argument(
        '--sample-rows',
        type=int,
        default=5,
        help='Number of sample rows to include (default: 5)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress'
    )

    args = parser.parse_args()

    # Validate path
    if not args.cdm_database.exists():
        print(f"Error: CDM database not found: {args.cdm_database}", file=sys.stderr)
        sys.exit(1)

    print(f"📊 Analyzing ENIGMA CDM Parquet Files")
    print(f"{'='*70}\n")
    print(f"📂 Database: {args.cdm_database}\n")

    # Categorize tables
    categories = categorize_tables(args.cdm_database)

    # Filter by category
    tables_to_analyze = []
    if args.category == 'all':
        tables_to_analyze = categories['static'] + categories['system'] + categories['dynamic']
    else:
        tables_to_analyze = categories[args.category]

    # Filter by specific table
    if args.table:
        tables_to_analyze = [t for t in tables_to_analyze if t.name == args.table]
        if not tables_to_analyze:
            print(f"Error: Table '{args.table}' not found", file=sys.stderr)
            sys.exit(1)

    # Analyze tables
    results = {
        'database_path': str(args.cdm_database),
        'total_tables': len(tables_to_analyze),
        'categories': {
            'static': len(categories['static']),
            'system': len(categories['system']),
            'dynamic': len(categories['dynamic']),
        },
        'tables': {}
    }

    print(f"📋 Table Categories:")
    print(f"   • Static (sdt_*):  {len(categories['static'])} tables")
    print(f"   • System (sys_*):  {len(categories['system'])} tables")
    print(f"   • Dynamic (ddt_*): {len(categories['dynamic'])} tables")
    print(f"\n{'='*70}\n")

    # Analyze each table
    for i, table_path in enumerate(tables_to_analyze, 1):
        table_name = table_path.name

        if args.verbose:
            print(f"[{i}/{len(tables_to_analyze)}] Analyzing {table_name}...")

        try:
            table_info = analyze_parquet_table(table_path, sample_rows=args.sample_rows)
            results['tables'][table_name] = table_info

            # Print summary
            if not args.descriptions_only and not args.schema_comparison:
                print(f"📦 {table_name}")
                print(f"   Rows: {table_info['total_rows']:,}")
                print(f"   Columns: {table_info['num_columns']}")

                # Show metadata if present
                if table_info.get('table_metadata'):
                    print(f"   Table metadata: {len(table_info['table_metadata'])} entries")

                # Show column descriptions if present
                col_with_desc = sum(1 for col in table_info['columns'] if col.get('metadata'))
                if col_with_desc > 0:
                    print(f"   Columns with metadata: {col_with_desc}")

                print()

        except Exception as e:
            print(f"   ❌ Error analyzing {table_name}: {e}")
            results['tables'][table_name] = {'error': str(e)}

    # Generate descriptions report
    if args.descriptions_only:
        print(f"\n{'='*70}")
        print(f"📝 TABLE AND COLUMN DESCRIPTIONS")
        print(f"{'='*70}\n")

        for table_name, table_info in results['tables'].items():
            if 'error' in table_info:
                continue

            descriptions = extract_descriptions_from_metadata(table_info)

            print(f"## {table_name}")
            if descriptions['table_description']:
                print(f"   Description: {descriptions['table_description']}")
            else:
                print(f"   Description: (none)")

            if descriptions['column_descriptions']:
                print(f"\n   Column Descriptions:")
                for col_name, desc in descriptions['column_descriptions'].items():
                    print(f"      • {col_name}: {desc}")
            else:
                print(f"   Column Descriptions: (none)")

            print()

    # Generate schema comparison
    if args.schema_comparison:
        print(f"\n{'='*70}")
        print(f"🔍 SCHEMA COMPARISON (for LinkML updates)")
        print(f"{'='*70}\n")

        for table_name, table_info in results['tables'].items():
            if 'error' in table_info:
                continue

            print(f"## {table_name}")
            schema_info = generate_schema_comparison(table_info)

            for col_name, col_details in schema_info.items():
                print(f"   {col_name}:")
                print(f"      Type: {col_details['parquet_type']} → {col_details['linkml_type']}")
                print(f"      Nullable: {col_details['nullable']}")
                if col_details['description']:
                    print(f"      Description: {col_details['description']}")

            print()

    # Save full results to JSON
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Full analysis saved to: {args.output}")

    # Print summary
    print(f"\n{'='*70}")
    print(f"✅ ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print(f"Analyzed {len(results['tables'])} tables")

    # Count tables with descriptions
    tables_with_desc = sum(
        1 for info in results['tables'].values()
        if info.get('table_metadata') and 'error' not in info
    )
    print(f"Tables with metadata: {tables_with_desc}")


if __name__ == "__main__":
    main()
