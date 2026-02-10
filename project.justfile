## Add your own just recipes here. This is imported by the main justfile.

# Visualize the CORAL schema as ER diagrams
[group('model development')]
visualize:
  @echo "🎨 Generating schema visualizations..."
  uv run python scripts/visualize_relationships.py
  uv run python scripts/visualize_schema.py
  @echo "✅ Diagrams saved to schema_diagrams/ and relationship_diagrams/"
  @echo "📄 Open schema_diagrams/schema_visualization.html to view all diagrams"

# Analyze the CORAL schema structure and relationships
[group('model development')]
analyze:
  @echo "🔍 Analyzing schema structure..."
  uv run python scripts/analyze_schema.py --matrix --output-dir analysis_output/
  @echo "✅ Analysis complete!"
  @echo "📊 Report printed above"
  @echo "📄 Detailed results saved to analysis_output/"

# Generate simplified schema overview diagrams (no attributes)
[group('model development')]
visualize-overview:
  @echo "🎨 Generating simplified overview diagrams..."
  uv run python scripts/visualize_schema.py --no-attributes --output-dir schema_diagrams/overview
  @echo "✅ Overview diagrams saved to schema_diagrams/overview/"

# Generate all schema visualizations in multiple formats (requires mermaid-cli)
[group('model development')]
visualize-all:
  @echo "🎨 Generating schema visualizations in all formats..."
  uv run python scripts/visualize_schema.py --format all
  @echo "✅ Diagrams saved to schema_diagrams/ (Mermaid, PNG, SVG)"
  @echo "📄 Open schema_diagrams/schema_visualization.html to view"

# Visualize entity relationships (foreign keys, hierarchies)
[group('model development')]
visualize-relationships:
  @echo "🔗 Generating relationship diagrams..."
  uv run python scripts/visualize_relationships.py
  @echo "✅ Relationship diagrams saved to relationship_diagrams/"
  @echo "📄 See relationship_diagrams/RELATIONSHIPS.md for details"

# Quick schema statistics
[group('model development')]
schema-stats:
  @echo "📊 Quick schema statistics:"
  @uv run python -c "from linkml_runtime.utils.schemaview import SchemaView; sv = SchemaView('{{source_schema_path}}'); print(f'  Classes: {len(list(sv.all_classes()))}'); print(f'  Slots: {len(list(sv.all_slots()))}')"

# Validate TSV files against schema
[group('model development')]
validate-tsv tsv_path:
  @echo "🔍 Validating TSV file: {{tsv_path}}"
  uv run python scripts/validate_tsv_linkml.py '{{tsv_path}}' --verbose

# Validate TSV with enhanced enum/FK validation and quality metrics
[group('model development')]
validate-tsv-enhanced tsv_path tsv_dir='data/export/exported_tsvs':
  @echo "🔍 Validating with enhanced checks: {{tsv_path}}"
  uv run python scripts/validate_tsv_linkml.py '{{tsv_path}}' \
    --enum-validate \
    --fk-validate \
    --quality-metrics \
    --tsv-dir {{tsv_dir}} \
    --report-format all \
    --verbose

# Batch validate all ENIGMA TSV files
[group('model development')]
validate-batch tsv_dir='data/export/exported_tsvs':
  @echo "📦 Batch validating all TSV files in {{tsv_dir}}..."
  uv run python scripts/validate_all_exported_tsvs.py \
    --tsv-dir {{tsv_dir}} \
    --report-format all \
    --verbose

# Batch validate with specific files
[group('model development')]
validate-batch-files tsv_dir='data/export/exported_tsvs' *files='':
  @echo "📦 Batch validating selected files: \"{{files}}\""
  uv run python scripts/validate_all_exported_tsvs.py \
    --tsv-dir {{tsv_dir}} \
    --include {{files}}... \
    --report-format all \
    --verbose

