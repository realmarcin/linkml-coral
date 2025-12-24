#!/usr/bin/env python3
"""
Extract ENIGMA CDM metadata from Spark parquet files.

This script parses the rich metadata stored in Spark-generated parquet files:
- Table-level metadata
- Column descriptions (from comment field)
- Column types and microtypes (ME: terms)
- Units (UO: terms)
- Constraints (primary keys, foreign keys, unique keys)
- Validation patterns
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import pyarrow.parquet as pq
except ImportError:
    print("Error: pyarrow not installed. Run: uv pip install pyarrow")
    sys.exit(1)


def parse_spark_row_metadata(parquet_file: pq.ParquetFile) -> Dict[str, Any]:
    """
    Parse Spark's org.apache.spark.sql.parquet.row.metadata.

    Returns:
        Dict with table and column metadata
    """
    metadata_key = b'org.apache.spark.sql.parquet.row.metadata'

    if not parquet_file.metadata.metadata or metadata_key not in parquet_file.metadata.metadata:
        return {}

    # Parse JSON metadata
    metadata_json = parquet_file.metadata.metadata[metadata_key].decode('utf-8')
    metadata = json.loads(metadata_json)

    return metadata


def extract_column_metadata(field_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract structured metadata from a Spark field.

    The 'comment' field contains JSON with:
    - description: Human-readable description
    - type: Field type (primary_key, foreign_key, unique_key, etc.)
    - references: FK target table.column
    - unit: Unit label
    """
    extracted = {}

    # Parse comment JSON if present
    if 'comment' in field_metadata:
        try:
            comment_data = json.loads(field_metadata['comment'])
            extracted['description'] = comment_data.get('description', '')
            extracted['field_type'] = comment_data.get('type', '')
            extracted['references'] = comment_data.get('references', '')
            extracted['unit_label'] = comment_data.get('unit', '')
        except json.JSONDecodeError:
            # Comment is not JSON, use as-is
            extracted['description'] = field_metadata['comment']

    # Add other metadata
    extracted['microtype'] = field_metadata.get('type_sys_oterm_id', '')
    extracted['units'] = field_metadata.get('units_sys_oterm_id', '')
    extracted['constraint'] = field_metadata.get('constraint', '')
    extracted['required'] = field_metadata.get('required', False)
    extracted['pk'] = field_metadata.get('pk', False)
    extracted['upk'] = field_metadata.get('upk', False)
    extracted['fk'] = field_metadata.get('fk', '')
    extracted['orig_name'] = field_metadata.get('orig_name', '')

    return extracted


def analyze_table(table_path: Path) -> Dict[str, Any]:
    """
    Analyze a single table and extract all metadata.

    Returns:
        Dict with table info and column metadata
    """
    table_name = table_path.name

    # Find parquet files
    parquet_files = list(table_path.glob("*.parquet"))
    if not parquet_files:
        return {'error': 'No parquet files found'}

    # Read first file for schema
    parquet_file = pq.ParquetFile(parquet_files[0])
    schema = parquet_file.schema_arrow

    # Parse Spark metadata
    spark_metadata = parse_spark_row_metadata(parquet_file)

    if not spark_metadata:
        return {'error': 'No Spark metadata found'}

    # Extract column information
    columns = {}
    for field_meta in spark_metadata.get('fields', []):
        col_name = field_meta['name']
        col_type = field_meta['type']
        col_nullable = field_meta.get('nullable', True)
        col_metadata = field_meta.get('metadata', {})

        # Extract structured metadata
        metadata = extract_column_metadata(col_metadata)

        columns[col_name] = {
            'type': col_type,
            'nullable': col_nullable,
            **metadata
        }

    # Count rows
    total_rows = sum(pq.ParquetFile(pf).metadata.num_rows for pf in parquet_files)

    return {
        'table_name': table_name,
        'total_rows': total_rows,
        'num_columns': len(columns),
        'columns': columns
    }


def generate_schema_yaml(table_info: Dict[str, Any], class_name: str) -> str:
    """
    Generate LinkML schema YAML for a table.

    Args:
        table_info: Table metadata from analyze_table()
        class_name: LinkML class name (e.g., "Sample")

    Returns:
        YAML string for the class definition
    """
    yaml_lines = []

    yaml_lines.append(f"  {class_name}:")
    yaml_lines.append(f"    description: >-")
    yaml_lines.append(f"      {table_info['table_name']} - {table_info['total_rows']:,} records")
    yaml_lines.append(f"    slots:")

    # Add slots
    for col_name, col_meta in table_info['columns'].items():
        yaml_lines.append(f"      - {col_name}")

    yaml_lines.append("")

    # Add slot definitions
    for col_name, col_meta in table_info['columns'].items():
        yaml_lines.append(f"  {col_name}:")

        if col_meta.get('description'):
            desc = col_meta['description'].replace('\n', ' ')
            yaml_lines.append(f"    description: {desc}")

        # Type mapping
        linkml_type = map_parquet_type_to_linkml(col_meta['type'])
        if linkml_type:
            yaml_lines.append(f"    range: {linkml_type}")

        # Required/identifier
        if col_meta.get('pk'):
            yaml_lines.append(f"    identifier: true")
            yaml_lines.append(f"    required: true")
        elif col_meta.get('upk'):
            yaml_lines.append(f"    required: true")
        elif col_meta.get('required'):
            yaml_lines.append(f"    required: true")

        # Microtype annotation
        if col_meta.get('microtype'):
            yaml_lines.append(f"    annotations:")
            yaml_lines.append(f"      microtype: {col_meta['microtype']}")

        # Units
        if col_meta.get('units'):
            if not col_meta.get('microtype'):  # Add annotations section if not already there
                yaml_lines.append(f"    annotations:")
            yaml_lines.append(f"      units: {col_meta['units']}")

        yaml_lines.append("")

    return '\n'.join(yaml_lines)


