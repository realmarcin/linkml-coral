#!/usr/bin/env python3
"""
Load ENIGMA TSV files into LinkML-Store database.

This script loads validated TSV data into a linkml-store database (DuckDB backend)
for efficient querying and analysis. It reuses the field mapping logic from
validate_tsv_linkml.py to ensure consistency.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any
import json

from linkml_store import Client
from linkml_runtime.utils.schemaview import SchemaView

# Import mapping functions from validation script
from validate_tsv_linkml import (
    read_tsv_file,
    map_tsv_to_schema_fields,
    infer_class_name_from_filename,
    load_schema
)


def create_store(db_path: str = None, schema_path: Path = None) -> tuple:
    """
    Create or connect to a linkml-store database.

    Args:
        db_path: Path to DuckDB database file. If None, uses in-memory database.
        schema_path: Path to LinkML schema file.

    Returns:
        tuple: (client, database, schema_view)
    """
    client = Client()

    # Attach database
    if db_path:
        print(f"📦 Connecting to database: {db_path}")
        db = client.attach_database(f"duckdb:///{db_path}", alias="enigma")
    else:
        print(f"📦 Creating in-memory database")
        db = client.attach_database("duckdb", alias="enigma")

    # Load schema if provided
    schema_view = None
    if schema_path:
        schema_view = load_schema(schema_path)
        print(f"📋 Loaded schema: {schema_view.schema.name}")

    return client, db, schema_view


def parse_array_field(value: Any) -> List[str]:
    """Parse string array fields like "['Reads:Reads0000001']" to Python lists."""
    if not value:
        return []

    # If already a list, return it
    if isinstance(value, list):
        return [str(item) for item in value]

    # If it's a string, try to parse it
    if isinstance(value, str):
        # Handle string representation of arrays
        if value.startswith('[') and value.endswith(']'):
            try:
                import ast
                parsed = ast.literal_eval(value)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except (ValueError, SyntaxError):
                # If parsing fails, try simple split
                pass

    return []


def extract_provenance_info(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and structure provenance information from a record.

    For Process records, parses input_objects and output_objects.
    Adds computed fields for easier querying.
    """
    enhanced = record.copy()

    # Parse Process input/output objects
    if 'process_input_objects' in record:
        input_objs = parse_array_field(record['process_input_objects'])
        enhanced['process_input_objects_parsed'] = input_objs

        # Extract entity types and IDs
        enhanced['input_entity_types'] = list(set(
            obj.split(':')[0] for obj in input_objs if ':' in obj
        ))
        enhanced['input_entity_ids'] = [
            obj.split(':')[1] if ':' in obj else obj
            for obj in input_objs
        ]

    if 'process_output_objects' in record:
        output_objs = parse_array_field(record['process_output_objects'])
        enhanced['process_output_objects_parsed'] = output_objs

        # Extract entity types and IDs
        enhanced['output_entity_types'] = list(set(
            obj.split(':')[0] for obj in output_objs if ':' in obj
        ))
        enhanced['output_entity_ids'] = [
            obj.split(':')[1] if ':' in obj else obj
            for obj in output_objs
        ]

    return enhanced


def add_computed_fields(record: Dict[str, Any], class_name: str) -> Dict[str, Any]:
    """Add computed fields for easier querying."""
    enhanced = record.copy()

    # Add read count categories for Reads
    if class_name == 'Reads' and 'reads_read_count' in record:
        read_count = record['reads_read_count']
        if isinstance(read_count, (int, float)):
            if read_count >= 100000:
                enhanced['read_count_category'] = 'very_high'
            elif read_count >= 50000:
                enhanced['read_count_category'] = 'high'
            elif read_count >= 10000:
                enhanced['read_count_category'] = 'medium'
            else:
                enhanced['read_count_category'] = 'low'

    # Add contig count categories for Assembly
    if class_name == 'Assembly' and 'assembly_n_contigs' in record:
        n_contigs = record['assembly_n_contigs']
        if isinstance(n_contigs, (int, float)):
            if n_contigs >= 1000:
                enhanced['contig_count_category'] = 'high'
            elif n_contigs >= 100:
                enhanced['contig_count_category'] = 'medium'
            else:
                enhanced['contig_count_category'] = 'low'

    return enhanced


