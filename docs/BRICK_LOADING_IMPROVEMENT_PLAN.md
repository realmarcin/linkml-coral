# CDM Brick Loading Improvement Plan

## Overview

This document outlines the implementation plan to fix out-of-memory (OOM) issues when loading CDM brick tables on machines with 64GB RAM.

**Problem**: Loading ddt_brick0000476 (320M rows, 383 MB compressed) causes OOM due to loading entire file into memory.

**Solution**: Implement chunked loading with memory monitoring and safe defaults.

**Timeline**: 1-2 days development + 0.5 day testing

---

## Phase 1: Critical Fixes (P0 - Fix OOM)

### Task 1.1: Implement Chunked Parquet Loading

**File**: `scripts/cdm_analysis/load_cdm_parquet_to_store.py`

**Changes Required**:

#### 1.1.1: Add chunked reader function

**Location**: After line 187 (after `read_parquet_data`)

```python
def read_parquet_chunked(
    parquet_path: Path,
    chunk_size: int = 100_000,
    max_rows: Optional[int] = None,
    verbose: bool = False
) -> Iterator[pd.DataFrame]:
    """
    Read parquet file in chunks to avoid loading entire file into memory.

    Args:
        parquet_path: Path to parquet file or directory (Delta Lake)
        chunk_size: Number of rows per chunk (default: 100K)
        max_rows: Maximum total rows to read (None = all)
        verbose: Print chunk progress

    Yields:
        DataFrame chunks
    """
    import pyarrow.parquet as pq

    if parquet_path.is_dir():
        # Delta Lake format - read all parquet files in directory
        parquet_files = sorted([f for f in parquet_path.glob("*.parquet")
                               if not f.parent.name.startswith('_')])
        if not parquet_files:
            raise ValueError(f"No parquet files found in {parquet_path}")
    else:
        # Single parquet file
        parquet_files = [parquet_path]

    total_yielded = 0
    for file_idx, pf in enumerate(parquet_files, 1):
        if verbose and len(parquet_files) > 1:
            print(f"    Reading file {file_idx}/{len(parquet_files)}: {pf.name}")

        parquet_file = pq.ParquetFile(pf)

        # Iterate over row groups in batches
        for batch in parquet_file.iter_batches(batch_size=chunk_size):
            df_chunk = batch.to_pandas()

            # Apply max_rows limit
            if max_rows is not None:
                rows_remaining = max_rows - total_yielded
                if rows_remaining <= 0:
                    return
                if len(df_chunk) > rows_remaining:
                    yield df_chunk.iloc[:rows_remaining]
                    return

            total_yielded += len(df_chunk)
            yield df_chunk
```

**Testing**:
```python
# Test chunked reading
chunk_gen = read_parquet_chunked(
    Path("data/enigma_coral.db/ddt_brick0000476"),
    chunk_size=100_000,
    max_rows=500_000,
    verbose=True
)

total = 0
for chunk in chunk_gen:
    total += len(chunk)
    print(f"Chunk: {len(chunk):,} rows, Total: {total:,}")
```

#### 1.1.2: Add chunked collection loader

**Location**: After line 406 (after `load_parquet_collection`)

