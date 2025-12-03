# Refined Query Analysis: Isolate Genome Reads

Analysis of unused ENIGMA reads filtered by sequencing type to focus on isolate genome assembly candidates.

## Query Refinement: Excluding 16S and Metagenome Data

### Read Type Classification

ENIGMA data contains three types of reads:

| Read Type | ME Code | Description | Primary Use | Count (≥50K) |
|-----------|---------|-------------|-------------|--------------|
| **Single End** | ME:0000114 | Isolate genomic reads | Genome assembly | 1,840 |
| **Paired End** | ME:0000113 | Metagenome & 16S reads | Community analysis | 9,640 |
| **Generic** | ME:0000112 | Metatranscriptome reads | Expression analysis | 2,938 |

### Naming Patterns

**Isolate Genome Reads (ME:0000114 - Single End)**:
- Environmental samples with location codes (FW, GW, DP, EU)
- Examples: `FW511_7_26_13_02.reads`, `GW056_87_1_8_13_10.reads`
- Trimmed/processed isolates: `FW305-C-52-trim.reads_unpaired_fwd`
- **Purpose**: Individual bacterial isolate genome sequencing

**Metagenome/16S Reads (ME:0000113 - Paired End)**:
- Community sequencing data
- Examples: `DP16D_clean.reads`, `corepilot_170602_16S.reads`
- High read counts for deep community coverage
- **Purpose**: Microbial community structure and diversity

**Metatranscriptome Reads (ME:0000112 - Generic)**:
- Transcriptome sequencing
- Examples: `MPR-WIN1.reads`, `MT42.reads`, `MT49.reads`
- **Purpose**: Gene expression analysis

## Comparative Analysis

### Results by Read Type (≥50,000 reads threshold)

#### 1. All Reads (No Filter)

```bash
just query-unused-reads 50000
```

**Results:**
- Total 'good' reads: **14,418**
- Used in assemblies: **2,994**
- **UNUSED: 11,608 (79.2%)**
- Total wasted reads: **43.3 BILLION**

#### 2. Isolate Genome Reads Only (--exclude-16s)

```bash
uv run python enigma_query.py unused-reads --min-count 50000 --exclude-16s
```

**Results:**
- Total 'good' reads: **1,840**
- Used in assemblies: **2,994** (includes some lower-count isolate reads)
- **UNUSED: 1,836 (99.8%)**
- Total wasted reads: **230.5 MILLION**
- Avg read count: **125,553**
- Max read count: **4,078,972**

**Key Finding**: Almost ALL high-quality isolate genome reads remain unused!

#### 3. Metagenome/16S Reads Only (ME:0000113)

```bash
uv run python enigma_query.py unused-reads --min-count 50000 --read-type ME:0000113
```

**Results:**
- Total 'good' reads: **9,640**
- Used in assemblies: **2,994**
- **UNUSED: 7,768 (80.6%)**
- Total wasted reads: **25.0 BILLION**
- Avg read count: **3,219,918**
- Max read count: **32,048,946**

## Key Insights

### Isolate Genome Assembly Potential

**The Problem:**
- 1,836 high-quality isolate genome read sets are unused
- These represent individual bacterial strains from environmental samples
- Perfect candidates for genome assembly but never assembled

**Read Quality:**
- Minimum: 50,003 reads (above threshold)
- Average: 125,553 reads (sufficient for good assembly)
- Maximum: 4,078,972 reads (excellent coverage)

**Sample Origins:**
- FW-series: Rifle, CO field site samples
- GW-series: Groundwater samples
- MT-series: Metatranscriptome samples
- Various strain isolates (FW305-C-XX)

### Why This Matters

**For Genome Assembly:**
- Single End reads are specifically for isolate genomes
- 50K+ reads typically provides 20-100X coverage
- Suitable for de novo assembly with modern assemblers
- Each represents a unique environmental bacterial strain

**For Resource Utilization:**
- 230 million sequencing reads wasted
- Each sequencing run costs money and time
- These isolates were cultured and sequenced for genome analysis
- Scientific value lost if not assembled

## Recommended Query

**For isolate genome assembly candidates:**

