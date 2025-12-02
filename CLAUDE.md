# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## linkml-coral

LinkML schema repository for CORAL, implementing the ENIGMA Common Data Model using the LinkML (Linked Data Modeling Language) framework. This project converts CORAL typedef JSON definitions into semantic LinkML schemas with enhanced validation and ontology integration.

## Initial Setup

**First-time setup requires initializing the CORAL submodule:**
```bash
git clone https://github.com/realmarcin/linkml-coral
cd linkml-coral
git submodule update --init --recursive
uv sync
```

The CORAL repository is included as a git submodule at `CORAL/` containing the source `typedef.json` file.

## Essential Commands

**Development workflow:**
```bash
just test          # Run all tests (schema, Python, examples)
just gen-project   # Generate project files from schema
just lint          # Lint the schema
just site          # Generate project and documentation locally
just testdoc       # Build docs and run test server
just visualize     # Generate schema ER diagrams
just analyze       # Analyze schema structure and relationships
```

**Dependency management:**
```bash
uv sync            # Install/sync dependencies
uv run <command>   # Run commands in the virtual environment
```

Never use `pip` directly - this project uses `uv` for dependency management.

## Repository Structure

**Core schema files (edit these):**
- `src/linkml_coral/schema/linkml_coral.yaml` - **PRIMARY SCHEMA - THE source of truth for all schema modifications**

**Source data from CORAL submodule:**
- `CORAL/back_end/python/var/typedef.json` - Original CORAL typedef JSON (from git submodule)
- `data/typedef.json` - Convenience copy of typedef.json (reference only, sync from submodule when needed)
- `data/coral_enigma_schema.yaml` - CORAL ENIGMA schema in YAML format (derived from typedef.json, reference only)

**Generated files (do not edit):**
- `src/linkml_coral/datamodel/` - Python dataclasses and Pydantic models
- `project/` - Other generated formats (Java, TypeScript, OWL, etc.)
- `docs/` - Generated documentation
- `examples/` - Generated examples

**Test data:**
- `tests/` - Unit tests directory (pytest-based tests in `tests/test_*.py`)
- `tests/data/valid/` - Valid example data files (naming: `ClassName-{name}.yaml`, e.g., `Sample-001.yaml`)
- `tests/data/invalid/` - Invalid examples for negative testing (used to verify validation catches errors)

**TSV validation tools:**
- `scripts/validate_tsv_linkml.py` - Main TSV validation script using linkml-validate
- `validate_small_files.sh` - Batch validation for files <10K records
- `validate_large_files.sh` - Validation for large TSV files with timeout handling
- `validate_all.sh` - Comprehensive validation of all TSV files
- Target data: `/Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/*.tsv`

**Utility scripts (scripts/ directory):**
- `analyze_schema.py`, `visualize_schema.py`, `visualize_relationships.py` - Production schema analysis tools
- `load_tsv_to_store.py`, `enigma_query.py`, `query_provenance_tracker.py` - Database and query tools
- `linkml_to_cdm.py` - CDM table naming converter
- `generate_enums_from_obo.py` - Auto-generate LinkML enums from OBO microtypes
- `update_schema_with_microtypes.py` - Update schema with semantic types and enums
- `validate_all_exported_tsvs.py`, `generate_html_validation_report.py` - Batch validation and reporting
- `test_*.py`, `debug_*.py`, `fix_*.py` - Exploratory/debug scripts (not part of test suite)

**Utility modules (src/linkml_coral/utils/):**
- `obo_parser.py` - OBO file parser for extracting microtypes and ontology terms

## Architecture Overview

This is a LinkML project that:
1. Defines semantic data models in YAML format
2. Generates multiple output formats (Python, TypeScript, Java, OWL, JSON Schema)
3. Validates data against schemas
4. Auto-generates documentation

**Key transformations from CORAL typedef JSON to LinkML:**
- Fixes coordinate validation (latitude range corrected from [-180,180] to [-90,90])
- Corrects FK typos (e.g., "Strain.Name" → "Strain.name")
- Adds semantic annotations and ontology prefix management
- Enhances validation with patterns, constraints, and type checking
- Maps CORAL scalar types: "text"→string, "int"→integer, "float"→float, "[text]"→multivalued
- Preserves provenance workflow annotations from typedef process_types/process_inputs

## OBO Microtype Integration