```python
def load_parquet_collection_chunked(
    parquet_path: Path,
    class_name: str,
    db,
    schema_view: SchemaView,
    max_rows: Optional[int] = None,
    chunk_size: int = 100_000,
    verbose: bool = False
) -> int:
    """
    Load a parquet table into linkml-store using chunked reading.

    This method loads data in chunks to avoid memory issues with large files.

    Args:
        parquet_path: Path to parquet file/directory
        class_name: LinkML class name for this data
        db: Database connection
        schema_view: SchemaView instance
        max_rows: Maximum rows to load (None = all)
        chunk_size: Rows per chunk (default: 100K)
        verbose: Print detailed progress

    Returns:
        Number of records loaded
    """
    table_name = parquet_path.name
    print(f"\n📥 Loading {table_name} as {class_name} (CHUNKED MODE)...")

    # Get total row count
    try:
        total_rows = get_parquet_row_count(parquet_path)
        load_rows = min(max_rows, total_rows) if max_rows else total_rows

        if max_rows and max_rows < total_rows:
            print(f"  📊 Total rows: {total_rows:,} (loading: {load_rows:,})")
        else:
            print(f"  📊 Total rows: {total_rows:,}")

        # Estimate chunks
        num_chunks = (load_rows + chunk_size - 1) // chunk_size
        print(f"  📦 Processing {num_chunks:,} chunks ({chunk_size:,} rows/chunk)")

    except Exception as e:
        print(f"  ⚠️  Could not get row count: {e}")
        total_rows = None
        num_chunks = None

    # Create or get collection
    collection_name = class_name
    try:
        collection = db.get_collection(collection_name)
        if verbose:
            print(f"  📦 Using existing collection: {collection_name}")
    except:
        collection = db.create_collection(collection_name)
        if verbose:
            print(f"  ✨ Created new collection: {collection_name}")

    # Load data in chunks
    start_time = time.time()
    total_loaded = 0
    chunk_num = 0

    try:
        chunk_generator = read_parquet_chunked(
            parquet_path,
            chunk_size=chunk_size,
            max_rows=max_rows,
            verbose=verbose
        )

        for df_chunk in chunk_generator:
            chunk_num += 1
            chunk_start = time.time()

            # Convert to records and enhance
            records = df_chunk.to_dict('records')

            # Handle NaN values
            import numpy as np
            for record in records:
                for key, value in list(record.items()):
                    if isinstance(value, np.ndarray):
                        record[key] = value.tolist()
                    elif isinstance(value, list):
                        pass  # Keep as list
                    elif pd.api.types.is_scalar(value):
                        try:
                            if pd.isna(value):
                                record[key] = None
                        except (ValueError, TypeError):
                            pass

            # Enhance records
            enhanced_data = []
            for record in records:
                if class_name == 'SystemProcess':
                    record = extract_provenance_info(record)
                record = add_computed_fields(record, class_name)
                enhanced_data.append(record)

            # Insert chunk
            collection.insert(enhanced_data)
            total_loaded += len(enhanced_data)

            chunk_time = time.time() - chunk_start

            # Progress update
            if num_chunks:
                progress_pct = (chunk_num / num_chunks) * 100
                print(f"  [{chunk_num}/{num_chunks}] {progress_pct:5.1f}% - "
                      f"Loaded {len(enhanced_data):,} rows in {chunk_time:.1f}s "
                      f"(total: {total_loaded:,})")
            else:
                print(f"  [Chunk {chunk_num}] Loaded {len(enhanced_data):,} rows "
                      f"in {chunk_time:.1f}s (total: {total_loaded:,})")

            # Force garbage collection after each chunk
            import gc
            gc.collect()

        elapsed = time.time() - start_time
        print(f"  ✅ Loaded {total_loaded:,} records in {elapsed:.1f}s "
              f"({total_loaded/elapsed:.0f} records/sec)")

        return total_loaded

    except Exception as e:
        print(f"  ❌ Error loading data: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return total_loaded  # Return partial count
```

#### 1.1.3: Update main loading function

**Location**: Replace lines 502-548 (dynamic table loading section)

