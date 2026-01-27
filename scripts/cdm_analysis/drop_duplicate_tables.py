#!/usr/bin/env python3
"""
Drop duplicate tables from CDM store database.

This script removes old LinkML class name tables (CamelCase) that were created
before the switch to CDM table naming conventions (sdt_*, sys_*, ddt_*).

Usage:
    python drop_duplicate_tables.py cdm_store.db
    python drop_duplicate_tables.py cdm_store.db --dry-run  # Preview only
"""

import argparse
import sys
from pathlib import Path

try:
    import duckdb
except ImportError:
    print("Error: duckdb not installed. Run: uv pip install duckdb")
    sys.exit(1)


# Duplicate tables to drop (old LinkML class names)
DUPLICATE_TABLES = [
    # Static entities (old names)
    'Location',
    'Sample',
    'Community',
    'Reads',
    'Assembly',
    'Bin',
    'Genome',
    'Gene',
    'Strain',
    'Taxon',
    'ASV',
    'Protocol',
    'Image',
    'Condition',
    'DubSeqLibrary',
    'TnSeqLibrary',
    'ENIGMA',

    # System tables (old names)
    'SystemTypedef',
    'SystemDDTTypedef',
    'SystemOntologyTerm',
    'SystemProcess',
    'SystemProcessInput',
    'SystemProcessOutput',

    # Dynamic data (old names)
    'DynamicDataArray',
]


def get_existing_tables(conn):
    """Get list of all tables in the database."""
    result = conn.execute("SHOW TABLES").fetchall()
    return [row[0] for row in result]


def drop_duplicate_tables(db_path: str, dry_run: bool = False, verbose: bool = False):
    """
    Drop duplicate tables from the database.

    Args:
        db_path: Path to DuckDB database file
        dry_run: If True, only show what would be dropped
        verbose: Print detailed information
    """
    if not Path(db_path).exists():
        print(f"Error: Database not found: {db_path}")
        sys.exit(1)

    print(f"{'='*60}")
    print(f"CDM Store: Drop Duplicate Tables")
    print(f"{'='*60}")
    print(f"Database: {db_path}")
    print(f"Mode: {'DRY RUN (preview only)' if dry_run else 'LIVE (will drop tables)'}")
    print()

    # Connect to database
    conn = duckdb.connect(db_path, read_only=dry_run)

    # Get all existing tables
    existing_tables = get_existing_tables(conn)
    print(f"Total tables in database: {len(existing_tables)}")
    print()

    # Find duplicate tables that exist
    tables_to_drop = [t for t in DUPLICATE_TABLES if t in existing_tables]
    tables_not_found = [t for t in DUPLICATE_TABLES if t not in existing_tables]

    if not tables_to_drop:
        print("✅ No duplicate tables found! Database is already clean.")
        conn.close()
        return 0

    print(f"Found {len(tables_to_drop)} duplicate tables to drop:")
    print()

    # Show what will be dropped with record counts
    for table in sorted(tables_to_drop):
        try:
            count_result = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            count = count_result[0] if count_result else 0
            print(f"  • {table:30s} ({count:,} records)")
        except Exception as e:
            print(f"  • {table:30s} (error counting: {e})")

    if tables_not_found and verbose:
        print()
        print(f"Tables already removed ({len(tables_not_found)}):")
        for table in sorted(tables_not_found):
            print(f"  • {table}")

    print()

    if dry_run:
        print("🔍 DRY RUN: No tables were dropped.")
        print("   Run without --dry-run to actually drop these tables.")
        conn.close()
        return 0

    # Drop tables
    print("Dropping duplicate tables...")
    dropped_count = 0
    failed = []

    for table in tables_to_drop:
        try:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
            dropped_count += 1
            if verbose:
                print(f"  ✓ Dropped {table}")
        except Exception as e:
            failed.append((table, str(e)))
            print(f"  ✗ Failed to drop {table}: {e}")

    print()
    print(f"✅ Dropped {dropped_count} duplicate tables")

    if failed:
        print()
        print(f"⚠️  Failed to drop {len(failed)} tables:")
        for table, error in failed:
            print(f"  • {table}: {error}")

    # Show remaining tables
    remaining_tables = get_existing_tables(conn)
    print()
    print(f"📊 Database now has {len(remaining_tables)} tables")

    if verbose:
        print()
        print("Remaining tables (CDM naming):")
        for table in sorted(remaining_tables):
            try:
                count_result = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
                count = count_result[0] if count_result else 0
                print(f"  • {table:30s} ({count:,} records)")
            except:
                print(f"  • {table:30s}")

    conn.close()
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Drop duplicate tables from CDM store database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview what will be dropped
  python drop_duplicate_tables.py cdm_store.db --dry-run

  # Actually drop duplicate tables
  python drop_duplicate_tables.py cdm_store.db

  # Drop with detailed output
  python drop_duplicate_tables.py cdm_store.db --verbose

This script removes old LinkML class name tables:
  - Location, Sample, Reads, Assembly, etc. → sdt_*
  - SystemProcess, SystemOntologyTerm, etc. → sys_*
  - DynamicDataArray → ddt_brick*
        """
    )

    parser.add_argument(
        'database',
        help='Path to DuckDB database file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be dropped without actually dropping'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed information'
    )

    args = parser.parse_args()

    try:
        return drop_duplicate_tables(args.database, dry_run=args.dry_run, verbose=args.verbose)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
