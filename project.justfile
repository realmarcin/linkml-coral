## Add your own just recipes here. This is imported by the main justfile.

# Visualize the CORAL schema as ER diagrams
[group('model development')]
visualize:
  @echo "🎨 Generating schema visualizations..."
  uv run python visualize_relationships.py
  uv run python visualize_schema.py
  @echo "✅ Diagrams saved to schema_diagrams/ and relationship_diagrams/"
  @echo "📄 Open schema_diagrams/schema_visualization.html to view all diagrams"

# Analyze the CORAL schema structure and relationships
[group('model development')]
analyze:
  @echo "🔍 Analyzing schema structure..."
  uv run python analyze_schema.py --matrix --output-dir analysis_output/
  @echo "✅ Analysis complete!"
  @echo "📊 Report printed above"
  @echo "📄 Detailed results saved to analysis_output/"

# Generate simplified schema overview diagrams (no attributes)
[group('model development')]
visualize-overview:
  @echo "🎨 Generating simplified overview diagrams..."
  uv run python visualize_schema.py --no-attributes --output-dir schema_diagrams/overview
  @echo "✅ Overview diagrams saved to schema_diagrams/overview/"

# Generate all schema visualizations in multiple formats (requires mermaid-cli)
[group('model development')]
visualize-all:
  @echo "🎨 Generating schema visualizations in all formats..."
  uv run python visualize_schema.py --format all
  @echo "✅ Diagrams saved to schema_diagrams/ (Mermaid, PNG, SVG)"
  @echo "📄 Open schema_diagrams/schema_visualization.html to view"

# Visualize entity relationships (foreign keys, hierarchies)
[group('model development')]
visualize-relationships:
  @echo "🔗 Generating relationship diagrams..."
  uv run python visualize_relationships.py
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
  uv run python validate_tsv_linkml.py '{{tsv_path}}' --verbose

# Validate TSV with enhanced enum/FK validation and quality metrics
[group('model development')]
validate-tsv-enhanced tsv_path tsv_dir='data/export/exported_tsvs':
  @echo "🔍 Validating with enhanced checks: {{tsv_path}}"
  uv run python validate_tsv_linkml.py '{{tsv_path}}' \
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
  uv run python validate_all_exported_tsvs.py \
    --tsv-dir {{tsv_dir}} \
    --report-format all \
    --verbose

# Batch validate with specific files
[group('model development')]
validate-batch-files tsv_dir='data/export/exported_tsvs' *files='':
  @echo "📦 Batch validating selected files: \"{{files}}\""
  uv run python validate_all_exported_tsvs.py \
    --tsv-dir {{tsv_dir}} \
    --include {{files}}... \
    --report-format all \
    --verbose

# Generate HTML report from JSON validation results
[group('model development')]
validate-report-html json_path:
  @echo "📊 Generating HTML report from {{json_path}}..."
  uv run python generate_html_validation_report.py '{{json_path}}'
  @echo "✅ HTML report generated!"

# Quick validation without enhanced checks
[group('model development')]
validate-quick tsv_path:
  @echo "⚡ Quick validation: {{tsv_path}}"
  uv run python validate_tsv_linkml.py {{tsv_path}}

# Load ENIGMA TSV data into linkml-store database
[group('data management')]
load-store tsv_dir='../ENIGMA_ASV_export' db='enigma_data.db':
  @echo "📦 Loading ENIGMA data into linkml-store..."
  uv run python load_tsv_to_store.py {{tsv_dir}} --db {{db}} --create-indexes --show-info --verbose
  @echo "✅ Database ready: {{db}}"

# Query: Find unused "good" reads not used in assemblies
[group('data management')]
query-unused-reads min_count='50000' db='enigma_data.db':
  @echo "🔍 Finding unused 'good' reads (min_count >= {{min_count}})..."
  uv run python enigma_query.py --db {{db}} unused-reads --min-count {{min_count}}

# Query: Find unused isolate genome reads (exclude 16S/metagenome)
[group('data management')]
query-unused-isolates min_count='50000' db='enigma_data.db':
  @echo "🧬 Finding unused isolate genome reads (min_count >= {{min_count}})..."
  uv run python enigma_query.py --db {{db}} unused-reads --min-count {{min_count}} --exclude-16s

# Query: Find unused metagenome/16S reads
[group('data management')]
query-unused-metagenomes min_count='50000' db='enigma_data.db':
  @echo "🦠 Finding unused metagenome/16S reads (min_count >= {{min_count}})..."
  uv run python enigma_query.py --db {{db}} unused-reads --min-count {{min_count}} --read-type ME:0000113

# Show database statistics
[group('data management')]
query-stats db='enigma_data.db':
  @echo "📊 Database statistics..."
  uv run python enigma_query.py --db {{db}} stats

# Show provenance lineage for an entity
[group('data management')]
query-lineage entity_type entity_id db='enigma_data.db':
  @echo "🔗 Tracing lineage for {{entity_type}} {{entity_id}}..."
  uv run python enigma_query.py --db {{db}} lineage {{entity_type}} {{entity_id}}

# General query interface
[group('data management')]
query-find collection db='enigma_data.db' *query_args='':
  @echo "🔍 Finding {{collection}} records..."
  uv run python enigma_query.py --db {{db}} find {{collection}} {{query_args}}

# Clean generated visualization and analysis outputs
[group('project management')]
clean-viz:
  @echo "🧹 Cleaning visualization and analysis outputs..."
  rm -rf schema_diagrams/ analysis_output/ relationship_diagrams/
  @echo "✅ Cleaned"