# Generate HTML report from JSON validation results
[group('model development')]
validate-report-html json_path:
  @echo "📊 Generating HTML report from {{json_path}}..."
  uv run python scripts/generate_html_validation_report.py '{{json_path}}'
  @echo "✅ HTML report generated!"

# Quick validation without enhanced checks
[group('model development')]
validate-quick tsv_path:
  @echo "⚡ Quick validation: {{tsv_path}}"
  uv run python scripts/validate_tsv_linkml.py "{{tsv_path}}"

# Load ENIGMA TSV data into linkml-store database
[group('data management')]
load-store tsv_dir='../ENIGMA_ASV_export' db='enigma_data.db':
  @echo "📦 Loading ENIGMA data into linkml-store..."
  uv run python scripts/load_tsv_to_store.py {{tsv_dir}} --db {{db}} --create-indexes --show-info --verbose
  @echo "✅ Database ready: {{db}}"

# Query: Find unused "good" reads not used in assemblies
[group('data management')]
query-unused-reads min_count='50000' db='enigma_data.db':
  @echo "🔍 Finding unused 'good' reads (min_count >= {{min_count}})..."
  uv run python scripts/enigma_query.py --db {{db}} unused-reads --min-count {{min_count}}

# Query: Find unused good reads using SQL (faster)
[group('data management')]
query-unused-reads-sql min_count='10000' db='enigma_data.db':
  @echo "🔍 Finding unused reads via SQL (min_count >= {{min_count}})..."
  uv run python scripts/enigma_query.py --db {{db}} unused-reads-sql --min-count {{min_count}}

# Query: Find unused isolate genome reads (exclude 16S/metagenome)
[group('data management')]
query-unused-isolates min_count='50000' db='enigma_data.db':
  @echo "🧬 Finding unused isolate genome reads (min_count >= {{min_count}})..."
  uv run python scripts/enigma_query.py --db {{db}} unused-reads --min-count {{min_count}} --exclude-16s

# Query: Find unused metagenome/16S reads
[group('data management')]
query-unused-metagenomes min_count='50000' db='enigma_data.db':
  @echo "🦠 Finding unused metagenome/16S reads (min_count >= {{min_count}})..."
  uv run python scripts/enigma_query.py --db {{db}} unused-reads --min-count {{min_count}} --read-type ME:0000113

# Show database statistics
[group('data management')]
query-stats db='enigma_data.db':
  @echo "📊 Database statistics..."
  uv run python scripts/enigma_query.py --db {{db}} stats

# Show provenance lineage for an entity
[group('data management')]
query-lineage entity_type entity_id db='enigma_data.db':
  @echo "🔗 Tracing lineage for {{entity_type}} {{entity_id}}..."
  uv run python scripts/enigma_query.py --db {{db}} lineage {{entity_type}} {{entity_id}}

# General query interface
[group('data management')]
query-find collection db='enigma_data.db' *query_args='':
  @echo "🔍 Finding {{collection}} records..."
  uv run python scripts/enigma_query.py --db {{db}} find {{collection}} {{query_args}}

# Find samples by criteria (depth, date, location)
[group('data management')]
query-samples *args:
  @echo "🔍 Finding samples..."
  uv run python scripts/enigma_query.py samples {{args}}

# Find high-count reads meeting threshold
[group('data management')]
query-high-reads min_reads='50000':
  @echo "🔍 Finding reads with count >= {{min_reads}}..."
  uv run python scripts/enigma_query.py samples-with-reads --min-reads {{min_reads}}

# Run arbitrary SQL query against the database
[group('data management')]
query-sql sql db='enigma_data.db':
  uv run python scripts/enigma_query.py --db {{db}} sql "{{sql}}"

# ============== Advanced Query Features ==============

# Validate collection data against LinkML schema
[group('data management')]
validate-collection collection db='enigma_data.db':
  @echo "🔍 Validating {{collection}} against schema..."
  uv run python scripts/enigma_advanced_query.py --db {{db}} validate {{collection}}