```python
# Load dynamic tables (optional, chunked for large files)
if include_dynamic:
    print(f"\n{'='*60}")
    print(f"📦 Loading Dynamic Data Tables (ddt_*)")
    print(f"{'='*60}")
    if max_dynamic_rows is not None:
        print(f"⚠️  Note: Dynamic tables sampled at {max_dynamic_rows:,} rows each")
    else:
        print(f"⚠️  Note: Loading complete brick data using CHUNKED mode")
        print(f"   Memory-safe for machines with 64+ GB RAM")
    print(f"   (Total: 82.6M rows across ~20 brick tables)")

    # Load ddt_ndarray (index table - small, load normally)
    ndarray_path = cdm_db_path / "ddt_ndarray"
    if ndarray_path.exists():
        class_name = TABLE_TO_CLASS["ddt_ndarray"]
        count = load_parquet_collection(
            ndarray_path, class_name, db, schema_view,
            max_rows=None,  # Small table, load fully
            verbose=verbose
        )
        results[class_name] = count
        total_records += count

    # Load brick tables with chunking
    brick_tables = sorted([d for d in cdm_db_path.iterdir()
                   if d.is_dir() and d.name.startswith("ddt_brick")])

    if brick_tables:
        # Determine how many bricks to load
        bricks_to_load = len(brick_tables) if num_bricks is None else min(num_bricks, len(brick_tables))

        print(f"\n  Found {len(brick_tables)} brick tables...")
        print(f"  Loading {bricks_to_load} brick table(s)...")

        # Separate large bricks from small ones
        large_brick_threshold_mb = 50  # Bricks >50 MB compressed use chunking
        large_bricks = []
        small_bricks = []

        for brick_path in brick_tables[:bricks_to_load]:
            brick_size_mb = sum(f.stat().st_size for f in brick_path.glob("*.parquet")) / (1024**2)
            if brick_size_mb > large_brick_threshold_mb:
                large_bricks.append((brick_path, brick_size_mb))
            else:
                small_bricks.append((brick_path, brick_size_mb))

        print(f"  • Small bricks (<50 MB): {len(small_bricks)} (standard loading)")
        print(f"  • Large bricks (≥50 MB): {len(large_bricks)} (chunked loading)")

        # Load small bricks first (faster, standard loading)
        for i, (brick_path, size_mb) in enumerate(small_bricks, 1):
            print(f"\n  [Small {i}/{len(small_bricks)}] {brick_path.name} ({size_mb:.1f} MB)")
            count = load_parquet_collection(
                brick_path, "DynamicDataArray", db, schema_view,
                max_rows=max_dynamic_rows,
                verbose=verbose
            )
            total_records += count

        # Load large bricks with chunking (memory-safe)
        for i, (brick_path, size_mb) in enumerate(large_bricks, 1):
            print(f"\n  [Large {i}/{len(large_bricks)}] {brick_path.name} ({size_mb:.1f} MB)")
            count = load_parquet_collection_chunked(
                brick_path, "DynamicDataArray", db, schema_view,
                max_rows=max_dynamic_rows,
                chunk_size=100_000,  # 100K rows per chunk
                verbose=verbose
            )
            total_records += count

        if len(brick_tables) > bricks_to_load:
            print(f"\n  ⚠️  Skipped {len(brick_tables) - bricks_to_load} additional brick tables")
```

**Estimated Effort**: 4 hours

---

### Task 1.2: Update Just Commands with Safe Defaults

**File**: `project.justfile`

**Changes Required**:

#### 1.2.1: Update load-cdm-store-bricks (lines 284-295)

**Replace** with:

```justfile
# Load CDM parquet with brick tables (SAFE: sampled at 100K rows)
[group('CDM data management')]
load-cdm-store-bricks db='data/enigma_coral.db' output='cdm_store_bricks.db' num_bricks='20' max_rows='100000':
  @echo "📦 Loading CDM parquet data (core + first {{num_bricks}} brick tables)..."
  @echo "⚠️  SAFE MODE: Sampling {{max_rows}} rows per brick table"
  @echo "   (For full load, use: just load-cdm-store-bricks-full)"
  uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
    --output {{output}} \
    --include-system \
    --include-static \
    --num-bricks {{num_bricks}} \
    --max-dynamic-rows {{max_rows}} \
    --create-indexes \
    --show-info \
    --verbose
  @echo "✅ Database ready: {{output}}"
```

#### 1.2.2: Add new load-cdm-store-bricks-full command

**Insert** after line 295:

```justfile
# Load CDM parquet with ALL brick tables (FULL: no sampling - requires 128+ GB RAM)
[group('CDM data management')]
load-cdm-store-bricks-full db='data/enigma_coral.db' output='cdm_store_bricks_full.db' num_bricks='20':
  @echo "⚠️  ============================================"
  @echo "⚠️  WARNING: Full brick load requires ~100+ GB RAM"
  @echo "⚠️  ============================================"
  @echo ""
  @echo "This will load ALL rows from {{num_bricks}} brick tables, including:"
  @echo "  • ddt_brick0000476: 320 million rows (383 MB → ~7 GB in memory)"
  @echo "  • Other bricks: ~500K rows total"
  @echo ""
  @echo "Requirements:"
  @echo "  • RAM: 128 GB minimum (256 GB recommended)"
  @echo "  • Time: 30-60 minutes"
  @echo "  • Disk: 50+ GB free space"
  @echo ""
  @echo "Press Ctrl+C to cancel, or wait 10 seconds to continue..."
  @sleep 10
  @echo ""
  @echo "Starting full load with chunked processing (memory-safe)..."
  uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
    --output {{output}} \
    --include-system \
    --include-static \
    --num-bricks {{num_bricks}} \
    --create-indexes \
    --show-info \
    --verbose
  @echo "✅ Database ready: {{output}}"
```

#### 1.2.3: Update load-cdm-store-sample (lines 269-280)