def map_parquet_type_to_linkml(parquet_type: str) -> str:
    """Map Parquet/Spark types to LinkML types."""
    type_map = {
        'long': 'integer',
        'integer': 'integer',
        'double': 'float',
        'float': 'float',
        'string': 'string',
        'boolean': 'boolean',
        'timestamp': 'datetime',
        'date': 'date',
    }

    return type_map.get(parquet_type, 'string')


def main():
    parser = argparse.ArgumentParser(
        description='Extract ENIGMA CDM metadata from Spark parquet files'
    )

    parser.add_argument(
        'cdm_database',
        type=Path,
        nargs='?',
        default=Path('data/jmc_coral.db'),
        help='Path to CDM database directory (default: data/jmc_coral.db)'
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
        '--output',
        type=Path,
        help='Save metadata to JSON file'
    )

    parser.add_argument(
        '--generate-schema',
        action='store_true',
        help='Generate LinkML schema YAML'
    )

    parser.add_argument(
        '--format',
        choices=['summary', 'detailed', 'json'],
        default='detailed',
        help='Output format (default: detailed)'
    )

    args = parser.parse_args()

    if not args.cdm_database.exists():
        print(f"Error: Database not found: {args.cdm_database}", file=sys.stderr)
        sys.exit(1)

    # Categorize tables
    tables = []
    for table_dir in sorted(args.cdm_database.iterdir()):
        if not table_dir.is_dir():
            continue

        name = table_dir.name

        # Filter by category
        if args.category == 'static' and not name.startswith('sdt_'):
            continue
        elif args.category == 'system' and not name.startswith('sys_'):
            continue
        elif args.category == 'dynamic' and not name.startswith('ddt_'):
            continue

        # Filter by specific table
        if args.table and name != args.table:
            continue

        tables.append(table_dir)

    print(f"📊 ENIGMA CDM Metadata Extraction")
    print(f"{'='*70}\n")
    print(f"Analyzing {len(tables)} table(s)...\n")

    # Analyze tables
    results = {}

    for table_path in tables:
        table_name = table_path.name
        print(f"📦 {table_name}")

        try:
            table_info = analyze_table(table_path)

            if 'error' in table_info:
                print(f"   ❌ {table_info['error']}\n")
                continue

            results[table_name] = table_info

            if args.format == 'summary':
                print(f"   Rows: {table_info['total_rows']:,}")
                print(f"   Columns: {table_info['num_columns']}")
                # Count columns with descriptions
                with_desc = sum(1 for c in table_info['columns'].values() if c.get('description'))
                print(f"   Columns with descriptions: {with_desc}")

            elif args.format == 'detailed':
                print(f"   Rows: {table_info['total_rows']:,}")
                print(f"   Columns: {table_info['num_columns']}\n")

                for col_name, col_meta in table_info['columns'].items():
                    flags = []
                    if col_meta.get('pk'):
                        flags.append('PK')
                    if col_meta.get('upk'):
                        flags.append('UNQ')
                    if col_meta.get('fk'):
                        flags.append(f"FK→{col_meta['fk']}")
                    if col_meta.get('required'):
                        flags.append('REQ')

                    flag_str = f" [{', '.join(flags)}]" if flags else ""

                    print(f"   • {col_name}: {col_meta['type']}{flag_str}")

                    if col_meta.get('description'):
                        desc = col_meta['description'][:100]
                        print(f"     → {desc}")

                    if col_meta.get('microtype'):
                        print(f"     Microtype: {col_meta['microtype']}")

                    if col_meta.get('units'):
                        print(f"     Units: {col_meta['units']}")

            print()

        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            import traceback
            traceback.print_exc()

    # Save to JSON
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Metadata saved to: {args.output}")

    # Generate schema YAML
    if args.generate_schema:
        print(f"\n{'='*70}")
        print(f"📋 LINKML SCHEMA YAML")
        print(f"{'='*70}\n")

        for table_name, table_info in results.items():
            # Convert table name to class name
            class_name = table_name.replace('sdt_', '').replace('sys_', 'System').title().replace('_', '')

            schema_yaml = generate_schema_yaml(table_info, class_name)
            print(schema_yaml)

    print(f"✅ Extracted metadata from {len(results)} table(s)")


if __name__ == "__main__":
    main()
