# ENIGMA Query Provenance - Executive Summary

## What is Deep Provenance Tracking?

Every query executed against the ENIGMA database is automatically tracked with complete metadata to ensure:
- **Reproducibility**: Exact recreation of results
- **Audit Trail**: Who ran what query, when, and why
- **Data Integrity**: Verification that data hasn't changed
- **Scientific Rigor**: Complete documentation of analysis methods

## What Gets Recorded

### For Every Query Execution:

1. **Who** - User and system information
   - Username, hostname
   - Operating system, platform
   - Python version

2. **When** - Temporal metadata
   - Start timestamp
   - End timestamp
   - Duration (seconds)

3. **What** - Query details
   - Query type (unused_reads, lineage, etc.)
   - Parameters (min_count, entity_id, etc.)
   - Description

4. **Which Data** - Database state
   - Database file path
   - File size and SHA256 checksum
   - Last modified timestamp
   - Record counts (reads, assemblies, processes)

5. **How** - Environment
   - Python executable path
   - Package versions (linkml-store, duckdb, pandas)
   - Platform details (CPU architecture)

6. **Results** - Query outcomes
   - Summary statistics
   - Output file paths
   - Success/failure status
   - Error messages (if any)

## Example: Real Query Provenance

**Query Executed:**
```bash
uv run python enigma_query.py unused-reads --min-count 100000
```

**Provenance Recorded:**
```json
{
  "execution_id": "1e16a3d7b455ebce",
  "start_time": "2025-10-14T12:55:01",
  "duration_seconds": 35.87,
  "query_type": "unused_reads",
  "parameters": {"min_count": 100000},
  "user": {"username": "marcin", "hostname": "marcins-MacBook-Pro.local"},
  "database": {
    "checksum": "057c70e695ae94c3cd783a14acdf07d8...",
    "size_mb": 13.01
  },
  "results": {
    "unused_good_reads": 10272,
    "total_wasted_reads": 43196839740
  }
}
```

## Key Benefits

### 1. Reproducibility

Recreate exact results months or years later:
```bash
# Find original execution
uv run python query_provenance_tracker.py --list

# View parameters and database state
uv run python query_provenance_tracker.py --report 1e16a3d7b455ebce

# Verify database integrity
# (compare checksum: 057c70e695ae94c3...)

# Re-run with exact same parameters
uv run python enigma_query.py unused-reads --min-count 100000
```

### 2. Audit Trail

Complete history of all queries:
```
Date/Time            Query Type    Duration  Status   User    ID
2025-10-14 12:55:01  unused_reads  35.9s     success  marcin  1e16a3d7b455ebce
2025-10-14 13:20:15  lineage       0.4s      success  alice   f1e2d3c4b5a6987
2025-10-14 14:05:32  stats         1.8s      success  bob     a7b2c4d1e3f5g6h
```

### 3. Data Integrity

Detect if database has been modified:
- Original checksum: `057c70e695ae94c3cd783a14acdf07d8...`
- Current checksum: `057c70e695ae94c3cd783a14acdf07d8...`
- **Match!** ✓ Data is unchanged

### 4. Scientific Publication

Include in methods section:
> "Queries were executed using enigma_query.py v1.0 (execution ID: 1e16a3d7b455ebce) on a database
> with SHA256 checksum 057c70e6... containing 19,307 reads and 3,427 assemblies. The query identified
> 10,272 unused high-quality reads (≥100K reads) representing 43.2 billion wasted sequencing reads."

## Usage

### Automatic Tracking (Default)

Just run queries normally - provenance is tracked automatically:
```bash
just query-unused-reads 50000
# Provenance automatically saved to: query_provenance/20251014_..._.json
```

### View History

```bash
# List all executions
uv run python query_provenance_tracker.py --list

# Generate detailed report
uv run python query_provenance_tracker.py --report <execution_id>
```

### Programmatic Access

```python
from query_provenance_tracker import QueryProvenanceTracker

# Load execution metadata
metadata = QueryProvenanceTracker.load_provenance("1e16a3d7b455ebce")

# Access any field
print(f"Duration: {metadata['execution']['duration_seconds']:.1f}s")
print(f"Results: {metadata['results']['unused_good_reads']} unused reads")
print(f"Database: {metadata['database']['checksum']}")
```

## File Locations

All provenance records stored in: `query_provenance/`

**Files created:**
- `20251014_125537_unused_reads_1e16a3d7b455ebce.json` - Full record
- `latest_unused_reads.json` - Most recent unused_reads query
- `latest_lineage.json` - Most recent lineage query
- `latest_stats.json` - Most recent stats query

## Comparison with Traditional Approaches

| Feature | Without Provenance | With Deep Provenance |
|---------|-------------------|----------------------|
| Who ran query | Unknown | Username, hostname recorded |
| When executed | Unknown | Precise timestamp |
| What parameters | Must remember | Automatically recorded |
| Database version | Unknown | SHA256 checksum |
| Reproducible | No | Yes, fully |
| Audit trail | No | Complete history |
| Environment | Unknown | Python version, packages |
| Results verification | Manual | Automatic checksum comparison |

## Real-World Example

**Scenario**: Six months after initial analysis, reviewer asks: "How did you get those results?"

**Without Provenance:**
- Uncertainty about exact parameters used
- Can't verify database hasn't changed
- Don't remember which Python version
- Results may not be reproducible

**With Provenance:**
```bash
# 1. Find the execution
uv run python query_provenance_tracker.py --list | grep "2025-04"

# 2. Get full details
uv run python query_provenance_tracker.py --report a1b2c3d4e5f6g7h8

# Output shows:
# - Exact parameters: min_count=50000
# - Database checksum: 057c70e6...
# - Python 3.13.8, linkml-store 0.2.11
# - Results: 11,608 unused reads

# 3. Verify database integrity
sha256sum enigma_data.db
# Matches! Database unchanged.

# 4. Re-run exact query
uv run python enigma_query.py unused-reads --min-count 50000

# 5. Results match exactly ✓
```

## Documentation

- **Complete Guide**: [DEPLOYMENT_PROVENANCE.md](DEPLOYMENT_PROVENANCE.md)
- **Query Reference**: [QUERY_REFERENCE.md](QUERY_REFERENCE.md)
- **Usage Guide**: [LINKML_STORE_USAGE.md](LINKML_STORE_USAGE.md)

## Summary

Deep provenance tracking provides:
✓ **Automatic** - No extra commands needed
✓ **Complete** - Full system state captured
✓ **Permanent** - Records saved as JSON files
✓ **Reproducible** - Exact recreation of results
✓ **Auditable** - Complete history of all queries
✓ **Scientific** - Meets publication standards

Every query you run creates a permanent, verifiable record of exactly what was done, when, by whom, and with what results.