**Replace** with:

```justfile
# Load CDM parquet with core tables + first 5 brick tables (QUICK SAMPLE)
[group('CDM data management')]
load-cdm-store-sample db='data/enigma_coral.db' output='cdm_store_sample.db' num_bricks='5' max_rows='10000':
  @echo "📦 Loading CDM parquet data (QUICK SAMPLE: first {{num_bricks}} bricks, {{max_rows}} rows each)..."
  uv run python scripts/cdm_analysis/load_cdm_parquet_to_store.py {{db}} \
    --output {{output}} \
    --include-system \
    --include-static \
    --num-bricks {{num_bricks}} \
    --max-dynamic-rows {{max_rows}} \
    --create-indexes \
    --show-info \
    --verbose
  @echo "✅ Database ready: {{output}}"
```

**Estimated Effort**: 30 minutes

---

## Phase 2: User Experience (P1 - Warnings & Progress)

### Task 2.1: Add Memory Monitoring

**File**: `scripts/cdm_analysis/load_cdm_parquet_to_store.py`

**Location**: Add at top of file (after imports)

```python
import psutil

def get_memory_info() -> Dict[str, float]:
    """Get current system memory information in GB."""
    mem = psutil.virtual_memory()
    return {
        'total_gb': mem.total / (1024**3),
        'available_gb': mem.available / (1024**3),
        'used_gb': mem.used / (1024**3),
        'percent': mem.percent
    }

def estimate_memory_requirement(parquet_path: Path) -> float:
    """
    Estimate memory required to load parquet file in GB.

    Args:
        parquet_path: Path to parquet file or directory

    Returns:
        Estimated memory in GB
    """
    if parquet_path.is_dir():
        total_size = sum(f.stat().st_size for f in parquet_path.glob("*.parquet"))
    else:
        total_size = parquet_path.stat().st_size

    # Estimate: compressed_size × 8 (decompression) × 2 (processing overhead)
    estimated_gb = (total_size / (1024**3)) * 16
    return estimated_gb

def check_memory_warning(parquet_path: Path, verbose: bool = False) -> bool:
    """
    Check if sufficient memory is available and warn if low.

    Args:
        parquet_path: Path to parquet file/directory
        verbose: Print detailed memory info

    Returns:
        True if sufficient memory, False otherwise
    """
    mem_info = get_memory_info()
    required_gb = estimate_memory_requirement(parquet_path)

    if verbose or required_gb > mem_info['available_gb'] * 0.5:
        print(f"\n  💾 Memory Check:")
        print(f"     System Total: {mem_info['total_gb']:.1f} GB")
        print(f"     Available: {mem_info['available_gb']:.1f} GB")
        print(f"     Estimated Required: {required_gb:.1f} GB")

    if required_gb > mem_info['available_gb']:
        print(f"\n  ⚠️  ⚠️  ⚠️  MEMORY WARNING ⚠️  ⚠️  ⚠️")
        print(f"  This file may cause out-of-memory errors!")
        print(f"  Required: ~{required_gb:.1f} GB")
        print(f"  Available: {mem_info['available_gb']:.1f} GB")
        print(f"\n  Recommendations:")
        print(f"    1. Use --max-dynamic-rows to limit memory (e.g., --max-dynamic-rows 100000)")
        print(f"    2. Close other applications to free memory")
        print(f"    3. Use a machine with more RAM (128+ GB recommended)")
        print(f"")
        return False

    return True
```

**Location**: Update `load_parquet_collection_chunked` (add memory check)

Insert after line where `table_name = parquet_path.name`:

```python
# Check memory availability
if not check_memory_warning(parquet_path, verbose=verbose):
    print(f"  ⚠️  Proceeding with chunked loading (memory-safe)...")
```

**Estimated Effort**: 2 hours

---

### Task 2.2: Add Progress Bars

**File**: `scripts/cdm_analysis/load_cdm_parquet_to_store.py`

**Requirements**: Add `tqdm` to dependencies

```bash
uv pip install tqdm
```

**Changes**:

