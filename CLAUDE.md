# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## linkml-coral

LinkML schema repository for CORAL, implementing the ENIGMA Common Data Model using the LinkML (Linked Data Modeling Language) framework. This project converts CORAL typedef JSON definitions into semantic LinkML schemas with enhanced validation and ontology integration.

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
- `data/typedef.json` - Original CORAL typedef JSON source (reference only)
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
- `validate_tsv_linkml.py` - Main TSV validation script using linkml-validate
- `validate_small_files.sh` - Batch validation for files <10K records
- `validate_large_files.sh` - Validation for large TSV files with timeout handling
- `validate_all.sh` - Comprehensive validation of all TSV files
- Target data: `/Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/*.tsv`

**Utility scripts (root directory):**
- `analyze_schema.py`, `visualize_schema.py`, `visualize_relationships.py` - Production schema analysis tools
- `load_tsv_to_store.py`, `enigma_query.py`, `query_provenance_tracker.py` - Database and query tools
- `linkml_to_cdm.py` - CDM table naming converter
- `test_*.py`, `debug_*.py`, `fix_*.py` - Exploratory/debug scripts (not part of test suite)

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

**Validate ENIGMA TSV files against schema:**
```bash
# Single file validation
uv run python validate_tsv_linkml.py /path/to/file.tsv --verbose

# Batch validation (small files <10K records)
./validate_small_files.sh

# Large files with timeout handling
./validate_large_files.sh

# All TSV files
./validate_all.sh

# Save converted YAML for inspection
uv run python validate_tsv_linkml.py file.tsv --save-yaml output_dir/
```

**Field mapping handled automatically:**
- TSV column names → LinkML schema slots (e.g., 'material_term_id' → 'sample_material')
- ASV data maps to OTU class, Process/Sample/Location/Community map directly
- Unmapped columns reported but don't cause validation failures

## Schema Visualization

**Generate ER diagrams and relationship visualizations:**
```bash
# Generate all visualizations (schema structure + relationships)
just visualize

# Or run scripts individually:
uv run python visualize_schema.py           # Schema structure diagrams
uv run python visualize_relationships.py    # Relationship-focused diagrams

# Specific formats
uv run python visualize_schema.py --no-attributes     # Simplified overview
uv run python visualize_schema.py --format all        # All formats (requires mermaid-cli)
uv run python visualize_relationships.py --format mermaid  # Mermaid only
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
uv run python analyze_schema.py

# Generate relationship matrix
uv run python analyze_schema.py --matrix

# Save detailed analysis
uv run python analyze_schema.py --output-dir analysis_output/ --matrix
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
uv run python load_tsv_to_store.py ../ENIGMA_ASV_export --db enigma_data.db --create-indexes
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
uv run python enigma_query.py --help
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
- Execution history: `uv run python query_provenance_tracker.py --list`
- Reproducibility: Database checksums, environment snapshots, parameter recording

**Documentation:**
- [QUERY_REFERENCE.md](QUERY_REFERENCE.md) - Quick reference for all query commands
- [DEPLOYMENT_PROVENANCE.md](DEPLOYMENT_PROVENANCE.md) - Deployment & provenance tracking guide
- [LINKML_STORE_USAGE.md](LINKML_STORE_USAGE.md) - Comprehensive database usage guide
- All queries support JSON export for standardized output
- All queries automatically create provenance records in `query_provenance/`

## CDM Table Naming Conventions

**Convert LinkML schema to CDM table definitions:**
```bash
# Generate CDM schema with naming conventions
python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml \
  --typedef data/typedef.json \
  --json-output cdm_schema.json \
  --report-output cdm_report.txt

# Check for schema issues only
python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml --check-only
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
- [CDM_NAMING_CONVENTIONS.md](CDM_NAMING_CONVENTIONS.md) - Complete specification
- [CDM_CONVERSION_SUMMARY.md](CDM_CONVERSION_SUMMARY.md) - Summary and examples
- [linkml_to_cdm.py](linkml_to_cdm.py) - Conversion tool source code

## Common Development Tasks

```bash
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