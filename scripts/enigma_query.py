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


def cmd_samples(query: ENIGMAProvenanceQuery, args):
    """Find samples by various criteria (depth, date, location)."""
    print(f"\n🔍 Query: Find Samples")
    print(f"{'='*60}\n")

    # Build filter description
    filters = []
    if args.depth_min is not None:
        filters.append(f"depth >= {args.depth_min}m")
    if args.depth_max is not None:
        filters.append(f"depth <= {args.depth_max}m")
    if args.date:
        filters.append(f"date = {args.date}")
    if args.location:
        filters.append(f"location contains '{args.location}'")

    if filters:
        print(f"Filters: {', '.join(filters)}\n")
    else:
        print("No filters applied (showing all samples)\n")

    # Get samples
    samples = query.get_collection("Sample").find({})

    # Apply filters
    filtered = []
    for s in samples.rows:
        depth = s.get('sample_depth')
        if args.depth_min is not None and (depth is None or depth < args.depth_min):
            continue
        if args.depth_max is not None and (depth is None or depth > args.depth_max):
            continue
        if args.date and s.get('sample_date') != args.date:
            continue
        if args.location and args.location not in str(s.get('sample_location', '')):
            continue
        filtered.append(s)

    print(f"Found {len(filtered)} samples matching criteria\n")

    if filtered:
        # Sort by depth (descending) if depth filter was used
        if args.depth_min is not None or args.depth_max is not None:
            filtered.sort(key=lambda x: x.get('sample_depth') or 0, reverse=True)

        # Display results in table format
        print(f"{'Sample ID':<18} | {'Location':<12} | {'Depth (m)':<10} | {'Date':<12}")
        print(f"{'-'*18}-+-{'-'*12}-+-{'-'*10}-+-{'-'*12}")

        for s in filtered[:args.limit]:
            sample_id = s.get('sample_id', '?')
            location = s.get('sample_location', '?')[:12]
            depth = s.get('sample_depth')
            depth_str = f"{depth:.2f}" if depth is not None else "N/A"
            date = s.get('sample_date', 'N/A')
            print(f"{sample_id:<18} | {location:<12} | {depth_str:<10} | {date:<12}")

        if len(filtered) > args.limit:
            print(f"\n... and {len(filtered) - args.limit} more (use --limit to show more)")

    # Export if requested
    if args.export and filtered:
        export_data = {
            'query': 'samples',
            'filters': {
                'depth_min': args.depth_min,
                'depth_max': args.depth_max,
                'date': args.date,
                'location': args.location,
            },
            'total_matches': len(filtered),
            'results': filtered[:args.limit]
        }
        export_path = Path(args.export)
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        print(f"\n💾 Results exported to: {export_path}")

    return 0


def cmd_sql(query: ENIGMAProvenanceQuery, args):
    """Execute arbitrary SQL query against the database."""
    import duckdb

    sql = args.sql

    print(f"\n🔍 SQL Query")
    print(f"{'='*60}\n")
    print(f"  {sql}\n")

    try:
        # Connect directly to DuckDB for raw SQL
        conn = duckdb.connect(args.db, read_only=True)
        result = conn.execute(sql)

        # Get column names
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()

        print(f"📊 Results: {len(rows)} rows\n")

        if rows:
            # Calculate column widths
            col_widths = []
            for i, col in enumerate(columns):
                max_width = len(str(col))
                for row in rows[:args.limit]:
                    val = row[i]
                    max_width = max(max_width, len(str(val) if val is not None else 'NULL'))
                col_widths.append(min(max_width, 40))  # Cap at 40 chars

            # Print header
            header = ' | '.join(f"{col:<{col_widths[i]}}" for i, col in enumerate(columns))
            print(header)
            print('-+-'.join('-' * w for w in col_widths))

            # Print rows
            for row in rows[:args.limit]:
                row_str = ' | '.join(
                    f"{str(val)[:col_widths[i]] if val is not None else 'NULL':<{col_widths[i]}}"
                    for i, val in enumerate(row)
                )
                print(row_str)

            if len(rows) > args.limit:
                print(f"\n... and {len(rows) - args.limit} more rows (use --limit to show more)")

        # Export if requested
        if args.export and rows:
            export_data = {
                'query': sql,
                'columns': columns,
                'row_count': len(rows),
                'results': [dict(zip(columns, row)) for row in rows[:args.limit]]
            }
            export_path = Path(args.export)
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            print(f"\n💾 Results exported to: {export_path}")

        conn.close()
        return 0

    except Exception as e:
        print(f"❌ SQL Error: {e}")
        return 1


