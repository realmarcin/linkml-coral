#!/usr/bin/env python3
"""
Update LinkML CDM schema files with metadata from parquet files.

This script:
1. Loads metadata from JSON catalogs
2. Updates schema YAML files with descriptions and annotations
3. Preserves existing schema structure
4. Adds validation patterns where applicable
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import ruamel.yaml


def load_catalogs(metadata_dir: Path) -> Dict[str, List[Dict[str, Any]]]:
    """Load all metadata catalogs."""
    combined_file = metadata_dir / 'all_catalogs.json'

    if not combined_file.exists():
        print(f"Error: Catalog file not found: {combined_file}", file=sys.stderr)
        sys.exit(1)

    with open(combined_file) as f:
        return json.load(f)


def create_column_lookup(column_catalog: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Create lookup table: table.column -> metadata."""
    lookup = {}
    for col in column_catalog:
        key = f"{col['table_name']}.{col['column_name']}"
        lookup[key] = col
    return lookup


def update_slot_with_metadata(
    slot_def: Dict[str, Any],
    metadata: Dict[str, Any],
    yaml: ruamel.yaml.YAML
) -> bool:
    """
    Update a slot definition with metadata.

    Returns:
        True if slot was modified
    """
    modified = False

    # Add description
    if metadata.get('description') and not slot_def.get('description'):
        slot_def['description'] = metadata['description']
        modified = True

    # Add annotations
    if not slot_def.get('annotations'):
        slot_def['annotations'] = {}

    annotations = slot_def['annotations']

    # Add microtype
    if metadata.get('microtype') and not annotations.get('microtype'):
        annotations['microtype'] = metadata['microtype']
        modified = True

    # Add units
    if metadata.get('units') and not annotations.get('units'):
        annotations['units'] = metadata['units']
        modified = True

    # Add constraint type
    if metadata.get('field_type') and not annotations.get('constraint_type'):
        annotations['constraint_type'] = metadata['field_type']
        modified = True

    # Add original name
    if metadata.get('original_name') and not annotations.get('original_name'):
        annotations['original_name'] = metadata['original_name']
        modified = True

    # Update identifier flag for primary keys
    if metadata.get('is_primary_key') and not slot_def.get('identifier'):
        slot_def['identifier'] = True
        modified = True

    # Update required flag
    if metadata.get('is_required') and not slot_def.get('required'):
        slot_def['required'] = True
        modified = True

    # Add pattern constraint
    if metadata.get('constraint_pattern') and not slot_def.get('pattern'):
        pattern = metadata['constraint_pattern']
        # Only add if it looks like a regex pattern (not an ontology constraint)
        if '\\' in pattern or pattern.startswith('^'):
            slot_def['pattern'] = pattern
            modified = True

    # Remove empty annotations
    if not annotations:
        del slot_def['annotations']

    return modified


def update_schema_file(
    schema_file: Path,
    column_lookup: Dict[str, Dict[str, Any]],
    dry_run: bool = False
) -> int:
    """
    Update a schema YAML file with metadata.

    Returns:
        Number of slots updated
    """
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    yaml.width = 4096  # Prevent line wrapping

    # Load schema
    with open(schema_file) as f:
        schema = yaml.load(f)

    if not schema or 'slots' not in schema:
        return 0

    slots_updated = 0

    # Update each slot
    for slot_name, slot_def in schema['slots'].items():
        # Try to find matching metadata
        # Look for exact match first
        metadata = None
        for key, meta in column_lookup.items():
            if meta['column_name'] == slot_name:
                metadata = meta
                break

        if not metadata:
            continue

        # Update slot
        if update_slot_with_metadata(slot_def, metadata, yaml):
            slots_updated += 1

    # Save updated schema
    if not dry_run and slots_updated > 0:
        with open(schema_file, 'w') as f:
            yaml.dump(schema, f)

    return slots_updated


def main():
    parser = argparse.ArgumentParser(
        description='Update LinkML CDM schema with metadata from parquet files'
    )

    parser.add_argument(
        '--metadata-dir',
        type=Path,
        default=Path('data/cdm_metadata'),
        help='Directory containing metadata catalog files'
    )

    parser.add_argument(
        '--schema-dir',
        type=Path,
        default=Path('src/linkml_coral/schema/cdm'),
        help='Directory containing CDM schema YAML files'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be updated without modifying files'
    )

    parser.add_argument(
        '--file',
        help='Update only this specific schema file'
    )

    args = parser.parse_args()

    print("📝 Updating LinkML CDM Schema with Metadata")
    print("="*70)
    print()

    # Load catalogs
    print("📥 Loading metadata catalogs...")
    catalogs = load_catalogs(args.metadata_dir)
    column_lookup = create_column_lookup(catalogs['column_catalog'])
    print(f"   ✅ Loaded metadata for {len(column_lookup)} columns")
    print()

    # Find schema files to update
    if args.file:
        schema_files = [args.schema_dir / args.file]
    else:
        schema_files = list(args.schema_dir.glob('*.yaml'))

    if not schema_files:
        print(f"Error: No schema files found in {args.schema_dir}", file=sys.stderr)
        sys.exit(1)

    # Update each schema file
    total_updated = 0

    for schema_file in sorted(schema_files):
        if not schema_file.exists():
            print(f"⚠️  File not found: {schema_file}")
            continue

        print(f"📄 Processing {schema_file.name}...")

        try:
            slots_updated = update_schema_file(
                schema_file,
                column_lookup,
                dry_run=args.dry_run
            )

            if slots_updated > 0:
                status = "would update" if args.dry_run else "updated"
                print(f"   ✅ {status} {slots_updated} slot(s)")
                total_updated += slots_updated
            else:
                print(f"   ℹ️  No changes needed")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()

        print()

    # Summary
    print("="*70)
    if args.dry_run:
        print(f"🔍 Dry run complete: {total_updated} slots would be updated")
    else:
        print(f"✅ Schema update complete: {total_updated} slots updated")
    print()


if __name__ == "__main__":
    main()
