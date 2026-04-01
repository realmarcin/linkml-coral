# CDM Store Quick Start Guide

Load and query KBase Common Data Model (CDM) parquet files using linkml-store with DuckDB backend.

## Load CDM Data into linkml-store

```bash
# Load core CDM tables (static entities + system tables, ~1.1M rows)
just load-cdm-store

# This will create a file called cdm_store.db (~44 MB)
# Takes approximately 60-90 seconds
```

### What gets loaded:

- **17 static entity tables**: Location, Sample, Reads, Assembly, Genome, Gene, ASV, Bin, Community, Strain, Taxon, Protocol, Image, Condition, DubSeqLibrary, TnSeqLibrary, ENIGMA
- **6 system tables**: Ontology terms, Type definitions, Process records, Process inputs/outputs
- **Total**: 1,110,656 records across 23 collections
- **Database size**: ~44 MB (highly compressed columnar storage)
- **Load time**: ~60-90 seconds (12,000+ records/sec)

## Example Queries

### 1. Show Database Statistics

```bash
just cdm-store-stats
```

**Output:**
```
📊 CDM Store Database Statistics
============================================================

📂 Database: cdm_store.db
📚 Total collections: 23
📄 Total records: 1,110,656

Collections:
  • ASV                               426,088 records (100K+)
  • Assembly                            6,854 records
  • Bin                                 1,246 records
  • Community                           4,418 records
  • Condition                           2,092 records
  • DubSeqLibrary                           6 records
  • ENIGMA                                  2 records
  • Gene                               30,030 records (10K+)
  • Genome                             13,376 records (10K+)
  • Image                                 436 records
  • Location                            1,188 records
  • Protocol                               84 records
  • Reads                              38,614 records (10K+)
  • Sample                              8,660 records
  • Strain                              6,220 records
  • SystemDDTTypedef                      202 records
  • SystemOntologyTerm                 21,188 records (10K+)
  • SystemProcess                     285,916 records (100K+)
  • SystemProcessInput                180,790 records (100K+)
  • SystemProcessOutput                76,456 records (10K+)
  • SystemTypedef                         236 records
  • Taxon                               6,552 records
  • TnSeqLibrary                            2 records
```

### 2. Find Samples from a Location

```bash
# Find all samples from a specific location
just cdm-find-samples EU02
```

**Output:**
```
🔍 Finding samples from location: EU02
============================================================

Found 100 sample(s):

  1. EU02-D01 (Sample0000001)
     Depth: 5.4m
     Date: 2019-07-29

  2. EU02-D02 (Sample0000033)
     Depth: 5.4m
     Date: 2019-08-05

  3. EU02-D03 (Sample0000065)
     Depth: 5.4m
     Date: 2019-08-06

  ... (continues)
```

### 3. Search Ontology Terms

```bash
# Search for soil-related terms
just cdm-search-oterm "soil"
```

**Output:**
```
🔍 Searching ontology terms for: 'soil'
============================================================

Found 50 term(s):

  1. ENVO:00001998: soil
     Soil is an environmental material which is primarily composed of minerals...

  2. ENVO:00002116: contaminated soil
     A portion of contaminated soil is a portion of soil with elevated levels...

  3. ENVO:00002117: creosote contaminated soil
     Soil which has elevated concentrations of creosote.

  4. ENVO:00002145: chromate contaminated soil
     Soil which has elevated concentrations of chromate.

  5. ENVO:00002259: agricultural soil

  6. ENVO:00002260: dune soil

  7. ENVO:00002261: forest soil
     A portion of soil which is found in a forested area.

  ... (continues)
```

### 4. Trace Provenance Lineage

```bash
# Trace what created an assembly and what it produced
just cdm-lineage Assembly Assembly0000001
```

**Output:**
```
🔗 Tracing lineage for: Assembly:Assembly0000001
============================================================

⬆️  Upstream (inputs that produced this entity):
  1. Process: Process0006710 (None)
     Inputs: Reads:Reads0000868

⬇️  Downstream (outputs produced by this entity):
  1. Process: Process0005950 (None)
     Outputs: Genome:Genome0000001
```

### 5. Using Python API Directly

```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts" / "cdm_analysis"))

from query_cdm_store import CDMStoreQuery

# Initialize
query = CDMStoreQuery('cdm_store.db')

# Get statistics
stats = query.stats()
print(f"Total records: {stats['total_records']:,}")
print(f"Collections: {stats['total_collections']}")

# Find samples by location
samples = query.find_samples_by_location('EU02', limit=10)
for sample in samples:
    print(f"Sample: {sample['sdt_sample_name']}")
    print(f"  ID: {sample['sdt_sample_id']}")
    print(f"  Depth: {sample.get('depth')}m")

# Search ontology terms
terms = query.search_ontology_terms('soil', limit=20)
for term in terms:
    print(f"{term['sys_oterm_id']}: {term['sys_oterm_name']}")

# Trace lineage
lineage = query.trace_lineage('Assembly', 'Assembly0000001')
print(f"Upstream processes: {len(lineage['upstream'])}")
print(f"Downstream processes: {len(lineage['downstream'])}")

# Access detailed provenance
for proc in lineage['upstream']:
    print(f"Process: {proc['process_id']}")
    print(f"  Type: {proc['process_type']}")
    print(f"  Inputs: {', '.join(proc['inputs'])}")
```

