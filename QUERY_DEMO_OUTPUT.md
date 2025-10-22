# ENIGMA Query System - Demo Output Examples

This document shows example outputs for all available query commands.

## 1. Main Query: Unused "Good" Reads

**Command:**
```bash
just query-unused-reads 50000
```

**Output:**
```
🔍 Query: Unused 'Good' Reads
============================================================

Finding reads with >= 50,000 raw reads that were NOT used in assemblies...

🔍 Finding unused reads with min_count >= 50000...
  📊 Total 'good' reads (>= 50000 reads): 14,418
  🔗 Reads used in assemblies: 2,994
  ⚠️  Unused 'good' reads: 11,608

📊 Results:
  • Total 'good' reads: 14,418
  • Used in assemblies: 2,994
  • UNUSED 'good' reads: 11,608
  • Utilization rate: 20.8%

📈 Unused Reads Statistics:
  • Min count: 50,003
  • Max count: 549,479,714
  • Avg count: 3,729,318
  • Total wasted reads: 43,289,920,880

🔬 Top 20 Unused Reads (by count):
   1. FW106-06-10-15-10-deep
      Read count: 549,479,714 (very_high)
      Link: https://narrative.kbase.us/#dataview/26837/...
   2. FW301-06-10-15-0.2-deep
      Read count: 373,129,474 (very_high)
   ...
```

**JSON Export:**
```bash
uv run python enigma_query.py unused-reads --min-count 50000 --export results.json
```

Creates `results.json` with:
- Query metadata (type, parameters)
- Summary statistics
- Full array of 11,608 unused read records

## 2. Database Statistics

**Command:**
```bash
just query-stats
```

**Output:**
```
📊 ENIGMA Database Statistics
============================================================

============================================================
📊 ENIGMA Data Summary
============================================================

Reads:
  total: 19307
  with_counts: 19307
  min_count: 64
  max_count: 549479714
  avg_count: 4061802.81
  categories:
    low: 4889
    medium: 8181
    high: 6104
    very_high: 133

Assembly:
  total: 3427

Process:
  total: 130560

🔬 Detailed Analysis:

  Processes:
    • Total processes: 130,560
    • Assembly processes (Reads→Assembly): 3,427

  Read Utilization:
    • Total reads: 19,307
    • Used in assemblies: 2,994
    • Unused: 16,313
    • Utilization rate: 15.5%
```

## 3. Provenance Lineage

**Command:**
```bash
just query-lineage Assembly Assembly0000497
```

**Output:**
```
🔗 Provenance Lineage: Assembly Assembly0000497
============================================================

Process Chain:
  • Number of process steps: 2

Inputs:
  • Reads: 1
    - Reads0001927
  • Samples: 1
    - Sample0003804
```

**JSON Export:**
```bash
uv run python enigma_query.py lineage Assembly Assembly0000497 --export lineage.json
```

Creates JSON with:
```json
{
  "assembly_id": "Assembly0000497",
  "process_count": 2,
  "input_reads": ["Reads0001927"],
  "input_samples": ["Sample0003804"],
  "process_chain": [/* process records */]
}
```

## 4. Entity Search

**Command:**
```bash
just query-find Reads --query read_count_category=very_high --limit 5
```

**Output:**
```
🔍 Find: Reads
============================================================

Found 5 results

Results:
  1. Reads0000015
     Name: FW106-06-10-15-10-deep
     read_count_category: very_high
  2. Reads0000016
     Name: FW301-06-10-15-0.2-deep
     read_count_category: very_high
  3. Reads0000017
     Name: EB271-03-01-R2-DNA9-2018-06-05.reads
     read_count_category: very_high
  ...
```

## All Commands Summary

| Command | Output | Export Format |
|---------|--------|---------------|
| `just query-unused-reads 50000` | Terminal stats + top 20 | JSON with all results |
| `just query-stats` | Terminal statistics | N/A |
| `just query-lineage <type> <id>` | Terminal lineage | JSON with full chain |
| `just query-find <coll> --query <q>` | Terminal results | JSON array |

## Export File Examples

All JSON exports follow this structure:

**Unused Reads Export:**
```json
{
  "query": "unused_reads",
  "parameters": {"min_count": 50000},
  "summary": {/* statistics */},
  "results": [/* all unused reads */]
}
```

**Lineage Export:**
```json
{
  "assembly_id": "Assembly0000497",
  "process_count": 2,
  "input_reads": ["Reads0001927"],
  "input_samples": ["Sample0003804"],
  "process_chain": [/* process details */]
}
```

**Entity Search Export:**
```json
[
  {/* read record 1 */},
  {/* read record 2 */},
  ...
]
```

## Key Findings

**Resource Utilization (50K threshold):**
- Only **20.8%** of high-quality reads were used in assemblies
- **79.2%** of high-quality reads remain unused
- **43 BILLION** raw reads wasted
- Top unused read: 549M reads (FW106-06-10-15-10-deep)

**Database Scale:**
- 281,813 total records
- 19,307 reads (varying quality)
- 3,427 assemblies
- 130,560 process records (provenance tracking)
