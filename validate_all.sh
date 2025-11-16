#!/bin/bash

# Validate all TSV files in ENIGMA_ASV_export directory using linkml-validate

echo "🔍 Starting comprehensive validation of all ENIGMA TSV files..."
echo "📁 Directory: /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/"
echo "🚀 Using linkml-validate engine"
echo "============================================================================"

# Record start time
start_time=$(date +%s)

# Run validation on all TSV files
uv run python validate_tsv_linkml.py \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/ASV.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/ASV_count.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Assembly.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Community.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Genome.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Location.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Process.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Protocol.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Reads.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Sample.tsv \
  /Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export/Strain.tsv \
  --max-errors 10 \
  --save-yaml validation_output_yaml \
  --timeout 1800

# Capture exit code
exit_code=$?

# Record end time and calculate duration
end_time=$(date +%s)
duration=$((end_time - start_time))

echo "============================================================================"
echo "⏱️  Total validation time: ${duration} seconds"

if [ $exit_code -eq 0 ]; then
    echo "🎉 All TSV files validated successfully!"
else
    echo "⚠️  Validation completed with errors (exit code: $exit_code)"
fi

echo "📋 Validation outputs saved to: validation_output_yaml/"
echo "📊 Run this command to see the summary:"
echo "    ls -la validation_output_yaml/"

exit $exit_code