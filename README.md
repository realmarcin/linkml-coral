<a href="https://github.com/dalito/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# linkml-coral

**LinkML schema repository for CORAL** implementing the ENIGMA Common Data Model (CDM) with comprehensive metadata management, semantic annotations, and interactive documentation.

This project converts CORAL typedef JSON definitions into semantic LinkML schemas with enhanced validation, ontology integration, and enterprise-grade metadata catalogs.

## 🎯 Key Features

- **100% Metadata Coverage**: All 291 columns fully documented with descriptions, microtypes, and constraints
- **Interactive Data Dictionary**: Searchable HTML interface with visual constraint badges
- **Semantic Annotations**: 69 microtype annotations (ME: terms) for semantic typing
- **DuckDB Metadata Catalogs**: Query-ready metadata tables for data discovery
- **Complex Query Framework**: Multi-table joins across static, system, and dynamic (brick) data
- **Automated Validation**: 46 validation rules with regex patterns and FK constraints
- **Provenance Tracking**: Complete lineage from samples through sequencing to analysis
- **⚡ High-Performance Loading**: Direct DuckDB import (10-50x faster than pandas, ~130K records/sec)

---

## 📋 Quick Setup Workflow

```bash
# 1. Clone and install
git clone https://github.com/realmarcin/linkml-coral
cd linkml-coral && uv sync

# 2. Obtain CDM parquet data (contact ENIGMA team)
# Place in: data/enigma_coral.db/

# 3. Load into DuckDB (creates cdm_store_sample.db)
just load-cdm-store-sample    # ~2 minutes, 2.4M records

# 4. Start querying!
just cdm-store-stats           # View statistics
just cdm-find-samples Location0000001  # Find samples
duckdb cdm_store_sample.db     # Direct SQL access
```

