# ENIGMA Query Reference

Quick reference for querying the ENIGMA database using linkml-store.

## Prerequisites

1. **Load the data first** (one-time setup):
   ```bash
   just load-store
   ```
   This creates `enigma_data.db` (10-13 MB) with all ENIGMA data.

## Main Query Commands

### 1. Find Unused "Good" Reads

**Question:** *How many reads with significant raw read counts were NOT used in assemblies?*

```bash
# Using justfile (recommended)
just query-unused-reads 50000

# Or directly
uv run python enigma_query.py --db enigma_data.db unused-reads --min-count 50000
```

**Refined Queries for Isolate Genomes:**

```bash
# Isolate genome reads only (exclude 16S/metagenome data)
just query-unused-isolates 50000

# Or directly
uv run python enigma_query.py unused-reads --min-count 50000 --exclude-16s

# Specific read type filter (e.g., Single End reads)
uv run python enigma_query.py unused-reads --min-count 50000 --read-type ME:0000114

# Metagenome/16S reads only
just query-unused-metagenomes 50000

# Or directly
uv run python enigma_query.py unused-reads --min-count 50000 --read-type ME:0000113
```

**Read Type Codes:**
- `ME:0000114` - Single End Read (isolate genome sequencing)
- `ME:0000113` - Paired End Read (metagenome/16S sequencing)
- `ME:0000112` - Generic Read Type (metatranscriptome)

**Output:**
- Summary statistics (total, used, unused, utilization rate)
- Statistics about unused reads (min, max, avg, total wasted)
- Top N unused reads by count (default: 20)

**Export to JSON:**
```bash
# Export all results
uv run python enigma_query.py unused-reads --min-count 50000 --export results.json

# Export isolate genome candidates
uv run python enigma_query.py unused-reads --min-count 50000 --exclude-16s --export isolate_genomes.json

# Export with custom top-N
uv run python enigma_query.py unused-reads --min-count 50000 --top-n 50 --export results.json
```

**JSON Structure:**
```json
{
  "query": "unused_reads",
  "parameters": {
    "min_count": 50000
  },
  "summary": {
    "min_count_threshold": 50000,
    "total_good_reads": 14418,
    "reads_used_in_assemblies": 2994,
    "unused_good_reads": 11608,
    "utilization_rate": 0.2077,
    "unused_stats": {
      "min_count": 50003,
      "max_count": 549479714,
      "avg_count": 3729317.79,
      "total_wasted_reads": 43289920880
    }
  },
  "results": [
    {
      "reads_id": "Reads0000001",
      "reads_name": "FW511_7_26_13_02.reads",
      "reads_read_count": 76138,
      "reads_read_type": "ME:0000114",
      "reads_sequencing_technology": "ME:0000117",
      "reads_link": "https://narrative.kbase.us/#dataview/...",
      "read_count_category": "high"
    }
    // ... 11,607 more results
  ]
}
```

### 2. Database Statistics

**View comprehensive database statistics:**

```bash
just query-stats

# Or directly
uv run python enigma_query.py stats
```

**Output:**
- Record counts per collection
- Read count distributions
- Process statistics
- Read utilization rates

### 3. Trace Provenance Lineage

**Trace the complete lineage for an entity:**

```bash
# Trace an assembly
just query-lineage Assembly Assembly0000001

# Trace a genome
just query-lineage Genome Genome0000001

# Or directly
uv run python enigma_query.py lineage Assembly Assembly0000001
```

**Output:**
- Process chain length
- Input reads used
- Input samples
- Full provenance tree

**Export to JSON:**
```bash
uv run python enigma_query.py lineage Assembly Assembly0000001 --export assembly_lineage.json
```

### 4. Find Entities by Criteria

**Search for entities using key=value filters:**

```bash
# Find high-count reads
just query-find Reads --query read_count_category=high

# Find assemblies by strain
uv run python enigma_query.py find Assembly --query assembly_strain=FW305-37 --limit 10

# Multiple criteria
uv run python enigma_query.py find Reads --query read_count_category=very_high --limit 50
```

**Export results:**
```bash
uv run python enigma_query.py find Reads --query read_count_category=very_high --export high_reads.json
```

## Common Workflows

### Compare Read Types

```bash
# Compare utilization across different read types
echo "=== All Reads ==="
just query-unused-reads 50000

echo "=== Isolate Genome Reads Only ==="
just query-unused-isolates 50000

echo "=== Metagenome/16S Reads Only ==="
just query-unused-metagenomes 50000

# Or use the comparison script
./read_type_comparison.sh
```

**Results at 50K threshold:**
- All reads: 14,418 total, 11,608 unused (79.2%)
- Isolate genomes: 1,840 total, 1,836 unused (99.8%!)
- Metagenomes: 9,640 total, 7,768 unused (80.6%)

### Compare Different Thresholds

```bash
# Compare utilization at different read count thresholds
for threshold in 10000 50000 100000 500000; do
  echo "=== Threshold: $threshold ==="
  uv run python enigma_query.py unused-reads --min-count $threshold --export unused_${threshold}.json
done

# For isolate genomes specifically
for threshold in 50000 100000 200000; do
  echo "=== Isolate Genomes, Threshold: $threshold ==="
  uv run python enigma_query.py unused-reads --min-count $threshold --exclude-16s --export isolates_unused_${threshold}.json
done
```

### Batch Export Multiple Queries

```bash
# Export unused reads at different thresholds
just query-unused-reads 10000 > unused_10k.txt
just query-unused-reads 50000 > unused_50k.txt
just query-unused-reads 100000 > unused_100k.txt

# Export by read type
just query-unused-isolates 50000 > unused_isolates_50k.txt
just query-unused-metagenomes 50000 > unused_metagenomes_50k.txt

# Export with JSON
uv run python enigma_query.py unused-reads --min-count 10000 --export unused_10k.json
uv run python enigma_query.py unused-reads --min-count 50000 --exclude-16s --export isolates_50k.json
uv run python enigma_query.py unused-reads --min-count 50000 --read-type ME:0000113 --export metagenomes_50k.json
```