# Semantic text search in a collection
[group('data management')]
search-collection collection query db='enigma_data.db':
  @echo "🔍 Searching {{collection}} for: {{query}}"
  uv run python scripts/enigma_advanced_query.py --db {{db}} search {{collection}} "{{query}}"

# Search by ontology term across collections
[group('data management')]
query-oterm term db='enigma_data.db':
  @echo "🔍 Searching for ontology term: {{term}}"
  uv run python scripts/enigma_advanced_query.py --db {{db}} oterm "{{term}}"

# Execute SPARQL query on RDF representation
[group('data management')]
query-sparql sparql db='enigma_data.db':
  @echo "🔍 Executing SPARQL query..."
  uv run python scripts/enigma_advanced_query.py --db {{db}} sparql "{{sparql}}"

# Clean generated visualization and analysis outputs
[group('project management')]
clean-viz:
  @echo "🧹 Cleaning visualization and analysis outputs..."
  rm -rf schema_diagrams/ analysis_output/ relationship_diagrams/
  @echo "✅ Cleaned"

# ============== KBase CDM Analysis & Schema ==============

# Analyze KBase CDM parquet tables
[group('CDM analysis')]
analyze-cdm db='data/enigma_coral.db':
  @echo "🔍 Analyzing KBase CDM parquet tables..."
  uv run python scripts/cdm_analysis/analyze_cdm_parquet.py {{db}}
  @echo "✅ Analysis complete!"
  @echo "📊 Results saved to docs/cdm_analysis/"

# Generate CDM schema report (JSON + detailed text)
[group('CDM analysis')]
cdm-report db='data/enigma_coral.db':
  @echo "📋 Generating CDM schema reports..."
  uv run python scripts/cdm_analysis/generate_cdm_schema_report.py {{db}}
  uv run python scripts/cdm_analysis/examine_typedef_details.py {{db}}
  @echo "✅ Reports generated in docs/cdm_analysis/"

# Compare CORAL and CDM schemas
[group('CDM analysis')]
cdm-compare-schemas:
  @echo "🔄 Comparing CORAL vs KBase CDM schemas..."
  @echo "Original CORAL: src/linkml_coral/schema/linkml_coral.yaml"
  @echo "KBase CDM: src/linkml_coral/schema/cdm/linkml_coral_cdm.yaml"
  @echo "Analysis: docs/cdm_analysis/CDM_PARQUET_ANALYSIS_REPORT.md"

# Validate single CDM parquet file
[group('CDM analysis')]
validate-cdm-parquet file class="":
  @echo "🔍 Validating CDM parquet file..."
  uv run python scripts/cdm_analysis/validate_parquet_linkml.py {{file}} {{if class != "" { "--class " + class } else { "" } }} --verbose

# Validate all CDM parquet tables (quick: sample validation)
[group('CDM analysis')]
validate-all-cdm-parquet db='data/enigma_coral.db':
  @echo "🔍 Validating all CDM parquet tables (sample mode)..."
  ./scripts/cdm_analysis/validate_all_cdm_parquet.sh {{db}}

# Full validation of all CDM data with detailed error report
[group('CDM analysis')]
validate-cdm-full db='data/enigma_coral.db':
  @echo "🔍 Running full validation on all CDM parquet data..."
  @echo "⚠️  This may take a while for large tables..."
  uv run python scripts/cdm_analysis/validate_cdm_full_report.py {{db}}
  @echo "✅ Validation complete! Check validation_reports/cdm_parquet/ for detailed report"

