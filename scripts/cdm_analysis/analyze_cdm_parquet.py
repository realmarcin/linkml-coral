#!/usr/bin/env python3
"""
Comprehensive analysis of KBase CDM parquet tables.
Analyzes system tables, static data tables (sdt_*), and dynamic data tables (ddt_*).
"""

import pandas as pd
from pathlib import Path
import json
from collections import defaultdict
from typing import Dict, List, Any

# Path to the parquet database
DB_PATH = Path("data/enigma_coral.db")

def find_parquet_file(table_dir: Path) -> Path:
    """Find the actual parquet file in a Delta Lake table directory."""
    # Look for .parquet files (not in _delta_log)
    parquet_files = [f for f in table_dir.glob('*.parquet') if not f.parent.name.startswith('_')]
    if parquet_files:
        return parquet_files[0]  # Return first parquet file
    return None

def get_parquet_info(table_dir: Path) -> Dict[str, Any]:
    """Get detailed information about a parquet table."""
    try:
        # Find the parquet file
        parquet_file = find_parquet_file(table_dir)
        if not parquet_file:
            return {'error': 'No parquet file found'}

        # Read the data
        df = pd.read_parquet(parquet_file)

        # Extract column information
        columns = []
        for col_name in df.columns:
            col_info = {
                'name': col_name,
                'type': str(df[col_name].dtype),
                'nullable': df[col_name].isna().any(),
                'sample_values': df[col_name].dropna().head(3).tolist() if not df.empty else []
            }
            columns.append(col_info)

        return {
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': columns,
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'dataframe': df  # Return df for further analysis
        }
    except Exception as e:
        return {'error': str(e)}

def analyze_system_tables():
    """Analyze all sys_* tables."""
    print("=" * 80)
    print("SYSTEM TABLES ANALYSIS")
    print("=" * 80)

    system_tables = {
        'sys_typedef': 'CORAL static type to CDM table mappings',
        'sys_ddt_typedef': 'Dynamic type (brick/microtype) mappings',
        'sys_oterm': 'Ontology term catalog',
        'sys_process': 'Process/workflow definitions',
        'sys_process_input': 'Process input specifications',
        'sys_process_output': 'Process output specifications'
    }

    results = {}

    for table_name, description in system_tables.items():
        print(f"\n{table_name.upper()}: {description}")
        print("-" * 80)

        table_dir = DB_PATH / table_name
        if not table_dir.exists():
            print(f"  ⚠️  Table directory not found at {table_dir}")
            continue

        info = get_parquet_info(table_dir)
        results[table_name] = info

        if 'error' in info:
            print(f"  ❌ Error: {info['error']}")
            continue

        print(f"  Rows: {info['row_count']:,}")
        print(f"  Columns: {info['column_count']}")
        print(f"  Memory: {info['memory_usage_mb']:.2f} MB")
        print(f"\n  Column Details:")

        for col in info['columns']:
            print(f"    - {col['name']}: {col['type']} (nullable={col['nullable']})")
            if col['sample_values']:
                sample_str = ', '.join([str(v)[:50] for v in col['sample_values'][:3]])
                print(f"      Sample: {sample_str}")

        # Special analysis for each system table
        df = info['dataframe']

        if table_name == 'sys_typedef':
            print(f"\n  CORAL Type → CDM Table Mappings:")
            for _, row in df.iterrows():
                print(f"    {row.get('coral_type', 'N/A')} → {row.get('cdm_table', 'N/A')}")

        elif table_name == 'sys_ddt_typedef':
            print(f"\n  Dynamic Type Summary:")
            if 'brick_type' in df.columns:
                print(f"    Unique brick types: {df['brick_type'].nunique()}")
            if 'microtype' in df.columns:
                print(f"    Unique microtypes: {df['microtype'].nunique()}")

        elif table_name == 'sys_oterm':
            print(f"\n  Ontology Term Summary:")
            if 'oterm_id' in df.columns:
                print(f"    Total terms: {df['oterm_id'].nunique():,}")
            if 'namespace' in df.columns or 'ontology' in df.columns:
                ns_col = 'namespace' if 'namespace' in df.columns else 'ontology'
                print(f"    Namespaces: {df[ns_col].value_counts().to_dict()}")

        elif table_name == 'sys_process':
            print(f"\n  Process Type Summary:")
            if 'process_type' in df.columns:
                print(f"    Process types: {df['process_type'].value_counts().to_dict()}")

    return results

