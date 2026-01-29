# Duplicate Tables Issue and Fix

## Problem

After switching to CDM table naming conventions, databases contained **duplicate tables** with both old and new naming schemes:

### Duplicate Tables Found

| Old Name (LinkML) | New Name (CDM) | Issue |
|-------------------|----------------|-------|
| `Location` | `sdt_location` | Duplicated static entity |
| `Sample` | `sdt_sample` | Duplicated static entity |
| `Reads` | `sdt_reads` | Duplicated static entity |
| `Assembly` | `sdt_assembly` | Duplicated static entity |
| `Taxon` | `sdt_taxon` | Duplicated static entity |
| `TnSeqLibrary` | `sdt_tnseq_library` | Duplicated static entity |
| `SystemProcess` | `sys_process` | Duplicated system table |
| `SystemOntologyTerm` | `sys_oterm` | Duplicated system table |
| `SystemTypedef` | `sys_typedef` | Duplicated system table |
| `SystemDDTTypedef` | `sys_ddt_typedef` | Duplicated system table |
| `SystemProcessInput` | `sys_process_input` | Duplicated system table |
| `SystemProcessOutput` | `sys_process_output` | Duplicated system table |
| `DynamicDataArray` | `ddt_brick*` | Old generic name vs specific brick names |

**Total**: ~25 duplicate tables consuming extra disk space and causing confusion.

## Root Cause

Two code paths in `load_cdm_parquet_to_store.py` were still creating collections with LinkML class names instead of CDM table names:

1. **Chunked loader** (`load_parquet_collection_chunked`):
   - Line 655: `collection_name = class_name` ❌
   - Should be: `collection = db.get_collection(table_name)` ✅

2. **Index creation** (`create_indexes`):
   - Lines 1129-1150: Used old names like `'Location'`, `'SystemProcess'` ❌
   - Should be: `'sdt_location'`, `'sys_process'` ✅

3. **No parquet file duplicates**: The parquet files were correctly named (sdt_*, sys_*, ddt_*) - issue was only in Python code.

## Solution

### Code Fixes (Commit 407eb55)

**1. Fixed chunked loader:**
```python
# Before
collection_name = class_name
collection = db.get_collection(collection_name)

# After
collection = db.get_collection(table_name)  # Use CDM name
```

**2. Fixed index creation:**
```python
# Before
index_specs = [
    ('Location', 'sdt_location_id'),
    ('SystemProcess', 'sys_process_id'),
    ...
]

# After
index_specs = [
    ('sdt_location', 'sdt_location_id'),
    ('sys_process', 'sys_process_id'),
    ...
]
```

### New Databases

After pulling the latest code (commit 407eb55+), newly created databases will **only** have CDM-named tables:
- ✅ sdt_location, sdt_sample, sdt_reads, sdt_assembly, etc.
- ✅ sys_process, sys_oterm, sys_typedef, etc.
- ✅ ddt_brick0000476, ddt_brick0000477, etc.

### Existing Databases

For databases created before this fix, use the cleanup script:

#### Preview what will be dropped (safe):
```bash
just cdm-drop-duplicates-dry-run cdm_store.db
```

Example output:
```
Found 25 duplicate tables to drop:

  • Assembly                      (3,427 records)
  • Location                      (596 records)
  • Sample                        (4,346 records)
  • SystemProcess                 (169,054 records)
  • SystemOntologyTerm            (21,200 records)
  ...

🔍 DRY RUN: No tables were dropped.
   Run without --dry-run to actually drop these tables.
```

#### Actually drop duplicates:
```bash
just cdm-drop-duplicates cdm_store.db
```

This will:
1. Show 5-second warning before proceeding
2. Drop all old LinkML-named tables
3. Keep only CDM-named tables (sdt_*, sys_*, ddt_*)
4. Show summary of what was dropped

#### Direct Python usage:
```bash
# Preview only
uv run python scripts/cdm_analysis/drop_duplicate_tables.py cdm_store.db --dry-run --verbose

# Actually drop
uv run python scripts/cdm_analysis/drop_duplicate_tables.py cdm_store.db --verbose
```

## Verification

### Check for duplicates:
```bash
duckdb cdm_store.db "SHOW TABLES" | grep -E "(^Location|^Sample|^SystemProcess)"
```

If you see tables without `sdt_` or `sys_` prefixes, you have duplicates.

### Expected clean state:
```bash
duckdb cdm_store.db
D SHOW TABLES;
```

Should show **only** CDM-named tables:
```
sdt_assembly
sdt_asv
sdt_bin
...
sys_oterm
sys_process
sys_process_input
...
ddt_brick0000476
ddt_brick0000477
...
ddt_ndarray
```

## Impact

### Before Fix
- **Tables**: ~48 tables (23 unique + 25 duplicates)
- **Disk usage**: ~2x necessary space
- **Confusion**: Which table to query? Location or sdt_location?

### After Fix
- **Tables**: ~33 tables (no duplicates)
- **Disk usage**: ~50% reduction
- **Clarity**: All tables use consistent CDM naming

## Timeline

- **Commit f482fe8** (2026-01-26): Fixed OOM errors on 64GB RAM
- **Commit 9610cd9** (2026-01-26): Switched to CDM table naming (introduced duplicates)
- **Commit e55cebd** (2026-01-26): Updated README with CDM naming
- **Commit 407eb55** (2026-01-26): Fixed remaining code paths creating duplicates ✅

## Recommendations

1. **Pull latest code**: `git pull origin linkml-store`
2. **For existing databases**: Run `just cdm-drop-duplicates-dry-run` then `just cdm-drop-duplicates`
3. **For new databases**: Just load normally - no duplicates will be created
4. **Always use CDM names in queries**: `sdt_sample`, `sys_process`, etc.

## See Also

- [64GB_RAM_LOADING_GUIDE.md](64GB_RAM_LOADING_GUIDE.md) - Memory optimization guide
- [CDM_NAMING_CONVENTIONS.md](CDM_NAMING_CONVENTIONS.md) - Complete CDM naming spec
- [scripts/cdm_analysis/drop_duplicate_tables.py](../scripts/cdm_analysis/drop_duplicate_tables.py) - Cleanup script