### 6. Export Query Results to JSON

```bash
# Export statistics to JSON
uv run python scripts/cdm_analysis/query_cdm_store.py \
    --db cdm_store.db stats --export stats.json

# Export search results
uv run python scripts/cdm_analysis/query_cdm_store.py \
    --db cdm_store.db search-oterm "soil" --export soil_terms.json

# Export lineage
uv run python scripts/cdm_analysis/query_cdm_store.py \
    --db cdm_store.db lineage Assembly Assembly0000001 \
    --export assembly_lineage.json

# Export samples
uv run python scripts/cdm_analysis/query_cdm_store.py \
    --db cdm_store.db find-samples --location EU02 \
    --export eu02_samples.json
```

## Quick Reference

| Command                          | Description                          |
|----------------------------------|--------------------------------------|
| `just load-cdm-store`            | Load all core CDM tables             |
| `just cdm-store-stats`           | Show database statistics             |
| `just cdm-find-samples <location>` | Find samples by location           |
| `just cdm-search-oterm <term>`   | Search ontology terms                |
| `just cdm-lineage <type> <id>`   | Trace provenance lineage             |
| `just clean-cdm-store`           | Delete database files                |

## Advanced Loading Options

### Include Dynamic Brick Tables

```bash
# Include dynamic brick tables (sampled at 10K rows each)
just load-cdm-store-full
```

### Custom Loading with Python

```bash
# Use Python directly with custom options
uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py \
    /path/to/jmc_coral.db \
    --output my_cdm.db \
    --include-static \
    --include-system \
    --include-dynamic \
    --max-dynamic-rows 50000 \
    --create-indexes \
    --show-info \
    --verbose
```

**Available options:**

- `--output, -o` - Output database path (default: `cdm_store.db`)
- `--schema` - Path to CDM LinkML schema
- `--include-static` - Load static entity tables (default: yes)
- `--no-static` - Skip static entity tables
- `--include-system` - Load system tables (default: yes)
- `--no-system` - Skip system tables
- `--include-dynamic` - Load dynamic brick tables (default: no, 82.6M rows)
- `--max-dynamic-rows` - Max rows per dynamic table (default: 10000)
- `--create-indexes` - Create indexes after loading
- `--show-info` - Show database information after loading
- `--verbose` - Verbose output

### Load Only Specific Tables

```bash
# Load only static tables
uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py \
    /path/to/jmc_coral.db \
    --output static_only.db \
    --include-static \
    --no-system

# Load only system tables
uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py \
    /path/to/jmc_coral.db \
    --output system_only.db \
    --no-static \
    --include-system
```

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
- Example: `sdt_location_name` references `Location.sdt_location_name`

### Ontology Terms
- Split into ID + name pairs
- Pattern: `{field}_sys_oterm_id` + `{field}_sys_oterm_name`
- Example: `material_sys_oterm_id` + `material_sys_oterm_name`

## Performance

### Loading Performance
- **Core tables** (static + system): ~60-90 seconds for 1.1M records
- **Load rate**: 12,000+ records/second
- **Database size**: 44 MB (highly compressed)

### Query Performance
- **Small tables** (<10K rows): Instantaneous
- **Medium tables** (10-100K rows): <1 second
- **Large tables** (>100K rows): 1-2 seconds
- **Provenance queries**: <1 second with indexes

## Architecture

```
CDM Parquet Files (Delta Lake format)
    ↓
load_cdm_parquet_to_store.py
    ↓
linkml-store (DuckDB backend)
    ↓
query_cdm_store.py (Python API)
    ↓
Justfile commands (CLI)
```

### Key Features

- **Delta Lake support**: Reads parquet files in Delta Lake directory format
- **NaN handling**: Converts pandas NaN to None for database compatibility
- **Array processing**: Converts numpy arrays to Python lists for SQL storage
- **Computed fields**: Automatic categorization (read_count_category, contig_count_category)
- **Provenance parsing**: Extracts entity types and IDs from process arrays
- **Indexing**: Automatic index creation for primary keys and foreign keys

## Troubleshooting

### Database not found
```bash
# Create database first
just load-cdm-store
```

### Collection not found
```bash
# Check available collections
just cdm-store-stats
```

Common collection names:
- Static entities: `Location`, `Sample`, `Reads`, `Assembly`, `Genome`
- System tables: `SystemOntologyTerm`, `SystemProcess`, `SystemTypedef`

### Memory issues
```bash
# Use sampling for large tables
uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py \
    /path/to/jmc_coral.db \
    --max-dynamic-rows 5000
```

## Related Documentation

- [CDM Parquet Store Guide](CDM_PARQUET_STORE_GUIDE.md) - Comprehensive guide
- [CDM Parquet Validation Guide](CDM_PARQUET_VALIDATION_GUIDE.md) - Data validation
- [CDM Schema Implementation](CDM_SCHEMA_IMPLEMENTATION_SUMMARY.md) - Schema details
- [linkml-store Documentation](https://linkml.io/linkml-store/) - linkml-store docs

## Support

For issues or questions:

1. Check validation reports: `just validate-cdm-full`
2. Review CDM analysis: `just analyze-cdm`
3. Examine schema: `src/linkml_coral/schema/cdm/linkml_coral_cdm.yaml`
4. Open issue: https://github.com/linkml/linkml-coral/issues