def cmd_unused_reads_sql(query: ENIGMAProvenanceQuery, args):
    """Find unused good reads using pure SQL (faster than Python iteration)."""
    import duckdb

    print(f"\n🔍 Query: Unused 'Good' Reads (SQL)")
    print(f"{'='*60}\n")

    # Build read type filter
    read_type_filter = ""
    read_type_params = []
    filter_desc = ""

    if args.exclude_16s:
        # Keep only Single End isolate genome reads (ME:0000114)
        read_type_filter = "AND reads_read_type = 'ME:0000114'"
        filter_desc = " (isolate genome reads only, excluding 16S/metagenome)"
    elif args.read_type:
        read_type_filter = "AND reads_read_type = ?"
        read_type_params = [args.read_type]
        filter_desc = f" (read type: {args.read_type})"

    print(f"Finding reads with >= {args.min_count:,} raw reads NOT used in assemblies{filter_desc}...\n")

    conn = duckdb.connect(args.db, read_only=True)

    # Summary statistics query - dynamically build with read type filter
    summary_sql = f"""
    WITH
    good_reads AS (
        SELECT reads_id FROM Reads
        WHERE reads_read_count >= ? {read_type_filter}
    ),
    used_reads AS (
        SELECT DISTINCT UNNEST(input_entity_ids) as reads_id
        FROM Process
        WHERE ARRAY_CONTAINS(input_entity_types, 'Reads')
          AND ARRAY_CONTAINS(output_entity_types, 'Assembly')
    ),
    used_good_reads AS (
        SELECT g.reads_id FROM good_reads g
        WHERE g.reads_id IN (SELECT reads_id FROM used_reads)
    )
    SELECT
        (SELECT COUNT(*) FROM good_reads) as total_good_reads,
        (SELECT COUNT(*) FROM used_good_reads) as reads_used_in_assemblies,
        (SELECT COUNT(*) FROM good_reads WHERE reads_id NOT IN (SELECT reads_id FROM used_reads)) as unused_good_reads
    """

    # Detail query for top unused reads
    detail_sql = f"""
    WITH used_reads AS (
        SELECT DISTINCT UNNEST(input_entity_ids) as reads_id
        FROM Process
        WHERE ARRAY_CONTAINS(input_entity_types, 'Reads')
          AND ARRAY_CONTAINS(output_entity_types, 'Assembly')
    )
    SELECT r.reads_id, r.reads_name, r.reads_read_count, r.read_count_category, r.reads_read_type
    FROM Reads r
    WHERE r.reads_read_count >= ? {read_type_filter}
      AND r.reads_id NOT IN (SELECT reads_id FROM used_reads)
    ORDER BY r.reads_read_count DESC
    LIMIT ?
    """

    try:
        # Build parameter list
        summary_params = [args.min_count] + read_type_params
        detail_params = [args.min_count] + read_type_params + [args.limit]

        # Execute summary query
        summary_result = conn.execute(summary_sql, summary_params).fetchone()
        total_good, used_in_assemblies, unused_good = summary_result

        utilization_rate = used_in_assemblies / total_good if total_good > 0 else 0

        print(f"📊 Summary:")
        print(f"  • Total 'good' reads (>= {args.min_count:,}): {total_good:,}")
        print(f"  • Used in assemblies: {used_in_assemblies:,}")
        print(f"  • UNUSED 'good' reads: {unused_good:,}")
        print(f"  • Utilization rate: {utilization_rate:.1%}")

        # Execute detail query
        detail_result = conn.execute(detail_sql, detail_params).fetchall()

        if detail_result:
            print(f"\n🔬 Top {len(detail_result)} Unused Reads (by count):\n")
            print(f"{'Reads ID':<18} | {'Name':<30} | {'Read Count':>12} | {'Type':<12} | {'Category':<10}")
            print(f"{'-'*18}-+-{'-'*30}-+-{'-'*12}-+-{'-'*12}-+-{'-'*10}")

            for row in detail_result:
                reads_id, name, count, category, read_type = row
                name_display = (name or reads_id)[:30]
                type_display = read_type or 'N/A'
                print(f"{reads_id:<18} | {name_display:<30} | {count:>12,} | {type_display:<12} | {category or 'N/A':<10}")

        # Export if requested
        if args.export:
            # Get all unused reads for export
            export_sql = f"""
            WITH used_reads AS (
                SELECT DISTINCT UNNEST(input_entity_ids) as reads_id
                FROM Process
                WHERE ARRAY_CONTAINS(input_entity_types, 'Reads')
                  AND ARRAY_CONTAINS(output_entity_types, 'Assembly')
            )
            SELECT r.reads_id, r.reads_name, r.reads_read_count, r.read_count_category, r.reads_read_type
            FROM Reads r
            WHERE r.reads_read_count >= ? {read_type_filter}
              AND r.reads_id NOT IN (SELECT reads_id FROM used_reads)
            ORDER BY r.reads_read_count DESC
            """
            export_params = [args.min_count] + read_type_params
            all_unused = conn.execute(export_sql, export_params).fetchall()

            export_data = {
                'query': 'unused_reads_sql',
                'parameters': {
                    'min_count': args.min_count,
                    'exclude_16s': getattr(args, 'exclude_16s', False),
                    'read_type': getattr(args, 'read_type', None)
                },
                'summary': {
                    'total_good_reads': total_good,
                    'reads_used_in_assemblies': used_in_assemblies,
                    'unused_good_reads': unused_good,
                    'utilization_rate': utilization_rate
                },
                'results': [
                    {'reads_id': r[0], 'reads_name': r[1], 'reads_read_count': r[2], 'read_count_category': r[3], 'reads_read_type': r[4]}
                    for r in all_unused
                ]
            }
            export_path = Path(args.export)
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            print(f"\n💾 Results exported to: {export_path}")

        conn.close()
        return 0

    except Exception as e:
        conn.close()
        print(f"❌ SQL Error: {e}")
        return 1