def analyze_static_tables():
    """Analyze all sdt_* tables."""
    print("\n\n" + "=" * 80)
    print("STATIC DATA TABLES (sdt_*) ANALYSIS")
    print("=" * 80)

    # Find all sdt_* tables
    sdt_tables = sorted([d.name for d in DB_PATH.iterdir() if d.is_dir() and d.name.startswith('sdt_')])

    results = {}
    total_rows = 0

    for table_name in sdt_tables:
        print(f"\n{table_name.upper()}")
        print("-" * 80)

        table_dir = DB_PATH / table_name
        if not table_dir.exists():
            print(f"  ⚠️  Table directory not found")
            continue

        info = get_parquet_info(table_dir)
        results[table_name] = info

        if 'error' in info:
            print(f"  ❌ Error: {info['error']}")
            continue

        total_rows += info['row_count']

        print(f"  Rows: {info['row_count']:,}")
        print(f"  Columns: {info['column_count']}")
        print(f"  Memory: {info['memory_usage_mb']:.2f} MB")

        # Identify primary key pattern
        df = info['dataframe']
        pk_candidates = [col for col in df.columns if col.endswith('_id') and 'sys_oterm' not in col]
        if pk_candidates:
            print(f"  Primary Key Candidates: {', '.join(pk_candidates)}")

        # Identify foreign key patterns
        fk_candidates = [col for col in df.columns if col.endswith('_id') and col not in pk_candidates and 'sys_oterm' not in col]
        if fk_candidates:
            print(f"  Foreign Key Candidates: {', '.join(fk_candidates)}")

        # Identify ontology term fields
        oterm_fields = [col for col in df.columns if 'sys_oterm' in col]
        if oterm_fields:
            print(f"  Ontology Term Fields: {', '.join(oterm_fields)}")

        print(f"\n  Column Details:")
        for col in info['columns']:
            nullable_str = "NULL" if col['nullable'] else "NOT NULL"
            print(f"    - {col['name']}: {col['type']} ({nullable_str})")

            # Show sample for specific interesting columns
            if col['sample_values'] and (col['name'].endswith('_id') or 'name' in col['name'] or 'type' in col['name']):
                sample_str = ', '.join([str(v)[:50] for v in col['sample_values'][:2]])
                print(f"      Sample: {sample_str}")

    print(f"\n\nSTATIC TABLES SUMMARY:")
    print(f"  Total tables: {len(sdt_tables)}")
    print(f"  Total rows: {total_rows:,}")
    print(f"  Tables by size:")
    sorted_tables = sorted([(name, results[name]['row_count']) for name in results if 'row_count' in results[name]],
                           key=lambda x: x[1], reverse=True)
    for name, count in sorted_tables[:10]:
        print(f"    {name}: {count:,} rows")

    return results

def analyze_dynamic_tables():
    """Analyze ddt_* tables."""
    print("\n\n" + "=" * 80)
    print("DYNAMIC DATA TABLES (ddt_*) ANALYSIS")
    print("=" * 80)

    # Find all ddt_* tables
    ddt_tables = sorted([d.name for d in DB_PATH.iterdir() if d.is_dir() and d.name.startswith('ddt_')])

    results = {}

    # First analyze ddt_ndarray (the index)
    print(f"\nDDT_NDARRAY (Brick Index)")
    print("-" * 80)

    ndarray_dir = DB_PATH / 'ddt_ndarray'
    if ndarray_dir.exists():
        info = get_parquet_info(ndarray_dir)
        results['ddt_ndarray'] = info

        if 'error' not in info:
            print(f"  Rows: {info['row_count']:,}")
            print(f"  Columns: {info['column_count']}")
            print(f"\n  Column Details:")
            for col in info['columns']:
                print(f"    - {col['name']}: {col['type']} (nullable={col['nullable']})")
                if col['sample_values']:
                    sample_str = ', '.join([str(v)[:50] for v in col['sample_values'][:2]])
                    print(f"      Sample: {sample_str}")

            df = info['dataframe']
            if 'brick_id' in df.columns:
                print(f"\n  Brick ID Summary:")
                print(f"    Unique bricks: {df['brick_id'].nunique()}")
                print(f"    Brick IDs: {sorted(df['brick_id'].unique())[:20]}")

    # Analyze brick tables
    brick_tables = [t for t in ddt_tables if t.startswith('ddt_brick')]
    print(f"\n\nBRICK TABLES ({len(brick_tables)} total)")
    print("-" * 80)

    for table_name in brick_tables[:5]:  # Show first 5 in detail
        print(f"\n{table_name.upper()}")
        print("  " + "-" * 76)

        table_dir = DB_PATH / table_name
        if not table_dir.exists():
            continue

        info = get_parquet_info(table_dir)
        results[table_name] = info

        if 'error' in info:
            print(f"  ❌ Error: {info['error']}")
            continue

        print(f"  Rows: {info['row_count']:,}")
        print(f"  Columns: {info['column_count']}")
        print(f"  Memory: {info['memory_usage_mb']:.2f} MB")
        print(f"\n  Columns:")
        for col in info['columns']:
            print(f"    - {col['name']}: {col['type']}")

    # Summary of all brick tables
    if len(brick_tables) > 5:
        print(f"\n  ... and {len(brick_tables) - 5} more brick tables")
        print(f"\n  All brick table IDs:")
        brick_ids = [t.replace('ddt_brick', '') for t in brick_tables]
        print(f"    {', '.join(brick_ids)}")

    return results

