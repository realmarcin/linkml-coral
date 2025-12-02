# LinkML-Store Database Usage Guide

## Overview

This guide explains how to use the linkml-store database system for querying ENIGMA genomic data. The system provides efficient querying capabilities for provenance tracking, resource utilization analysis, and complex relationship queries.

## Quick Start

### 1. Load Data

Load the validated ENIGMA TSV files into a linkml-store database:

```bash
# Using justfile (recommended)
just load-store

# Or directly with custom path
uv run python load_tsv_to_store.py /path/to/tsv/files --db enigma_data.db --create-indexes
```

This creates a **DuckDB database** file (`enigma_data.db`) with all ENIGMA data loaded and indexed.

### 2. Run Queries

```bash
# Answer: "How many good reads were NOT used in assemblies?"
just query-unused-reads 50000  # min 50K reads

# Show database statistics
just query-stats

# Trace provenance lineage
just query-lineage Assembly Assembly0000001

# Find entities
just query-find Reads --query read_count_category=high
```

## Main Query: Unused "Good" Reads

### The Question

**"How many 'good' reads and contigs (with significant number of raw reads) were NOT used in an assembly?"**

### The Answer

```bash
# Find unused reads with >= 50,000 raw reads
uv run python enigma_query.py unused-reads --min-count 50000

# Or using justfile
just query-unused-reads 50000
```

### Example Output

```
🔍 Query: Unused 'Good' Reads
============================================================

Finding reads with >= 50,000 raw reads that were NOT used in assemblies...

  📊 Total 'good' reads (>= 50,000 reads): 14,418
  🔗 Reads used in assemblies: 2,994
  ⚠️  Unused 'good' reads: 11,608

📊 Results:
  • Total 'good' reads: 14,418
  • Used in assemblies: 2,994
  • UNUSED 'good' reads: 11,608
  • Utilization rate: 20.8%

📈 Unused Reads Statistics:
  • Min count: 50,003
  • Max count: 549,479,714
  • Avg count: 3,729,318
  • Total wasted reads: 43,289,920,880

🔬 Top 10 Unused Reads (by count):
  1. FW106-06-10-15-10-deep
      Read count: 549,479,714 (very_high)
      Link: https://narrative.kbase.us/#dataview/26837/FW106-06-10-15-10-deep
  2. FW301-06-10-15-0.2-deep
      Read count: 373,129,474 (very_high)
      Link: https://narrative.kbase.us/#dataview/26837/FW301-06-10-15-0.2-deep
  ...
```

### How It Works

The query:
1. **Finds all "good" reads** - Reads with `read_count >= threshold`
2. **Identifies reads used in assemblies** - By parsing `Process.input_objects` where `output_objects` contains Assembly
3. **Computes set difference** - `unused = all_good_reads - reads_used_in_assemblies`
4. **Reports statistics** - Including counts, utilization rates, and wasted resources

## Available Commands

### Load Data

```bash
# Load all TSV files
just load-store

# Load specific collections only
uv run python load_tsv_to_store.py ../ENIGMA_ASV_export \
  --collections Reads Assembly Process

# Load to custom database location
just load-store /path/to/tsvs /path/to/database.db

# Load with detailed output
uv run python load_tsv_to_store.py ../ENIGMA_ASV_export \
  --db enigma_data.db \
  --create-indexes \
  --show-info \
  --verbose
```

### Query: Unused Reads

```bash
# Basic query (all reads)
just query-unused-reads 50000

# Isolate genome reads only (exclude 16S/metagenome data)
just query-unused-isolates 50000

# Metagenome/16S reads only
just query-unused-metagenomes 50000

# Export results to JSON
uv run python enigma_query.py unused-reads \
  --min-count 50000 \
  --export unused_reads.json

# Export isolate genome candidates
uv run python enigma_query.py unused-reads \
  --min-count 50000 \
  --exclude-16s \
  --export isolate_genomes.json

# Specific read type filter (ME:0000114, ME:0000113, ME:0000112)
uv run python enigma_query.py unused-reads \
  --min-count 50000 \
  --read-type ME:0000114 \
  --export single_end_reads.json

# Show more/fewer results
uv run python enigma_query.py unused-reads \
  --min-count 10000 \
  --top-n 50
```

**Read Type Classification:**
- `ME:0000114` - Single End Read (isolate genome sequencing)
- `ME:0000113` - Paired End Read (metagenome/16S sequencing)
- `ME:0000112` - Generic Read Type (metatranscriptome sequencing)

### Query: Database Statistics

```bash
# Show comprehensive statistics
just query-stats

# Output includes:
# - Total records per collection
# - Read count distributions
# - Process statistics
# - Utilization rates
```

### Query: Provenance Lineage

```bash
# Trace lineage for an assembly
just query-lineage Assembly Assembly0000001

# Export lineage to JSON
uv run python enigma_query.py lineage Assembly Assembly0000001 \
  --export assembly_lineage.json

# Outputs:
# - Process chain length
# - Input reads used
# - Input samples
# - Full provenance tree
```

### Query: Find Entities

```bash
# Find reads with high read counts
just query-find Reads --query read_count_category=high

# Find assemblies by strain
uv run python enigma_query.py find Assembly \
  --query assembly_strain=FW305-37 \
  --limit 10

# Export results
uv run python enigma_query.py find Reads \
  --query read_count_category=very_high \
  --export high_count_reads.json
```

## Database Structure

### Collections

The database contains the following collections (tables):