The schema integrates semantic type definitions from CORAL's `context_measurement_ontology.obo`, which defines **298 microtypes** with the `ME:` prefix. Microtypes provide semantic meaning and validation rules for data fields.

**Microtype categories:**
- **oterm_ref**: Controlled vocabulary types (enums) - e.g., ReadType, SequencingTechnology, Strand
- **string**: Text with patterns - e.g., Date (YYYY-MM-DD), Time (HH:MM:SS), Link (URLs)
- **int/float**: Numeric measurements - e.g., Count, Depth, Elevation, Rate
- **object_ref**: Foreign key references to other entities

**Schema components derived from OBO:**

1. **Semantic Types** (10 reusable types in `types:` section):
   - `Date`, `Time`, `Link` - String-based with patterns
   - `Latitude`, `Longitude` - Float with range constraints
   - `Count`, `Size`, `Rate` - Numeric with constraints
   - `Depth`, `Elevation` - Measurement types with units

2. **Enums** (23 auto-generated from OBO in `enums:` section):
   - `ReadTypeEnum` (Paired End, Single End)
   - `SequencingTechnologyEnum` (Illumina, Pacbio, Nanopore)
   - `StrandEnum` (Forward, Reverse Complement)
   - `CommunityTypeEnum` (Isolate Community, Enrichment, Assemblage, Environmental Community)
   - ...and 19 more covering biological, chemical, and experimental contexts

3. **Microtype Annotations** (on all 105 slots):
   - `microtype`: ME: term defining semantic meaning
   - `microtype_data_type`: Data type category (string, int, float, oterm_ref, object_ref)
   - `type_term`: Original ME: term from typedef.json

**Regenerating enums from OBO:**
```bash
# Auto-generate enum definitions from OBO file
uv run python scripts/generate_enums_from_obo.py --obo CORAL/example/enigma/ontologies/context_measurement_ontology.obo --output generated_enums.yaml

# Update schema with new enums and types
uv run python scripts/update_schema_with_microtypes.py --dry-run  # Preview changes
uv run python scripts/update_schema_with_microtypes.py            # Apply changes
```

**OBO Parser Utility** (`src/linkml_coral/utils/obo_parser.py`):
- Parses OBO format ontology files
- Extracts microtypes and their properties (data_type, valid_units, etc.)
- Builds term hierarchies and relationships
- Used by enum generator and schema update scripts

## Testing Strategy

```bash
just test  # Runs all tests in sequence:
```
1. **Schema validation** - Ensures schema can be processed
2. **Python unit tests** - Uses pytest (functional style preferred)
3. **Example validation** - Tests valid/invalid data against schema

For specific tests:
```bash
uv run pytest tests/test_specific.py::test_name  # Run single test
uv run pytest -xvs                               # Stop on first failure, verbose
```

## LinkML Best Practices

- **Naming**: CamelCase for classes, snake_case for slots/attributes
- **Polymorphism**: Use `type` field with `type_designator: true`
- **Documentation**: Include meaningful descriptions for all elements
- **Standards**: Map to existing standards (e.g., dcterms, OBO terms)
- **Ontology terms**: Never guess IDs - use OLS MCP to look up terms

## TSV Data Validation

The validation system provides comprehensive checking of ENIGMA TSV files against the LinkML schema with **enum validation**, **foreign key validation**, **data quality metrics**, and **multi-format reporting**.

### Quick Validation Commands

**Using just commands (recommended):**
```bash
# Quick validation (linkml-validate only)
just validate-quick data/export/exported_tsvs/Sample.tsv

# Enhanced validation (enum + FK + quality metrics)
just validate-tsv-enhanced data/export/exported_tsvs/Sample.tsv

# Batch validate all TSV files
just validate-batch

# Batch validate specific files
just validate-batch-files Sample Reads Assembly

# Generate HTML report from JSON results
just validate-report-html validation_reports/validation_report_20241115_143022.json
```

**Direct Python commands:**
```bash
# Basic validation
uv run python scripts/validate_tsv_linkml.py /path/to/file.tsv --verbose

# Enhanced validation with all features
uv run python scripts/validate_tsv_linkml.py /path/to/file.tsv \
  --enum-validate \
  --fk-validate \
  --quality-metrics \
  --tsv-dir data/export/exported_tsvs \
  --report-format all \
  --verbose

# Batch validation of all TSV files
uv run python scripts/validate_all_exported_tsvs.py \
  --tsv-dir data/export/exported_tsvs \
  --report-format all

# Generate HTML report from JSON results
uv run python scripts/generate_html_validation_report.py validation_report.json
```

