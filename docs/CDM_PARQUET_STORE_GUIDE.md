# CDM Parquet → linkml-store Loading Guide

## Overview

This guide explains how to load KBase Common Data Model (CDM) parquet files into a queryable linkml-store DuckDB database for efficient analysis and querying.

**What is CDM?** The KBase Common Data Model is a comprehensive data warehouse containing:
- 44 parquet tables (157 MB total)
- 515K rows across static entities and system tables
- 82.6M additional rows in dynamic brick tables
- Complete ENIGMA genomic and experimental data

**Why linkml-store?** LinkML-Store provides:
- Fast DuckDB-based columnar storage
- Schema validation against LinkML models
- Pythonic query interface
- Easy integration with LinkML ecosystem

## Quick Start

### 1. Load CDM Data (Static + System Tables)

Load the core CDM tables (23 tables, 515K rows):

```bash
# Using default paths
just load-cdm-store

# Or specify paths
just load-cdm-store data/enigma_coral.db output.db
```

This loads:
- **Static entity tables (sdt_*)**: Location, Sample, Reads, Assembly, Genome, Gene, etc. (17 tables, 273K rows)
- **System tables (sys_*)**: Ontology terms, Type definitions, Process records (6 tables, 242K rows)

**Expected output:**
```
📦 Loading CDM parquet data into linkml-store...
📦 Connecting to database: cdm_store.db
📋 Loaded schema: kbase-cdm

============================================================
📦 Loading Static Entity Tables (sdt_*)
============================================================

📥 Loading sdt_location as Location...
  📊 Total rows: 42
  ✅ Loaded 42 records in 0.15s

📥 Loading sdt_sample as Sample...
  📊 Total rows: 4,330
  ✅ Loaded 4,330 records in 0.45s

... (continues for all tables)

📊 Summary: Loaded 515,109 total records across 23 collections
⏱️  Total time: 45.2s (11,399 records/sec)

💾 Database saved to: cdm_store.db
   Size: 48.23 MB
```

### 2. Query the Database

Show database statistics:

```bash
just cdm-store-stats
```

Find samples from a location:

```bash
just cdm-find-samples Location0000001
```

Search ontology terms:

```bash
just cdm-search-oterm "soil"
```

Trace provenance lineage:

```bash
just cdm-lineage Assembly Assembly0000001
```

## Loading Options

### Option 1: Core Tables Only (Default)

**Tables:** Static entities (sdt_*) + System tables (sys_*)
**Size:** ~50 MB database, 515K rows
**Time:** ~1 minute

```bash
just load-cdm-store
```

### Option 2: Include Dynamic Brick Tables (Sampled)

**Tables:** Core + Dynamic bricks (sampled at 10K rows each)
**Size:** ~100 MB database
**Time:** ~2-3 minutes

```bash
just load-cdm-store-full
```

### Option 3: Custom Loading

Use the Python script directly for fine-grained control:

```bash
# Load only static tables
uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py \
    data/enigma_coral.db \
    --output my_cdm.db \
    --include-static \
    --no-system

# Load with custom dynamic brick sampling
uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py \
    data/enigma_coral.db \
    --include-dynamic \
    --max-dynamic-rows 50000

# Verbose output for debugging
uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py \
    data/enigma_coral.db \
    --verbose
```

## CDM Table Structure

### Static Entity Tables (sdt_*)

17 tables representing core scientific entities:

