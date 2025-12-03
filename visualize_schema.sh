#!/bin/bash

# Convenience script for common schema visualization tasks

echo "🎨 CORAL LinkML Schema Visualization"
echo "===================================="

# Default output directory
OUTPUT_DIR="schema_diagrams"

# Parse command line arguments
COMMAND=${1:-all}

case $COMMAND in
  all)
    echo "📊 Generating all schema diagrams..."
    uv run python visualize_schema.py --format all
    ;;
    
  overview)
    echo "📊 Generating overview diagram (no attributes)..."
    uv run python visualize_schema.py --no-attributes --output-dir "${OUTPUT_DIR}/overview"
    ;;
    
  core)
    echo "📊 Generating core entity diagrams..."
    mkdir -p "${OUTPUT_DIR}/core"
    
    # Sample workflow
    uv run gen-erdiagram src/linkml_coral/schema/linkml_coral.yaml \
      --classes Location Sample Community \
      > "${OUTPUT_DIR}/core/sample_workflow.mmd"
    
    # Sequencing workflow  
    uv run gen-erdiagram src/linkml_coral/schema/linkml_coral.yaml \
      --classes Reads Assembly Genome Gene \
      > "${OUTPUT_DIR}/core/sequencing_workflow.mmd"
      
    echo "✅ Core diagrams saved to ${OUTPUT_DIR}/core/"
    ;;
    
  clean)
    echo "🧹 Cleaning generated diagrams..."
    rm -rf "${OUTPUT_DIR}"
    echo "✅ Cleaned"
    ;;
    
  help|--help|-h)
    echo "Usage: ./visualize_schema.sh [command]"
    echo ""
    echo "Commands:"
    echo "  all       - Generate all diagrams in multiple formats (default)"
    echo "  overview  - Generate simplified overview without attributes"
    echo "  core      - Generate core workflow diagrams"
    echo "  clean     - Remove all generated diagrams"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./visualize_schema.sh           # Generate all diagrams"
    echo "  ./visualize_schema.sh overview  # Simple overview"
    echo "  ./visualize_schema.sh core      # Core workflows only"
    ;;
    
  *)
    echo "Unknown command: $COMMAND"
    echo "Use './visualize_schema.sh help' for usage information"
    exit 1
    ;;
esac

# Open HTML viewer if it exists
if [ -f "${OUTPUT_DIR}/schema_visualization.html" ]; then
  echo ""
  echo "📄 View diagrams: ${OUTPUT_DIR}/schema_visualization.html"
  
  # Try to open in browser (macOS)
  if command -v open &> /dev/null; then
    echo "🌐 Opening in browser..."
    open "${OUTPUT_DIR}/schema_visualization.html"
  fi
fi