### Validation Features

**1. Schema Compliance (linkml-validate)**
- Validates data structure against LinkML schema definitions
- Checks required fields, data types, and patterns
- Enforces range constraints and cardinality rules

**2. Enum Value Pre-Validation (`--enum-validate`)**
- Validates enum fields before full LinkML validation
- Checks against 23 auto-generated enums from OBO microtypes
- Handles ontology term format: `"Label <PREFIX:ID>"`
- Reports invalid enum values with valid alternatives

**3. Foreign Key Validation (`--fk-validate`)**
- Validates FK references across all TSV files
- Builds FK index from entity IDs in TSV directory
- Checks referential integrity for object_ref fields
- Handles both simple IDs and bracket notation `[EntityType:ID]`
- Validates multivalued FK arrays

**4. Data Quality Metrics (`--quality-metrics`)**
- Completeness: Percentage of non-empty values per field
- Unique values: Count of distinct values
- Value distribution: Top 10 most common values
- Numeric statistics: min, max, mean, median, stdev (for numeric fields)
- Outlier detection: Z-score based outlier identification

**5. Multi-Format Reporting (`--report-format`)**
- **console**: Human-readable terminal output (default)
- **json**: Machine-readable JSON with full validation results
- **csv**: Tabular format for spreadsheet analysis
- **all**: Generate all formats simultaneously

**6. HTML Report Generation**
- Interactive HTML reports with filtering and sorting
- Summary cards with pass/warning/error counts
- Expandable file sections (auto-expand files with errors)
- Quality metrics visualization with progress bars
- Detailed validation issue tables with entity IDs and line numbers

### Field Mapping (Automatic)

TSV column names are automatically mapped to LinkML schema slots:
- Direct mapping: `sample_id` → `sample_id`
- Class prefix removal: `id` → `sample_id` (when validating Sample class)
- Special mappings: `material_term_id` → `sample_material`
- ASV data maps to OTU class
- Process/Sample/Location/Community map directly to schema classes
- Unmapped columns are reported but don't cause validation failures

### Validation Workflow Examples

**Example 1: Validate single file with full checks**
```bash
just validate-tsv-enhanced data/export/exported_tsvs/Reads.tsv
# Output:
# - Console report with enum/FK issues
# - JSON report: validation_reports/validation_report_TIMESTAMP.json
# - CSV report: validation_reports/validation_report_TIMESTAMP.csv
# - Quality metrics for all fields
```

**Example 2: Batch validate and generate HTML**
```bash
# Step 1: Batch validate all TSVs
just validate-batch

# Step 2: Generate HTML report
just validate-report-html validation_reports/batch_TIMESTAMP/validation_report_TIMESTAMP.json

# Step 3: Open HTML in browser
open validation_reports/batch_TIMESTAMP/validation_report_TIMESTAMP.html
```

**Example 3: Validate specific entity types**
```bash
# Only validate Sample, Reads, and Assembly files
just validate-batch-files Sample Reads Assembly

# Outputs to: validation_reports/batch_TIMESTAMP/
```

### Validation Output Structure

**JSON Report Format:**
```json
{
  "validation_date": "2024-11-15T14:30:22",
  "files": [
    {
      "filename": "Sample.tsv",
      "total_records": 1523,
      "pass_count": 1520,
      "warning_count": 2,
      "error_count": 1,
      "pass_rate": 0.998,
      "record_results": [
        {
          "record_line": 42,
          "entity_id": "SAMPLE123",
          "status": "ERROR",
          "results": [
            {
              "status": "ERROR",
              "message": "Invalid enum value",
              "field": "sample_material",
              "value": "unknown_material",
              "expected": "One of: soil, sediment, water, ..."
            }
          ]
        }
      ],
      "quality_metrics": {
        "sample_id": {
          "completeness": 100.0,
          "unique_count": 1523,
          "non_empty_count": 1523
        }
      }
    }
  ]
}
```

### Legacy Validation Scripts

For backward compatibility, shell scripts are still available:
```bash
./validate_small_files.sh   # Batch validation for files <10K records
./validate_large_files.sh   # Validation for large TSV files with timeout handling
./validate_all.sh           # Comprehensive validation of all TSV files
```

**Note:** These scripts use basic linkml-validate without enhanced features. Use `just validate-batch` for full validation capabilities.

## Schema Visualization