| Table | LinkML Class | Rows | Description |
|-------|--------------|------|-------------|
| `sdt_location` | Location | 42 | Sampling locations with coordinates |
| `sdt_sample` | Sample | 4,330 | Environmental samples |
| `sdt_community` | Community | 2,150 | Microbial communities |
| `sdt_reads` | Reads | 19,307 | Sequencing reads datasets |
| `sdt_assembly` | Assembly | 3,427 | Genome assemblies |
| `sdt_bin` | Bin | 1,234 | Metagenomic bins |
| `sdt_genome` | Genome | 6,688 | Annotated genomes |
| `sdt_gene` | Gene | 15,015 | Annotated genes |
| `sdt_strain` | Strain | 8,901 | Microbial strains |
| `sdt_taxon` | Taxon | 1,234 | Taxonomic classifications |
| `sdt_asv` | ASV | 213,044 | Amplicon sequence variants |
| `sdt_protocol` | Protocol | 42 | Experimental protocols |
| `sdt_image` | Image | 15 | Microscopy images |
| `sdt_condition` | Condition | 234 | Growth conditions |
| `sdt_dubseq_library` | DubSeqLibrary | 12 | DubSeq libraries |
| `sdt_tnseq_library` | TnSeqLibrary | 8 | TnSeq libraries |
| `sdt_enigma` | ENIGMA | 1 | Root entity |

### System Tables (sys_*)

6 tables for metadata and provenance:

| Table | LinkML Class | Rows | Description |
|-------|--------------|------|-------------|
| `sys_typedef` | SystemTypedef | 118 | Type definitions |
| `sys_ddt_typedef` | SystemDDTTypedef | 101 | Dynamic data type defs |
| `sys_oterm` | SystemOntologyTerm | 10,594 | Ontology term catalog |
| `sys_process` | SystemProcess | 142,958 | Provenance records |
| `sys_process_input` | SystemProcessInput | 90,395 | Process inputs (denormalized) |
| `sys_process_output` | SystemProcessOutput | 38,228 | Process outputs (denormalized) |

### Dynamic Data Tables (ddt_*)

21 tables for measurement arrays:

| Table | Rows | Default Strategy |
|-------|------|------------------|
| `ddt_ndarray` | 20 | Full load |
| `ddt_brick*` (20 tables) | 82.6M total | Sampled or skipped |

## CDM Naming Conventions

The CDM uses specific naming patterns different from the original CORAL schema:

### Primary Keys
- Pattern: `sdt_{entity}_id` (e.g., `sdt_sample_id`)
- Example: `Sample0000001`

### Entity Names
- Pattern: `sdt_{entity}_name` (e.g., `sdt_sample_name`)
- Used in foreign key references instead of IDs

### Foreign Keys
- Use `_name` suffix, not `_id`
- Example: `location_ref` references `Location.sdt_location_name`

### Ontology Terms
- Split into ID + name pairs
- Pattern: `{field}_sys_oterm_id` + `{field}_sys_oterm_name`
- Example: `material_sys_oterm_id` + `material_sys_oterm_name`

## Query Interface

### Python API

```python
from scripts.cdm_analysis.query_cdm_store import CDMStoreQuery

# Initialize
query = CDMStoreQuery('cdm_store.db')

# Get statistics
stats = query.stats()
print(f"Total records: {stats['total_records']:,}")

# Find samples by location
samples = query.find_samples_by_location('Location0000001')

# Search ontology terms
terms = query.search_ontology_terms('soil')

# Trace provenance
lineage = query.trace_lineage('Assembly', 'Assembly0000001')
```

### Command Line

```bash
# Show database stats
python scripts/cdm_analysis/query_cdm_store.py --db cdm_store.db stats

# Find samples
python scripts/cdm_analysis/query_cdm_store.py --db cdm_store.db \
    find-samples --location Location0000001

# Search ontology terms
python scripts/cdm_analysis/query_cdm_store.py --db cdm_store.db \
    search-oterm "soil"

# Trace lineage
python scripts/cdm_analysis/query_cdm_store.py --db cdm_store.db \
    lineage Assembly Assembly0000001

# Export results to JSON
python scripts/cdm_analysis/query_cdm_store.py --db cdm_store.db \
    stats --export stats.json
```

### Justfile Commands

```bash
# Statistics
just cdm-store-stats

# Find samples
just cdm-find-samples Location0000001

# Search ontology terms
just cdm-search-oterm "soil"

# Trace lineage
just cdm-lineage Assembly Assembly0000001
```

## Common Queries

