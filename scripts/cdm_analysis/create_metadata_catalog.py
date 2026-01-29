#!/usr/bin/env python3
"""
Create comprehensive CDM metadata catalog for DuckDB loading.

This script:
1. Combines all extracted metadata into unified catalogs
2. Generates DuckDB-ready table definitions
3. Creates column-level metadata for searchable catalog
4. Prepares validation rules catalog
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


def load_metadata_files(metadata_dir: Path) -> Dict[str, Any]:
    """Load all metadata JSON files."""
    metadata = {
        'static': {},
        'system': {},
        'dynamic': {}
    }

    static_file = metadata_dir / 'static_tables_metadata.json'
    system_file = metadata_dir / 'system_tables_metadata.json'
    dynamic_file = metadata_dir / 'dynamic_tables_metadata.json'

    if static_file.exists():
        with open(static_file) as f:
            metadata['static'] = json.load(f)

    if system_file.exists():
        with open(system_file) as f:
            metadata['system'] = json.load(f)

    if dynamic_file.exists():
        with open(dynamic_file) as f:
            metadata['dynamic'] = json.load(f)

    return metadata


def create_column_catalog(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Create column-level metadata catalog.

    Returns:
        List of column records suitable for DuckDB loading
    """
    catalog = []

    for category, tables in metadata.items():
        for table_name, table_info in tables.items():
            for col_name, col_meta in table_info.get('columns', {}).items():
                record = {
                    'table_name': table_name,
                    'table_category': category,
                    'column_name': col_name,
                    'column_type': col_meta.get('type', ''),
                    'description': col_meta.get('description', ''),
                    'microtype': col_meta.get('microtype', None),
                    'units': col_meta.get('units', None),
                    'is_primary_key': bool(col_meta.get('pk')),
                    'is_unique_key': bool(col_meta.get('upk')),
                    'is_foreign_key': bool(col_meta.get('fk')),
                    'fk_references': col_meta.get('fk', None) or col_meta.get('references', None),
                    'is_required': bool(col_meta.get('required')),
                    'is_nullable': col_meta.get('nullable', True),
                    'constraint_pattern': col_meta.get('constraint', None),
                    'original_name': col_meta.get('orig_name', None),
                    'field_type': col_meta.get('field_type', None),
                }
                catalog.append(record)

    return catalog