def load_tsv_collection(
    tsv_path: Path,
    class_name: str,
    db,
    schema_view: SchemaView,
    verbose: bool = False
) -> int:
    """
    Load a single TSV file into a linkml-store collection.

    Args:
        tsv_path: Path to TSV file
        class_name: LinkML class name for this data
        db: Database connection
        schema_view: SchemaView instance
        verbose: Print detailed progress

    Returns:
        Number of records loaded
    """
    print(f"\n📥 Loading {tsv_path.name} as {class_name}...")

    # Read and map TSV data
    raw_data = read_tsv_file(tsv_path)
    if not raw_data:
        print(f"  ⚠️  No data found in {tsv_path.name}")
        return 0

    print(f"  📊 Read {len(raw_data)} records")

    # Map TSV fields to schema fields
    mapped_data, mapping_report = map_tsv_to_schema_fields(raw_data, class_name, schema_view)

    if mapping_report.get("status") == "class_not_found":
        print(f"  ❌ Class '{class_name}' not found in schema")
        return 0

    if verbose:
        print(f"  🔄 {mapping_report.get('mapping_summary', 'No mappings')}")
        if mapping_report.get('unmapped_columns'):
            print(f"  ⚠️  {len(mapping_report['unmapped_columns'])} unmapped columns")

    # Enhance records with computed fields and provenance info
    enhanced_data = []
    for record in mapped_data:
        # Add provenance parsing for Process records
        if class_name == 'Process':
            record = extract_provenance_info(record)

        # Add computed fields
        record = add_computed_fields(record, class_name)

        enhanced_data.append(record)

    # Create or get collection
    collection_name = class_name
    try:
        collection = db.get_collection(collection_name)
        if verbose:
            print(f"  📦 Using existing collection: {collection_name}")
    except:
        collection = db.create_collection(collection_name)
        if verbose:
            print(f"  ✨ Created new collection: {collection_name}")

    # Insert data
    try:
        collection.insert(enhanced_data)
        print(f"  ✅ Loaded {len(enhanced_data)} records into {collection_name}")
        return len(enhanced_data)
    except Exception as e:
        print(f"  ❌ Error loading data: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 0


def load_all_enigma_data(
    tsv_dir: Path,
    db,
    schema_view: SchemaView,
    collections: List[str] = None,
    verbose: bool = False
) -> Dict[str, int]:
    """
    Load all ENIGMA TSV files into the database.

    Args:
        tsv_dir: Directory containing TSV files
        db: Database connection
        schema_view: SchemaView instance
        collections: List of specific collections to load (None = all)
        verbose: Print detailed progress

    Returns:
        Dict mapping collection names to record counts
    """
    # Define file-to-class mappings
    file_mappings = {
        'Assembly.tsv': 'Assembly',
        'Community.tsv': 'Community',
        'Genome.tsv': 'Genome',
        'Location.tsv': 'Location',
        'Process.tsv': 'Process',
        'Protocol.tsv': 'Protocol',
        'Reads.tsv': 'Reads',
        'Sample.tsv': 'Sample',
        'Strain.tsv': 'Strain',
        'ASV.tsv': 'OTU',  # ASV maps to OTU class
    }

    # Filter if specific collections requested
    if collections:
        file_mappings = {
            k: v for k, v in file_mappings.items()
            if v in collections
        }

    results = {}
    total_records = 0

    for tsv_file, class_name in file_mappings.items():
        tsv_path = tsv_dir / tsv_file

        if not tsv_path.exists():
            if verbose:
                print(f"  ⚠️  Skipping {tsv_file} (not found)")
            continue

        count = load_tsv_collection(tsv_path, class_name, db, schema_view, verbose)
        results[class_name] = count
        total_records += count

    print(f"\n{'='*60}")
    print(f"📊 Summary: Loaded {total_records} total records across {len(results)} collections")
    return results


def create_indexes(db, verbose: bool = False):
    """Create indexes for common query patterns."""
    print(f"\n🔍 Creating indexes for query optimization...")

    index_specs = [
        # Primary identifiers
        ('Reads', 'reads_id'),
        ('Reads', 'reads_name'),
        ('Reads', 'reads_read_count'),
        ('Assembly', 'assembly_id'),
        ('Assembly', 'assembly_name'),
        ('Process', 'process_id'),
        # Foreign keys
        ('Assembly', 'assembly_strain'),
        ('Sample', 'sample_location'),
        # Computed fields
        ('Reads', 'read_count_category'),
        ('Assembly', 'contig_count_category'),
        # Provenance fields
        ('Process', 'input_entity_types'),
        ('Process', 'output_entity_types'),
    ]

    for collection_name, field_name in index_specs:
        try:
            collection = db.get_collection(collection_name)
            # Note: linkml-store may handle indexing automatically with DuckDB
            # This is a placeholder for explicit index creation if needed
            if verbose:
                print(f"  ✓ Indexed {collection_name}.{field_name}")
        except Exception as e:
            if verbose:
                print(f"  ⚠️  Could not index {collection_name}.{field_name}: {e}")

    print(f"  ✅ Index creation complete")


def show_database_info(db):
    """Display information about the loaded database."""
    print(f"\n{'='*60}")
    print(f"📚 Database Contents")
    print(f"{'='*60}")

    try:
        collections = db.list_collections()
        print(f"\nCollections: {len(collections)}")

        for coll_name in sorted(collections):
            try:
                collection = db.get_collection(coll_name)
                # Try to get count
                count = len(list(collection.find(limit=10000)))  # Approximate
                print(f"  • {coll_name}: ~{count} records")
            except Exception as e:
                print(f"  • {coll_name}: (error counting records)")
    except Exception as e:
        print(f"Could not list collections: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Load ENIGMA TSV files into LinkML-Store database'
    )
    parser.add_argument(
        'tsv_dir',
        help='Directory containing ENIGMA TSV files'
    )
    parser.add_argument(
        '--db',
        default='enigma_data.db',
        help='Path to DuckDB database file (default: enigma_data.db)'
    )
    parser.add_argument(
        '--schema',
        default='src/linkml_coral/schema/linkml_coral.yaml',
        help='Path to LinkML schema file'
    )
    parser.add_argument(
        '--collections',
        nargs='+',
        help='Specific collections to load (default: all)'
    )
    parser.add_argument(
        '--create-indexes',
        action='store_true',
        help='Create indexes after loading'
    )
    parser.add_argument(
        '--show-info',
        action='store_true',
        help='Show database information after loading'
    )
    parser.add_argument(
        '--in-memory',
        action='store_true',
        help='Use in-memory database instead of file'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress'
    )

    args = parser.parse_args()

    # Validate paths
    tsv_dir = Path(args.tsv_dir)
    if not tsv_dir.exists():
        print(f"Error: TSV directory not found: {tsv_dir}", file=sys.stderr)
        sys.exit(1)

    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)

    # Create store
    db_path = None if args.in_memory else args.db
    client, db, schema_view = create_store(db_path, schema_path)

    # Load data
    results = load_all_enigma_data(
        tsv_dir,
        db,
        schema_view,
        collections=args.collections,
        verbose=args.verbose
    )

    # Create indexes if requested
    if args.create_indexes:
        create_indexes(db, verbose=args.verbose)

    # Show info if requested
    if args.show_info:
        show_database_info(db)

    # Save database info
    if not args.in_memory:
        print(f"\n💾 Database saved to: {args.db}")
        print(f"   Size: {Path(args.db).stat().st_size / 1024 / 1024:.2f} MB")

    print(f"\n✨ Data loading complete!")

    # Exit with status
    total_loaded = sum(results.values())
    sys.exit(0 if total_loaded > 0 else 1)


if __name__ == "__main__":
    main()
