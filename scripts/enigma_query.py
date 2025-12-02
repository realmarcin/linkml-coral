#!/usr/bin/env python3
"""
ENIGMA Query CLI - User-friendly command-line interface for querying ENIGMA data.

This tool provides easy access to common queries and analyses of the ENIGMA
genomic dataset stored in linkml-store.
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional

from query_enigma_provenance import ENIGMAProvenanceQuery
from query_provenance_tracker import QueryProvenanceTracker


def cmd_unused_reads(query: ENIGMAProvenanceQuery, args):
    """Find unused 'good' reads that were not used in assemblies."""
    # Start provenance tracking
    tracker = QueryProvenanceTracker(args.db, args.provenance_dir)
    params = {
        "min_count": args.min_count,
        "top_n": args.top_n,
        "ids_only": args.ids_only,
        "exclude_16s": args.exclude_16s if hasattr(args, 'exclude_16s') else False
    }
    if hasattr(args, 'read_type') and args.read_type:
        params["read_type"] = args.read_type

    desc = f"Find unused reads with >= {args.min_count} raw reads"
    if args.exclude_16s:
        desc += " (isolate genome reads only)"
    elif hasattr(args, 'read_type') and args.read_type:
        desc += f" (read type: {args.read_type})"

    execution_id = tracker.start_query(
        query_type="unused_reads",
        parameters=params,
        description=desc
    )

    print(f"\n🔍 Query: Unused 'Good' Reads")
    print(f"{'='*60}\n")
    print(f"Finding reads with >= {args.min_count:,} raw reads that were NOT used in assemblies...\n")

    try:
        unused_reads, summary = query.get_unused_reads(
            min_count=args.min_count,
            return_details=not args.ids_only,
            read_type=args.read_type if hasattr(args, 'read_type') else None,
            exclude_16s=args.exclude_16s if hasattr(args, 'exclude_16s') else False
        )

        # Print summary
        print(f"📊 Results:")
        print(f"  • Total 'good' reads: {summary['total_good_reads']:,}")
        print(f"  • Used in assemblies: {summary['reads_used_in_assemblies']:,}")
        print(f"  • UNUSED 'good' reads: {summary['unused_good_reads']:,}")
        print(f"  • Utilization rate: {summary['utilization_rate']:.1%}")

        if 'unused_stats' in summary:
            print(f"\n📈 Unused Reads Statistics:")
            stats = summary['unused_stats']
            print(f"  • Min count: {stats['min_count']:,}")
            print(f"  • Max count: {stats['max_count']:,}")
            print(f"  • Avg count: {stats['avg_count']:,.0f}")
            print(f"  • Total wasted reads: {stats['total_wasted_reads']:,}")

        # Show top unused reads
        if unused_reads and not args.ids_only:
            print(f"\n🔬 Top {min(args.top_n, len(unused_reads))} Unused Reads (by count):")
            sorted_unused = sorted(
                unused_reads,
                key=lambda x: x.get('reads_read_count', 0),
                reverse=True
            )
            for i, r in enumerate(sorted_unused[:args.top_n], 1):
                name = r.get('reads_name', r['reads_id'])
                count = r.get('reads_read_count', 0)
                category = r.get('read_count_category', 'unknown')
                print(f"  {i:2d}. {name}")
                print(f"      Read count: {count:,} ({category})")
                if r.get('reads_link'):
                    print(f"      Link: {r['reads_link']}")

        # Export if requested
        output_files = {}
        if args.export:
            export_data = {
                'query': 'unused_reads',
                'parameters': {'min_count': args.min_count},
                'summary': summary,
                'results': unused_reads if not args.ids_only else list(unused_reads),
                'provenance': {'execution_id': execution_id}
            }
            export_path = Path(args.export)
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            print(f"\n💾 Results exported to: {export_path}")
            output_files['results'] = str(export_path)

        # Record database stats and complete provenance tracking
        db_stats = {
            'total_reads': summary['total_good_reads'] + (len(query.get_all_reads()) - summary['total_good_reads']),
            'total_assemblies': len(query.get_all_assemblies()),
            'total_processes': query.get_collection("Process").find({}).num_rows
        }
        tracker.record_database_stats(db_stats)
        tracker.end_query(summary, output_files)

        return 0

    except Exception as e:
        tracker.end_query({}, error=str(e))
        raise


def cmd_stats(query: ENIGMAProvenanceQuery, args):
    """Show database statistics."""
    print(f"\n📊 ENIGMA Database Statistics")
    print(f"{'='*60}\n")

    query.print_summary()

    # Additional detailed stats
    print(f"\n🔬 Detailed Analysis:")

    # Process statistics
    all_processes_count = query.get_collection("Process").find({}).num_rows
    assembly_processes = query.get_reads_to_assembly_processes()

    print(f"\n  Processes:")
    print(f"    • Total processes: {all_processes_count:,}")
    print(f"    • Assembly processes (Reads→Assembly): {len(assembly_processes):,}")

    # Read utilization
    reads_used = query.get_reads_used_in_assemblies()
    all_reads = query.get_all_reads()

    print(f"\n  Read Utilization:")
    print(f"    • Total reads: {len(all_reads):,}")
    print(f"    • Used in assemblies: {len(reads_used):,}")
    print(f"    • Unused: {len(all_reads) - len(reads_used):,}")
    if all_reads:
        print(f"    • Utilization rate: {len(reads_used) / len(all_reads):.1%}")

    return 0


def cmd_lineage(query: ENIGMAProvenanceQuery, args):
    """Show provenance lineage for an entity."""
    entity_type = args.entity_type
    entity_id = args.entity_id

    print(f"\n🔗 Provenance Lineage: {entity_type} {entity_id}")
    print(f"{'='*60}\n")

    if entity_type == 'Assembly':
        lineage = query.get_assembly_lineage(entity_id)

        print(f"Process Chain:")
        print(f"  • Number of process steps: {lineage['process_count']}")

        print(f"\nInputs:")
        print(f"  • Reads: {len(lineage['input_reads'])}")
        if lineage['input_reads']:
            for read_id in lineage['input_reads'][:10]:
                print(f"    - {read_id}")
            if len(lineage['input_reads']) > 10:
                print(f"    ... and {len(lineage['input_reads']) - 10} more")

        print(f"  • Samples: {len(lineage['input_samples'])}")
        if lineage['input_samples']:
            for sample_id in lineage['input_samples'][:10]:
                print(f"    - {sample_id}")

        # Export if requested
        if args.export:
            export_path = Path(args.export)
            with open(export_path, 'w') as f:
                json.dump(lineage, f, indent=2, default=str)
            print(f"\n💾 Lineage exported to: {export_path}")
    else:
        # Generic provenance chain
        chain = query.get_entity_provenance_chain(entity_type, entity_id)
        print(f"Process chain length: {len(chain)}")

        for i, process in enumerate(chain, 1):
            print(f"\n  Step {i}: {process['process_id']}")
            print(f"    Inputs: {', '.join(process.get('input_entity_types', []))}")
            print(f"    Outputs: {', '.join(process.get('output_entity_types', []))}")

    return 0


def cmd_find(query: ENIGMAProvenanceQuery, args):
    """Find entities by criteria."""
    collection_name = args.collection

    print(f"\n🔍 Find: {collection_name}")
    print(f"{'='*60}\n")

    try:
        collection = query.get_collection(collection_name)

        # Build query from key=value pairs
        query_dict = {}
        if args.query:
            for kv in args.query:
                if '=' in kv:
                    key, value = kv.split('=', 1)
                    # Try to convert to int if possible
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                    query_dict[key] = value

        # Execute query
        qr = collection.find(query_dict)
        results = qr.rows[:args.limit] if len(qr.rows) < args.limit else list(collection.find_iter(query_dict))[:args.limit]

        print(f"Found {len(results)} results")

        if results:
            print(f"\nResults:")
            for i, record in enumerate(results[:args.limit], 1):
                # Show key fields
                id_field = f"{collection_name.lower()}_id"
                name_field = f"{collection_name.lower()}_name"

                record_id = record.get(id_field, record.get('id', '?'))
                record_name = record.get(name_field, record.get('name', ''))

                print(f"  {i}. {record_id}")
                if record_name:
                    print(f"     Name: {record_name}")

                # Show query-relevant fields
                for key in query_dict.keys():
                    if key in record:
                        print(f"     {key}: {record[key]}")

        # Export if requested
        if args.export and results:
            export_path = Path(args.export)
            with open(export_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n💾 Results exported to: {export_path}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Query ENIGMA genomic data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find unused reads with >50k raw reads
  enigma_query.py unused-reads --min-count 50000

  # Show database statistics
  enigma_query.py stats

  # Show lineage for an assembly
  enigma_query.py lineage Assembly Assembly0000001

  # Find reads by criteria
  enigma_query.py find Reads --query read_count_category=high --limit 20

  # Export results to JSON
  enigma_query.py unused-reads --min-count 10000 --export results.json
        """
    )

    parser.add_argument(
        '--db',
        default='enigma_data.db',
        help='Path to database file (default: enigma_data.db)'
    )
    parser.add_argument(
        '--provenance-dir',
        default='query_provenance',
        help='Directory for provenance tracking (default: query_provenance)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # unused-reads command
    parser_unused = subparsers.add_parser(
        'unused-reads',
        help='Find unused "good" reads not used in assemblies'
    )
    parser_unused.add_argument(
        '--min-count',
        type=int,
        default=10000,
        help='Minimum read count threshold (default: 10000)'
    )
    parser_unused.add_argument(
        '--top-n',
        type=int,
        default=20,
        help='Number of top results to show (default: 20)'
    )
    parser_unused.add_argument(
        '--ids-only',
        action='store_true',
        help='Return only IDs, not full records'
    )
    parser_unused.add_argument(
        '--export',
        metavar='FILE',
        help='Export results to JSON file'
    )
    parser_unused.add_argument(
        '--read-type',
        metavar='TYPE',
        help='Filter by read type (e.g., ME:0000114 for Single End)'
    )
    parser_unused.add_argument(
        '--exclude-16s',
        action='store_true',
        help='Exclude 16S/metagenome data (keep only Single End isolate genome reads)'
    )

    # stats command
    parser_stats = subparsers.add_parser(
        'stats',
        help='Show database statistics'
    )

    # lineage command
    parser_lineage = subparsers.add_parser(
        'lineage',
        help='Show provenance lineage for an entity'
    )
    parser_lineage.add_argument(
        'entity_type',
        choices=['Assembly', 'Genome', 'Reads', 'Sample'],
        help='Type of entity'
    )
    parser_lineage.add_argument(
        'entity_id',
        help='Entity ID'
    )
    parser_lineage.add_argument(
        '--export',
        metavar='FILE',
        help='Export lineage to JSON file'
    )

    # find command
    parser_find = subparsers.add_parser(
        'find',
        help='Find entities by criteria'
    )
    parser_find.add_argument(
        'collection',
        help='Collection name (Reads, Assembly, Process, etc.)'
    )
    parser_find.add_argument(
        '--query',
        nargs='+',
        help='Query as key=value pairs'
    )
    parser_find.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Maximum number of results (default: 100)'
    )
    parser_find.add_argument(
        '--export',
        metavar='FILE',
        help='Export results to JSON file'
    )

    args = parser.parse_args()

    # Check if database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"❌ Error: Database not found: {db_path}")
        print(f"\n💡 Tip: Create the database first with:")
        print(f"   uv run python load_tsv_to_store.py /path/to/tsv/files")
        return 1

    # Initialize query interface
    try:
        query = ENIGMAProvenanceQuery(str(db_path))
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return 1

    # Execute command
    if not args.command:
        parser.print_help()
        return 1

    commands = {
        'unused-reads': cmd_unused_reads,
        'stats': cmd_stats,
        'lineage': cmd_lineage,
        'find': cmd_find,
    }

    return commands[args.command](query, args)


if __name__ == "__main__":
    sys.exit(main())
