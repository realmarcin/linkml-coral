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

---

## 🚀 Quick Start

### Initial Setup

```bash
git clone https://github.com/realmarcin/linkml-coral
cd linkml-coral
git submodule update --init --recursive  # Initialize CORAL submodule
uv sync
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

### Load Sample Database (Static Tables + 10 Bricks)

```bash
# Load all static tables + first 10 brick tables (~60 seconds)
just load-cdm-store-sample

# Result: 2.4M records, 24 collections, 25 MB database
```

### Basic Queries

```bash
# Show database statistics
just cdm-store-stats

# Find samples from a location
just cdm-find-samples EU02

# Search ontology terms
just cdm-search-oterm "soil"

# Trace provenance lineage
just cdm-lineage Assembly Assembly0000001
```

### Complex Multi-Table Queries

```bash
# Demo: Location → Samples → Molecular Measurements (brick data)
just cdm-demo-location-molecules

# Demo: Sample → Reads → Assembly → Genome → Genes pipeline
just cdm-demo-pipeline

# Demo: ASV → Taxonomy + Community Abundance (brick data)
just cdm-demo-asv-taxonomy

# Run all demonstrations
just cdm-demo-all
```

**What gets loaded:**
- **Static tables (sdt_*)**: 273K records (Location, Sample, Reads, Assembly, Genome, Gene, ASV, etc.)
- **System tables (sys_*)**: 243K records (Ontology terms, Process records, Provenance)
- **Dynamic tables (ddt_*)**: 1.9M records (10 brick tables with measurement arrays)
- **Total**: 2.4M records across 24 collections with indexes

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

```bash
# Load databases
just load-cdm-store                # Core tables only (fast)
just load-cdm-store-sample         # Core + 10 brick tables (recommended)
just load-cdm-store-bricks         # Core + 20 brick tables
just load-cdm-store-full           # All tables (sampled)

# Query databases
just cdm-store-stats               # Database statistics
just cdm-find-samples <location>   # Find samples by location
just cdm-search-oterm <term>       # Search ontology terms
just cdm-lineage <type> <id>       # Trace provenance

# Complex query demos
just cdm-demo-all                  # Run all query demonstrations
```

### Metadata Tools

```bash
# Extract metadata from parquet
uv run python scripts/cdm_analysis/extract_cdm_metadata.py data/jmc_coral.db \
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
│   └── jmc_coral.db/              # CDM parquet files (44 tables)
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