def create_table_catalog(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Create table-level metadata catalog.

    Returns:
        List of table records suitable for DuckDB loading
    """
    catalog = []

    for category, tables in metadata.items():
        for table_name, table_info in tables.items():
            # Count constraints
            columns = table_info.get('columns', {})
            pk_count = sum(1 for c in columns.values() if c.get('pk'))
            fk_count = sum(1 for c in columns.values() if c.get('fk'))
            unique_count = sum(1 for c in columns.values() if c.get('upk'))
            required_count = sum(1 for c in columns.values() if c.get('required'))

            record = {
                'table_name': table_name,
                'table_category': category,
                'total_rows': table_info.get('total_rows', 0),
                'num_columns': table_info.get('num_columns', 0),
                'num_primary_keys': pk_count,
                'num_foreign_keys': fk_count,
                'num_unique_keys': unique_count,
                'num_required_columns': required_count,
                'description': f"{category} table with {table_info.get('num_columns', 0)} columns",
            }
            catalog.append(record)

    return catalog


def create_validation_catalog(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Create validation rules catalog.

    Returns:
        List of validation rules for each constrained column
    """
    catalog = []

    for category, tables in metadata.items():
        for table_name, table_info in tables.items():
            for col_name, col_meta in table_info.get('columns', {}).items():
                # Skip columns without constraints
                if not col_meta.get('constraint'):
                    continue

                record = {
                    'table_name': table_name,
                    'column_name': col_name,
                    'validation_type': 'pattern',
                    'validation_pattern': col_meta.get('constraint'),
                    'description': col_meta.get('description', ''),
                    'microtype': col_meta.get('microtype', None),
                }
                catalog.append(record)

                # Add FK validation rules
                if col_meta.get('fk'):
                    fk_record = {
                        'table_name': table_name,
                        'column_name': col_name,
                        'validation_type': 'foreign_key',
                        'validation_pattern': col_meta.get('fk'),
                        'description': f"Foreign key to {col_meta.get('fk')}",
                        'microtype': col_meta.get('microtype', None),
                    }
                    catalog.append(fk_record)

    return catalog


def create_microtype_catalog(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Create microtype usage catalog.

    Returns:
        List of microtype occurrences across all tables
    """
    microtype_usage = defaultdict(list)

    for category, tables in metadata.items():
        for table_name, table_info in tables.items():
            for col_name, col_meta in table_info.get('columns', {}).items():
                microtype = col_meta.get('microtype')
                if microtype:
                    microtype_usage[microtype].append({
                        'table_name': table_name,
                        'column_name': col_name,
                        'category': category,
                        'description': col_meta.get('description', ''),
                    })

    catalog = []
    for microtype, occurrences in microtype_usage.items():
        record = {
            'microtype': microtype,
            'usage_count': len(occurrences),
            'tables': list(set(o['table_name'] for o in occurrences)),
            'columns': [f"{o['table_name']}.{o['column_name']}" for o in occurrences],
            'example_description': occurrences[0]['description'] if occurrences else '',
        }
        catalog.append(record)

    return sorted(catalog, key=lambda x: -x['usage_count'])


def create_relationship_catalog(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Create FK relationship catalog.

    Returns:
        List of all FK relationships
    """
    catalog = []

    for category, tables in metadata.items():
        for table_name, table_info in tables.items():
            for col_name, col_meta in table_info.get('columns', {}).items():
                fk_ref = col_meta.get('fk') or col_meta.get('references')
                if not fk_ref:
                    continue

                # Parse FK reference
                if '.' in fk_ref:
                    target_table, target_column = fk_ref.split('.', 1)
                else:
                    target_table = fk_ref
                    target_column = None

                record = {
                    'source_table': table_name,
                    'source_column': col_name,
                    'target_table': target_table,
                    'target_column': target_column,
                    'relationship_type': 'many_to_one',
                    'is_required': bool(col_meta.get('required')),
                    'description': col_meta.get('description', ''),
                }
                catalog.append(record)

    return catalog


def generate_duckdb_ddl(catalogs: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    Generate DuckDB DDL statements for metadata tables.

    Args:
        catalogs: Dict of catalog name -> list of records

    Returns:
        DDL SQL string
    """
    ddl = []

    ddl.append("-- ENIGMA CDM Metadata Catalog Tables")
    ddl.append("-- Generated from parquet metadata")
    ddl.append("")

    # Column metadata table
    ddl.append("CREATE OR REPLACE TABLE cdm_column_metadata (")
    ddl.append("  table_name VARCHAR NOT NULL,")
    ddl.append("  table_category VARCHAR NOT NULL,")
    ddl.append("  column_name VARCHAR NOT NULL,")
    ddl.append("  column_type VARCHAR,")
    ddl.append("  description TEXT,")
    ddl.append("  microtype VARCHAR,")
    ddl.append("  units VARCHAR,")
    ddl.append("  is_primary_key BOOLEAN DEFAULT FALSE,")
    ddl.append("  is_unique_key BOOLEAN DEFAULT FALSE,")
    ddl.append("  is_foreign_key BOOLEAN DEFAULT FALSE,")
    ddl.append("  fk_references VARCHAR,")
    ddl.append("  is_required BOOLEAN DEFAULT FALSE,")
    ddl.append("  is_nullable BOOLEAN DEFAULT TRUE,")
    ddl.append("  constraint_pattern VARCHAR,")
    ddl.append("  original_name VARCHAR,")
    ddl.append("  field_type VARCHAR,")
    ddl.append("  PRIMARY KEY (table_name, column_name)")
    ddl.append(");")
    ddl.append("")

    # Table metadata table
    ddl.append("CREATE OR REPLACE TABLE cdm_table_metadata (")
    ddl.append("  table_name VARCHAR PRIMARY KEY,")
    ddl.append("  table_category VARCHAR NOT NULL,")
    ddl.append("  total_rows BIGINT,")
    ddl.append("  num_columns INTEGER,")
    ddl.append("  num_primary_keys INTEGER,")
    ddl.append("  num_foreign_keys INTEGER,")
    ddl.append("  num_unique_keys INTEGER,")
    ddl.append("  num_required_columns INTEGER,")
    ddl.append("  description TEXT")
    ddl.append(");")
    ddl.append("")

    # Validation rules table
    ddl.append("CREATE OR REPLACE TABLE cdm_validation_rules (")
    ddl.append("  table_name VARCHAR NOT NULL,")
    ddl.append("  column_name VARCHAR NOT NULL,")
    ddl.append("  validation_type VARCHAR NOT NULL,")
    ddl.append("  validation_pattern VARCHAR,")
    ddl.append("  description TEXT,")
    ddl.append("  microtype VARCHAR")
    ddl.append(");")
    ddl.append("")

    # Microtype catalog table
    ddl.append("CREATE OR REPLACE TABLE cdm_microtype_catalog (")
    ddl.append("  microtype VARCHAR PRIMARY KEY,")
    ddl.append("  usage_count INTEGER,")
    ddl.append("  tables VARCHAR[],")
    ddl.append("  columns VARCHAR[],")
    ddl.append("  example_description TEXT")
    ddl.append(");")
    ddl.append("")

    # Relationship catalog table
    ddl.append("CREATE OR REPLACE TABLE cdm_relationship_catalog (")
    ddl.append("  source_table VARCHAR NOT NULL,")
    ddl.append("  source_column VARCHAR NOT NULL,")
    ddl.append("  target_table VARCHAR NOT NULL,")
    ddl.append("  target_column VARCHAR,")
    ddl.append("  relationship_type VARCHAR,")
    ddl.append("  is_required BOOLEAN,")
    ddl.append("  description TEXT")
    ddl.append(");")
    ddl.append("")

    # Create indexes for searching
    ddl.append("-- Indexes for fast searching")
    ddl.append("CREATE INDEX idx_column_description ON cdm_column_metadata(description);")
    ddl.append("CREATE INDEX idx_column_microtype ON cdm_column_metadata(microtype);")
    ddl.append("CREATE INDEX idx_validation_table ON cdm_validation_rules(table_name);")
    ddl.append("")

    return '\n'.join(ddl)


def main():
    parser = argparse.ArgumentParser(
        description='Create comprehensive CDM metadata catalog'
    )

    parser.add_argument(
        '--metadata-dir',
        type=Path,
        default=Path('data/cdm_metadata'),
        help='Directory containing extracted metadata JSON files'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('data/cdm_metadata'),
        help='Output directory for catalog files'
    )

    parser.add_argument(
        '--generate-ddl',
        action='store_true',
        help='Generate DuckDB DDL statements'
    )

    args = parser.parse_args()

    print("📊 Creating CDM Metadata Catalogs")
    print("="*70)
    print()

    # Load all metadata
    print("📥 Loading metadata files...")
    metadata = load_metadata_files(args.metadata_dir)

    total_tables = (
        len(metadata['static']) +
        len(metadata['system']) +
        len(metadata['dynamic'])
    )
    print(f"   ✅ Loaded metadata from {total_tables} tables")
    print()

    # Create catalogs
    print("📋 Creating catalogs...")

    column_catalog = create_column_catalog(metadata)
    print(f"   • Column catalog: {len(column_catalog)} columns")

    table_catalog = create_table_catalog(metadata)
    print(f"   • Table catalog: {len(table_catalog)} tables")

    validation_catalog = create_validation_catalog(metadata)
    print(f"   • Validation catalog: {len(validation_catalog)} rules")

    microtype_catalog = create_microtype_catalog(metadata)
    print(f"   • Microtype catalog: {len(microtype_catalog)} microtypes")

    relationship_catalog = create_relationship_catalog(metadata)
    print(f"   • Relationship catalog: {len(relationship_catalog)} relationships")
    print()

    # Save catalogs
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("💾 Saving catalog files...")

    catalogs = {
        'column_catalog': column_catalog,
        'table_catalog': table_catalog,
        'validation_catalog': validation_catalog,
        'microtype_catalog': microtype_catalog,
        'relationship_catalog': relationship_catalog,
    }

    for catalog_name, catalog_data in catalogs.items():
        output_file = args.output_dir / f'{catalog_name}.json'
        with open(output_file, 'w') as f:
            json.dump(catalog_data, f, indent=2)
        print(f"   ✅ {catalog_name}.json ({len(catalog_data)} records)")

    # Generate combined catalog
    combined_file = args.output_dir / 'all_catalogs.json'
    with open(combined_file, 'w') as f:
        json.dump(catalogs, f, indent=2)
    print(f"   ✅ all_catalogs.json (combined)")
    print()

    # Generate DuckDB DDL
    if args.generate_ddl:
        print("🗄️  Generating DuckDB DDL...")
        ddl = generate_duckdb_ddl(catalogs)

        ddl_file = args.output_dir / 'cdm_metadata_schema.sql'
        with open(ddl_file, 'w') as f:
            f.write(ddl)
        print(f"   ✅ cdm_metadata_schema.sql")
        print()

    print("="*70)
    print("✅ Metadata catalogs created successfully!")
    print()
    print(f"Output directory: {args.output_dir}")
    print()
    print("Files created:")
    print("  • column_catalog.json - All column metadata")
    print("  • table_catalog.json - All table metadata")
    print("  • validation_catalog.json - Validation rules")
    print("  • microtype_catalog.json - Microtype usage")
    print("  • relationship_catalog.json - FK relationships")
    print("  • all_catalogs.json - Combined catalog")
    if args.generate_ddl:
        print("  • cdm_metadata_schema.sql - DuckDB DDL")


if __name__ == "__main__":
    main()