**Generate ER diagrams and relationship visualizations:**
```bash
# Generate all visualizations (schema structure + relationships)
just visualize

# Or run scripts individually:
uv run python scripts/visualize_schema.py           # Schema structure diagrams
uv run python scripts/visualize_relationships.py    # Relationship-focused diagrams

# Specific formats
uv run python scripts/visualize_schema.py --no-attributes     # Simplified overview
uv run python scripts/visualize_schema.py --format all        # All formats (requires mermaid-cli)
uv run python scripts/visualize_relationships.py --format mermaid  # Mermaid only
```

**Outputs:**
- `schema_diagrams/schema_visualization.html` - Interactive HTML viewer with all diagrams
  - Schema structure with entity attributes
  - Entity relationship diagrams (Mermaid + Graphviz)
  - Navigation between sections
- `relationship_diagrams/` - Detailed relationship analysis
  - `relationships.mmd` - Mermaid ER diagram with relationship notation
  - `relationships.png/svg` - Graphviz visualization
  - `RELATIONSHIPS.md` - Comprehensive documentation
  - `relationships.txt` - Detailed text report

**Relationship visualization features:**
- Shows foreign key relationships with cardinality (one-to-one, many-to-many)
- Highlights required vs optional relationships
- Identifies self-referential relationships (hierarchies)
- Displays provenance workflow connections
- Color-coded by relationship type

## Schema Analysis

**Analyze schema structure and relationships:**
```bash
# Basic analysis report
uv run python scripts/analyze_schema.py

# Generate relationship matrix
uv run python scripts/analyze_schema.py --matrix

# Save detailed analysis
uv run python scripts/analyze_schema.py --output-dir analysis_output/ --matrix
```

Provides statistics on classes, slots, foreign keys, ontology usage, and entity relationships.

## LinkML-Store Database for Querying

**Load ENIGMA data into queryable database:**
```bash
# Load all TSV files into linkml-store (DuckDB backend)
just load-store

# Load from custom directory
just load-store /path/to/tsv/files enigma.db

# Or run directly
uv run python scripts/load_tsv_to_store.py ../ENIGMA_ASV_export --db enigma_data.db --create-indexes
```

**Query the database:**
```bash
# Answer the key question: unused "good" reads not used in assemblies
just query-unused-reads 50000  # Reads with >=50K raw reads

# Show database statistics
just query-stats

# Trace provenance lineage for an assembly
just query-lineage Assembly Assembly0000001

# Find entities by criteria
just query-find Reads --query read_count_category=high --limit 20

# Direct CLI usage
uv run python scripts/enigma_query.py --help
```

**Key queries available:**
- `unused-reads`: Find "good" reads (high read count) NOT used in assemblies
- `stats`: Database-wide statistics and utilization metrics
- `lineage`: Trace complete provenance chain for any entity
- `find`: Generic search across any collection

**Database structure:**
- Backend: DuckDB (columnar, efficient for analytics)
- Collections: Reads (19K), Assembly (3K), Process (130K), Sample, Location, etc.
- Computed fields: read_count_category, provenance parsing, etc.
- 281,813 total records across 10 collections

**Provenance Tracking:**
- Every query execution is automatically tracked
- Complete metadata: user, system, database state, parameters, results
- Execution history: `uv run python scripts/query_provenance_tracker.py --list`
- Reproducibility: Database checksums, environment snapshots, parameter recording

**Documentation:**
- [docs/QUERY_REFERENCE.md](docs/QUERY_REFERENCE.md) - Quick reference for all query commands
- [docs/DEPLOYMENT_PROVENANCE.md](docs/DEPLOYMENT_PROVENANCE.md) - Deployment & provenance tracking guide
- [docs/LINKML_STORE_USAGE.md](docs/LINKML_STORE_USAGE.md) - Comprehensive database usage guide
- All queries support JSON export for standardized output
- All queries automatically create provenance records in `query_provenance/`

## CDM Table Naming Conventions

**Convert LinkML schema to CDM table definitions:**
```bash
# Generate CDM schema with naming conventions
python scripts/linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml \
  --typedef data/typedef.json \
  --json-output cdm_schema.json \
  --report-output cdm_report.txt

# Check for schema issues only
python scripts/linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml --check-only
```

