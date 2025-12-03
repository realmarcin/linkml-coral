#!/usr/bin/env python3
"""
Generate a comprehensive JSON report of the KBase CDM schema structure.
"""

import pandas as pd
from pathlib import Path
import json
from typing import Dict, List, Any

DB_PATH = Path("/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db")

def find_parquet_file(table_dir: Path) -> Path:
    """Find the actual parquet file in a Delta Lake table directory."""
    parquet_files = [f for f in table_dir.glob('*.parquet') if not f.parent.name.startswith('_')]
    if parquet_files:
        return parquet_files[0]
    return None

def analyze_table_schema(table_dir: Path) -> Dict[str, Any]:
    """Extract schema details from a table."""
    parquet_file = find_parquet_file(table_dir)
    if not parquet_file:
        return None

    df = pd.read_parquet(parquet_file)

    columns = []
    for col_name in df.columns:
        try:
            unique_count = int(df[col_name].nunique()) if len(df) > 0 else 0
        except (TypeError, ValueError):
            # Column contains unhashable types like lists/arrays
            unique_count = -1

        col_data = {
            'name': col_name,
            'dtype': str(df[col_name].dtype),
            'nullable': bool(df[col_name].isna().any()),
            'unique_count': unique_count,
            'null_count': int(df[col_name].isna().sum()),
            'sample_values': [str(v)[:200] for v in df[col_name].dropna().head(5).tolist()]  # Truncate long values
        }

        # Classify column type
        if col_name.endswith('_id') and 'sys_oterm' not in col_name:
            if unique_count > 0 and unique_count == len(df) and not df[col_name].isna().any():
                col_data['classification'] = 'primary_key'
            else:
                col_data['classification'] = 'foreign_key'
        elif col_name.endswith('_sys_oterm_id'):
            col_data['classification'] = 'ontology_term_id'
        elif col_name.endswith('_sys_oterm_name'):
            col_data['classification'] = 'ontology_term_name'
        elif col_name.endswith('_name'):
            col_data['classification'] = 'name_field'
        else:
            col_data['classification'] = 'data_field'

        columns.append(col_data)

    return {
        'row_count': len(df),
        'column_count': len(df.columns),
        'columns': columns,
        'memory_usage_mb': float(df.memory_usage(deep=True).sum() / 1024 / 1024)
    }

def extract_typedef_mappings() -> Dict[str, Any]:
    """Extract type definitions from sys_typedef."""
    typedef_dir = DB_PATH / 'sys_typedef'
    parquet_file = find_parquet_file(typedef_dir)
    if not parquet_file:
        return {}

    df = pd.read_parquet(parquet_file)

    # Group by type_name
    types = {}
    for type_name in df['type_name'].unique():
        type_df = df[df['type_name'] == type_name]
        fields = []
        for _, row in type_df.iterrows():
            field = {
                'field_name': row['field_name'],
                'cdm_column_name': row['cdm_column_name'],
                'scalar_type': row['scalar_type'],
                'required': bool(row.get('required', False)) if pd.notna(row.get('required')) else None,
                'pk': bool(row.get('pk', False)) if pd.notna(row.get('pk')) else None,
                'upk': bool(row.get('upk', False)) if pd.notna(row.get('upk')) else None,
                'fk': row.get('fk') if pd.notna(row.get('fk')) else None,
                'constraint': row.get('constraint') if pd.notna(row.get('constraint')) else None,
                'comment': row.get('comment', ''),
                'units_sys_oterm_id': row.get('units_sys_oterm_id') if pd.notna(row.get('units_sys_oterm_id')) else None,
                'type_sys_oterm_id': row.get('type_sys_oterm_id') if pd.notna(row.get('type_sys_oterm_id')) else None,
            }
            fields.append(field)
        types[type_name] = fields

    return types

def extract_ddt_typedef() -> List[Dict[str, Any]]:
    """Extract dynamic type definitions."""
    ddt_typedef_dir = DB_PATH / 'sys_ddt_typedef'
    parquet_file = find_parquet_file(ddt_typedef_dir)
    if not parquet_file:
        return []

    df = pd.read_parquet(parquet_file)

    records = []
    for _, row in df.iterrows():
        record = {
            'ddt_ndarray_id': row['ddt_ndarray_id'],
            'cdm_column_name': row['cdm_column_name'],
            'cdm_column_data_type': row['cdm_column_data_type'],
            'scalar_type': row['scalar_type'],
            'fk': row.get('fk') if pd.notna(row.get('fk')) else None,
            'comment': row.get('comment', ''),
            'unit_sys_oterm_id': row.get('unit_sys_oterm_id') if pd.notna(row.get('unit_sys_oterm_id')) else None,
            'unit_sys_oterm_name': row.get('unit_sys_oterm_name') if pd.notna(row.get('unit_sys_oterm_name')) else None,
            'dimension_number': int(row['dimension_number']) if pd.notna(row.get('dimension_number')) else None,
            'dimension_oterm_id': row.get('dimension_oterm_id') if pd.notna(row.get('dimension_oterm_id')) else None,
            'dimension_oterm_name': row.get('dimension_oterm_name') if pd.notna(row.get('dimension_oterm_name')) else None,
            'variable_number': int(row['variable_number']),
            'variable_oterm_id': row['variable_oterm_id'],
            'variable_oterm_name': row['variable_oterm_name'],
        }
        records.append(record)

    return records

