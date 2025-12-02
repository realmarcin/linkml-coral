#!/usr/bin/env python3
"""
Query ENIGMA provenance data in LinkML-Store.

This library provides functions for querying provenance relationships,
lineage tracking, and resource utilization analysis in the ENIGMA dataset.
"""

from typing import List, Dict, Any, Set, Optional, Tuple
from pathlib import Path
from linkml_store import Client


class ENIGMAProvenanceQuery:
    """Query interface for ENIGMA provenance and lineage data."""

    def __init__(self, db_path: str = "enigma_data.db"):
        """
        Initialize the query interface.

        Args:
            db_path: Path to the DuckDB database file
        """
        self.client = Client()
        self.db = self.client.attach_database(f"duckdb:///{db_path}", alias="enigma")
        self.db_path = db_path

    def get_collection(self, name: str):
        """Get a collection by name."""
        return self.db.get_collection(name)

    # ========================================================================
    # Reads Queries
    # ========================================================================

    def get_all_reads(
        self,
        min_count: Optional[int] = None,
        max_count: Optional[int] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all reads, optionally filtered by read count.

        Args:
            min_count: Minimum read count threshold
            max_count: Maximum read count threshold
            category: Read count category ('low', 'medium', 'high', 'very_high')

        Returns:
            List of read records
        """
        collection = self.get_collection("Reads")

        # Build query
        query = {}
        if category:
            query['read_count_category'] = category

        # Get all matching records (use find_iter to get all rows, not just first 100)
        results = list(collection.find_iter(query))

        # Filter by count if specified (since linkml-store may not support $gte)
        if min_count is not None:
            results = [r for r in results if r.get('reads_read_count', 0) >= min_count]
        if max_count is not None:
            results = [r for r in results if r.get('reads_read_count', 0) <= max_count]

        return results

    def get_reads_summary(self) -> Dict[str, Any]:
        """Get summary statistics for all reads."""
        reads = self.get_all_reads()

        if not reads:
            return {'total': 0, 'categories': {}}

        read_counts = [r.get('reads_read_count', 0) for r in reads if r.get('reads_read_count')]

        categories = {}
        for r in reads:
            cat = r.get('read_count_category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1

        return {
            'total': len(reads),
            'with_counts': len(read_counts),
            'min_count': min(read_counts) if read_counts else 0,
            'max_count': max(read_counts) if read_counts else 0,
            'avg_count': sum(read_counts) / len(read_counts) if read_counts else 0,
            'categories': categories
        }

    # ========================================================================
    # Assembly Queries
    # ========================================================================

    def get_all_assemblies(self) -> List[Dict[str, Any]]:
        """Get all assembly records."""
        collection = self.get_collection("Assembly")
        return list(collection.find_iter({}))

    def get_assemblies_by_strain(self, strain_name: str) -> List[Dict[str, Any]]:
        """Get all assemblies for a specific strain."""
        collection = self.get_collection("Assembly")
        return list(collection.find_iter({'assembly_strain': strain_name}))

    # ========================================================================
    # Process and Provenance Queries
    # ========================================================================

    def get_all_processes(
        self,
        input_type: Optional[str] = None,
        output_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get process records, optionally filtered by input/output entity types.

        Args:
            input_type: Filter by input entity type (e.g., 'Reads', 'Sample')
            output_type: Filter by output entity type (e.g., 'Assembly', 'Genome')

        Returns:
            List of process records
        """
        collection = self.get_collection("Process")

        # Build query
        query = {}
        # Note: linkml-store may not support array contains, so we filter after retrieval
        results = list(collection.find_iter(query))

        # Apply filters
        if input_type:
            results = [p for p in results
                      if input_type in p.get('input_entity_types', [])]
        if output_type:
            results = [p for p in results
                      if output_type in p.get('output_entity_types', [])]

        return results

    def get_reads_to_assembly_processes(self) -> List[Dict[str, Any]]:
        """
        Get all processes that take Reads as input and produce Assembly as output.

        Returns:
            List of process records
        """
        return self.get_all_processes(input_type='Reads', output_type='Assembly')

    def extract_entity_ids(self, process_records: List[Dict], field: str, entity_type: str) -> Set[str]:
        """
        Extract entity IDs from process input or output fields.

        Args:
            process_records: List of process records
            field: 'input' or 'output'
            entity_type: Type of entity to extract (e.g., 'Reads', 'Assembly')

        Returns:
            Set of entity IDs
        """
        ids = set()
        field_key = f'{field}_entity_ids' if field in ['input', 'output'] else field

        for process in process_records:
            # Get the parsed objects
            if field == 'input':
                objects = process.get('process_input_objects_parsed', [])
            elif field == 'output':
                objects = process.get('process_output_objects_parsed', [])
            else:
                continue

            # Extract IDs for the specified entity type
            for obj in objects:
                if ':' in obj:
                    obj_type, obj_id = obj.split(':', 1)
                    if obj_type == entity_type:
                        ids.add(obj_id)

        return ids

    def get_reads_used_in_assemblies(self) -> Set[str]:
        """
        Get set of Reads IDs that were used to create assemblies.

        Returns:
            Set of reads IDs that were used as input to assembly processes
        """
        # Get all processes that create assemblies
        assembly_processes = self.get_reads_to_assembly_processes()

        # Extract reads IDs from input objects
        reads_ids = self.extract_entity_ids(assembly_processes, 'input', 'Reads')

        return reads_ids

    # ========================================================================
    # The Target Query: Unused "Good" Reads
    # ========================================================================

    def get_unused_reads(
        self,
        min_count: int = 10000,
        return_details: bool = True,
        read_type: Optional[str] = None,
        exclude_16s: bool = False
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Find "good" reads (with significant read counts) that were NOT used in assemblies.

        This is the main query to answer:
        "How many good reads were NOT used in an assembly?"

        Args:
            min_count: Minimum read count to consider a read "good"
            return_details: If True, return full records; if False, just IDs
            read_type: Filter by read type (e.g., 'ME:0000114' for Single End isolate reads)
            exclude_16s: If True, exclude 16S/amplicon data (filters out Paired End and generic types)

        Returns:
            Tuple of (unused_reads_list, summary_stats)
        """
        print(f"🔍 Finding unused reads with min_count >= {min_count}...")
        if read_type:
            print(f"  🔬 Filtering by read type: {read_type}")
        if exclude_16s:
            print(f"  🧬 Excluding 16S/metagenome data (keeping only Single End isolate reads)")

        # Step 1: Get all "good" reads
        all_good_reads = self.get_all_reads(min_count=min_count)

        # Apply read type filters
        if exclude_16s:
            # Keep only Single End reads (ME:0000114) which are isolate genomic data
            all_good_reads = [r for r in all_good_reads
                            if r.get('reads_read_type') == 'ME:0000114']
        elif read_type:
            all_good_reads = [r for r in all_good_reads
                            if r.get('reads_read_type') == read_type]

        all_good_reads_ids = {r['reads_id'] for r in all_good_reads}
        filter_desc = " (isolate genome reads)" if exclude_16s else ""
        print(f"  📊 Total 'good' reads{filter_desc} (>= {min_count} reads): {len(all_good_reads_ids)}")

        # Step 2: Find which reads were used in assemblies
        reads_used_in_assemblies = self.get_reads_used_in_assemblies()
        print(f"  🔗 Reads used in assemblies: {len(reads_used_in_assemblies)}")

        # Step 3: Compute set difference
        unused_reads_ids = all_good_reads_ids - reads_used_in_assemblies
        print(f"  ⚠️  Unused 'good' reads: {len(unused_reads_ids)}")

        # Step 4: Retrieve full records if requested
        if return_details:
            unused_reads = [r for r in all_good_reads if r['reads_id'] in unused_reads_ids]
        else:
            unused_reads = list(unused_reads_ids)

        # Step 5: Generate summary statistics
        summary = {
            'min_count_threshold': min_count,
            'total_good_reads': len(all_good_reads_ids),
            'reads_used_in_assemblies': len(reads_used_in_assemblies),
            'unused_good_reads': len(unused_reads_ids),
            'utilization_rate': len(reads_used_in_assemblies) / len(all_good_reads_ids)
                               if all_good_reads_ids else 0
        }

        if return_details and unused_reads:
            # Add stats about unused reads
            unused_counts = [r.get('reads_read_count', 0) for r in unused_reads]
            summary['unused_stats'] = {
                'min_count': min(unused_counts) if unused_counts else 0,
                'max_count': max(unused_counts) if unused_counts else 0,
                'avg_count': sum(unused_counts) / len(unused_counts) if unused_counts else 0,
                'total_wasted_reads': sum(unused_counts)
            }

        return unused_reads, summary

    # ========================================================================
    # Lineage and Provenance Tracking
    # ========================================================================

    def get_entity_provenance_chain(
        self,
        entity_type: str,
        entity_id: str,
        max_depth: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Trace the complete provenance chain for an entity.

        Args:
            entity_type: Type of entity (e.g., 'Assembly', 'Genome')
            entity_id: ID of the entity
            max_depth: Maximum depth to traverse

        Returns:
            List of process records in the provenance chain
        """
        # Get all processes
        all_processes = list(self.get_collection("Process").find_iter({}))

        # Build forward and backward maps
        output_to_process = {}  # entity -> processes that created it
        input_to_process = {}   # entity -> processes that used it

        for process in all_processes:
            outputs = process.get('process_output_objects_parsed', [])
            inputs = process.get('process_input_objects_parsed', [])

            for obj in outputs:
                if obj not in output_to_process:
                    output_to_process[obj] = []
                output_to_process[obj].append(process)

            for obj in inputs:
                if obj not in input_to_process:
                    input_to_process[obj] = []
                input_to_process[obj].append(process)

        # Trace backward (inputs)
        entity_ref = f"{entity_type}:{entity_id}"
        chain = []
        visited = set()

        def trace_backward(ref, depth=0):
            if depth >= max_depth or ref in visited:
                return
            visited.add(ref)

            # Find processes that created this entity
            creating_processes = output_to_process.get(ref, [])
            for process in creating_processes:
                if process['process_id'] not in [p['process_id'] for p in chain]:
                    chain.append(process)

                    # Recursively trace inputs
                    for input_obj in process.get('process_input_objects_parsed', []):
                        trace_backward(input_obj, depth + 1)

        trace_backward(entity_ref)
        return chain

    def get_assembly_lineage(self, assembly_id: str) -> Dict[str, Any]:
        """
        Get the complete lineage for an assembly (what reads/samples went into it).

        Args:
            assembly_id: Assembly ID

        Returns:
            Dictionary with lineage information
        """
        chain = self.get_entity_provenance_chain('Assembly', assembly_id)

        lineage = {
            'assembly_id': assembly_id,
            'process_chain': chain,
            'input_reads': set(),
            'input_samples': set(),
            'process_count': len(chain)
        }

        for process in chain:
            for obj in process.get('process_input_objects_parsed', []):
                if ':' in obj:
                    obj_type, obj_id = obj.split(':', 1)
                    if obj_type == 'Reads':
                        lineage['input_reads'].add(obj_id)
                    elif obj_type == 'Sample':
                        lineage['input_samples'].add(obj_id)

        lineage['input_reads'] = list(lineage['input_reads'])
        lineage['input_samples'] = list(lineage['input_samples'])

        return lineage

    # ========================================================================
    # Utility Functions
    # ========================================================================

    def print_summary(self):
        """Print a summary of the database contents."""
        print("\n" + "="*60)
        print("📊 ENIGMA Data Summary")
        print("="*60)

        collections_info = {
            'Reads': self.get_reads_summary(),
            'Assembly': {'total': len(self.get_all_assemblies())},
            'Process': {'total': self.get_collection("Process").find({}).num_rows}
        }

        for coll_name, info in collections_info.items():
            print(f"\n{coll_name}:")
            for key, value in info.items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for k, v in value.items():
                        print(f"    {k}: {v}")
                elif isinstance(value, float):
                    print(f"  {key}: {value:.2f}")
                else:
                    print(f"  {key}: {value}")


def main():
    """Demo/test the query interface."""
    import argparse

    parser = argparse.ArgumentParser(description='Query ENIGMA provenance data')
    parser.add_argument('--db', default='enigma_data.db', help='Database file path')
    parser.add_argument('--summary', action='store_true', help='Show database summary')
    parser.add_argument('--unused-reads', type=int, metavar='MIN_COUNT',
                       help='Find unused reads with min count')
    parser.add_argument('--assembly-lineage', metavar='ASSEMBLY_ID',
                       help='Show lineage for an assembly')

    args = parser.parse_args()

    # Check if database exists
    if not Path(args.db).exists():
        print(f"Error: Database not found: {args.db}")
        print(f"Run 'uv run python load_tsv_to_store.py' first to create the database")
        return 1

    # Initialize query interface
    query = ENIGMAProvenanceQuery(args.db)

    if args.summary:
        query.print_summary()

    if args.unused_reads:
        unused, summary = query.get_unused_reads(min_count=args.unused_reads)
        print(f"\n📊 Unused Reads Analysis (min_count >= {args.unused_reads}):")
        for key, value in summary.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            elif isinstance(value, float):
                print(f"  {key}: {value:.1%}" if 'rate' in key else f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")

        if unused:
            print(f"\n  Top 10 unused reads by count:")
            sorted_unused = sorted(unused, key=lambda x: x.get('reads_read_count', 0), reverse=True)
            for r in sorted_unused[:10]:
                print(f"    • {r.get('reads_name', r['reads_id'])}: {r.get('reads_read_count', 0):,} reads")

    if args.assembly_lineage:
        lineage = query.get_assembly_lineage(args.assembly_lineage)
        print(f"\n🔗 Assembly Lineage: {args.assembly_lineage}")
        print(f"  Process steps: {lineage['process_count']}")
        print(f"  Input reads: {len(lineage['input_reads'])}")
        print(f"  Input samples: {len(lineage['input_samples'])}")

        if lineage['input_reads']:
            print(f"\n  Reads used:")
            for read_id in lineage['input_reads'][:10]:
                print(f"    • {read_id}")
            if len(lineage['input_reads']) > 10:
                print(f"    ... and {len(lineage['input_reads']) - 10} more")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