def cmd_samples_with_reads(query: ENIGMAProvenanceQuery, args):
    """Find reads meeting count threshold (high-quality reads)."""
    print(f"\n🔍 Query: High-Count Reads")
    print(f"{'='*60}\n")
    print(f"Finding reads with count >= {args.min_reads:,}...\n")

    # Get all reads and filter by threshold
    all_reads = query.get_all_reads(min_count=args.min_reads)

    print(f"Found {len(all_reads)} reads with count >= {args.min_reads:,}\n")

    if all_reads:
        # Sort by read count (descending)
        sorted_reads = sorted(
            all_reads,
            key=lambda x: x.get('reads_read_count', 0),
            reverse=True
        )

        # Display results
        print(f"{'Reads ID':<18} | {'Name':<30} | {'Read Count':<12} | {'Category':<10}")
        print(f"{'-'*18}-+-{'-'*30}-+-{'-'*12}-+-{'-'*10}")

        for r in sorted_reads[:args.limit]:
            reads_id = r.get('reads_id', '?')
            name = r.get('reads_name', '?')[:30]
            count = r.get('reads_read_count', 0)
            category = r.get('read_count_category', 'unknown')

            print(f"{reads_id:<18} | {name:<30} | {count:>10,} | {category:<10}")

        if len(sorted_reads) > args.limit:
            print(f"\n... and {len(sorted_reads) - args.limit} more (use --limit to show more)")

        # Summary stats
        all_counts = [r.get('reads_read_count', 0) for r in all_reads]
        print(f"\n📊 Summary:")
        print(f"  • Total matching reads: {len(all_reads):,}")
        print(f"  • Total read count: {sum(all_counts):,}")
        print(f"  • Average per read: {sum(all_counts) / len(all_counts):,.0f}")
        print(f"  • Min: {min(all_counts):,}")
        print(f"  • Max: {max(all_counts):,}")

        # Category breakdown
        from collections import Counter
        categories = Counter(r.get('read_count_category', 'unknown') for r in all_reads)
        print(f"\n  Categories:")
        for cat, count in categories.most_common():
            print(f"    • {cat}: {count:,}")

    # Export if requested
    if args.export and all_reads:
        sorted_reads = sorted(
            all_reads,
            key=lambda x: x.get('reads_read_count', 0),
            reverse=True
        )
        export_data = {
            'query': 'high_count_reads',
            'min_reads': args.min_reads,
            'total_reads': len(all_reads),
            'results': sorted_reads[:args.limit]
        }
        export_path = Path(args.export)
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        print(f"\n💾 Results exported to: {export_path}")

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

  # Find samples by depth range
  enigma_query.py samples --depth-min 10

  # Find samples from specific location
  enigma_query.py samples --location EU --limit 20

  # Find samples with high read counts
  enigma_query.py samples-with-reads --min-reads 100000

  # Run arbitrary SQL query
  enigma_query.py sql "SELECT sample_location, COUNT(*) FROM Sample GROUP BY 1"

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

    # samples command
    parser_samples = subparsers.add_parser(
        'samples',
        help='Find samples by criteria (depth, date, location)'
    )
    parser_samples.add_argument(
        '--depth-min',
        type=float,
        metavar='METERS',
        help='Minimum depth in meters'
    )
    parser_samples.add_argument(
        '--depth-max',
        type=float,
        metavar='METERS',
        help='Maximum depth in meters'
    )
    parser_samples.add_argument(
        '--date',
        metavar='YYYY-MM-DD',
        help='Sample date (exact match)'
    )
    parser_samples.add_argument(
        '--location',
        metavar='PATTERN',
        help='Location name pattern (substring match)'
    )
    parser_samples.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Maximum number of results (default: 100)'
    )
    parser_samples.add_argument(
        '--export',
        metavar='FILE',
        help='Export results to JSON file'
    )

    # samples-with-reads command (actually finds high-count reads)
    parser_swr = subparsers.add_parser(
        'samples-with-reads',
        help='Find reads meeting count threshold (high-quality reads)'
    )
    parser_swr.add_argument(
        '--min-reads',
        type=int,
        default=50000,
        help='Minimum read count threshold (default: 50000)'
    )
    parser_swr.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Maximum number of results (default: 100)'
    )
    parser_swr.add_argument(
        '--export',
        metavar='FILE',
        help='Export results to JSON file'
    )

    # sql command - run arbitrary SQL
    parser_sql = subparsers.add_parser(
        'sql',
        help='Execute arbitrary SQL query'
    )
    parser_sql.add_argument(
        'sql',
        help='SQL query to execute'
    )
    parser_sql.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Maximum number of rows to display (default: 100)'
    )
    parser_sql.add_argument(
        '--export',
        metavar='FILE',
        help='Export results to JSON file'
    )

    # unused-reads-sql command - faster SQL version
    parser_unused_sql = subparsers.add_parser(
        'unused-reads-sql',
        help='Find unused good reads using pure SQL (faster)'
    )
    parser_unused_sql.add_argument(
        '--min-count',
        type=int,
        default=10000,
        help='Minimum read count threshold (default: 10000)'
    )
    parser_unused_sql.add_argument(
        '--limit',
        type=int,
        default=20,
        help='Maximum results to show (default: 20)'
    )
    parser_unused_sql.add_argument(
        '--read-type',
        metavar='TYPE',
        help='Filter by read type (e.g., ME:0000114 for Single End)'
    )
    parser_unused_sql.add_argument(
        '--exclude-16s',
        action='store_true',
        help='Exclude 16S/metagenome data (keep only Single End isolate genome reads ME:0000114)'
    )
    parser_unused_sql.add_argument(
        '--export',
        metavar='FILE',
        help='Export all results to JSON file'
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
        'unused-reads-sql': cmd_unused_reads_sql,
        'stats': cmd_stats,
        'lineage': cmd_lineage,
        'find': cmd_find,
        'samples': cmd_samples,
        'samples-with-reads': cmd_samples_with_reads,
        'sql': cmd_sql,
    }

    return commands[args.command](query, args)


if __name__ == "__main__":
    sys.exit(main())