**CDM Naming Rules:**
- Tables: `sdt_<snake_case_name>` (e.g., `Location` → `sdt_location`)
- Primary keys: `<table>_id` (e.g., `sample_id`)
- Foreign keys: `<referenced_table>_id` or `_ids` for arrays
- All columns: lowercase snake_case with underscores only
- Preferred names: If typedef.json defines `preferred_name`, use it (e.g., `OTU` → `ASV` → `sdt_asv`)

**Outputs:**
- `cdm_schema.json` - Machine-readable JSON schema with full metadata
- `cdm_report.txt` - Human-readable report with table/column details
- No changes required to LinkML schema

**Documentation:**
- [docs/CDM_NAMING_CONVENTIONS.md](docs/CDM_NAMING_CONVENTIONS.md) - Complete specification
- [docs/CDM_CONVERSION_SUMMARY.md](docs/CDM_CONVERSION_SUMMARY.md) - Summary and examples
- [scripts/linkml_to_cdm.py](scripts/linkml_to_cdm.py) - Conversion tool source code

## CDM Parquet → linkml-store Database

**Load KBase CDM parquet data into queryable linkml-store database:**

```bash
# Load core CDM tables (static entities + system tables, 515K rows)
just load-cdm-store

# Load with custom paths
just load-cdm-store /path/to/jmc_coral.db output.db

# Load including dynamic brick tables (sampled at 10K rows each)
just load-cdm-store-full
```

**Query the CDM store database:**

```bash
# Show database statistics
just cdm-store-stats

# Find samples from a location
just cdm-find-samples Location0000001

# Search ontology terms
just cdm-search-oterm "soil"

# Trace provenance lineage
just cdm-lineage Assembly Assembly0000001

# Or use Python script directly
uv run python scripts/cdm_analysis/query_cdm_store.py --help
```

**CDM Database Structure:**
- **44 parquet tables** from KBase CDM (157 MB total)
- **Static entities (sdt_*)**: Location, Sample, Reads, Assembly, Genome, Gene, etc. (17 tables, 273K rows)
- **System tables (sys_*)**: Ontology terms, Type definitions, Process records (6 tables, 242K rows)
- **Dynamic tables (ddt_*)**: Measurement arrays in brick tables (21 tables, 82.6M rows - optionally sampled)

**Key Features:**
- Fast DuckDB-based columnar storage (~50 MB database for core tables)
- Schema validation against CDM LinkML schema
- Computed fields (read_count_category, contig_count_category)
- Parsed provenance arrays (input/output entity types and IDs)
- Efficient querying and analysis

**Documentation:**
- [docs/CDM_PARQUET_STORE_GUIDE.md](docs/CDM_PARQUET_STORE_GUIDE.md) - Complete loading and querying guide
- [docs/CDM_PARQUET_VALIDATION_GUIDE.md](docs/CDM_PARQUET_VALIDATION_GUIDE.md) - Parquet validation guide
- [scripts/cdm_analysis/load_cdm_parquet_to_store.py](scripts/cdm_analysis/load_cdm_parquet_to_store.py) - Loader source code
- [scripts/cdm_analysis/query_cdm_store.py](scripts/cdm_analysis/query_cdm_store.py) - Query interface

## Common Development Tasks

```bash
# Update CORAL submodule and sync typedef.json:
git submodule update --remote CORAL                # Pull latest CORAL changes
cp CORAL/back_end/python/var/typedef.json data/    # Sync typedef.json to data/

# After modifying schema:
just gen-project    # Regenerate all derived files
just test          # Verify changes don't break anything

# Documentation:
just testdoc       # Preview docs locally at http://localhost:8000

# Linting:
just lint          # Check schema quality
uv run ruff check  # Python linting

# Visualization & Analysis:
just visualize           # Generate ER diagrams
just visualize-overview  # Simplified diagrams without attributes
just visualize-all       # All formats (requires mermaid-cli)
just analyze            # Full schema analysis report
just schema-stats       # Quick statistics

# Data validation:
just validate-tsv <file> # Validate specific TSV file

# Data querying (requires loaded database):
just load-store                  # Load TSV data into database first
just query-unused-reads 50000    # Find unused reads
just query-stats                 # Show statistics
just query-lineage Assembly ID   # Trace provenance

# Cleanup:
just clean              # Clean all generated files
just clean-viz          # Clean only visualization outputs
```

## Configuration Files

- `config.yaml` - LinkML generator configuration
- `pyproject.toml` - Python project configuration
- `.editorconfig` - 4 spaces for Python, 2 for YAML/JSON
- `mkdocs.yml` - Documentation site configuration