def analyze_schema_differences():
    """Compare CDM schema to original CORAL/LinkML schema."""
    print("\n\n" + "=" * 80)
    print("SCHEMA DIFFERENCES ANALYSIS")
    print("=" * 80)

    print("\nKey observations:")

    # Read some tables to identify patterns
    patterns = {
        'ontology_splitting': [],
        'new_fields': [],
        'renamed_fields': [],
        'normalized_structures': []
    }

    # Check a few representative tables
    sample_tables = ['sdt_sample', 'sdt_location', 'sdt_asv']

    for table_name in sample_tables:
        table_dir = DB_PATH / table_name
        if table_dir.exists():
            parquet_file = find_parquet_file(table_dir)
            if not parquet_file:
                continue
            df = pd.read_parquet(parquet_file)

            # Look for ontology term splitting pattern
            oterm_fields = [col for col in df.columns if 'sys_oterm' in col]
            if oterm_fields:
                base_fields = set()
                for field in oterm_fields:
                    if field.endswith('_sys_oterm_id'):
                        base = field.replace('_sys_oterm_id', '')
                        base_fields.add(base)
                    elif field.endswith('_sys_oterm_name'):
                        base = field.replace('_sys_oterm_name', '')
                        base_fields.add(base)

                if base_fields:
                    patterns['ontology_splitting'].append({
                        'table': table_name,
                        'base_fields': list(base_fields),
                        'oterm_fields': oterm_fields
                    })

    print("\n1. ONTOLOGY TERM SPLITTING PATTERN:")
    for item in patterns['ontology_splitting']:
        print(f"   {item['table']}:")
        for base in item['base_fields']:
            print(f"     {base} → {base}_sys_oterm_id + {base}_sys_oterm_name")

    print("\n2. NAMING CONVENTIONS:")
    print("   - Tables: sdt_<snake_case>")
    print("   - Primary keys: <table_name>_id")
    print("   - Foreign keys: <referenced_table>_id")
    print("   - Ontology refs: <field>_sys_oterm_id + <field>_sys_oterm_name")

    return patterns

def generate_summary_report():
    """Generate comprehensive summary report."""
    print("\n\n" + "=" * 80)
    print("COMPREHENSIVE ANALYSIS REPORT")
    print("=" * 80)

    # Count all tables by category
    all_dirs = list(DB_PATH.iterdir())
    sys_tables = [d.name for d in all_dirs if d.is_dir() and d.name.startswith('sys_')]
    sdt_tables = [d.name for d in all_dirs if d.is_dir() and d.name.startswith('sdt_')]
    ddt_tables = [d.name for d in all_dirs if d.is_dir() and d.name.startswith('ddt_')]

    print(f"\nTABLE INVENTORY:")
    print(f"  System tables (sys_*): {len(sys_tables)}")
    print(f"  Static data tables (sdt_*): {len(sdt_tables)}")
    print(f"  Dynamic data tables (ddt_*): {len(ddt_tables)}")
    print(f"  Total tables: {len(sys_tables) + len(sdt_tables) + len(ddt_tables)}")

    print(f"\nSYSTEM TABLES:")
    for table in sorted(sys_tables):
        print(f"  - {table}")

    print(f"\nSTATIC DATA TABLES:")
    for table in sorted(sdt_tables):
        print(f"  - {table}")

    print(f"\nDYNAMIC DATA TABLES:")
    print(f"  - ddt_ndarray (brick index)")
    brick_tables = [t for t in ddt_tables if t.startswith('ddt_brick')]
    print(f"  - {len(brick_tables)} brick tables: {', '.join([t.replace('ddt_brick', 'brick') for t in sorted(brick_tables)])}")

def main():
    """Run comprehensive analysis."""
    print("KBASE CDM PARQUET TABLE ANALYSIS")
    print("=" * 80)
    print(f"Database location: {DB_PATH}")
    print()

    # Run all analyses
    sys_results = analyze_system_tables()
    sdt_results = analyze_static_tables()
    ddt_results = analyze_dynamic_tables()
    schema_diffs = analyze_schema_differences()
    generate_summary_report()

    print("\n\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()
