#!/usr/bin/env python3
"""
CDM Store Query CLI - Query interface for KBase CDM linkml-store database.

This tool provides user-friendly queries for the CDM parquet data loaded
into linkml-store.

Usage:
    # Show database statistics
    python query_cdm_store.py --db cdm_store.db stats

    # Find samples from a specific location
    python query_cdm_store.py --db cdm_store.db find-samples --location "Location0000001"

    # Search ontology terms
    python query_cdm_store.py --db cdm_store.db search-oterm "soil"

    # Trace provenance for an entity (uses CDM table names)
    python query_cdm_store.py --db cdm_store.db lineage sdt_assembly Assembly0000001
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

from linkml_store import Client


class CDMStoreQuery:
    """Query interface for CDM store database."""

    def __init__(self, db_path: str):
        """
        Initialize query interface.

        Args:
            db_path: Path to DuckDB database file
        """
        self.db_path = db_path
        self.client = Client()
        self.db = self.client.attach_database(f"duckdb:///{db_path}", alias="cdm")

    def get_collection(self, collection_name: str):
        """Get a collection from the database."""
        try:
            return self.db.get_collection(collection_name)
        except Exception as e:
            raise ValueError(f"Collection '{collection_name}' not found: {e}")

    def stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        stats = {
            'database': self.db_path,
            'collections': {}
        }

        # Get list of collection names
        collection_objs = self.db.list_collections()
        # Extract names - may be string or collection object
        collection_names = []
        for c in collection_objs:
            if isinstance(c, str):
                collection_names.append(c)
            elif hasattr(c, 'alias'):
                collection_names.append(c.alias)
            elif hasattr(c, 'target_class_name'):
                collection_names.append(c.target_class_name)
            else:
                continue

        total_records = 0

        for coll_name in sorted(collection_names):
            try:
                collection = self.get_collection(coll_name)
                result = collection.find(limit=100000)

                # Handle different result types
                if hasattr(result, 'num_rows'):
                    count = result.num_rows
                elif hasattr(result, 'rows'):
                    count = len(result.rows)
                else:
                    # Fallback: try to get rows
                    rows = list(result)
                    count = len(rows)

                total_records += count
                stats['collections'][coll_name] = count
            except Exception as e:
                stats['collections'][coll_name] = f"Error: {e}"

        stats['total_records'] = total_records
        stats['total_collections'] = len(collection_names)

        return stats

    def find_by_id(self, collection_name: str, entity_id: str) -> Optional[Dict]:
        """
        Find entity by ID.

        Args:
            collection_name: CDM table name (e.g., "sdt_sample", "sys_process")
            entity_id: Entity ID to find
        """
        collection = self.get_collection(collection_name)

        # Try different ID field patterns
        id_fields = [
            f"{collection_name}_id",  # e.g., sdt_sample_id
            f"{collection_name.replace('sdt_', '').replace('sys_', '')}_id",  # e.g., sample_id
            "id"
        ]

        for id_field in id_fields:
            try:
                results = list(collection.find({id_field: entity_id}, limit=1))
                if results:
                    return results[0]
            except:
                continue

        return None

    def find_samples_by_location(self, location_name: str, limit: int = 100) -> List[Dict]:
        """Find all samples from a specific location."""
        try:
            collection = self.get_collection("sdt_sample")
            result = collection.find({"sdt_location_name": location_name}, limit=limit)

            # Extract rows from result
            if hasattr(result, 'rows'):
                return result.rows
            else:
                return list(result)
        except Exception as e:
            raise ValueError(f"Error finding samples: {e}")

    def search_ontology_terms(self, search_term: str, limit: int = 50) -> List[Dict]:
        """Search ontology terms by name or ID pattern."""
        try:
            collection = self.get_collection("sys_oterm")
            # Simple search - linkml-store may support more advanced filtering
            result = collection.find(limit=10000)

            # Extract rows
            if hasattr(result, 'rows'):
                all_terms = result.rows
            else:
                all_terms = list(result)

            # Filter by search term
            search_lower = search_term.lower()
            results = [
                term for term in all_terms
                if search_lower in str(term.get('sys_oterm_name', '')).lower()
                   or search_lower in str(term.get('sys_oterm_id', '')).lower()
            ]

            return results[:limit]
        except Exception as e:
            raise ValueError(f"Error searching ontology terms: {e}")

    def get_processes_for_entity(self, entity_type: str, entity_id: str) -> Dict[str, List[Dict]]:
        """Get all processes involving an entity (as input or output)."""
        try:
            process_coll = self.get_collection("sys_process")
            result = process_coll.find(limit=100000)

            # Extract rows
            if hasattr(result, 'rows'):
                all_processes = result.rows
            else:
                all_processes = list(result)

            entity_ref = f"{entity_type}:{entity_id}"

            inputs = []
            outputs = []

            for proc in all_processes:
                # Check input objects
                input_objs = proc.get('input_objects_parsed', [])
                if entity_ref in input_objs:
                    inputs.append(proc)

                # Check output objects
                output_objs = proc.get('output_objects_parsed', [])
                if entity_ref in output_objs:
                    outputs.append(proc)

            return {
                'as_input': inputs,
                'as_output': outputs
            }
        except Exception as e:
            raise ValueError(f"Error getting processes: {e}")

    def trace_lineage(self, entity_type: str, entity_id: str, max_depth: int = 10) -> Dict:
        """Trace complete provenance lineage for an entity."""
        lineage = {
            'entity': f"{entity_type}:{entity_id}",
            'upstream': [],  # Entities that produced this entity
            'downstream': []  # Entities produced by this entity
        }

        try:
            processes = self.get_processes_for_entity(entity_type, entity_id)

            # Upstream: processes where entity is output
            for proc in processes['as_output']:
                upstream_entry = {
                    'process_id': proc.get('sys_process_id'),
                    'process_type': proc.get('sys_process_type_sys_oterm_name'),
                    'inputs': proc.get('input_objects_parsed', [])
                }
                lineage['upstream'].append(upstream_entry)

            # Downstream: processes where entity is input
            for proc in processes['as_input']:
                downstream_entry = {
                    'process_id': proc.get('sys_process_id'),
                    'process_type': proc.get('sys_process_type_sys_oterm_name'),
                    'outputs': proc.get('output_objects_parsed', [])
                }
                lineage['downstream'].append(downstream_entry)

            return lineage

        except Exception as e:
            raise ValueError(f"Error tracing lineage: {e}")


def cmd_stats(query: CDMStoreQuery, args):
    """Show database statistics."""
    print(f"\n📊 CDM Store Database Statistics")
    print(f"{'='*60}\n")

    stats = query.stats()

    print(f"📂 Database: {stats['database']}")
    print(f"📚 Total collections: {stats['total_collections']}")
    print(f"📄 Total records: {stats['total_records']:,}\n")

    print(f"Collections:")
    for coll_name, count in stats['collections'].items():
        if isinstance(count, int):
            print(f"  • {coll_name:30s} {count:>10,} records")
        else:
            print(f"  • {coll_name:30s} {count}")

    if args.export:
        export_path = Path(args.export)
        with open(export_path, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        print(f"\n💾 Statistics exported to: {export_path}")

    return 0


def cmd_find_samples(query: CDMStoreQuery, args):
    """Find samples by location."""
    print(f"\n🔍 Finding samples from location: {args.location}")
    print(f"{'='*60}\n")

    samples = query.find_samples_by_location(args.location, limit=args.limit)

    print(f"Found {len(samples)} sample(s):\n")

    for i, sample in enumerate(samples, 1):
        sample_id = sample.get('sdt_sample_id')
        sample_name = sample.get('sdt_sample_name')
        depth = sample.get('depth')
        date = sample.get('date')

        print(f"  {i}. {sample_name} ({sample_id})")
        if depth:
            print(f"     Depth: {depth}m")
        if date:
            print(f"     Date: {date}")
        print()

    if args.export:
        export_data = {
            'query': 'find_samples',
            'location': args.location,
            'count': len(samples),
            'results': samples
        }
        export_path = Path(args.export)
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        print(f"💾 Results exported to: {export_path}")

    return 0


def cmd_search_oterm(query: CDMStoreQuery, args):
    """Search ontology terms."""
    print(f"\n🔍 Searching ontology terms for: '{args.term}'")
    print(f"{'='*60}\n")

    terms = query.search_ontology_terms(args.term, limit=args.limit)

    print(f"Found {len(terms)} term(s):\n")

    for i, term in enumerate(terms, 1):
        term_id = term.get('sys_oterm_id')
        term_name = term.get('sys_oterm_name')
        term_def = term.get('sys_oterm_definition', '')

        print(f"  {i}. {term_id}: {term_name}")
        if term_def and len(term_def) < 100:
            print(f"     {term_def}")
        elif term_def:
            print(f"     {term_def[:100]}...")
        print()

    if args.export:
        export_data = {
            'query': 'search_oterm',
            'search_term': args.term,
            'count': len(terms),
            'results': terms
        }
        export_path = Path(args.export)
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        print(f"💾 Results exported to: {export_path}")

    return 0


def cmd_lineage(query: CDMStoreQuery, args):
    """Trace provenance lineage."""
    print(f"\n🔗 Tracing lineage for: {args.entity_type}:{args.entity_id}")
    print(f"{'='*60}\n")

    lineage = query.trace_lineage(args.entity_type, args.entity_id)

    # Show upstream (what produced this entity)
    print(f"⬆️  Upstream (inputs that produced this entity):")
    if lineage['upstream']:
        for i, entry in enumerate(lineage['upstream'], 1):
            print(f"  {i}. Process: {entry['process_id']} ({entry['process_type']})")
            print(f"     Inputs: {', '.join(entry['inputs'][:5])}")
            if len(entry['inputs']) > 5:
                print(f"            ... and {len(entry['inputs']) - 5} more")
            print()
    else:
        print(f"  (No upstream processes found)\n")

    # Show downstream (what this entity produced)
    print(f"⬇️  Downstream (outputs produced by this entity):")
    if lineage['downstream']:
        for i, entry in enumerate(lineage['downstream'], 1):
            print(f"  {i}. Process: {entry['process_id']} ({entry['process_type']})")
            print(f"     Outputs: {', '.join(entry['outputs'][:5])}")
            if len(entry['outputs']) > 5:
                print(f"             ... and {len(entry['outputs']) - 5} more")
            print()
    else:
        print(f"  (No downstream processes found)\n")

    if args.export:
        export_data = {
            'query': 'lineage',
            'entity': f"{args.entity_type}:{args.entity_id}",
            'lineage': lineage
        }
        export_path = Path(args.export)
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        print(f"💾 Lineage exported to: {export_path}")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description='CDM Store Query CLI - Query KBase CDM linkml-store database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show database statistics (tables now use CDM naming)
  python query_cdm_store.py --db cdm_store.db stats

  # Find samples from a location
  python query_cdm_store.py --db cdm_store.db find-samples --location Location0000001

  # Search ontology terms
  python query_cdm_store.py --db cdm_store.db search-oterm "soil"

  # Trace lineage for an assembly (use CDM table name: sdt_assembly)
  python query_cdm_store.py --db cdm_store.db lineage sdt_assembly Assembly0000001

  # Export results to JSON
  python query_cdm_store.py --db cdm_store.db stats --export stats.json
        """
    )

    parser.add_argument(
        '--db',
        default='cdm_store.db',
        help='Path to CDM store database (default: cdm_store.db)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')
    stats_parser.add_argument('--export', help='Export stats to JSON file')

    # Find samples command
    find_samples_parser = subparsers.add_parser('find-samples', help='Find samples by location')
    find_samples_parser.add_argument('--location', required=True, help='Location name or ID')
    find_samples_parser.add_argument('--limit', type=int, default=100, help='Max results (default: 100)')
    find_samples_parser.add_argument('--export', help='Export results to JSON file')

    # Search ontology terms command
    search_oterm_parser = subparsers.add_parser('search-oterm', help='Search ontology terms')
    search_oterm_parser.add_argument('term', help='Search term (in name or ID)')
    search_oterm_parser.add_argument('--limit', type=int, default=50, help='Max results (default: 50)')
    search_oterm_parser.add_argument('--export', help='Export results to JSON file')

    # Lineage command
    lineage_parser = subparsers.add_parser('lineage', help='Trace provenance lineage')
    lineage_parser.add_argument('entity_type', help='CDM table name (e.g., sdt_assembly, sdt_reads)')
    lineage_parser.add_argument('entity_id', help='Entity ID (e.g., Assembly0000001)')
    lineage_parser.add_argument('--export', help='Export lineage to JSON file')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Check database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {args.db}", file=sys.stderr)
        print(f"\nCreate database first:", file=sys.stderr)
        print(f"  just load-cdm-store", file=sys.stderr)
        sys.exit(1)

    # Initialize query interface
    try:
        query = CDMStoreQuery(str(db_path))
    except Exception as e:
        print(f"Error connecting to database: {e}", file=sys.stderr)
        sys.exit(1)

    # Execute command
    try:
        if args.command == 'stats':
            return cmd_stats(query, args)
        elif args.command == 'find-samples':
            return cmd_find_samples(query, args)
        elif args.command == 'search-oterm':
            return cmd_search_oterm(query, args)
        elif args.command == 'lineage':
            return cmd_lineage(query, args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1

    except Exception as e:
        print(f"\nError executing query: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