def extract_process_model() -> Dict[str, Any]:
    """Extract process/provenance model information."""
    process_dir = DB_PATH / 'sys_process'
    parquet_file = find_parquet_file(process_dir)
    if not parquet_file:
        return {}

    df = pd.read_parquet(parquet_file)

    sample_processes = []
    for _, row in df.head(3).iterrows():
        record = {}
        for k, v in row.items():
            # Convert numpy arrays and other non-JSON-serializable types to strings
            if isinstance(v, (list, tuple)):
                record[k] = [str(item) for item in v]
            elif hasattr(v, 'tolist'):  # numpy array
                record[k] = str(v.tolist())
            else:
                record[k] = str(v) if pd.notna(v) else None
        sample_processes.append(record)

    return {
        'total_processes': len(df),
        'process_types': df['process_sys_oterm_name'].value_counts().to_dict() if 'process_sys_oterm_name' in df.columns else {},
        'sample_processes': sample_processes,
    }

def extract_ontology_terms() -> Dict[str, Any]:
    """Extract ontology term catalog summary."""
    oterm_dir = DB_PATH / 'sys_oterm'
    parquet_file = find_parquet_file(oterm_dir)
    if not parquet_file:
        return {}

    df = pd.read_parquet(parquet_file)

    ontology_counts = df['sys_oterm_ontology'].value_counts().to_dict() if 'sys_oterm_ontology' in df.columns else {}

    sample_terms = []
    if all(c in df.columns for c in ['sys_oterm_id', 'sys_oterm_name', 'sys_oterm_ontology']):
        for _, row in df.head(10).iterrows():
            sample_terms.append({
                'sys_oterm_id': str(row['sys_oterm_id']) if pd.notna(row['sys_oterm_id']) else None,
                'sys_oterm_name': str(row['sys_oterm_name']) if pd.notna(row['sys_oterm_name']) else None,
                'sys_oterm_ontology': str(row['sys_oterm_ontology']) if pd.notna(row['sys_oterm_ontology']) else None
            })

    return {
        'total_terms': len(df),
        'ontology_distribution': ontology_counts,
        'sample_terms': sample_terms
    }

def main():
    """Generate comprehensive schema report."""
    print("Generating CDM Schema Report...")

    report = {
        'database_path': str(DB_PATH),
        'system_tables': {},
        'static_tables': {},
        'dynamic_tables': {},
        'type_definitions': {},
        'ddt_type_definitions': [],
        'process_model': {},
        'ontology_catalog': {},
        'summary': {}
    }

    # System tables
    print("Analyzing system tables...")
    for table_name in ['sys_typedef', 'sys_ddt_typedef', 'sys_oterm', 'sys_process', 'sys_process_input', 'sys_process_output']:
        table_dir = DB_PATH / table_name
        if table_dir.exists():
            schema = analyze_table_schema(table_dir)
            if schema:
                report['system_tables'][table_name] = schema

    # Static data tables
    print("Analyzing static data tables...")
    sdt_tables = sorted([d.name for d in DB_PATH.iterdir() if d.is_dir() and d.name.startswith('sdt_')])
    for table_name in sdt_tables:
        table_dir = DB_PATH / table_name
        schema = analyze_table_schema(table_dir)
        if schema:
            report['static_tables'][table_name] = schema

    # Dynamic tables
    print("Analyzing dynamic data tables...")
    ddt_ndarray_dir = DB_PATH / 'ddt_ndarray'
    if ddt_ndarray_dir.exists():
        schema = analyze_table_schema(ddt_ndarray_dir)
        if schema:
            report['dynamic_tables']['ddt_ndarray'] = schema

    brick_tables = sorted([d.name for d in DB_PATH.iterdir() if d.is_dir() and d.name.startswith('ddt_brick')])
    for table_name in brick_tables:
        table_dir = DB_PATH / table_name
        schema = analyze_table_schema(table_dir)
        if schema:
            report['dynamic_tables'][table_name] = schema

    # Extract type definitions
    print("Extracting type definitions...")
    report['type_definitions'] = extract_typedef_mappings()
    report['ddt_type_definitions'] = extract_ddt_typedef()
    report['process_model'] = extract_process_model()
    report['ontology_catalog'] = extract_ontology_terms()

    # Generate summary
    total_rows = sum(t['row_count'] for t in report['static_tables'].values())
    total_rows += sum(t['row_count'] for t in report['dynamic_tables'].values())

    report['summary'] = {
        'total_system_tables': len(report['system_tables']),
        'total_static_tables': len(report['static_tables']),
        'total_dynamic_tables': len(report['dynamic_tables']),
        'total_tables': len(report['system_tables']) + len(report['static_tables']) + len(report['dynamic_tables']),
        'total_data_rows': total_rows,
        'total_types_defined': len(report['type_definitions']),
        'static_table_names': list(report['static_tables'].keys()),
        'largest_static_tables': sorted(
            [(k, v['row_count']) for k, v in report['static_tables'].items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
    }

    # Save report
    output_path = Path('/Users/marcin/Documents/KBase/CDM/ENIGMA/linkml-coral/cdm_schema_report.json')
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved to: {output_path}")
    print(f"\nSummary:")
    print(f"  Total tables: {report['summary']['total_tables']}")
    print(f"  Static tables: {report['summary']['total_static_tables']}")
    print(f"  Dynamic tables: {report['summary']['total_dynamic_tables']}")
    print(f"  Total data rows: {report['summary']['total_data_rows']:,}")
    print(f"  Type definitions: {report['summary']['total_types_defined']}")

if __name__ == '__main__':
    main()