### 1. Get All Samples from a Location

```python
query = CDMStoreQuery('cdm_store.db')
samples = query.find_samples_by_location('Location0000001')

for sample in samples:
    print(f"Sample: {sample['sdt_sample_name']}")
    print(f"  Depth: {sample.get('depth')}m")
    print(f"  Date: {sample.get('date')}")
```

### 2. Search Ontology Terms

```python
# Find all soil-related terms
terms = query.search_ontology_terms('soil', limit=50)

for term in terms:
    print(f"{term['sys_oterm_id']}: {term['sys_oterm_name']}")
```

### 3. Trace Assembly Provenance

```python
lineage = query.trace_lineage('Assembly', 'Assembly0000001')

# What reads were used to create this assembly?
for process in lineage['upstream']:
    print(f"Process: {process['process_type']}")
    for input_ref in process['inputs']:
        print(f"  Input: {input_ref}")
```

### 4. Get Database Statistics

```python
stats = query.stats()

print(f"Database: {stats['database']}")
print(f"Collections: {stats['total_collections']}")
print(f"Total records: {stats['total_records']:,}")

for coll_name, count in stats['collections'].items():
    print(f"  {coll_name}: {count:,}")
```

## Performance Considerations

### Loading Time

| Dataset | Tables | Rows | Size | Time |
|---------|--------|------|------|------|
| Static + System | 23 | 515K | 50 MB | ~1 min |
| + Dynamic (sampled) | 28 | ~615K | 100 MB | ~2-3 min |

### Query Performance

- **Small tables** (<10K rows): Instantaneous
- **Medium tables** (10-100K rows): <1 second
- **Large tables** (>100K rows): 1-5 seconds
- **Full table scans**: May require optimization

### Optimization Tips

1. **Use indexes** (created automatically with `--create-indexes`)
2. **Limit result sets** (use `limit` parameters)
3. **Filter early** (query by ID/name when possible)
4. **Export large results** (use JSON export for downstream processing)

## Data Quality Notes

### Known Issues

1. **NULL Values in Required Fields**
   - Some CDM tables have NULL values in fields marked as required
   - Example: `sdt_enigma.sdt_enigma_id` may be NULL
   - Loader handles these gracefully (converts pandas NaN → None)

2. **Foreign Key References**
   - CDM uses `_name` fields for foreign keys, not `_id`
   - Example: `Sample.location_ref` → `Location.sdt_location_name`
   - Ensure proper join queries

3. **Ontology Term Splitting**
   - Single fields in original CORAL split into ID + name
   - Example: `material` → `material_sys_oterm_id` + `material_sys_oterm_name`
   - Both fields preserved in linkml-store

### Validation

Validate parquet data before loading:

```bash
# Validate single table
just validate-cdm-parquet /path/to/sdt_sample Sample

# Validate all tables (sample mode)
just validate-all-cdm-parquet

# Full validation with detailed report
just validate-cdm-full
```

## Troubleshooting

### "Database not found"

```bash
# Create database first
just load-cdm-store
```

### "Collection not found"

Check collection names:

```bash
just cdm-store-stats
```

Common collection names:
- Static entities: `Location`, `Sample`, `Reads`, `Assembly`, `Genome`
- System tables: `SystemOntologyTerm`, `SystemProcess`, `SystemTypedef`

### "Error reading parquet"

Verify CDM database path:

```bash
ls -lh data/enigma_coral.db/
```

Check for Delta Lake format (directories with `_delta_log/`):

```bash
ls -la data/enigma_coral.db/sdt_sample/
```

### Memory Issues

For very large queries, use sampling or export:

```python
# Sample large tables during load
python scripts/cdm_analysis/load_cdm_parquet_to_store.py \
    data/enigma_coral.db \
    --max-dynamic-rows 5000

# Or query in chunks
collection = db.get_collection("ASV")
results = list(collection.find(limit=1000))
```

## Integration with CDM Analysis Tools

### CDM Schema

The loader uses the CDM LinkML schema:

