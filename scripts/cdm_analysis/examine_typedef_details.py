#!/usr/bin/env python3
"""
Examine specific details from sys_typedef to understand CORAL → CDM mappings.
"""

import pandas as pd
from pathlib import Path

DB_PATH = Path("data/enigma_coral.db")

def find_parquet_file(table_dir: Path) -> Path:
    """Find the actual parquet file in a Delta Lake table directory."""
    parquet_files = [f for f in table_dir.glob('*.parquet') if not f.parent.name.startswith('_')]
    return parquet_files[0] if parquet_files else None

def analyze_typedef():
    """Analyze sys_typedef in detail."""
    typedef_dir = DB_PATH / 'sys_typedef'
    parquet_file = find_parquet_file(typedef_dir)
    if not parquet_file:
        print("sys_typedef not found")
        return

    df = pd.read_parquet(parquet_file)

    print("=" * 80)
    print("SYS_TYPEDEF DETAILED ANALYSIS")
    print("=" * 80)

    # Group by type_name
    types = df['type_name'].unique()
    print(f"\nTotal Entity Types Defined: {len(types)}")
    print(f"Entity Types: {sorted(types)}")

    for type_name in sorted(types):
        print(f"\n{'=' * 80}")
        print(f"TYPE: {type_name}")
        print(f"{'=' * 80}")

        type_df = df[df['type_name'] == type_name].copy()

        # Identify primary key
        pk_fields = type_df[type_df['pk'] == True]
        if not pk_fields.empty:
            print(f"\nPrimary Key:")
            for _, row in pk_fields.iterrows():
                print(f"  {row['field_name']} → {row['cdm_column_name']} ({row['scalar_type']})")

        # Identify foreign keys
        fk_fields = type_df[type_df['fk'].notna()]
        if not fk_fields.empty:
            print(f"\nForeign Keys:")
            for _, row in fk_fields.iterrows():
                print(f"  {row['field_name']} → {row['cdm_column_name']} references {row['fk']}")

        # Identify ontology-constrained fields
        constraint_fields = type_df[type_df['constraint'].notna()]
        if not constraint_fields.empty:
            print(f"\nOntology/Constraint Fields:")
            for _, row in constraint_fields.iterrows():
                constraint = row['constraint']
                if constraint and ':' in str(constraint):  # Likely ontology constraint
                    print(f"  {row['field_name']} → {row['cdm_column_name']} (ontology: {constraint})")
                else:
                    print(f"  {row['field_name']} → {row['cdm_column_name']} (pattern: {constraint})")

        # Show all fields
        print(f"\nAll Fields ({len(type_df)} total):")
        for _, row in type_df.iterrows():
            required_str = "REQUIRED" if row.get('required') == True else "OPTIONAL"
            fk_str = f" → {row['fk']}" if pd.notna(row.get('fk')) else ""
            constraint_str = f" [{row['constraint']}]" if pd.notna(row.get('constraint')) else ""
            unit_str = f" unit={row['units_sys_oterm_id']}" if pd.notna(row.get('units_sys_oterm_id')) else ""

            print(f"  - {row['field_name']:25} {row['cdm_column_name']:40} {row['scalar_type']:10} {required_str}{fk_str}{constraint_str}{unit_str}")
            if row.get('comment'):
                print(f"      # {row['comment']}")

def analyze_ddt_typedef():
    """Analyze sys_ddt_typedef in detail."""
    ddt_typedef_dir = DB_PATH / 'sys_ddt_typedef'
    parquet_file = find_parquet_file(ddt_typedef_dir)
    if not parquet_file:
        print("sys_ddt_typedef not found")
        return

    df = pd.read_parquet(parquet_file)

    print("\n\n" + "=" * 80)
    print("SYS_DDT_TYPEDEF DETAILED ANALYSIS")
    print("=" * 80)

    # Group by brick
    bricks = df['ddt_ndarray_id'].unique()
    print(f"\nTotal Bricks Defined: {len(bricks)}")

    for brick_id in sorted(bricks)[:5]:  # Show first 5 in detail
        print(f"\n{'=' * 80}")
        print(f"BRICK: {brick_id}")
        print(f"{'=' * 80}")

        brick_df = df[df['ddt_ndarray_id'] == brick_id].copy()

        # Group by dimension
        dimensions = brick_df[brick_df['dimension_number'].notna()]['dimension_number'].unique()
        if len(dimensions) > 0:
            print(f"\nDimensions:")
            for dim in sorted(dimensions):
                dim_df = brick_df[brick_df['dimension_number'] == dim]
                if not dim_df.empty:
                    dim_row = dim_df.iloc[0]
                    print(f"  Dimension {int(dim)}: {dim_row['dimension_oterm_name']} ({dim_row['dimension_oterm_id']})")
                    print(f"    Variables:")
                    for _, row in dim_df.iterrows():
                        print(f"      - {row['cdm_column_name']:40} {row['scalar_type']:15} var#{row['variable_number']}: {row['variable_oterm_name']}")

        # Show value variables (no dimension_number)
        value_vars = brick_df[brick_df['dimension_number'].isna()]
        if not value_vars.empty:
            print(f"\nValue Variables:")
            for _, row in value_vars.iterrows():
                unit_str = f" [{row['unit_sys_oterm_name']}]" if pd.notna(row.get('unit_sys_oterm_name')) else ""
                print(f"  - {row['cdm_column_name']:40} {row['scalar_type']:15} {row['variable_oterm_name']}{unit_str}")
                if row.get('comment'):
                    print(f"      # {row['comment']}")

def main():
    """Run detailed typedef analysis."""
    analyze_typedef()
    analyze_ddt_typedef()

if __name__ == '__main__':
    main()
