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

# Clean generated visualization and analysis outputs
[group('project management')]
clean-viz:
  @echo "🧹 Cleaning visualization and analysis outputs..."
  rm -rf schema_diagrams/ analysis_output/ relationship_diagrams/
  @echo "✅ Cleaned"

# ============== KBase CDM Analysis & Schema ==============

# Analyze KBase CDM parquet tables
[group('CDM analysis')]
analyze-cdm db='/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db':
  @echo "🔍 Analyzing KBase CDM parquet tables..."
  uv run python scripts/cdm_analysis/analyze_cdm_parquet.py {{db}}
  @echo "✅ Analysis complete!"
  @echo "📊 Results saved to docs/cdm_analysis/"

# Generate CDM schema report (JSON + detailed text)
[group('CDM analysis')]
cdm-report db='/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db':
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
validate-all-cdm-parquet db='/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db':
  @echo "🔍 Validating all CDM parquet tables (sample mode)..."
  ./scripts/cdm_analysis/validate_all_cdm_parquet.sh {{db}}

# Full validation of all CDM data with detailed error report
[group('CDM analysis')]
validate-cdm-full db='/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db':
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
load-cdm-store db='/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db' output='cdm_store.db':
  @echo "📦 Loading CDM parquet data into linkml-store..."
  uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
    --output {{output}} \
    --include-system \
    --include-static \
    --create-indexes \
    --show-info \
    --verbose
  @echo "✅ Database ready: {{output}}"

# Load CDM parquet with dynamic brick tables (sampled)
[group('CDM data management')]
load-cdm-store-full db='/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db' output='cdm_store_full.db':
  @echo "📦 Loading CDM parquet data (including dynamic tables)..."
  @echo "⚠️  Note: Dynamic brick tables sampled at 10K rows each"
  uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
    --output {{output}} \
    --include-system \
    --include-static \
    --include-dynamic \
    --max-dynamic-rows 10000 \
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

# Clean CDM store databases
[group('CDM data management')]
clean-cdm-store:
  @echo "🧹 Cleaning CDM store databases..."
  rm -f cdm_store.db cdm_store_full.db
  @echo "✅ Cleaned CDM store databases"