```
src/linkml_coral/schema/cdm/linkml_coral_cdm.yaml
├── cdm_base.yaml          # Base types and mixins
├── cdm_static_entities.yaml    # 17 entity classes
├── cdm_system_tables.yaml      # 6 system classes
└── cdm_dynamic_data.yaml       # Brick infrastructure
```

### CDM Analysis Scripts

Related tools:

```bash
# Analyze parquet structure
just analyze-cdm

# Generate schema reports
just cdm-report

# Validate parquet data
just validate-all-cdm-parquet

# Full validation with error report
just validate-cdm-full
```

### Comparison with TSV Loader

| Aspect | TSV Loader | CDM Parquet Loader |
|--------|------------|-------------------|
| **Input** | 10 TSV files | 44 parquet tables |
| **Schema** | `linkml_coral.yaml` | `linkml_coral_cdm.yaml` |
| **Tables** | 10 collections | 23-44 collections |
| **Rows** | 280K | 515K (static+system) |
| **Size** | ~10 MB | ~50 MB |
| **Ontology** | Single fields | Split ID+name fields |
| **Foreign Keys** | Use IDs | Use names |

## Advanced Usage

### Custom Computed Fields

The loader adds computed fields automatically:

```python
# Reads: read_count_category
#   - 'very_high': >= 100K reads
#   - 'high': >= 50K reads
#   - 'medium': >= 10K reads
#   - 'low': < 10K reads

# Assembly: contig_count_category
#   - 'high': >= 1000 contigs
#   - 'medium': >= 100 contigs
#   - 'low': < 100 contigs
```

Query by computed fields:

```python
collection = db.get_collection("Reads")
high_quality = list(collection.find({'read_count_category': 'very_high'}))
```

### Provenance Parsing

SystemProcess records have parsed provenance arrays:

```python
collection = db.get_collection("SystemProcess")
processes = list(collection.find(limit=10))

for proc in processes:
    # Original arrays
    print(f"Inputs: {proc['sys_process_input_objects']}")
    print(f"Outputs: {proc['sys_process_output_objects']}")

    # Parsed fields (added by loader)
    print(f"Input types: {proc['input_entity_types']}")
    print(f"Input IDs: {proc['input_entity_ids']}")
    print(f"Output types: {proc['output_entity_types']}")
    print(f"Output IDs: {proc['output_entity_ids']}")
```

### Direct linkml-store API

For advanced queries, use linkml-store directly:

```python
from linkml_store import Client

client = Client()
db = client.attach_database("duckdb:///cdm_store.db", alias="cdm")

# Get collection
samples = db.get_collection("Sample")

# Query with filters
results = list(samples.find({'depth': {'$gt': 100}}))

# Complex queries
for result in results:
    print(f"Sample {result['sdt_sample_name']} at {result['depth']}m")
```

## Next Steps

1. **Load the data**: `just load-cdm-store`
2. **Explore collections**: `just cdm-store-stats`
3. **Try queries**: `just cdm-find-samples Location0000001`
4. **Integrate into workflows**: Use Python API in your scripts
5. **Contribute queries**: Add new query types to `query_cdm_store.py`

## Related Documentation

- [CDM Parquet Validation Guide](CDM_PARQUET_VALIDATION_GUIDE.md)
- [CDM Schema Implementation Summary](CDM_SCHEMA_IMPLEMENTATION_SUMMARY.md)
- [CDM Parquet Analysis Report](cdm_analysis/CDM_PARQUET_ANALYSIS_REPORT.md)
- [linkml-store Documentation](https://linkml.io/linkml-store/)
- [LinkML Documentation](https://linkml.io/linkml/)

## Support

For issues or questions:

1. Check validation reports: `just validate-cdm-full`
2. Review CDM analysis: `just analyze-cdm`
3. Examine schema: `src/linkml_coral/schema/cdm/linkml_coral_cdm.yaml`
4. Open issue: https://github.com/linkml/linkml-coral/issues
