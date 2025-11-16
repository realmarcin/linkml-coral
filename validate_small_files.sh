#!/bin/bash

# Validate smaller TSV files first (quick validation for immediate feedback)

echo "🔍 Validating smaller ENIGMA TSV files with linkml-validate..."
echo "📋 This validates files with < 10K records for quick feedback"
echo "============================================================================"

start_time=$(date +%s)

uv run python validate_tsv_linkml.py \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Location.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Protocol.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Assembly.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Sample.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Community.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Strain.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Genome.tsv \
  --max-errors 5 \
  --save-yaml small_files_yaml \
  --verbose

exit_code=$?
end_time=$(date +%s)
duration=$((end_time - start_time))

echo "============================================================================"
echo "⏱️  Validation time: ${duration} seconds"

if [ $exit_code -eq 0 ]; then
    echo "✅ Small files validation completed successfully!"
    echo "🚀 You can now run validate_large_files.sh for the larger files"
else
    echo "❌ Some files had validation errors"
fi

exit $exit_code