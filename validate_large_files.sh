#!/bin/bash

# Validate larger TSV files (may take several minutes)

echo "🔍 Validating large ENIGMA TSV files with linkml-validate..."
echo "⚠️  This may take 5-15 minutes for large files"
echo "============================================================================"

start_time=$(date +%s)

echo "📊 Validating Reads.tsv (19K records)..."
uv run python validate_tsv_linkml.py \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Reads.tsv \
  --max-errors 5 \
  --save-yaml large_files_yaml

echo ""
echo "📊 Validating ASV.tsv (112K records)..."
uv run python validate_tsv_linkml.py \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/ASV.tsv \
  --max-errors 5 \
  --save-yaml large_files_yaml

echo ""
echo "📊 Validating Process.tsv (131K records)..."
uv run python validate_tsv_linkml.py \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Process.tsv \
  --max-errors 5 \
  --save-yaml large_files_yaml

echo ""
echo "📊 Checking ASV_count.tsv (no schema mapping)..."
uv run python validate_tsv_linkml.py \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/ASV_count.tsv \
  --max-errors 5

exit_code=$?
end_time=$(date +%s)
duration=$((end_time - start_time))

echo "============================================================================"
echo "⏱️  Total validation time: ${duration} seconds"

if [ $exit_code -eq 0 ]; then
    echo "✅ Large files validation completed successfully!"
else
    echo "❌ Some files had validation errors"
fi

echo "📋 All validation outputs saved to: large_files_yaml/"

exit $exit_code