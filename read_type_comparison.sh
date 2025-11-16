#!/bin/bash
echo "=== ENIGMA Reads Analysis by Type ==="
echo ""

echo "1. All Reads (no filter):"
uv run python enigma_query.py --db enigma_data.db unused-reads --min-count 50000 --top-n 0 2>&1 | grep -E "(Total 'good'|Used in|UNUSED|Utilization|Total wasted)"

echo ""
echo "2. Isolate Genome Reads Only (Single End, ME:0000114):"
uv run python enigma_query.py --db enigma_data.db unused-reads --min-count 50000 --exclude-16s --top-n 0 2>&1 | grep -E "(Total 'good'|Used in|UNUSED|Utilization|Total wasted)"

echo ""
echo "3. Metagenome/16S Reads (Paired End, ME:0000113):"
uv run python enigma_query.py --db enigma_data.db unused-reads --min-count 50000 --read-type ME:0000113 --top-n 0 2>&1 | grep -E "(Total 'good'|Used in|UNUSED|Utilization|Total wasted)"