**📖 See detailed instructions below in [Quick Start](#-quick-start) section**

---

## ⚡ Performance Improvements

**Direct DuckDB Import** (January 2026):
- **10-50x faster** loading of parquet files
- **Minimal memory usage** via streaming imports
- **~130,000 records/sec** for brick tables
- Automatically enabled for all loading commands
- Graceful fallback to pandas if needed

See [DIRECT_DUCKDB_IMPORT_FIX.md](DIRECT_DUCKDB_IMPORT_FIX.md) for technical details.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (3.13 recommended)
- **uv** package manager - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- **DuckDB** (optional, for direct SQL queries) - Installed automatically with uv sync
- **just** command runner (optional but recommended) - [Install just](https://github.com/casey/just#installation)

### Hardware Requirements

Different loading operations have varying hardware requirements:

| Operation | RAM Required | Time Estimate | Output Size | Use Case |
|-----------|-------------|---------------|-------------|----------|
| **Core only** | 4 GB | ~30 seconds | 50 MB | Quick exploration |
| **Core + Sample** | 8 GB | ~2 minutes | 25 MB | Recommended start ⭐ |
| **Core + 20 bricks** | 16 GB | ~5 minutes | 150 MB | Development/testing |
| **Full (sampled)** | 32 GB | ~10 minutes | 500 MB | Analysis with samples |
| **Full (unsampled, 64GB optimized)** | 64 GB | 30-60 minutes | 15-20 GB | Complete dataset ⭐ NEW! |
| **Full (unsampled, fast)** | 128 GB+ | 15-30 minutes | 15-20 GB | Complete dataset (faster) |

**Performance Notes:**
- **Direct DuckDB import**: 10-50x faster than pandas (enabled by default)
- **Loading speed**: ~130,000 records/sec for brick tables, ~40,000 records/sec for static tables
- **Memory usage**: Chunked loading prevents OOM errors on 64GB machines ⭐ **NEW: Full support for 64GB RAM!**
- **Recommended**: 64 GB RAM now sufficient for complete unsampled dataset (no data loss)

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/realmarcin/linkml-coral
cd linkml-coral

# Initialize CORAL submodule (contains source typedef.json)
git submodule update --init --recursive

# Install dependencies with uv
uv sync

# Verify installation
uv run python --version
just --version  # Optional but recommended
```

### Step 2: Get CDM Parquet Data

The CDM parquet data is stored in the `data/enigma_coral.db/` directory structure. You need to obtain this data from the ENIGMA project:

**Option A: Copy from existing location** (if you have access):
```bash
# Example: copy from shared storage
cp -r /path/to/enigma_coral.db data/
```

**Option B: Download from KBase** (contact ENIGMA team for access):
```bash
# Download instructions will be provided by the ENIGMA data team
```

**Verify parquet data structure:**
```bash
ls data/enigma_coral.db/
# Should show directories like: sdt_sample/, sdt_reads/, sys_process/, etc.
```

### Step 3: Load Data into DuckDB

Choose a loading option based on your hardware and use case:

#### Option 1: Core Tables Only (Fast) ⚡
```bash
just load-cdm-store
```
- **Output**: `cdm_store.db` (50 MB)
- **Records**: 515K across 23 collections
- **RAM**: 4 GB minimum
- **Time**: ~30 seconds
- **Use case**: Quick exploration, basic queries

#### Option 2: Core + Sample Bricks (Recommended) ⭐
```bash
just load-cdm-store-sample
```
- **Output**: `cdm_store_sample.db` (25 MB)
- **Records**: 2.4M across 24 collections (10 brick tables)
- **RAM**: 8 GB minimum
- **Time**: ~2 minutes
- **Use case**: Development, testing with measurement data

#### Option 3: Core + 20 Brick Tables
```bash
just load-cdm-store-bricks [db] [output] [num_bricks] [max_rows]

# Examples:
just load-cdm-store-bricks                                    # Load 20 bricks, 100K rows each
just load-cdm-store-bricks data/enigma_coral.db out.db 10 50000  # Load 10 bricks, 50K rows each
```
- **Output**: `cdm_store_bricks.db` (150 MB with 100K rows/brick)
- **Records**: ~5M across 23 collections
- **RAM**: 16 GB minimum (32 GB recommended)
- **Time**: ~5 minutes
- **Parameters**:
  - `db`: Input parquet database path (default: `data/enigma_coral.db`)
  - `output`: Output DuckDB file (default: `cdm_store_bricks.db`)
  - `num_bricks`: Number of brick tables to load (default: `20`)
  - `max_rows`: Max rows per brick (default: `100000`, sampled for safety)

#### Option 4: Full Load with Sampling
```bash
just load-cdm-store-full [db] [output] [max_rows]

# Examples:
just load-cdm-store-full                                      # Load all, 10K rows per brick
just load-cdm-store-full data/enigma_coral.db out.db 50000   # Load all, 50K rows per brick
```
- **Output**: `cdm_store_full.db` (500 MB with 10K rows/brick)
- **Records**: ~82M sampled from full dataset
- **RAM**: 32 GB minimum (64 GB recommended)
- **Time**: ~10 minutes
- **Parameters**:
  - `db`: Input parquet database path
  - `output`: Output DuckDB file
  - `max_rows`: Sample size per brick (default: `10000`)

#### Option 5: Full Bricks (64GB RAM Optimized) ⭐ NEW!
```bash
just load-cdm-store-bricks-64gb [db] [output] [num_bricks]

# Example:
just load-cdm-store-bricks-64gb                               # Load 20 full bricks (no sampling)
```
- **Output**: `cdm_store_bricks_full.db` (15-20 GB unsampled)
- **Records**: 320M+ rows (full dataset, no sampling)
- **RAM**: 64 GB minimum (no upper limit needed!)
- **Time**: 30-60 minutes
- **Features**:
  - ✅ Automatic chunked loading for files >100M rows
  - ✅ Memory-safe for 64GB machines
  - ✅ No data loss - complete unsampled dataset
  - ✅ Tables use CDM naming (sdt_*, sys_*, ddt_*) matching BERDL
- **Parameters**:
  - `db`: Input parquet database path (default: `data/enigma_coral.db`)
  - `output`: Output DuckDB file (default: `cdm_store_bricks_full.db`)
  - `num_bricks`: Number of brick tables to load (default: `20`)

#### Option 6: Full Bricks (128GB+ RAM, Faster)
```bash
just load-cdm-store-bricks-full [db] [output] [num_bricks] [max_rows]

# Examples:
just load-cdm-store-bricks-full                                    # Full load (faster on 128GB+)
just load-cdm-store-bricks-full data/enigma_coral.db out.db 20 100000  # Sampled (safer)
```
- **Output**: `cdm_store_bricks_full.db` (15-20 GB unsampled)
- **Records**: Up to 320M+ rows if unsampled
- **RAM**: 128 GB minimum (256 GB recommended) if `max_rows=0`
- **Time**: 15-30 minutes for full load (faster than 64GB mode)
- **Note**: Use Option 5 (64GB optimized) if you have 64GB RAM
- **Parameters**:
  - `db`: Input parquet database path
  - `output`: Output DuckDB file
  - `num_bricks`: Number of brick tables (default: `20`)
  - `max_rows`: Sample size per brick (default: `0` = unlimited, **use with caution!**)

**What gets loaded** (tables use CDM naming matching BERDL):
- **Static entities (sdt_*)**: sdt_location, sdt_sample, sdt_reads, sdt_assembly, sdt_genome, sdt_gene, sdt_asv, etc. (273K records)
- **System tables (sys_*)**: sys_oterm, sys_typedef, sys_process, sys_process_input, sys_process_output (243K records)
- **Dynamic bricks (ddt_*)**: ddt_brick0000476, ddt_brick0000477, etc. N-dimensional measurement arrays (2.1M-320M records, optional)
- **Indexes**: Automatic indexing on ID fields for fast queries

**Performance Features:**
- ⚡ **Direct DuckDB import**: 10-50x faster than pandas (enabled by default)
- 💾 **Memory-safe chunking**: Automatic for large files
- 🎯 **Configurable sampling**: Control memory usage with `max_rows` parameter

### Step 4: Run Queries

**View database contents:**
```bash
just cdm-store-stats
# Shows: Collection counts, memory usage, index status
```

**Simple queries:**
```bash
# Find samples from a specific location
just cdm-find-samples Location0000001

# Search ontology terms
just cdm-search-oterm "soil"

# Trace provenance lineage (use CDM table name)
just cdm-lineage sdt_assembly Assembly0000001
```

**Direct DuckDB queries:**
```bash
# Connect to database
duckdb cdm_store.db

# Example queries:
SELECT COUNT(*) FROM sdt_sample;
SELECT * FROM sdt_sample LIMIT 5;
SELECT * FROM sys_oterm WHERE sys_oterm_name LIKE '%soil%';

# Join samples with their locations
SELECT
  s.sdt_sample_name,
  s.sdt_location_name,
  s.depth_meter,
  s.material_sys_oterm_name
FROM sdt_sample s
LIMIT 10;
```

**Python queries via linkml-store** (uses CDM table names):
```bash
# Run query scripts
uv run python scripts/cdm_analysis/query_cdm_store.py --help

# Custom queries in Python:
from linkml_store import Client
client = Client()
db = client.attach_database("cdm_store.db", alias="cdm")
collection = db.get_collection("sdt_sample")  # Use CDM table names!
results = collection.find({"material_sys_oterm_name": "soil"})
```

### Troubleshooting Setup

**Issue: Missing parquet data**
```bash
# Check if data directory exists
ls data/enigma_coral.db/

# If missing, you need to obtain the data:
# 1. Contact ENIGMA data team for access
# 2. Copy from shared storage if you have access
# 3. Download from KBase (instructions from team)
```

**Issue: `uv` command not found**
```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv

# Verify installation
uv --version
```

**Issue: `just` command not found**
```bash
# Install just (macOS)
brew install just

# Or download from: https://github.com/casey/just/releases
# just is optional - you can use uv run python commands directly
```

**Issue: Database loading fails**
```bash
# Ensure parquet data structure is correct
ls data/enigma_coral.db/ | head
# Should show: sdt_sample/, sdt_reads/, sys_process/, etc.

# Try loading with verbose output
uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py \
  data/enigma_coral.db \
  --output test.db \
  --create-indexes \
  --verbose
```

### Explore the Data Dictionary

**Interactive HTML (Recommended):**
```bash
open docs/cdm_data_dictionary.html
```

Features:
- 🔍 **Live search** - Filter tables, columns, and descriptions
- 📊 **Statistics dashboard** - Overview of 44 tables, 291 columns
- 🏷️ **Visual badges** - PK, FK, UNIQUE, REQUIRED constraints
- 📱 **Responsive design** - Works on all devices

**Markdown:**
```bash
cat docs/CDM_DATA_DICTIONARY.md
```

---

## 📊 CDM Data Store: Query Examples

This section shows how to query the loaded DuckDB database using different interfaces.

### Database Loading Options

| Command | Records | Output Size | RAM | Time | Description |
|---------|---------|-------------|-----|------|-------------|
| `just load-cdm-store` | 515K | 50 MB | 4 GB | ~30s | Core tables only ⚡ |
| `just load-cdm-store-sample` | 2.4M | 25 MB | 8 GB | ~2m | Core + 10 bricks ⭐ |
| `just load-cdm-store-bricks` | ~5M | 150 MB | 16 GB | ~5m | Core + 20 bricks (100K/ea) |
| `just load-cdm-store-full` | ~82M | 500 MB | 32 GB | ~10m | All tables (10K samples) |
| `just load-cdm-store-bricks-64gb` | 320M+ | 15-20 GB | 64 GB | ~45m | Full unsampled ⭐ NEW! 64GB optimized |
| `just load-cdm-store-bricks-full` | 320M+ | 15-20 GB | 128 GB+ | ~20m | Full unsampled (faster on high RAM) |

**Performance:** Direct DuckDB import provides 10-50x speedup over pandas (enabled by default)

**Table Naming:** All tables use CDM conventions matching BERDL (sdt_*, sys_*, ddt_*)

### Query Interface 1: Natural Language Queries (AI-Powered) 🤖 NEW!

**Ask questions in plain English** - Claude API translates them to SQL and executes them:

```bash
# Using the skill (with Claude Code)
/nl-sql-query
# Then: "How many samples are there?"

# Using just commands
just cdm-nl-query "Show me the top 10 locations by sample count"
just cdm-nl-query "Find samples with depth greater than 100"
just cdm-nl-query "List reads with read_count over 50000"

# JSON output for programmatic use
just cdm-nl-query-json "Count assemblies by type"

# Verbose mode (see generated SQL)
just cdm-nl-query-verbose "What are the most common sample materials?"
```

**Requirements:**
- Set `ANTHROPIC_API_KEY` environment variable
- Database must be loaded (see options above)

**Example Queries:**
- "How many samples are in the database?"
- "Show me reads with more than 100,000 read count"
- "Find assemblies with their corresponding samples"
- "List locations with the most samples"

**More examples**: See `skills/nl-sql-query/EXAMPLES.md` for 50+ example queries

**Schema-Aware Queries** (recommended for complex queries):
```bash
# Using the skill (with Claude Code)
/schema-query

# Using just commands - leverages LinkML schema
just cdm-schema-query "Find samples with their location information"
just cdm-schema-query "Show assemblies with their read data"

# Explore the data model
just cdm-schema-info              # Show all classes
just cdm-schema-explore Sample    # Explore specific class
just cdm-schema-suggest           # Get query ideas
```

**Advantages of schema-aware queries:**
- Understands relationships from LinkML schema
- Auto-generates proper JOINs
- Knows required vs optional fields
- Leverages semantic annotations
- Provides intelligent query suggestions

---

### Query Interface 2: Just Commands (Pre-defined Queries)

**Database Statistics:**
```bash
just cdm-store-stats
# Shows:
# - Collection counts (e.g., sdt_sample: 4,118 records)
# - Database size and index status
# - Memory usage
```

**Entity Lookups:**
```bash
# Find samples from a specific location
just cdm-find-samples Location0000001
# Returns: All samples collected at that location with metadata

# Search ontology terms (fuzzy search)
just cdm-search-oterm "soil"
# Returns: All ontology terms matching "soil" (ENVO terms, etc.)

# Trace provenance lineage (forward and backward)
just cdm-lineage Assembly Assembly0000001
# Returns: Complete workflow chain from sample → assembly
```

**Complex Query Demonstrations:**
```bash
# Demo 1: Location → Samples → Measurements (joins static + dynamic)
just cdm-demo-location-molecules
# Shows: How to query across static entities and brick data

# Demo 2: End-to-end sequencing pipeline
just cdm-demo-pipeline
# Shows: Sample → Reads → Assembly → Genome → Genes

# Demo 3: ASV taxonomy and abundance
just cdm-demo-asv-taxonomy
# Shows: Amplicon data with community abundance from bricks

# Run all demos
just cdm-demo-all
```

### Query Interface 3: DuckDB CLI (Direct SQL)

**Launch DuckDB CLI:**
```bash
duckdb cdm_store.db
```

**Example Queries:**

**1. Count records in each table:**
```sql
-- Show all collections
SHOW TABLES;

-- Count samples
SELECT COUNT(*) FROM sdt_sample;

-- Count by material type
SELECT material_sys_oterm_name, COUNT(*) as count
FROM sdt_sample
GROUP BY material_sys_oterm_name
ORDER BY count DESC;
```

**2. Find samples with metadata:**
```sql
-- Samples from soil with depth information
SELECT
  sdt_sample_name,
  sdt_location_name,
  depth_meter,
  material_sys_oterm_name,
  date
FROM sdt_sample
WHERE material_sys_oterm_name LIKE '%soil%'
  AND depth_meter IS NOT NULL
ORDER BY depth_meter DESC
LIMIT 10;
```

**3. Join samples and reads:**
```sql
-- Find reads from soil samples
SELECT
  r.sdt_reads_name,
  r.read_count_count_unit as read_count,
  r.sequencing_technology_sys_oterm_name as tech,
  s.sdt_sample_name,
  s.material_sys_oterm_name as material
FROM sdt_reads r
JOIN sys_process_output po ON po.sdt_reads_id = r.sdt_reads_id
JOIN sys_process_input pi ON pi.sys_process_id = po.sys_process_id
JOIN sdt_sample s ON s.sdt_sample_id = pi.sdt_sample_id
WHERE s.material_sys_oterm_name LIKE '%soil%'
LIMIT 10;
```

**4. Provenance queries:**
```sql
-- Find all processes that created assemblies
SELECT
  p.sys_process_id,
  p.process_sys_oterm_name,
  p.person_sys_oterm_name,
  p.date_start,
  COUNT(*) as assembly_count
FROM sys_process p
JOIN sys_process_output po ON po.sys_process_id = p.sys_process_id
WHERE po.output_object_type = 'Assembly'
GROUP BY p.sys_process_id, p.process_sys_oterm_name,
         p.person_sys_oterm_name, p.date_start
ORDER BY assembly_count DESC
LIMIT 10;
```

**5. Search ontology terms:**
```sql
-- Find all measurement-related ontology terms
SELECT sys_oterm_id, sys_oterm_name, sys_oterm_definition
FROM sys_oterm
WHERE sys_oterm_name LIKE '%concentration%'
   OR sys_oterm_definition LIKE '%measurement%'
ORDER BY sys_oterm_name;
```

**6. Query brick measurement data** (if loaded with --load-cdm-store-sample or higher):
```sql
-- Example: Query brick measurements
SELECT * FROM ddt_brick0000010 LIMIT 10;

-- Find bricks with specific dimensions
SELECT
  ddt_ndarray_id,
  berdl_column_name,
  dimension_oterm_name,
  variable_oterm_name
FROM sys_ddt_typedef
WHERE dimension_oterm_name LIKE '%Environmental Sample%'
ORDER BY ddt_ndarray_id;
```

### Query Interface 4: Python Scripts

**Pre-built query scripts:**
```bash
# General query interface
uv run python scripts/cdm_analysis/query_cdm_store.py \
  --database cdm_store.db \
  --query stats

# Find samples by criteria
uv run python scripts/cdm_analysis/query_cdm_store.py \
  --database cdm_store.db \
  --collection sdt_sample \
  --query '{"material_sys_oterm_name": {"$regex": "soil"}}'

# Complex demo queries (requires brick data)
uv run python scripts/cdm_analysis/demo_complex_query.py
```

**Custom Python queries:**
```python
from linkml_store import Client

# Connect to database
client = Client()
db = client.attach_database("cdm_store.db", alias="cdm")

# Example 1: Query samples
samples = db.get_collection("sdt_sample")
soil_samples = samples.find({"material_sys_oterm_name": {"$regex": "soil"}})
print(f"Found {len(list(soil_samples))} soil samples")

# Example 2: Count records
for collection_name in db.list_collections():
    collection = db.get_collection(collection_name)
    count = collection.count()
    print(f"{collection_name}: {count:,} records")

# Example 3: Complex query with joins (via DuckDB)
import duckdb
conn = duckdb.connect("cdm_store.db")
result = conn.execute("""
    SELECT s.sdt_sample_name, COUNT(r.sdt_reads_id) as read_count
    FROM sdt_sample s
    LEFT JOIN sys_process_input pi ON pi.sdt_sample_id = s.sdt_sample_id
    LEFT JOIN sys_process_output po ON po.sys_process_id = pi.sys_process_id
    LEFT JOIN sdt_reads r ON r.sdt_reads_id = po.sdt_reads_id
    GROUP BY s.sdt_sample_name
    HAVING read_count > 0
    ORDER BY read_count DESC
    LIMIT 10
""").fetchdf()
print(result)
```

### Query Performance Tips

1. **Use indexes** - Automatically created for all ID fields during load
2. **Filter early** - Add WHERE clauses before JOINs when possible
3. **Limit results** - Use LIMIT for exploratory queries
4. **Query static tables first** - Much smaller than brick tables
5. **Use just commands** - Pre-optimized queries with provenance tracking

### Troubleshooting

**Database not found:**
```bash
# Verify database exists
ls -lh cdm_store.db

# Reload if needed
just load-cdm-store
```

**Empty results:**
```bash
# Check if data loaded correctly
just cdm-store-stats

# Verify table contents
duckdb cdm_store.db "SELECT COUNT(*) FROM sdt_sample"
```

**Slow queries:**
```bash
# Check if indexes exist
duckdb cdm_store.db "PRAGMA show_tables"

# Rebuild database with indexes
just load-cdm-store  # Uses --create-indexes by default
```

### Next Steps

- 📖 See **[CDM Parquet Store Guide](docs/CDM_PARQUET_STORE_GUIDE.md)** for comprehensive query examples
- 🔍 Browse **[Interactive Data Dictionary](docs/cdm_data_dictionary.html)** to understand table schemas
- 📊 Review **[Metadata Catalogs](data/cdm_metadata/README.md)** for query-ready metadata

---

## 🗄️ CDM Metadata Catalogs

All metadata extracted from parquet files is available as structured JSON in `data/cdm_metadata/`:

### Available Catalogs

| Catalog | Records | Description |
|---------|---------|-------------|
| `column_catalog.json` | 291 | All column metadata (DuckDB ready) |
| `table_catalog.json` | 44 | Table statistics and metadata |
| `validation_catalog.json` | 46 | Validation rules and patterns |
| `microtype_catalog.json` | 69 | Semantic type usage (ME: terms) |
| `relationship_catalog.json` | 108 | FK relationships |

### Query Metadata in DuckDB

```bash
# Load metadata catalogs
duckdb cdm_with_metadata.db < data/cdm_metadata/cdm_metadata_schema.sql

# Find all columns about sequencing
duckdb cdm_with_metadata.db "
  SELECT table_name, column_name, description
  FROM cdm_column_metadata
  WHERE description ILIKE '%sequencing%';
"

# Find all foreign key relationships
duckdb cdm_with_metadata.db "
  SELECT source_table, source_column, target_table, target_column
  FROM cdm_relationship_catalog
  WHERE source_table = 'sdt_sample';
"
```

See [`data/cdm_metadata/README.md`](data/cdm_metadata/README.md) for detailed examples.

---

## 📚 Documentation

### Primary Documentation
- **[Interactive Data Dictionary](docs/cdm_data_dictionary.html)** - Browse all tables and columns (HTML)
- **[CDM Data Dictionary](docs/CDM_DATA_DICTIONARY.md)** - Complete reference (Markdown)
- **[Metadata Integration Summary](CDM_METADATA_INTEGRATION_SUMMARY.md)** - Overview of metadata system
- **[Metadata Analysis](CDM_PARQUET_METADATA_ANALYSIS.md)** - Detailed parquet metadata analysis

### CDM-Specific Guides
- **[CDM Metadata Catalogs](data/cdm_metadata/README.md)** - Query examples and usage
- **[CDM Parquet Store Guide](docs/CDM_PARQUET_STORE_GUIDE.md)** - Loading and querying parquet data
- **[CDM Naming Conventions](docs/CDM_NAMING_CONVENTIONS.md)** - Table/column naming rules
- **[CDM Schema Implementation](docs/CDM_SCHEMA_IMPLEMENTATION_SUMMARY.md)** - Architecture overview

### MkDocs Site
- **[https://realmarcin.github.io/linkml-coral](https://realmarcin.github.io/linkml-coral)** - Generated schema documentation

---

## 🛠️ Essential Commands

All commands use [just](https://github.com/casey/just/). Run `just` or `just --list` to see all available commands.

### Development Workflow

```bash
just test          # Run all tests (schema, Python, examples)
just gen-project   # Generate project files from schema
just lint          # Lint the schema
just site          # Generate project and documentation locally
just testdoc       # Build docs and run test server
```

### Schema Visualization

```bash
just visualize     # Generate schema ER diagrams
just analyze       # Analyze schema structure and relationships
```

### Data Loading and Querying

**Prerequisites:** Obtain CDM parquet data first (see Quick Start → Step 2)

```bash
# Load databases (creates DuckDB files)
just load-cdm-store                # Core only (~30s, 4GB RAM, 515K records)
just load-cdm-store-sample         # Core + 10 bricks (~2m, 8GB RAM, 2.4M) ⭐ Recommended
just load-cdm-store-bricks         # Core + 20 bricks (~5m, 16GB RAM, 5M)
just load-cdm-store-full           # All sampled (~10m, 32GB RAM, 82M)
just load-cdm-store-bricks-64gb    # Full unsampled (~45m, 64GB RAM, 320M+) ⭐ NEW! Optimized for 64GB
just load-cdm-store-bricks-full    # Full unsampled (~20m, 128GB+ RAM, 320M+) Faster on high RAM

# Query databases (use after loading)
just cdm-store-stats               # Show database statistics
just cdm-find-samples <location>   # Find samples by location ID
just cdm-search-oterm <term>       # Search ontology terms (fuzzy)
just cdm-lineage <type> <id>       # Trace provenance lineage

# Complex query demonstrations (requires --load-cdm-store-sample or higher)
just cdm-demo-location-molecules   # Location → Samples → Measurements
just cdm-demo-pipeline             # Sample → Reads → Assembly → Genome
just cdm-demo-asv-taxonomy         # ASV taxonomy and abundance
just cdm-demo-all                  # Run all query demonstrations

# Direct SQL queries
duckdb cdm_store.db                # Launch DuckDB CLI for SQL queries
```

**Performance Note:** All loading commands use direct DuckDB import for 10-50x speedup

### Metadata Tools

```bash
# Extract metadata from parquet
uv run python scripts/cdm_analysis/extract_cdm_metadata.py data/enigma_coral.db \
  --category static \
  --format detailed

# Generate data dictionary
uv run python scripts/cdm_analysis/generate_data_dictionary.py

# Update schema with metadata
uv run python scripts/cdm_analysis/update_schema_with_metadata.py --dry-run
```

---

## 📁 Repository Structure

```
linkml-coral/
├── data/
│   ├── cdm_metadata/              # Metadata catalogs (JSON + SQL)
│   │   ├── column_catalog.json    # 291 columns with full metadata
│   │   ├── table_catalog.json     # 44 tables statistics
│   │   ├── validation_catalog.json # 46 validation rules
│   │   ├── microtype_catalog.json # 69 semantic types
│   │   ├── relationship_catalog.json # 108 FK relationships
│   │   └── cdm_metadata_schema.sql # DuckDB DDL
│   └── enigma_coral.db/              # CDM parquet files (44 tables)
│
├── docs/
│   ├── cdm_data_dictionary.html   # Interactive data dictionary ⭐
│   ├── CDM_DATA_DICTIONARY.md     # Markdown reference
│   └── [CDM guides]               # Various CDM documentation
│
├── src/linkml_coral/schema/
│   ├── linkml_coral.yaml          # CORAL ENIGMA schema
│   └── cdm/                       # KBase CDM schemas ⭐
│       ├── linkml_coral_cdm.yaml  # Main CDM schema
│       ├── cdm_static_entities.yaml # 17 static tables
│       ├── cdm_system_tables.yaml # 6 system tables
│       ├── cdm_dynamic_data.yaml  # Brick infrastructure
│       └── cdm_base.yaml          # Common types/mixins
│
├── scripts/
│   ├── cdm_analysis/              # CDM metadata tools ⭐
│   │   ├── extract_cdm_metadata.py
│   │   ├── create_metadata_catalog.py
│   │   ├── generate_data_dictionary.py
│   │   ├── update_schema_with_metadata.py
│   │   ├── demo_complex_query.py
│   │   ├── load_cdm_parquet_to_store.py
│   │   └── query_cdm_store.py
│   └── [other scripts]
│
├── output/                        # Generated reports & databases (gitignored)
│   ├── *.db                       # Test database files
│   ├── *_ANALYSIS.md              # Analysis reports
│   ├── *_GUIDE.md                 # Implementation guides
│   └── README.md                  # Output directory documentation
│
├── tests/                         # Unit tests and test data
├── examples/                      # Usage examples
└── project/                       # Generated files (auto)
```

---

## 🔬 CDM Metadata Statistics

### Coverage
- **Tables**: 44 (17 static, 6 system, 21 dynamic)
- **Columns**: 291 (100% documented)
- **Descriptions**: 291 (100% coverage)
- **Microtypes**: 69 unique semantic types (ME: terms)
- **FK Relationships**: 108 documented
- **Validation Rules**: 46 patterns and constraints
- **Total Data**: 2.6M records

### Table Categories

| Category | Tables | Columns | Rows | Description |
|----------|--------|---------|------|-------------|
| **Static (sdt_*)** | 17 | 106 | 273K | Core domain entities |
| **System (sys_*)** | 6 | 69 | 243K | Metadata & provenance |
| **Dynamic (ddt_*)** | 21 | 116 | 2.1M | Measurement arrays |

### Top Static Tables
- `sdt_asv`: 213K records (Amplicon Sequence Variants)
- `sdt_reads`: 19K records (Sequencing reads)
- `sdt_gene`: 15K records (Gene annotations)
- `sdt_genome`: 7K records (Genome assemblies)
- `sdt_sample`: 4K records (Environmental samples)

### Top System Tables
- `sys_process`: 143K records (Provenance workflows)
- `sys_process_input`: 90K records (Process inputs)
- `sys_process_output`: 38K records (Process outputs)
- `sys_oterm`: 11K records (Ontology terms)

---

## 🧪 Testing and Validation

```bash
# Run all tests
just test

# Validate TSV data against schema
just validate-tsv data/export/exported_tsvs/Sample.tsv

# Batch validate with enhanced checks
just validate-batch

# Generate HTML validation report
just validate-report-html validation_reports/report.json
```

---

## 🔄 Update CORAL Submodule

To sync with the latest CORAL typedef.json:

```bash
git submodule update --remote CORAL
cp CORAL/back_end/python/var/typedef.json data/
```

---

## 📖 Key Concepts

### Microtype Annotations
Every column has a semantic microtype (ME: term) defining its meaning:
- `ME:0000267`: Unique identifier
- `ME:0000102`: Name field
- `ME:0000219`: Depth measurement (with UO:0000008 meter units)
- `ME:0000228`: Location reference

### Ontology Term Splitting
CORAL ontology fields are split into ID + name pairs for efficient querying:
- CORAL: `material` → CDM: `material_sys_oterm_id` + `material_sys_oterm_name`
- Enables FK validation + human-readable labels without joins

### Dynamic Data Bricks
N-dimensional measurement arrays stored in brick tables:
- Flexible schema defined in `sys_ddt_typedef`
- Semantic dimensions via ontology terms
- 20 example bricks with 2.1M measurements

### Provenance Model
Complete lineage tracking:
- `sys_process`: Workflow definitions
- `sys_process_input`: Input entities
- `sys_process_output`: Output entities
- Trace from samples → reads → assemblies → genomes → genes

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes with descriptive messages
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 Credits

- **Template**: [linkml-project-copier](https://github.com/dalito/linkml-project-copier) - [doi:10.5281/zenodo.15163584](https://doi.org/10.5281/zenodo.15163584)
- **CORAL**: ENIGMA Common Ontology for Research and Learning Analytics
- **KBase**: KBase Common Data Model for ENIGMA data integration
- **LinkML**: [Linked Data Modeling Language](https://linkml.io/)

---

## 📄 License

See [LICENSE](LICENSE) for details.

---

**Ready to explore? Start with the [Interactive Data Dictionary](docs/cdm_data_dictionary.html) 🎯**