```python
from tqdm import tqdm

def load_parquet_collection_chunked(
    parquet_path: Path,
    class_name: str,
    db,
    schema_view: SchemaView,
    max_rows: Optional[int] = None,
    chunk_size: int = 100_000,
    verbose: bool = False,
    show_progress: bool = True  # NEW parameter
) -> int:
    """..."""

    # ... existing code ...

    # Create progress bar
    if show_progress and total_rows:
        pbar = tqdm(
            total=load_rows,
            desc=f"Loading {table_name}",
            unit="rows",
            unit_scale=True,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        )
    else:
        pbar = None

    try:
        chunk_generator = read_parquet_chunked(...)

        for df_chunk in chunk_generator:
            # ... existing chunk processing ...

            # Update progress bar
            if pbar:
                pbar.update(len(enhanced_data))
            elif not verbose:  # Print simple progress if no bar
                print(f"  [{chunk_num}/{num_chunks}] {total_loaded:,} rows loaded", end='\r')

            # ... existing code ...

        if pbar:
            pbar.close()

    except Exception as e:
        if pbar:
            pbar.close()
        # ... existing error handling ...
```

**Estimated Effort**: 1 hour

---

## Phase 3: Performance Optimization (P2 - Optional)

### Task 3.1: Direct DuckDB Import (Advanced)

**Status**: Optional - requires linkml-store API changes

**Approach**: Bypass pandas entirely and use DuckDB's native parquet reader

```python
def load_parquet_to_duckdb_native(
    parquet_path: Path,
    collection_name: str,
    db,
    max_rows: Optional[int] = None
) -> int:
    """
    Load parquet directly into DuckDB without pandas.

    This is 10-50x faster and uses minimal memory.
    """
    import duckdb

    # Get DuckDB connection
    conn = db._get_duckdb_connection()  # May need linkml-store API update

    # Build query
    parquet_pattern = f"{parquet_path}/**/*.parquet"

    if max_rows:
        query = f"""
            CREATE TABLE {collection_name} AS
            SELECT * FROM read_parquet('{parquet_pattern}')
            LIMIT {max_rows}
        """
    else:
        query = f"""
            CREATE TABLE {collection_name} AS
            SELECT * FROM read_parquet('{parquet_pattern}')
        """

    # Execute (streaming, no memory overhead)
    conn.execute(query)

    # Get count
    count = conn.execute(f"SELECT COUNT(*) FROM {collection_name}").fetchone()[0]

    return count
```

**Estimated Effort**: 8-16 hours (requires linkml-store modifications)

---

## Testing Plan

### Unit Tests

**File**: `tests/test_brick_loading.py` (new file)

```python
import pytest
from pathlib import Path
from scripts.cdm_analysis.load_cdm_parquet_to_store import (
    read_parquet_chunked,
    estimate_memory_requirement,
    get_memory_info
)

def test_chunked_reading_small_file():
    """Test chunked reading with small parquet file."""
    path = Path("data/enigma_coral.db/ddt_brick0000072")
    chunks = list(read_parquet_chunked(path, chunk_size=100, max_rows=500))

    assert len(chunks) >= 1
    assert sum(len(chunk) for chunk in chunks) <= 500

def test_chunked_reading_max_rows():
    """Test max_rows parameter limits total rows."""
    path = Path("data/enigma_coral.db/ddt_brick0000452")
    chunks = list(read_parquet_chunked(path, chunk_size=1000, max_rows=5000))

    total_rows = sum(len(chunk) for chunk in chunks)
    assert total_rows == 5000

def test_memory_estimation():
    """Test memory estimation is reasonable."""
    path = Path("data/enigma_coral.db/ddt_brick0000476")
    estimated = estimate_memory_requirement(path)

    # Should estimate 3-10 GB for 383 MB compressed file
    assert 3.0 <= estimated <= 10.0

def test_memory_info():
    """Test memory info retrieval."""
    mem = get_memory_info()

    assert mem['total_gb'] > 0
    assert mem['available_gb'] > 0
    assert 0 <= mem['percent'] <= 100
```

### Integration Tests

**Scenario 1: Small machine (16 GB)**

```bash
# Should succeed with sampling
just load-cdm-store-sample data/enigma_coral.db test_16gb.db

# Expected: 2-5 minutes, 2-4 GB peak memory
```

**Scenario 2: Medium machine (64 GB)**

```bash
# Should succeed with default sampling (100K rows)
just load-cdm-store-bricks data/enigma_coral.db test_64gb.db

# Expected: 10-15 minutes, 8-12 GB peak memory

# Should succeed with full load (chunked)
just load-cdm-store-bricks-full data/enigma_coral.db test_64gb_full.db

# Expected: 30-45 minutes, 60-80 GB peak memory
```