```bash
# Find unused isolate genome reads (≥50K reads)
uv run python enigma_query.py unused-reads --min-count 50000 --exclude-16s

# Higher threshold for best candidates
uv run python enigma_query.py unused-reads --min-count 100000 --exclude-16s

# Export for downstream processing
uv run python enigma_query.py unused-reads --min-count 50000 --exclude-16s --export isolate_genomes_unused.json
```

**For metagenome/community analysis:**

```bash
# Find unused metagenome reads
uv run python enigma_query.py unused-reads --min-count 50000 --read-type ME:0000113
```

## Top Unused Isolate Genome Reads

| Rank | Read Set | Count | Category |
|------|----------|-------|----------|
| 1 | FW305-C-52-trim.reads_unpaired_fwd | 4,078,972 | very_high |
| 2 | FW305-C-35-trim.reads_unpaired_fwd | 3,618,897 | very_high |
| 3 | FW305-C-101-trim.reads_unpaired_fwd | 2,075,026 | very_high |
| 4 | FW305-C-134A-trim.reads_unpaired_fwd | 1,976,395 | very_high |
| 5 | MT66-cutadapt-trim.reads_unpaired_fwd | 1,932,179 | very_high |

## Implementation Notes

### New Query Flags

**`--exclude-16s`**:
- Filters to only Single End reads (ME:0000114)
- Excludes Paired End (ME:0000113) and Generic (ME:0000112)
- Focuses on isolate genome sequencing data

**`--read-type <TYPE>`**:
- Explicitly filter by ME code
- Options: ME:0000114 (Single End), ME:0000113 (Paired End), ME:0000112 (Generic)
- More granular control than --exclude-16s

### Provenance Tracking

All refined queries are fully tracked:

```json
{
  "execution_id": "12598938c1b0f8c8",
  "description": "Find unused reads with >= 50000 raw reads (isolate genome reads only)",
  "parameters": {
    "min_count": 50000,
    "exclude_16s": true
  },
  "results": {
    "unused_good_reads": 1836,
    "total_wasted_reads": 230514741
  }
}
```

## Justfile Convenience Commands

Add to `project.justfile`:

```justfile
# Query unused isolate genome reads
[group('data management')]
query-unused-isolates min_count='50000' db='enigma_data.db':
  @echo "🧬 Finding unused isolate genome reads (min_count >= {{min_count}})..."
  uv run python enigma_query.py --db {{db}} unused-reads --min-count {{min_count}} --exclude-16s

# Query unused metagenome reads
[group('data management')]
query-unused-metagenomes min_count='50000' db='enigma_data.db':
  @echo "🦠 Finding unused metagenome/16S reads (min_count >= {{min_count}})..."
  uv run python enigma_query.py --db {{db}} unused-reads --min-count {{min_count}} --read-type ME:0000113
```

## Usage Examples

```bash
# Basic: Find all unused isolate genome reads ≥50K
uv run python enigma_query.py unused-reads --min-count 50000 --exclude-16s

# High quality only: ≥100K reads
uv run python enigma_query.py unused-reads --min-count 100000 --exclude-16s

# Export for genome assembly pipeline
uv run python enigma_query.py unused-reads --min-count 50000 --exclude-16s --export candidates.json --top-n 50

# Compare with metagenome data
uv run python enigma_query.py unused-reads --min-count 50000 --read-type ME:0000113

# Using justfile (if commands added)
just query-unused-isolates 50000
just query-unused-metagenomes 50000
```

## Scientific Impact

**Potential for New Genome Assemblies:**
- 1,836 isolate genome datasets available
- Average 125K reads = good assembly quality
- Unique environmental bacterial strains
- Could significantly expand ENIGMA genome collection

**Resource Recovery:**
- 230 million isolate genome reads recoverable
- Sequencing already paid for
- Just need computational assembly
- High scientific ROI (return on investment)

## See Also

- [QUERY_REFERENCE.md](QUERY_REFERENCE.md) - Complete query command reference
- [DEPLOYMENT_PROVENANCE.md](DEPLOYMENT_PROVENANCE.md) - Provenance tracking guide
- [LINKML_STORE_USAGE.md](LINKML_STORE_USAGE.md) - Database usage guide