### Generate Summary Report

```bash
# Create comprehensive analysis report
{
  echo "# ENIGMA Data Analysis Report"
  echo "Generated: $(date)"
  echo ""
  echo "## Database Statistics"
  uv run python enigma_query.py stats
  echo ""
  echo "## Unused Reads Analysis (50K+ threshold)"
  uv run python enigma_query.py unused-reads --min-count 50000
} > enigma_analysis_report.txt
```

## Python API Usage

For programmatic access in scripts or notebooks:

```python
from query_enigma_provenance import ENIGMAProvenanceQuery

# Initialize
query = ENIGMAProvenanceQuery("enigma_data.db")

# Get unused reads with details (all reads)
unused_reads, summary = query.get_unused_reads(min_count=50000, return_details=True)

print(f"Unused reads: {summary['unused_good_reads']}")
print(f"Utilization rate: {summary['utilization_rate']:.1%}")
print(f"Total wasted reads: {summary['unused_stats']['total_wasted_reads']:,}")

# Get unused isolate genome reads only
isolate_reads, isolate_summary = query.get_unused_reads(
    min_count=50000,
    return_details=True,
    exclude_16s=True  # Filter to Single End reads only
)

print(f"Unused isolate genomes: {isolate_summary['unused_good_reads']}")
print(f"Average read count: {isolate_summary['unused_stats']['avg_count']:,.0f}")

# Get unused reads by specific type
metagenome_reads, meta_summary = query.get_unused_reads(
    min_count=50000,
    return_details=True,
    read_type='ME:0000113'  # Paired End reads
)

print(f"Unused metagenomes: {meta_summary['unused_good_reads']}")

# Get assembly lineage
lineage = query.get_assembly_lineage("Assembly0000001")
print(f"Process steps: {lineage['process_count']}")
print(f"Input reads: {len(lineage['input_reads'])}")

# Get all reads by category
high_count_reads = query.get_all_reads(category='very_high')
print(f"Very high count reads: {len(high_count_reads)}")

# Custom queries on collections
reads_collection = query.get_collection("Reads")
for read in reads_collection.find_iter({'read_count_category': 'very_high'}):
    print(f"{read['reads_name']}: {read['reads_read_count']:,}")
```

## Output File Naming Conventions

**Recommended naming:**
- Query results: `{query_type}_{threshold}_{date}.json`
  - Example: `unused_reads_50000_2025-01-14.json`
- Reports: `{analysis_type}_report_{date}.txt`
  - Example: `resource_utilization_report_2025-01-14.txt`
- Lineage exports: `{entity_type}_{entity_id}_lineage.json`
  - Example: `Assembly_Assembly0000001_lineage.json`

## Database Information

**Database file:** `enigma_data.db` (10-13 MB)

**Collections:**
- Reads: 19,307 records
- Assembly: 3,427 records
- Process: 130,560 records (provenance tracking)
- Sample: 4,119 records
- Genome: 6,688 records
- Strain: 3,106 records
- Location: 594 records
- Community: 2,140 records
- Protocol: 42 records
- OTU: 111,830 records

**Total:** 281,813 records

## Performance Notes

- Simple queries (by ID): < 100ms
- Unused reads analysis: 2-5 seconds (full scan of 19K reads + 130K processes)
- Lineage trace: < 500ms
- Database statistics: 1-2 seconds

## Troubleshooting

**Database not found:**
```bash
# Create the database first
just load-store
```

**Query too slow:**
```bash
# Reload database with indexes (if not already done)
rm enigma_data.db
just load-store
```

**Out of memory:**
```bash
# Use lower thresholds or limit result sets
uv run python enigma_query.py unused-reads --min-count 100000  # Higher threshold = fewer results
```

## Provenance Tracking

Every query execution is automatically tracked with complete metadata for reproducibility and auditing.

### What is Tracked

- **Execution**: Unique ID, timestamp, duration, parameters, status
- **User**: Username, hostname, platform
- **Database**: Checksum, size, modification time, record counts
- **Environment**: Python version, package versions
- **Results**: Summary statistics, output files

### View Execution History

```bash
# List all executions
uv run python query_provenance_tracker.py --list

# Generate report for specific execution
uv run python query_provenance_tracker.py --report <execution_id>
```

### Provenance Records

All executions saved in `query_provenance/`:
- `YYYYMMDD_HHMMSS_querytype_execid.json` - Full provenance record
- `latest_querytype.json` - Most recent execution of each type

Each query displays its execution ID:
```
📋 Provenance record saved: query_provenance/20251014_125537_unused_reads_1e16a3d7b455ebce.json
   Execution ID: 1e16a3d7b455ebce
```

### Reproducing Results

```bash
# 1. Find the execution ID from output or history
uv run python query_provenance_tracker.py --list

# 2. Get the provenance record
uv run python query_provenance_tracker.py --report 1e16a3d7b455ebce

# 3. Verify database hasn't changed (check checksum)
# 4. Re-run with same parameters
```

## See Also

- [REFINED_QUERY_ANALYSIS.md](REFINED_QUERY_ANALYSIS.md) - Refined query analysis for isolate genome reads
- [DEPLOYMENT_PROVENANCE.md](DEPLOYMENT_PROVENANCE.md) - Complete deployment & provenance guide
- [LINKML_STORE_USAGE.md](LINKML_STORE_USAGE.md) - Detailed usage guide
- [CLAUDE.md](CLAUDE.md) - Main project documentation
