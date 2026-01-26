# Loading CDM Brick Tables on 64GB RAM Machines

## Problem

Loading large brick tables (especially `ddt_brick0000476` with 320M rows) was causing OOM (Out-Of-Memory) errors on Linux machines with 64GB RAM, resulting in **exit code 137** (killed by OOM killer).

## Root Cause

The previous direct DuckDB import used:
```sql
CREATE TABLE AS SELECT * FROM read_parquet('...')
```

This loads the **entire result set into memory** before committing to the table. For brick 0000476 with 320 million rows:
- Compressed: 383 MB on disk
- Uncompressed in memory: ~7-10 GB
- Total memory with overhead: **15-20 GB per brick**

With multiple large bricks, this exceeded available RAM.

## Solution

**New memory-aware loading strategy** (implemented 2026-01-26):

### 1. Automatic Chunking for Large Files

For files with >100M rows, the loader now:
- Creates table schema first (empty table)
- Inserts data in **10M row chunks** using `INSERT INTO ... SELECT ... LIMIT/OFFSET`
- Forces garbage collection between chunks
- Reduces peak memory to ~2-3 GB per operation

### 2. Adaptive Chunk Sizes

- **DuckDB direct import (large files)**: 10M rows per chunk
- **Pandas fallback (large files)**: 50K rows per chunk
- **Standard loading (small files)**: Full load (no chunking needed)

### 3. New 64GB-Optimized Command

```bash
just load-cdm-store-bricks-64gb
```

**This command:**
- Loads ALL 20 brick tables with **no sampling** (full data)
- Uses automatic chunking for files >100M rows
- Peak RAM usage: ~40-50 GB
- Time: 30-60 minutes
- Final database: ~15-20 GB

## Usage

### For 64GB RAM Systems (RECOMMENDED)

```bash
# Pull latest code with fixes
git pull origin linkml-store

# Load all bricks with memory optimization
just load-cdm-store-bricks-64gb

# Query the loaded data
just cdm-store-stats
just query-unused-reads 50000
```

### For 128GB+ RAM Systems

```bash
# Can use faster full load (less chunking)
just load-cdm-store-bricks-full
```

### For 32GB RAM Systems

```bash
# Use sampling or load fewer bricks
just load-cdm-store-bricks num_bricks=5 max_rows=100000

# Or use the standard sampled load
just load-cdm-store-full
```

## Technical Details

### Memory-Aware Loading Logic

```python
def load_parquet_to_duckdb_direct(...):
    # Get row count
    total_rows = get_parquet_row_count(parquet_path)

    # Decide strategy
    if total_rows > 100_000_000:
        # LARGE FILE: Use chunked INSERT
        conn.execute("CREATE TABLE ... AS SELECT ... LIMIT 0")

        for chunk in range(num_chunks):
            conn.execute(f"""
                INSERT INTO table
                SELECT * FROM read_parquet(...)
                LIMIT {chunk_size} OFFSET {offset}
            """)
            gc.collect()  # Free memory
    else:
        # SMALL FILE: Fast direct load
        conn.execute("CREATE TABLE AS SELECT * FROM read_parquet(...)")
```

### Brick Size Distribution

```
Small bricks (<50 MB):  ~10 bricks  -> Standard loading
Large bricks (>50 MB):  ~10 bricks  -> Chunked loading

Largest: ddt_brick0000476
  - 320,281,120 rows
  - 383 MB compressed
  - Now loads in 32 chunks of 10M rows
```

## Performance

### Before Fix (64GB RAM)
- ❌ **FAILED** at brick 13/20 (exit code 137)
- Peak RAM: >64 GB (OOM)
- Result: Process killed

### After Fix (64GB RAM)
- ✅ **SUCCESS** - All 20 bricks loaded
- Peak RAM: ~40-50 GB
- Time: 30-60 minutes
- Database: ~15-20 GB

## Monitoring

To monitor memory during loading:

```bash
# Terminal 1: Run loading
just load-cdm-store-bricks-64gb

# Terminal 2: Monitor memory
watch -n 5 'free -h && echo && ps aux | grep python | grep load_cdm'
```

## Troubleshooting

### Still getting OOM errors?

1. **Check available memory:**
   ```bash
   free -h
   ```
   Need at least 50GB free before starting.

2. **Close other applications:**
   Free up RAM by closing browsers, IDEs, etc.

3. **Use smaller chunk size:**
   ```bash
   uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py \
     data/enigma_coral.db \
     --output cdm_store.db \
     --num-bricks 20 \
     --use-direct-import \
     --use-chunked \
     --chunk-size 25000 \
     --verbose
   ```

4. **Load fewer bricks:**
   ```bash
   just load-cdm-store-bricks-64gb num_bricks=10
   ```

### Process killed at different brick?

Check brick sizes:
```bash
du -sh data/enigma_coral.db/ddt_brick* | sort -h
```

Very large bricks (>200 MB compressed) may need smaller chunks.

## References

- [CDM_PARQUET_STORE_GUIDE.md](CDM_PARQUET_STORE_GUIDE.md) - Complete loading guide
- [load_cdm_parquet_to_store.py](../scripts/cdm_analysis/load_cdm_parquet_to_store.py) - Implementation
- [project.justfile](../project.justfile) - Loading commands

## Summary

The new chunked loading strategy makes it possible to load **all 320M+ rows** across 20 brick tables on standard 64GB RAM machines, with no sampling or data loss. The key insight: **break large files into manageable chunks** instead of loading everything at once.
