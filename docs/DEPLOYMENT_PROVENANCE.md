# ENIGMA Query System - Deployment & Provenance Tracking

Complete guide for deploying the ENIGMA query system with deep provenance tracking.

## Table of Contents

- [System Overview](#system-overview)
- [Deployment Steps](#deployment-steps)
- [Provenance Tracking](#provenance-tracking)
- [Query Execution Records](#query-execution-records)
- [Reproducibility](#reproducibility)
- [Auditing & Compliance](#auditing--compliance)

## System Overview

The ENIGMA query system provides:
- **Data Layer**: LinkML-Store database with 281K records
- **Query Layer**: Python CLI and API for provenance-aware queries
- **Provenance Layer**: Complete execution metadata tracking
- **Reproducibility**: Full system state capture for result verification

### Components

1. **Database**: `enigma_data.db` (DuckDB, 13 MB)
2. **Query Interface**: `enigma_query.py` CLI
3. **Provenance Tracker**: `query_provenance_tracker.py`
4. **Query Records**: JSON files in `query_provenance/`

## Deployment Steps

### Step 1: Environment Setup

```bash
# Clone repository
cd /path/to/linkml-coral

# Install dependencies
uv sync

# Verify installation
uv run python -c "import linkml_store; print('✓ linkml-store installed')"
```

**Record**: Document repository commit hash:
```bash
git rev-parse HEAD > deployment/commit_hash.txt
git log -1 --format="%H %ci %s" > deployment/commit_info.txt
```

### Step 2: Database Creation

```bash
# Load ENIGMA data
just load-store

# Verify database
uv run python enigma_query.py stats

# Record database metadata
ls -lh enigma_data.db
sha256sum enigma_data.db > deployment/database_checksum.txt
stat enigma_data.db > deployment/database_stats.txt
```

**Provenance Record**:
- Database file: `enigma_data.db`
- Source TSV directory: `/Users/marcin/Documents/KBase/CDM/ENIGMA/ENIGMA_ASV_export`
- Load date: 2025-10-14
- Schema version: `src/linkml_coral/schema/linkml_coral.yaml`
- Total records: 281,813

### Step 3: Test Query Execution

```bash
# Run test query with provenance tracking
uv run python enigma_query.py unused-reads --min-count 50000

# Verify provenance record created
ls -l query_provenance/

# View execution history
uv run python query_provenance_tracker.py --list
```

### Step 4: Deployment Verification

```bash
# Create deployment manifest
cat > deployment/manifest.json << EOF
{
  "deployment_date": "$(date -Iseconds)",
  "git_commit": "$(git rev-parse HEAD)",
  "git_branch": "$(git branch --show-current)",
  "database_file": "enigma_data.db",
  "database_size_mb": $(stat -f%z enigma_data.db | awk '{print $1/1024/1024}'),
  "database_checksum": "$(shasum -a 256 enigma_data.db | awk '{print $1}')",
  "python_version": "$(python3 --version)",
  "system": "$(uname -s)",
  "hostname": "$(hostname)"
}
EOF
```

## Provenance Tracking

Every query execution is automatically tracked with complete metadata.

### What is Tracked

**Execution Metadata**:
- Unique execution ID (16-character hash)
- Query type (`unused_reads`, `lineage`, `stats`, `find`)
- Parameters (min_count, entity_id, etc.)
- Start/end timestamps
- Duration in seconds
- Success/failure status

**User & System**:
- Username
- Hostname
- Operating system and platform
- Python version and executable path

**Database State**:
- Database file path
- File size and checksum (SHA256)
- Last modified timestamp
- Record counts at execution time

**Environment**:
- Python packages (linkml-store, duckdb, pandas versions)
- Platform information

**Results**:
- Summary statistics from query
- Output file paths (if exported)
- Error messages (if failed)

### Provenance Directory Structure

```
query_provenance/
├── 20251014_125537_unused_reads_1e16a3d7b455ebce.json
├── 20251014_130045_unused_reads_a7b2c4d1e3f5g6h7.json
├── 20251014_131220_lineage_f1e2d3c4b5a6987.json
├── latest_unused_reads.json  # Most recent unused_reads query
├── latest_lineage.json        # Most recent lineage query
└── latest_stats.json          # Most recent stats query
```

**Naming Convention**: `YYYYMMDD_HHMMSS_querytype_executionid.json`

### Provenance Record Structure

```json
{
  "execution": {
    "execution_id": "1e16a3d7b455ebce",
    "start_time": "2025-10-14T12:55:01.546537",
    "end_time": "2025-10-14T12:55:37.416499",
    "duration_seconds": 35.87,
    "query_type": "unused_reads",
    "description": "Find unused reads with >= 100000 raw reads",
    "parameters": {"min_count": 100000, "top_n": 5},
    "status": "success"
  },
  "user": {
    "username": "marcin",
    "hostname": "marcins-MacBook-Pro.local",
    "platform": "macOS-13.7.8-arm64-arm-64bit-Mach-O",
    "python_version": "3.13.8 (main, Oct 10 2025...)"
  },
  "database": {
    "path": "enigma_data.db",
    "size_mb": 13.01,
    "checksum": "057c70e695ae94c3cd783a14acdf07d8...",
    "last_modified": "2025-10-14T12:29:25.287121"
  },
  "database_stats": {
    "total_reads": 19307,
    "total_assemblies": 3427,
    "total_processes": 130560
  },
  "environment": {
    "python_executable": ".venv/bin/python3",
    "platform_info": {"system": "Darwin", "machine": "arm64"},
    "key_packages": {
      "linkml-store": "0.2.11",
      "duckdb": "1.4.1",
      "pandas": "2.3.3"
    }
  },
  "results": {
    "total_good_reads": 13020,
    "unused_good_reads": 10272,
    "utilization_rate": 0.23,
    "unused_stats": {
      "total_wasted_reads": 43196839740
    }
  }
}
```

## Query Execution Records

### Viewing Execution History

```bash
# List all executions
uv run python query_provenance_tracker.py --list

# Output:
# Date/Time            Query Type    Duration  Status   User    ID
# 2025-10-14 12:55:01  unused_reads  35.9s     success  marcin  1e16a3d7b455ebce
```

### Generating Provenance Reports

```bash
# Generate human-readable report
uv run python query_provenance_tracker.py --report 1e16a3d7b455ebce

# Save report to file
uv run python query_provenance_tracker.py --report 1e16a3d7b455ebce > reports/query_1e16a3d7b455ebce.txt
```

### Programmatic Access

```python
from query_provenance_tracker import QueryProvenanceTracker

# Load a specific execution
metadata = QueryProvenanceTracker.load_provenance("1e16a3d7b455ebce")

print(f"Query: {metadata['execution']['query_type']}")
print(f"Date: {metadata['execution']['start_time']}")
print(f"Results: {metadata['results']['unused_good_reads']} unused reads")
print(f"Database checksum: {metadata['database']['checksum']}")

# List all executions
executions = QueryProvenanceTracker.list_executions()
for exec in executions:
    print(f"{exec['start_time']}: {exec['query_type']} - {exec['status']}")
```

## Reproducibility

### Verifying Query Results

To verify that a query can be reproduced:

1. **Check database integrity**:
   ```bash
   # Compare checksums
   EXEC_ID="1e16a3d7b455ebce"
   RECORDED_CHECKSUM=$(jq -r '.database.checksum' query_provenance/${EXEC_ID}.json)
   CURRENT_CHECKSUM=$(shasum -a 256 enigma_data.db | awk '{print $1}')

   if [ "$RECORDED_CHECKSUM" == "$CURRENT_CHECKSUM" ]; then
       echo "✓ Database unchanged"
   else
       echo "⚠ Database has been modified"
   fi
   ```

2. **Re-run with same parameters**:
   ```bash
   # Extract parameters from provenance record
   MIN_COUNT=$(jq -r '.execution.parameters.min_count' query_provenance/latest_unused_reads.json)

   # Re-execute
   uv run python enigma_query.py unused-reads --min-count $MIN_COUNT
   ```

3. **Compare results**:
   ```bash
   # Compare result statistics
   jq '.results' query_provenance/${EXEC_ID}_rerun.json > results_rerun.json
   jq '.results' query_provenance/${EXEC_ID}.json > results_original.json
   diff results_original.json results_rerun.json
   ```

### Long-term Preservation

For archival and long-term reproducibility:

```bash
# Create reproducibility package
mkdir -p archives/$(date +%Y%m%d)_enigma_query

# Include all necessary components
cp enigma_data.db archives/.../
cp -r query_provenance/ archives/.../
cp src/linkml_coral/schema/linkml_coral.yaml archives/.../
cp enigma_query.py query_enigma_provenance.py query_provenance_tracker.py archives/.../

# Document environment
uv pip list > archives/.../requirements.txt
git log -1 > archives/.../git_commit.txt

# Create archive
tar czf enigma_query_$(date +%Y%m%d).tar.gz archives/$(date +%Y%m%d)_enigma_query/
```

## Auditing & Compliance

### Query Audit Trail

All queries are automatically logged with:
- Who ran the query (username, hostname)
- When it was run (timestamp)
- What was queried (type, parameters)
- What data was accessed (database checksum, size)
- What results were obtained (summary statistics)

### Compliance Features

**Data Integrity**:
- Database checksums verify data hasn't changed
- Timestamps track when database was last modified
- Record counts ensure completeness

**Execution Tracking**:
- Every query gets unique execution ID
- All parameters recorded
- Success/failure status logged
- Duration tracked for performance analysis

**User Attribution**:
- Username and hostname captured
- Platform information recorded
- Python environment documented

### Generating Audit Reports

```bash
# Monthly audit report
MONTH="2025-10"
cat > audit_reports/${MONTH}_audit.md << EOF
# Query Audit Report - ${MONTH}

$(uv run python query_provenance_tracker.py --list | grep "^${MONTH}")

## Summary
- Total Queries: $(ls query_provenance/${MONTH}*.json | wc -l)
- Unique Users: $(jq -r '.user.username' query_provenance/${MONTH}*.json | sort -u | wc -l)
- Success Rate: $(jq -r 'select(.execution.status=="success")' query_provenance/${MONTH}*.json | wc -l)

## Query Types
$(jq -r '.execution.query_type' query_provenance/${MONTH}*.json | sort | uniq -c)
EOF
```

## Best Practices

### For Each Deployment

1. **Document the deployment**:
   - Git commit hash
   - Database source and date
   - Environment details

2. **Verify integrity**:
   - Run test queries
   - Check provenance records
   - Compare with expected results

3. **Archive provenance**:
   - Back up query_provenance/ directory
   - Store with database snapshot
   - Include deployment manifest

### For Each Query Execution

1. **Review provenance record**:
   - Check execution completed successfully
   - Verify parameters are correct
   - Note execution ID for future reference

2. **Export important results**:
   - Use `--export` flag for JSON output
   - Include execution ID in export
   - Store exports with provenance records

3. **Document findings**:
   - Link to execution ID in reports
   - Include key statistics
   - Note any anomalies

## Troubleshooting

**Missing provenance records**:
- Check `query_provenance/` directory exists
- Verify write permissions
- Ensure `--provenance-dir` parameter is correct

**Checksum mismatches**:
- Database has been modified since query
- Re-load from source TSV files
- Verify database integrity

**Cannot reproduce results**:
- Database version changed
- Different linkml-store version
- Check environment differences in provenance record

## See Also

- [QUERY_REFERENCE.md](QUERY_REFERENCE.md) - Query command reference
- [LINKML_STORE_USAGE.md](LINKML_STORE_USAGE.md) - Database usage guide
- [CLAUDE.md](CLAUDE.md) - Main project documentation
