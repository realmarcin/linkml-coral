#!/usr/bin/env python3
"""
Demonstrate complex queries across multiple tables and brick data.

This script shows how to perform sophisticated queries that join:
- Static entity tables (sdt_*)
- System tables (sys_*)
- Dynamic brick tables (ddt_*)

Example Query: Find samples from a location with their molecular measurements,
sequencing data, ASV taxonomy, and provenance information.
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

from linkml_store import Client


class ComplexCDMQuery:
    """Demonstrate complex queries across CDM tables and bricks."""

    def __init__(self, db_path: str):
        """Initialize query interface."""
        self.db_path = db_path
        self.client = Client()
        self.db = self.client.attach_database(f"duckdb:///{db_path}", alias="cdm")

    def get_collection(self, collection_name: str):
        """Get a collection from the database."""
        try:
            return self.db.get_collection(collection_name)
        except Exception as e:
            raise ValueError(f"Collection '{collection_name}' not found: {e}")

    def _get_rows(self, query_result) -> List[dict]:
        """Get rows from linkml-store query result."""
        if hasattr(query_result, 'rows'):
            return query_result.rows
        elif isinstance(query_result, list):
            return query_result
        else:
            return list(query_result)

    def query_location_to_molecules(self, location_id: str = None, limit: int = 5) -> Dict[str, Any]:
        """
        Complex query: Location → Samples → Molecular Measurements (brick data)

        This query demonstrates:
        1. Static table access (Location, Sample)
        2. Dynamic brick data access (DynamicDataArray)
        3. Ontology term resolution (SystemOntologyTerm)
        4. Multi-table joins

        Args:
            location_id: Location ID to filter (default: use first location)
            limit: Maximum samples to return

        Returns:
            Dict with location info, samples, and their molecular measurements
        """
        print("\n" + "="*70)
        print("🔬 COMPLEX QUERY: Location → Samples → Molecular Measurements")
        print("="*70)

        # Step 1: Get location info
        print(f"\n📍 Step 1: Fetching location data...")
        location_coll = self.get_collection("Location")

        if location_id:
            locations = self._get_rows(location_coll.find({"sdt_location_id": location_id}))
        else:
            # Get first location
            locations = self._get_rows(location_coll.find(limit=1))

        if not locations:
            print(f"  ❌ No location found")
            return {}

        location = locations[0]
        location_id = location.get('sdt_location_id')
        location_name = location.get('sdt_location_name', 'Unknown')

        print(f"  ✅ Location: {location_name} ({location_id})")
        print(f"     Coordinates: {location.get('sdt_location_latitude')}, {location.get('sdt_location_longitude')}")

        # Step 2: Find samples from this location
        print(f"\n🧪 Step 2: Finding samples from location {location_id}...")
        sample_coll = self.get_collection("Sample")

        # Find samples with this location_id
        samples = self._get_rows(sample_coll.find(limit=limit))
        # Filter for matching location (field name might vary)
        samples_at_location = []
        for sample in samples:
            loc_ref = sample.get('sdt_sample_location_id') or sample.get('location_ref')
            if loc_ref == location_id:
                samples_at_location.append(sample)

        if not samples_at_location:
            print(f"  ⚠️  No samples found at this location")
            # Still show some samples for demo
            samples_at_location = samples[:limit]
            print(f"  📊 Showing {len(samples_at_location)} sample(s) from database (any location)")
        else:
            print(f"  ✅ Found {len(samples_at_location)} sample(s)")

        # Step 3: Get molecular measurements from brick data
        print(f"\n💧 Step 3: Fetching molecular measurements (brick data)...")
        dynamic_coll = self.get_collection("DynamicDataArray")

        results = {
            'location': {
                'id': location_id,
                'name': location_name,
                'latitude': location.get('sdt_location_latitude'),
                'longitude': location.get('sdt_location_longitude'),
            },
            'samples': []
        }

        for sample in samples_at_location[:limit]:
            sample_id = sample.get('sdt_sample_id')
            sample_name = sample.get('sdt_sample_name', sample_id)

            print(f"\n  📌 Sample: {sample_name}")

            # Find molecular measurements for this sample in brick data
            # Look for records with sample_name field
            brick_data = self._get_rows(dynamic_coll.find(limit=10))

            # Filter for this sample
            sample_measurements = []
            for record in brick_data:
                rec_sample = record.get('sdt_sample_name')
                if rec_sample == sample_name:
                    sample_measurements.append(record)
                    if len(sample_measurements) >= 3:  # Limit for demo
                        break

            sample_info = {
                'id': sample_id,
                'name': sample_name,
                'material': sample.get('sdt_sample_material'),
                'description': sample.get('sdt_sample_description'),
                'molecular_measurements': []
            }

            if sample_measurements:
                print(f"     ✅ Found {len(sample_measurements)} molecular measurement(s)")
                for i, measurement in enumerate(sample_measurements[:3], 1):
                    # Extract measurement info
                    mol_name = measurement.get('molecule_from_list_sys_oterm_name', 'Unknown')
                    mol_weight = measurement.get('molecule_molecular_weight_dalton')

                    meas_info = {
                        'molecule': mol_name,
                        'molecular_weight': mol_weight,
                    }

                    # Add any numeric measurements found
                    for key, value in measurement.items():
                        if isinstance(value, (int, float)) and 'molecule' not in key.lower():
                            meas_info[key] = value

                    sample_info['molecular_measurements'].append(meas_info)
                    print(f"        {i}. {mol_name} (MW: {mol_weight})")
            else:
                print(f"     ⚠️  No molecular measurements in brick data")

            results['samples'].append(sample_info)

        return results

    def query_sample_to_genome_pipeline(self, sample_id: str = None) -> Dict[str, Any]:
        """
        Complex query: Sample → Reads → Assembly → Genome → Genes

        This demonstrates the complete sequencing pipeline with provenance:
        1. Sample collection
        2. Sequencing (Reads with quality metrics)
        3. Assembly
        4. Binning → Genome
        5. Gene calling
        6. Provenance tracking through SystemProcess

        Args:
            sample_id: Sample ID to trace (default: use first sample)

        Returns:
            Dict with complete pipeline information
        """
        print("\n" + "="*70)
        print("🧬 COMPLEX QUERY: Sample → Reads → Assembly → Genome → Genes")
        print("="*70)

        # Step 1: Get sample
        print(f"\n🧪 Step 1: Fetching sample data...")
        sample_coll = self.get_collection("Sample")

        if sample_id:
            samples = self._get_rows(sample_coll.find({"sdt_sample_id": sample_id}))
        else:
            samples = self._get_rows(sample_coll.find(limit=1))

        if not samples:
            print(f"  ❌ No sample found")
            return {}

        sample = samples[0]
        sample_id = sample.get('sdt_sample_id')
        sample_name = sample.get('sdt_sample_name', sample_id)

        print(f"  ✅ Sample: {sample_name}")
        print(f"     Material: {sample.get('sdt_sample_material')}")

        results = {
            'sample': {
                'id': sample_id,
                'name': sample_name,
                'material': sample.get('sdt_sample_material'),
            },
            'pipeline': {
                'reads': [],
                'assemblies': [],
                'genomes': [],
                'genes': []
            }
        }

        # Step 2: Find Reads from this sample
        print(f"\n📖 Step 2: Finding sequencing reads...")
        reads_coll = self.get_collection("Reads")

        # Find reads with this sample_id
        all_reads = self._get_rows(reads_coll.find(limit=100))
        sample_reads = []
        for read in all_reads:
            read_sample = read.get('sdt_reads_sample_id') or read.get('sample_ref')
            if read_sample == sample_id:
                sample_reads.append(read)

        if sample_reads:
            print(f"  ✅ Found {len(sample_reads)} read dataset(s)")
            for i, read in enumerate(sample_reads[:3], 1):
                read_count = read.get('sdt_reads_read_count')
                read_info = {
                    'id': read.get('sdt_reads_id'),
                    'read_count': read_count,
                    'read_count_category': read.get('read_count_category', 'unknown'),
                }
                results['pipeline']['reads'].append(read_info)
                count_str = f"{read_count:,}" if read_count is not None else "N/A"
                print(f"     {i}. {read_info['id']}: {count_str} reads ({read_info['read_count_category']})")
        else:
            print(f"  ⚠️  No reads found for this sample")

        # Step 3: Find Assemblies (via provenance)
        print(f"\n🧩 Step 3: Finding assemblies...")
        assembly_coll = self.get_collection("Assembly")
        process_coll = self.get_collection("SystemProcess")

        # Find processes that used these reads
        read_ids = [r.get('sdt_reads_id') for r in sample_reads if r.get('sdt_reads_id')]
        assemblies = []

        if read_ids:
            # Find assembly processes
            all_processes = self._get_rows(process_coll.find(limit=1000))
            for proc in all_processes:
                input_ids = proc.get('input_entity_ids', [])
                # Check if any of our read IDs are in inputs
                if input_ids and any(rid and rid in str(input_ids) for rid in read_ids if rid):
                    # Check outputs for assemblies
                    output_types = proc.get('output_entity_types', [])
                    if 'Assembly' in output_types:
                        output_ids = proc.get('output_entity_ids', [])
                        for out_id in output_ids:
                            # Get assembly details
                            asm_list = self._get_rows(assembly_coll.find({"sdt_assembly_id": out_id}, limit=1))
                            if asm_list:
                                assemblies.append(asm_list[0])

        if assemblies:
            print(f"  ✅ Found {len(assemblies)} assembl(y/ies)")
            for i, assembly in enumerate(assemblies[:3], 1):
                asm_info = {
                    'id': assembly.get('sdt_assembly_id'),
                    'n_contigs': assembly.get('sdt_assembly_n_contigs'),
                    'contig_category': assembly.get('contig_count_category', 'unknown'),
                }
                results['pipeline']['assemblies'].append(asm_info)
                print(f"     {i}. {asm_info['id']}: {asm_info['n_contigs']} contigs ({asm_info['contig_category']})")
        else:
            print(f"  ⚠️  No assemblies found")

        # Step 4: Find Genomes
        print(f"\n🦠 Step 4: Finding genomes...")
        genome_coll = self.get_collection("Genome")
        bin_coll = self.get_collection("Bin")

        # Find bins from assemblies
        assembly_ids = [a.get('sdt_assembly_id') for a in assemblies]
        bins = []

        if assembly_ids:
            all_bins = self._get_rows(bin_coll.find(limit=100))
            for bin_rec in all_bins:
                bin_asm = bin_rec.get('sdt_bin_assembly_id')
                if bin_asm in assembly_ids:
                    bins.append(bin_rec)

        # Find genomes from bins
        genomes = []
        if bins:
            bin_ids = [b.get('sdt_bin_id') for b in bins]
            all_genomes = self._get_rows(genome_coll.find(limit=100))
            for genome in all_genomes:
                genome_bin = genome.get('sdt_genome_bin_id')
                if genome_bin in bin_ids:
                    genomes.append(genome)

        if genomes:
            print(f"  ✅ Found {len(genomes)} genome(s)")
            for i, genome in enumerate(genomes[:3], 1):
                genome_info = {
                    'id': genome.get('sdt_genome_id'),
                    'name': genome.get('sdt_genome_name'),
                }
                results['pipeline']['genomes'].append(genome_info)
                print(f"     {i}. {genome_info['name']} ({genome_info['id']})")
        else:
            print(f"  ⚠️  No genomes found")

        # Step 5: Find Genes
        print(f"\n🧬 Step 5: Finding genes...")
        gene_coll = self.get_collection("Gene")

        # Find genes from genomes
        genes = []
        if genomes:
            genome_ids = [g.get('sdt_genome_id') for g in genomes]
            all_genes = self._get_rows(gene_coll.find(limit=100))
            for gene in all_genes:
                gene_genome = gene.get('sdt_gene_genome_id')
                if gene_genome in genome_ids:
                    genes.append(gene)

        if genes:
            print(f"  ✅ Found {len(genes)} gene(s)")
            for i, gene in enumerate(genes[:5], 1):
                gene_info = {
                    'id': gene.get('sdt_gene_id'),
                    'name': gene.get('sdt_gene_name'),
                }
                results['pipeline']['genes'].append(gene_info)
                print(f"     {i}. {gene_info['name']} ({gene_info['id']})")
        else:
            print(f"  ⚠️  No genes found")

        return results

    def query_asv_taxonomy_with_measurements(self, limit: int = 5) -> Dict[str, Any]:
        """
        Complex query: ASV → Taxonomy (brick) + Community abundance (brick)

        This demonstrates:
        1. Static ASV table
        2. Dynamic taxonomic classification data (brick)
        3. Dynamic abundance data (brick)
        4. Ontology term resolution

        Args:
            limit: Maximum ASVs to return

        Returns:
            Dict with ASV info, taxonomy, and abundance data
        """
        print("\n" + "="*70)
        print("🦠 COMPLEX QUERY: ASV → Taxonomy + Community Abundance")
        print("="*70)

        # Step 1: Get ASVs
        print(f"\n📊 Step 1: Fetching ASV data...")
        asv_coll = self.get_collection("ASV")
        asvs = self._get_rows(asv_coll.find(limit=limit))

        print(f"  ✅ Found {len(asvs)} ASV(s)")

        results = {
            'asvs': []
        }

        # Step 2: Get taxonomy and abundance from brick data
        print(f"\n🔬 Step 2: Fetching taxonomy and abundance (brick data)...")
        dynamic_coll = self.get_collection("DynamicDataArray")

        for i, asv in enumerate(asvs, 1):
            asv_id = asv.get('sdt_asv_id')
            asv_name = asv.get('sdt_asv_name', asv_id)

            print(f"\n  📌 ASV {i}: {asv_name}")

            asv_info = {
                'id': asv_id,
                'name': asv_name,
                'taxonomy': [],
                'abundance': []
            }

            # Find taxonomy records in brick data
            brick_records = self._get_rows(dynamic_coll.find(limit=50))

            taxonomy_recs = []
            abundance_recs = []

            for record in brick_records:
                rec_asv = record.get('sdt_asv_name')
                if rec_asv == asv_name:
                    # Check if it's taxonomy or abundance
                    if 'sdt_taxon_name' in record or 'taxonomic_level_sys_oterm_name' in record:
                        taxonomy_recs.append(record)
                    elif 'count_count_unit' in record or 'sdt_community_name' in record:
                        abundance_recs.append(record)

                if len(taxonomy_recs) >= 3 and len(abundance_recs) >= 3:
                    break

            if taxonomy_recs:
                print(f"     ✅ Found {len(taxonomy_recs)} taxonomic classification(s)")
                for tax in taxonomy_recs[:3]:
                    tax_info = {
                        'level': tax.get('taxonomic_level_sys_oterm_name'),
                        'taxon': tax.get('sdt_taxon_name'),
                        'confidence': tax.get('confidence_confidence_unit')
                    }
                    asv_info['taxonomy'].append(tax_info)
                    print(f"        • {tax_info['level']}: {tax_info['taxon']} (conf: {tax_info['confidence']})")

            if abundance_recs:
                print(f"     ✅ Found {len(abundance_recs)} abundance measurement(s)")
                for abund in abundance_recs[:3]:
                    abund_info = {
                        'community': abund.get('sdt_community_name'),
                        'count': abund.get('count_count_unit')
                    }
                    asv_info['abundance'].append(abund_info)
                    print(f"        • Community: {abund_info['community']}, Count: {abund_info['count']}")

            results['asvs'].append(asv_info)

        return results


def main():
    parser = argparse.ArgumentParser(
        description='Demonstrate complex queries across CDM tables and bricks',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--db',
        default='cdm_store_sample.db',
        help='Path to CDM store database (default: cdm_store_sample.db)'
    )

    parser.add_argument(
        'query',
        choices=['location-molecules', 'pipeline', 'asv-taxonomy', 'all'],
        help='Query to demonstrate'
    )

    parser.add_argument(
        '--location-id',
        help='Location ID for location-molecules query'
    )

    parser.add_argument(
        '--sample-id',
        help='Sample ID for pipeline query'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=5,
        help='Maximum results to return (default: 5)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()

    # Initialize query interface
    if not Path(args.db).exists():
        print(f"Error: Database not found: {args.db}", file=sys.stderr)
        print(f"\nRun: just load-cdm-store-sample", file=sys.stderr)
        sys.exit(1)

    query = ComplexCDMQuery(args.db)

    # Execute query
    results = {}

    if args.query == 'location-molecules' or args.query == 'all':
        results['location_molecules'] = query.query_location_to_molecules(
            location_id=args.location_id,
            limit=args.limit
        )

    if args.query == 'pipeline' or args.query == 'all':
        results['pipeline'] = query.query_sample_to_genome_pipeline(
            sample_id=args.sample_id
        )

    if args.query == 'asv-taxonomy' or args.query == 'all':
        results['asv_taxonomy'] = query.query_asv_taxonomy_with_measurements(
            limit=args.limit
        )

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("\n" + "="*70)
        print("✅ QUERY COMPLETE")
        print("="*70)
        print(f"\nRun with --json flag to see full structured results")


if __name__ == "__main__":
    main()