- **Reads** - Sequencing reads with read counts
- **Assembly** - Genome assemblies with contig counts
- **Process** - Provenance tracking records
- **Sample** - Sample metadata
- **Location** - Geographic locations
- **Strain** - Bacterial strains
- **Genome** - Genome sequences
- **Community** - Microbial communities
- **Protocol** - Experimental protocols

### Computed Fields

Additional fields added during loading for easier querying:

**Reads**:
- `read_count_category`: 'low', 'medium', 'high', 'very_high'
  - very_high: >= 100,000 reads
  - high: >= 50,000 reads
  - medium: >= 10,000 reads
  - low: < 10,000 reads

**Assembly**:
- `contig_count_category`: 'low', 'medium', 'high'
  - high: >= 1,000 contigs
  - medium: >= 100 contigs
  - low: < 100 contigs

**Process** (provenance):
- `process_input_objects_parsed`: Parsed array of input entities
- `process_output_objects_parsed`: Parsed array of output entities
- `input_entity_types`: List of input entity types (e.g., ['Reads', 'Sample'])
- `output_entity_types`: List of output entity types (e.g., ['Assembly'])
- `input_entity_ids`: List of input entity IDs
- `output_entity_ids`: List of output entity IDs

## Python API Usage

For programmatic access:

```python
from query_enigma_provenance import ENIGMAProvenanceQuery

# Initialize
query = ENIGMAProvenanceQuery("enigma_data.db")

# Get unused reads
unused_reads, summary = query.get_unused_reads(min_count=50000)
print(f"Unused: {summary['unused_good_reads']}")
print(f"Utilization: {summary['utilization_rate']:.1%}")

# Get assembly lineage
lineage = query.get_assembly_lineage("Assembly0000001")
print(f"Input reads: {len(lineage['input_reads'])}")

# Get all reads by category
high_count_reads = query.get_all_reads(category='very_high')
print(f"Very high count reads: {len(high_count_reads)}")

# Get summary statistics
summary = query.get_reads_summary()
print(f"Total reads: {summary['total']}")
print(f"Avg count: {summary['avg_count']:,.0f}")
```

## Performance

### Database Size

- Database file: 10-13 MB (compressed DuckDB format)
- Total records: 281,813 across all collections
- Reads: 19,307 records
- Assemblies: 3,427 records
- Processes: 130,560 records
- OTU: 111,830 records
- Other entities: ~16,000 records

### Query Performance

- Simple queries (by ID): < 100ms
- Unused reads analysis: 2-5 seconds (full scan of 19K reads + 130K processes)
- Full lineage trace: < 500ms
- Complex provenance queries: 2-10 seconds
- Database statistics: 1-2 seconds

### Optimization

The loader creates indexes on:
- Primary identifiers (IDs, names)
- Foreign keys
- Computed fields (categories)
- Provenance entity types

## Troubleshooting

### Database Not Found

```
❌ Error: Database not found: enigma_data.db
💡 Tip: Create the database first with:
   just load-store
```

**Solution**: Load the data first using `just load-store`

### Import Error

```
ModuleNotFoundError: No module named 'linkml_store'
```

**Solution**: Ensure linkml-store is installed:
```bash
uv sync  # Install all dependencies
```

### Empty Results

If queries return no results:
1. Check database was loaded successfully: `just query-stats`
2. Verify collection names are correct (case-sensitive)
3. Try broader query parameters

### Performance Issues

If queries are slow:
1. Ensure indexes were created: Use `--create-indexes` flag
2. Check database size: `ls -lh enigma_data.db`
3. Reduce result limits for large queries

## Advanced Usage

### Custom Queries

```python
from query_enigma_provenance import ENIGMAProvenanceQuery

query = ENIGMAProvenanceQuery("enigma_data.db")

# Get collection directly
reads_collection = query.get_collection("Reads")

# Custom query
results = reads_collection.find({
    'read_count_category': 'very_high'
})

# Process results
for read in results:
    print(f"{read['reads_name']}: {read['reads_read_count']:,}")
```

### Bulk Export

```bash
# Export all unused reads
uv run python enigma_query.py unused-reads \
  --min-count 10000 \
  --export unused_reads_10k.json

# Export multiple thresholds
for threshold in 10000 50000 100000; do
  uv run python enigma_query.py unused-reads \
    --min-count $threshold \
    --export unused_reads_${threshold}.json
done
```

### Integration with Analysis Pipelines

```python
import json
from query_enigma_provenance import ENIGMAProvenanceQuery

# Load database
query = ENIGMAProvenanceQuery("enigma_data.db")

# Run analysis
unused, summary = query.get_unused_reads(min_count=50000, return_details=True)

# Export for downstream analysis
with open('unused_reads_analysis.json', 'w') as f:
    json.dump({
        'summary': summary,
        'unused_reads': unused,
        'recommendations': [
            f"Consider using {r['reads_name']}" for r in unused[:5]
        ]
    }, f, indent=2)
```

## See Also

- [QUERY_REFERENCE.md](QUERY_REFERENCE.md) - Complete query command reference
- [REFINED_QUERY_ANALYSIS.md](REFINED_QUERY_ANALYSIS.md) - Refined query analysis for isolate genome reads
- [DEPLOYMENT_PROVENANCE.md](DEPLOYMENT_PROVENANCE.md) - Provenance tracking and deployment guide
- [CLAUDE.md](CLAUDE.md) - Main project documentation
- [LinkML-Store Documentation](https://linkml.io/linkml-store/) - Official linkml-store docs
- [DuckDB Documentation](https://duckdb.org/docs/) - Database backend docs