# Clean CDM analysis outputs
[group('CDM analysis')]
clean-cdm:
  @echo "🧹 Cleaning CDM analysis outputs..."
  rm -rf docs/cdm_analysis/*.json docs/cdm_analysis/*.txt cdm_diagrams/ validation_reports/cdm_parquet/
  @echo "✅ Cleaned CDM outputs"

# ============== KBase CDM Data Management ==============

# Load CDM parquet data into linkml-store database
[group('CDM data management')]
load-cdm-store db='data/enigma_coral.db' output='cdm_store.db':
  @echo "📦 Loading CDM parquet data into linkml-store..."
  uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
    --output {{output}} \
    --include-system \
    --include-static \
    --create-indexes \
    --show-info \
    --verbose
  @echo "✅ Database ready: {{output}}"

# Load CDM parquet with core tables + first 5 brick tables (QUICK SAMPLE)
[group('CDM data management')]
load-cdm-store-sample db='data/enigma_coral.db' output='cdm_store_sample.db' num_bricks='5' max_rows='10000':
  @echo "📦 Loading CDM parquet data (QUICK SAMPLE: first {{num_bricks}} bricks, {{max_rows}} rows each)..."
  uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
    --output {{output}} \
    --include-system \
    --include-static \
    --num-bricks {{num_bricks}} \
    --max-dynamic-rows {{max_rows}} \
    --create-indexes \
    --show-info \
    --verbose
  @echo "✅ Database ready: {{output}}"

# Load CDM parquet with brick tables (SAFE: sampled at 100K rows, uses direct DuckDB import)
[group('CDM data management')]
load-cdm-store-bricks db='data/enigma_coral.db' output='cdm_store_bricks.db' num_bricks='20' max_rows='100000':
  @echo "📦 Loading CDM parquet data (core + first {{num_bricks}} brick tables)..."
  @echo "⚠️  SAFE MODE: Sampling {{max_rows}} rows per brick table"
  @echo "   Using fast direct DuckDB import (10-50x faster than pandas)"
  @echo "   (For full load, use: just load-cdm-store-bricks-full)"
  uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
    --output {{output}} \
    --include-system \
    --include-static \
    --num-bricks {{num_bricks}} \
    --max-dynamic-rows {{max_rows}} \
    --create-indexes \
    --show-info \
    --verbose
  @echo "✅ Database ready: {{output}}"

# Load CDM parquet with ALL brick tables - optimized for 64GB RAM (RECOMMENDED)
[group('CDM data management')]
load-cdm-store-bricks-64gb db='data/enigma_coral.db' output='cdm_store_bricks_full.db' num_bricks='999':
  @echo "📦 Loading {{num_bricks}} brick tables (64GB RAM optimized)"
  @echo ""
  @echo "Optimizations for 64GB RAM:"
  @echo "  • Chunked DuckDB loading for files >100M rows"
  @echo "  • 10M row chunks for DuckDB INSERT"
  @echo "  • 50K row chunks for pandas fallback"
  @echo "  • Aggressive garbage collection"
  @echo "  • Full data loading (no sampling)"
  @echo ""
  @echo "Expected:"
  @echo "  • Time: 30-60 minutes for 20 bricks"
  @echo "  • Peak RAM: ~40-50 GB"
  @echo "  • Database size: ~15-20 GB"
  @echo ""
  uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
    --output {{output}} \
    --include-system \
    --include-static \
    --num-bricks {{num_bricks}} \
    --use-direct-import \
    --use-chunked \
    --chunk-size 50000 \
    --create-indexes \
    --show-info \
    --verbose
  @echo "✅ Database ready: {{output}}"

# Load CDM parquet with ALL brick tables (FULL: optional sampling, default no limit)
[group('CDM data management')]
load-cdm-store-bricks-full db='data/enigma_coral.db' output='cdm_store_bricks_full.db' num_bricks='999' max_rows='0':
  @echo "⚠️  ============================================"
  @echo "⚠️  WARNING: Full brick load may require 128+ GB RAM"
  @echo "⚠️  ============================================"
  @echo ""
  @echo "Loading {{num_bricks}} brick tables..."
  @if [ "{{max_rows}}" = "0" ]; then \
    echo "  • Mode: FULL LOAD (all 320M+ rows)"; \
    echo "  • ddt_brick0000476: 320 million rows (383 MB → ~7 GB in memory)"; \
    echo "  • RAM Required: 64 GB minimum (128 GB recommended for old code)"; \
    echo "  • Time: 30-60 minutes (with new chunked loading)"; \
  else \
    echo "  • Mode: SAMPLED ({{max_rows}} rows per brick)"; \
    echo "  • This is safer for 64GB machines"; \
  fi
  @echo ""
  @echo "Uses optimizations:"
  @echo "  • Direct DuckDB import (10-50x faster)"
  @echo "  • Automatic chunking for files >100M rows (NEW!)"
  @echo ""
  @if [ "{{max_rows}}" = "0" ]; then \
    echo "Press Ctrl+C to cancel, or wait 10 seconds to continue..."; \
    sleep 10; \
  fi
  @echo ""
  @echo "Starting brick load..."
  @if [ "{{max_rows}}" = "0" ]; then \
    uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
      --output {{output}} \
      --include-system \
      --include-static \
      --num-bricks {{num_bricks}} \
      --create-indexes \
      --show-info \
      --verbose; \
  else \
    uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
      --output {{output}} \
      --include-system \
      --include-static \
      --num-bricks {{num_bricks}} \
      --max-dynamic-rows {{max_rows}} \
      --create-indexes \
      --show-info \
      --verbose; \
  fi
  @echo "✅ Database ready: {{output}}"

# Drop duplicate tables from CDM store database (preview only)
[group('CDM data management')]
cdm-drop-duplicates-dry-run db='cdm_store.db':
  @echo "🔍 Previewing duplicate tables in {{db}}..."
  uv run python scripts/cdm_analysis/drop_duplicate_tables.py {{db}} --dry-run --verbose

# Drop duplicate tables from CDM store database (DESTRUCTIVE!)
[group('CDM data management')]
cdm-drop-duplicates db='cdm_store.db':
  @echo "⚠️  WARNING: This will DROP duplicate tables from {{db}}"
  @echo "   Duplicate tables: Location, Sample, SystemProcess, etc. (old LinkML names)"
  @echo "   Keeping: sdt_*, sys_*, ddt_* (CDM naming conventions)"
  @echo ""
  @echo "Press Ctrl+C to cancel, or wait 5 seconds to continue..."
  @sleep 5
  uv run python scripts/cdm_analysis/drop_duplicate_tables.py {{db}} --verbose

# Load CDM parquet with ALL dynamic brick tables (sampled, configurable)
[group('CDM data management')]
load-cdm-store-full db='data/enigma_coral.db' output='cdm_store_full.db' max_rows='10000':
  @echo "📦 Loading CDM parquet data (including ALL ~20 brick tables)..."
  @echo "⚠️  Note: Each brick sampled at {{max_rows}} rows (prevents huge database)"
  uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
    --output {{output}} \
    --include-system \
    --include-static \
    --include-dynamic \
    --max-dynamic-rows {{max_rows}} \
    --create-indexes \
    --show-info \
    --verbose
  @echo "✅ Database ready: {{output}}"

# Show CDM store database statistics
[group('CDM data management')]
cdm-store-stats db='cdm_store.db':
  @echo "📊 Querying CDM Store statistics..."
  uv run python scripts/cdm_analysis/query_cdm_store.py --db {{db}} stats

# Find samples from a specific location
[group('CDM data management')]
cdm-find-samples location db='cdm_store.db':
  @echo "🔍 Finding samples from location: {{location}}..."
  uv run python scripts/cdm_analysis/query_cdm_store.py --db {{db}} find-samples --location {{location}}

# Search ontology terms
[group('CDM data management')]
cdm-search-oterm term db='cdm_store.db':
  @echo "🔍 Searching ontology terms for: {{term}}..."
  uv run python scripts/cdm_analysis/query_cdm_store.py --db {{db}} search-oterm "{{term}}"

# Trace provenance lineage for an entity
[group('CDM data management')]
cdm-lineage entity_type entity_id db='cdm_store.db':
  @echo "🔗 Tracing lineage for {{entity_type}}:{{entity_id}}..."
  uv run python scripts/cdm_analysis/query_cdm_store.py --db {{db}} lineage {{entity_type}} {{entity_id}}

# Natural language SQL query (AI-powered)
[group('CDM data management')]
cdm-nl-query query db='cdm_store.db':
  @echo "🤖 Natural language query: {{query}}"
  uv run python scripts/cdm_analysis/nl_sql_query.py --db {{db}} "{{query}}"

# Natural language SQL query with JSON output
[group('CDM data management')]
cdm-nl-query-json query db='cdm_store.db':
  @echo "🤖 Natural language query (JSON output): {{query}}"
  uv run python scripts/cdm_analysis/nl_sql_query.py --db {{db}} "{{query}}" --json

# Natural language SQL query with verbose output
[group('CDM data management')]
cdm-nl-query-verbose query db='cdm_store.db':
  @echo "🤖 Natural language query (verbose): {{query}}"
  uv run python scripts/cdm_analysis/nl_sql_query.py --db {{db}} "{{query}}" --verbose

# Schema-aware query using LinkML schema
[group('CDM data management')]
cdm-schema-query query db='cdm_store.db':
  @echo "🧠 Schema-aware query: {{query}}"
  uv run python scripts/cdm_analysis/schema_aware_query.py --db {{db}} "{{query}}"

# Schema-aware query with JSON output
[group('CDM data management')]
cdm-schema-query-json query db='cdm_store.db':
  @echo "🧠 Schema-aware query (JSON): {{query}}"
  uv run python scripts/cdm_analysis/schema_aware_query.py --db {{db}} "{{query}}" --json

# Schema-aware query with verbose output
[group('CDM data management')]
cdm-schema-query-verbose query db='cdm_store.db':
  @echo "🧠 Schema-aware query (verbose): {{query}}"
  uv run python scripts/cdm_analysis/schema_aware_query.py --db {{db}} "{{query}}" --verbose

# Show LinkML schema information
[group('CDM data management')]
cdm-schema-info db='cdm_store.db':
  @echo "📋 Displaying LinkML schema information..."
  uv run python scripts/cdm_analysis/schema_aware_query.py --db {{db}} --show-schema

# Explore a specific LinkML class
[group('CDM data management')]
cdm-schema-explore class db='cdm_store.db':
  @echo "🔍 Exploring LinkML class: {{class}}"
  uv run python scripts/cdm_analysis/schema_aware_query.py --db {{db}} --explore-class {{class}}

# Get schema-based query suggestions
[group('CDM data management')]
cdm-schema-suggest db='cdm_store.db':
  @echo "💡 Generating query suggestions from schema..."
  uv run python scripts/cdm_analysis/schema_aware_query.py --db {{db}} --suggest-queries

# Unified query interface (auto-detects complexity)
[group('CDM data management')]
cdm-query query db='cdm_store.db':
  @echo "🎯 Unified query: {{query}}"
  uv run python scripts/cdm_analysis/cdm_unified_query.py --db {{db}} "{{query}}"

# Unified query with JSON output
[group('CDM data management')]
cdm-query-json query db='cdm_store.db':
  @echo "🎯 Unified query (JSON): {{query}}"
  uv run python scripts/cdm_analysis/cdm_unified_query.py --db {{db}} "{{query}}" --json

# Unified query with verbose output
[group('CDM data management')]
cdm-query-verbose query db='cdm_store.db':
  @echo "🎯 Unified query (verbose): {{query}}"
  uv run python scripts/cdm_analysis/cdm_unified_query.py --db {{db}} "{{query}}" --verbose

# Unified query forcing fast strategy
[group('CDM data management')]
cdm-query-fast query db='cdm_store.db':
  @echo "⚡ Unified query (fast): {{query}}"
  uv run python scripts/cdm_analysis/cdm_unified_query.py --db {{db}} "{{query}}" --fast

# Unified query forcing schema-aware strategy
[group('CDM data management')]
cdm-query-schema-aware query db='cdm_store.db':
  @echo "🧠 Unified query (schema-aware): {{query}}"
  uv run python scripts/cdm_analysis/cdm_unified_query.py --db {{db}} "{{query}}" --schema-aware

# Unified schema info
[group('CDM data management')]
cdm-query-info db='cdm_store.db':
  @echo "📋 Schema information..."
  uv run python scripts/cdm_analysis/cdm_unified_query.py --db {{db}} --info

# Unified schema exploration
[group('CDM data management')]
cdm-query-explore class db='cdm_store.db':
  @echo "🔍 Exploring class: {{class}}"
  uv run python scripts/cdm_analysis/cdm_unified_query.py --db {{db}} --explore {{class}}

# Unified query suggestions
[group('CDM data management')]
cdm-query-suggest db='cdm_store.db':
  @echo "💡 Query suggestions..."
  uv run python scripts/cdm_analysis/cdm_unified_query.py --db {{db}} --suggest

# Demo: Complex query - Location → Samples → Molecular Measurements (brick data)
[group('CDM data management')]
cdm-demo-location-molecules db='cdm_store_sample.db' limit='3':
  @echo "🔬 DEMO: Complex query across static tables and bricks..."
  @echo "   Query: Location → Samples → Molecular Measurements"
  uv run python scripts/cdm_analysis/demo_complex_query.py --db {{db}} --limit {{limit}} location-molecules

# Demo: Complex query - Sample → Reads → Assembly → Genome → Genes pipeline
[group('CDM data management')]
cdm-demo-pipeline db='cdm_store_sample.db':
  @echo "🧬 DEMO: Complex query through sequencing pipeline..."
  @echo "   Query: Sample → Reads → Assembly → Genome → Genes"
  uv run python scripts/cdm_analysis/demo_complex_query.py --db {{db}} pipeline

# Demo: Complex query - ASV → Taxonomy + Community Abundance (brick data)
[group('CDM data management')]
cdm-demo-asv-taxonomy db='cdm_store_sample.db' limit='5':
  @echo "🦠 DEMO: Complex query for ASV taxonomy and abundance..."
  @echo "   Query: ASV → Taxonomic Classification + Community Abundance"
  uv run python scripts/cdm_analysis/demo_complex_query.py --db {{db}} --limit {{limit}} asv-taxonomy

# Demo: Run all complex queries
[group('CDM data management')]
cdm-demo-all db='cdm_store_sample.db':
  @echo "🚀 DEMO: Running all complex query demonstrations..."
  uv run python scripts/cdm_analysis/demo_complex_query.py --db {{db}} all

# Clean CDM store databases
[group('CDM data management')]
clean-cdm-store:
  @echo "🧹 Cleaning CDM store databases..."
  rm -f cdm_store.db cdm_store_full.db
  @echo "✅ Cleaned CDM store databases"

# ============== CORAL Brick Data Management ==============

# Index all brick files (fast metadata scan)
[group('brick data management')]
index-bricks brick_dir='data/export/exported_bricks':
  @echo "📋 Indexing brick files..."
  uv run python scripts/index_bricks.py {{brick_dir}} -o brick_index.json --report -v
  @echo "✅ Index saved to brick_index.json"

# Parse and preview brick files (dry run)
[group('brick data management')]
parse-bricks brick_dir='data/export/exported_bricks' limit='5':
  @echo "📦 Parsing brick files from {{brick_dir}}..."
  uv run python scripts/brick_parser.py {{brick_dir}} --limit {{limit}} --verbose

# Load CORAL brick files into DuckDB (optimized)
[group('brick data management')]
load-bricks brick_dir='data/export/exported_bricks' db='brick_data.db':
  @echo "📦 Loading brick files into {{db}}..."
  uv run python scripts/load_bricks_to_store.py {{brick_dir}} --db {{db}} --show-stats
  @echo "✅ Bricks loaded to {{db}}"

# Load only small bricks (< 1MB) for quick testing
[group('brick data management')]
load-bricks-small db='brick_small.db':
  @echo "📦 Loading small bricks (< 1MB)..."
  uv run python scripts/load_bricks_to_store.py data/export/exported_bricks \
    --index brick_index.json --max-size 1000000 --db {{db}} --show-stats -v
  @echo "✅ Small bricks loaded to {{db}}"

# Load bricks by data type
[group('brick data management')]
load-bricks-type data_type db='brick_data.db':
  @echo "📦 Loading bricks of type: {{data_type}}..."
  uv run python scripts/load_bricks_to_store.py data/export/exported_bricks \
    --index brick_index.json --data-type "{{data_type}}" --db {{db}} --show-stats -v
  @echo "✅ Loaded {{data_type}} bricks to {{db}}"

# Load bricks with limit (for testing)
[group('brick data management')]
load-bricks-test brick_dir='data/export/exported_bricks' db='brick_test.db' limit='10':
  @echo "📦 Loading {{limit}} brick files into {{db}}..."
  uv run python scripts/load_bricks_to_store.py {{brick_dir}} --db {{db}} --limit {{limit}} --show-stats --verbose
  @echo "✅ Test load complete"

# Show brick database statistics
[group('brick data management')]
brick-stats db='brick_data.db':
  @echo "📊 Brick database statistics..."
  uv run python scripts/load_bricks_to_store.py data/export/exported_bricks --db {{db}} --show-stats 2>/dev/null || uv run python -c "import duckdb; conn = duckdb.connect('{{db}}', read_only=True); print(conn.execute('SELECT COUNT(*) as bricks FROM brick_index').fetchone()[0], 'bricks'); print(conn.execute('SELECT COUNT(*) as rows FROM brick_data').fetchone()[0], 'data rows')"

# Query brick data by type
[group('brick data management')]
query-bricks-by-type data_type db='brick_data.db':
  @echo "🔍 Finding bricks of type: {{data_type}}..."
  uv run python -c "import duckdb; conn = duckdb.connect('{{db}}', read_only=True); r = conn.execute(\"SELECT brick_id, name, total_rows FROM brick_index WHERE data_type LIKE '%{{data_type}}%' ORDER BY total_rows DESC\").fetchall(); [print(f'{x[0]}: {x[2]:,} rows - {x[1]}') for x in r]"

# Query specific brick metadata
[group('brick data management')]
query-brick brick_id db='brick_data.db':
  @echo "📦 Brick: {{brick_id}}"
  uv run python -c "import duckdb, json; conn = duckdb.connect('{{db}}', read_only=True); r = conn.execute(\"SELECT * FROM brick_index WHERE brick_id = '{{brick_id}}'\").fetchone(); cols = [d[0] for d in conn.description]; print('\\n'.join(f'{c}: {v}' for c, v in zip(cols, r) if v))"

# Query brick dimension metadata
[group('brick data management')]
query-brick-dims brick_id db='brick_data.db':
  @echo "📐 Dimensions for {{brick_id}}..."
  uv run python -c "import duckdb; conn = duckdb.connect('{{db}}', read_only=True); r = conn.execute(\"SELECT dim_number, dim_name, entity_type, dim_size FROM brick_dimensions WHERE brick_id = '{{brick_id}}' ORDER BY dim_number\").fetchall(); [print(f'Dim {x[0]}: {x[1]} ({x[2]}) - {x[3]} values') for x in r]"

# Clean brick databases and index
[group('brick data management')]
clean-bricks:
  @echo "🧹 Cleaning brick databases and index..."
  rm -f brick_data.db brick_test.db brick_small.db brick_index.json
  @echo "✅ Cleaned brick databases"