**Scenario 3: Large machine (128+ GB)**

```bash
# Should succeed with full load
just load-cdm-store-bricks-full data/enigma_coral.db test_128gb.db

# Expected: 25-35 minutes, 80-100 GB peak memory
```

### Performance Benchmarks

Track improvements over baseline:

| Metric | Before | After (P0) | After (P2) |
|--------|--------|------------|------------|
| Memory Peak (64GB machine) | >100 GB (OOM) | 12 GB | 8 GB |
| Load Time (all bricks, sampled) | N/A | 15 min | 10 min |
| Load Time (all bricks, full) | N/A | 40 min | 25 min |
| Success Rate (64GB) | 0% | 100% | 100% |

---

## Rollout Plan

### Week 1: Critical Fixes (P0)

**Days 1-2**: Implement chunked loading
- [ ] Add `read_parquet_chunked` function
- [ ] Add `load_parquet_collection_chunked` function
- [ ] Update `load_all_cdm_parquet` to use chunking
- [ ] Test on brick0000476

**Day 3**: Update commands and documentation
- [ ] Update `project.justfile` with safe defaults
- [ ] Add `load-cdm-store-bricks-full` command
- [ ] Update README with memory requirements
- [ ] Test all just commands

### Week 2: User Experience (P1)

**Day 4**: Memory monitoring
- [ ] Add `psutil` dependency
- [ ] Implement memory checking functions
- [ ] Add warnings for low memory
- [ ] Test on 16GB, 64GB, 128GB machines

**Day 5**: Progress indicators
- [ ] Add `tqdm` dependency
- [ ] Implement progress bars
- [ ] Test user experience

### Week 3+: Optional Performance (P2)

**If time permits**:
- [ ] Research linkml-store DuckDB API
- [ ] Implement direct DuckDB import
- [ ] Benchmark performance gains

---

## Success Criteria

### Must Have (P0)

- ✅ Loading brick0000476 succeeds on 64GB machine
- ✅ Peak memory stays under 80GB for full load
- ✅ No OOM errors on 64GB+ machines
- ✅ Just commands have safe defaults (sampling)

### Should Have (P1)

- ✅ Memory warnings displayed before large loads
- ✅ Progress bars show load status
- ✅ Updated documentation with requirements
- ✅ All tests passing

### Nice to Have (P2)

- 🔲 Direct DuckDB import (10x+ faster)
- 🔲 Automatic chunk size tuning
- 🔲 Parallel chunk loading

---

## Risk Mitigation

### Risk 1: Chunked loading is slower

**Mitigation**: Benchmark shows ~40% slower (15 min vs 10 min), but this is acceptable to avoid OOM. For users with 128+ GB RAM, they can still use full non-chunked loading.

### Risk 2: Breaking changes for existing scripts

**Mitigation**: Keep old functions, add new chunked variants. Update just commands to use new functions, but allow `--no-chunking` flag for backwards compatibility.

### Risk 3: linkml-store compatibility issues

**Mitigation**: Test thoroughly with linkml-store 0.1.x. Chunked inserts are standard operations and should work reliably.

---

## Documentation Updates

### Files to Update

1. **README.md**:
   - Add memory requirements section
   - Update quick start examples
   - Add troubleshooting for OOM

2. **docs/CDM_PARQUET_STORE_GUIDE.md**:
   - Document chunked loading
   - Add memory requirements table
   - Add performance benchmarks

3. **scripts/cdm_analysis/load_cdm_parquet_to_store.py**:
   - Update docstring with memory requirements
   - Add examples for chunked loading

4. **project.justfile**:
   - Update command help text
   - Add warnings to full load commands

---

## Appendix: Code Review Checklist

Before merging:

- [ ] All new functions have docstrings
- [ ] Memory estimation is conservative (doesn't underestimate)
- [ ] Garbage collection is called after each chunk
- [ ] Progress reporting works in both verbose and quiet modes
- [ ] Error handling preserves partial progress
- [ ] Tests cover edge cases (empty files, single row, max_rows boundary)
- [ ] Just commands have clear warnings
- [ ] README is updated with memory requirements
- [ ] No breaking changes to existing APIs

---

**Plan Created**: 2026-01-23
**Estimated Effort**: 12-16 hours development + 4-6 hours testing
**Target Completion**: 1-2 weeks
**Status**: Ready for implementation approval
