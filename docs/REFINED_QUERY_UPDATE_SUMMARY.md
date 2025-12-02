# Refined Query Update Summary

## Overview

This document summarizes the updates made to add refined query capabilities for filtering ENIGMA reads by type, specifically to identify isolate genome assembly candidates.

## What Was Added

### 1. Query Filtering Capabilities

**New Command-Line Flags:**
- `--exclude-16s`: Filter to only Single End reads (ME:0000114) - isolate genome sequencing data
- `--read-type <TYPE>`: Filter by specific read type (ME:0000114, ME:0000113, ME:0000112)

**Read Type Classification:**
- **ME:0000114** - Single End Read (isolate genome sequencing)
  - 1,840 reads ≥50K threshold
  - 1,836 unused (99.8%!)
  - Perfect candidates for genome assembly

- **ME:0000113** - Paired End Read (metagenome/16S sequencing)
  - 9,640 reads ≥50K threshold
  - 7,768 unused (80.6%)
  - Community diversity analysis

- **ME:0000112** - Generic Read Type (metatranscriptome)
  - 2,938 reads ≥50K threshold
  - Gene expression analysis

### 2. New Justfile Commands

Added to `project.justfile`:

```bash
# Query unused isolate genome reads
just query-unused-isolates 50000

# Query unused metagenome/16S reads
just query-unused-metagenomes 50000
```

### 3. Updated Documentation

**QUERY_REFERENCE.md**:
- Added refined query examples
- Included read type codes and descriptions
- Updated Common Workflows section with read type comparisons
- Enhanced Python API examples with filtering parameters

**LINKML_STORE_USAGE.md**:
- Added read type filtering examples
- Included read type classification
- Added links to refined query analysis

**QUERY_COMMANDS_SUMMARY.txt**:
- Added new justfile commands
- Included comparative results by read type
- Updated documentation links

**REFINED_QUERY_ANALYSIS.md** (new):
- Complete analysis of read types
- Comparative results across all read types
- Scientific impact assessment
- Usage examples and recommendations

### 4. Code Updates

**query_enigma_provenance.py**:
```python
def get_unused_reads(
    self,
    min_count: int = 10000,
    return_details: bool = True,
    read_type: Optional[str] = None,      # NEW
    exclude_16s: bool = False              # NEW
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
```

**enigma_query.py**:
- Added `--exclude-16s` argument
- Added `--read-type` argument
- Integrated filtering into provenance tracking
- Updated descriptions based on filter parameters

### 5. Provenance Tracking Enhancement

All refined queries are fully tracked with:
- Filter parameters (exclude_16s, read_type)
- Updated descriptions indicating filtering
- Complete execution metadata

Example provenance record:
```json
{
  "execution": {
    "execution_id": "4b5bebb97a960f2f",
    "description": "Find unused reads with >= 50000 raw reads (isolate genome reads only)",
    "parameters": {
      "min_count": 50000,
      "exclude_16s": true
    }
  },
  "results": {
    "total_good_reads": 1840,
    "unused_good_reads": 1836,
    "utilization_rate": 1.6271739130434784
  }
}
```

## Key Findings

### Comparative Results (50K threshold)

| Read Type | Total | Unused | % Unused | Wasted Reads |
|-----------|-------|--------|----------|--------------|
| **All reads** | 14,418 | 11,608 | 79.2% | 43.3 billion |
| **Isolate genomes** (ME:0000114) | 1,840 | 1,836 | **99.8%** | 230.5 million |
| **Metagenomes** (ME:0000113) | 9,640 | 7,768 | 80.6% | 25.0 billion |

### Scientific Impact

**Isolate Genome Assembly Opportunity:**
- 1,836 unused isolate genome read sets identified
- Average read count: 125,553 (sufficient for good assembly)
- Maximum read count: 4,078,972 (excellent coverage)
- Each represents a unique environmental bacterial strain
- Could significantly expand ENIGMA genome collection

**Top Unused Isolate Genome Reads:**
1. FW305-C-52-trim.reads_unpaired_fwd - 4,078,972 reads
2. FW305-C-35-trim.reads_unpaired_fwd - 3,618,897 reads
3. FW305-C-101-trim.reads_unpaired_fwd - 2,075,026 reads
4. FW305-C-134A-trim.reads_unpaired_fwd - 1,976,395 reads
5. MT66-cutadapt-trim.reads_unpaired_fwd - 1,932,179 reads

## Usage Examples

### Command-Line

```bash
# Find unused isolate genome reads
just query-unused-isolates 50000

# Find unused metagenome reads
just query-unused-metagenomes 50000

# Export isolate genome candidates for assembly pipeline
uv run python enigma_query.py unused-reads --min-count 50000 --exclude-16s --export isolate_genomes.json

# Compare all read types
./read_type_comparison.sh
```

### Python API

```python
from query_enigma_provenance import ENIGMAProvenanceQuery

query = ENIGMAProvenanceQuery("enigma_data.db")

# Get unused isolate genome reads
isolate_reads, summary = query.get_unused_reads(
    min_count=50000,
    return_details=True,
    exclude_16s=True
)

print(f"Unused isolate genomes: {summary['unused_good_reads']}")
print(f"Average read count: {summary['unused_stats']['avg_count']:,.0f}")

# Get unused metagenome reads
meta_reads, meta_summary = query.get_unused_reads(
    min_count=50000,
    return_details=True,
    read_type='ME:0000113'
)

print(f"Unused metagenomes: {meta_summary['unused_good_reads']}")
```

## Testing

All commands have been tested and verified:

```bash
✅ just query-unused-isolates 50000
   - Returns 1,836 unused isolate genome reads
   - Properly filters to ME:0000114 (Single End)
   - Provenance tracked correctly

✅ just query-unused-metagenomes 50000
   - Returns 7,768 unused metagenome reads
   - Properly filters to ME:0000113 (Paired End)
   - Provenance tracked correctly

✅ uv run python enigma_query.py unused-reads --min-count 50000 --read-type ME:0000114
   - Same results as --exclude-16s flag
   - Explicit type filtering works correctly
```

## Files Modified

1. **query_enigma_provenance.py** - Added filtering logic to get_unused_reads()
2. **enigma_query.py** - Added CLI arguments and description updates
3. **project.justfile** - Added convenience commands
4. **QUERY_REFERENCE.md** - Updated with refined query examples
5. **LINKML_STORE_USAGE.md** - Added read type filtering documentation
6. **QUERY_COMMANDS_SUMMARY.txt** - Updated with new commands and results

## Files Created

1. **REFINED_QUERY_ANALYSIS.md** - Complete analysis of read type refinement
2. **read_type_comparison.sh** - Script to compare results across read types
3. **REFINED_QUERY_UPDATE_SUMMARY.md** (this file) - Summary of updates

## Next Steps (Recommendations)

1. **Genome Assembly Pipeline**: Use the 1,836 unused isolate genome reads for de novo assembly
2. **Quality Analysis**: Analyze read quality metrics for assembly candidates
3. **Batch Processing**: Create workflow to assemble top N isolate genomes
4. **Stakeholder Report**: Generate report for ENIGMA team about unused resources

## See Also

- [REFINED_QUERY_ANALYSIS.md](REFINED_QUERY_ANALYSIS.md) - Complete read type analysis
- [QUERY_REFERENCE.md](QUERY_REFERENCE.md) - Full query command reference
- [DEPLOYMENT_PROVENANCE.md](DEPLOYMENT_PROVENANCE.md) - Provenance tracking guide
- [LINKML_STORE_USAGE.md](LINKML_STORE_USAGE.md) - Database usage guide
