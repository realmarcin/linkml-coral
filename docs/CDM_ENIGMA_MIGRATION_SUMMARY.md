# CDM Schema Migration Summary - enigma_coral.db

**Date**: 2026-01-20
**Migration**: jmc_coral.db → enigma_coral.db
**Schema Version**: 1.0.0 (updated)

## Overview

This document summarizes the migration from the jmc_coral.db parquet structure to the updated enigma_coral.db structure, which includes explicit unit suffixes on measurement fields and naming improvements for better clarity.

## Key Changes

### 1. Database Path Migration
- **Old**: `/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db`
- **New**: `data/enigma_coral.db` (relative path)

### 2. Field Renames with Unit Suffixes

#### Static Entity Tables (19 field renames across 9 tables)

##### sdt_location (2 fields)
| Old Field Name | New Field Name | Unit | Description |
|---------------|----------------|------|-------------|
| `latitude` | `latitude_degree` | UO:0000185 (degree) | Latitude in decimal degrees |
| `longitude` | `longitude_degree` | UO:0000185 (degree) | Longitude in decimal degrees |

##### sdt_sample (2 fields)
| Old Field Name | New Field Name | Unit | Description |
|---------------|----------------|------|-------------|
| `depth` | `depth_meter` | UO:0000008 (meter) | Depth in meters |
| `elevation` | `elevation_meter` | UO:0000008 (meter) | Elevation in meters |

##### sdt_reads (1 field)
| Old Field Name | New Field Name | Unit | Description |
|---------------|----------------|------|-------------|
| `read_count` | `read_count_count_unit` | UO:0000189 (count) | Number of reads |

##### sdt_assembly (1 field)
| Old Field Name | New Field Name | Unit | Description |
|---------------|----------------|------|-------------|
| `n_contigs` | `n_contigs_count_unit` | UO:0000189 (count) | Number of contigs |

##### sdt_genome (2 fields)
| Old Field Name | New Field Name | Unit | Description |
|---------------|----------------|------|-------------|
| `n_contigs` | `n_contigs_count_unit` | UO:0000189 (count) | Number of contigs |
| `n_features` | `n_features_count_unit` | UO:0000189 (count) | Number of annotated features |

##### sdt_gene (3 fields)
| Old Field Name | New Field Name | Unit | Description |
|---------------|----------------|------|-------------|
| `contig_number` | `contig_number_count_unit` | UO:0000189 (count) | Contig number |
| `start` | `start_base_pair` | UO:0000244 (base pair) | Start position on contig |
| `stop` | `stop_base_pair` | UO:0000244 (base pair) | Stop position on contig |

##### sdt_image (1 field)
| Old Field Name | New Field Name | Unit | Description |
|---------------|----------------|------|-------------|
| `size` | `size_byte` | UO:0000233 (byte) | File size in bytes |

##### sdt_dubseq_library (1 field)
| Old Field Name | New Field Name | Unit | Description |
|---------------|----------------|------|-------------|
| `n_fragments` | `n_fragments_count_unit` | UO:0000189 (count) | Number of fragments |

##### sdt_tnseq_library (6 field updates)
**Note**: TnSeqLibrary fields already had correct naming with unit suffixes in enigma_coral.db

| Field Name | Unit | Description |
|-----------|------|-------------|
| `n_mapped_reads_count_unit` | UO:0000189 (count) | Number of mapped reads |
| `n_barcodes_count_unit` | UO:0000189 (count) | Number of barcodes |
| `n_insertion_locations_count_unit` | UO:0000189 (count) | Number of insertion locations |
| `n_usable_barcodes_count_unit` | UO:0000189 (count) | Number of usable barcodes |
| `hit_rate_essential_ratio_unit` | UO:0000191 (ratio) | Hit rate for essential genes |
| `hit_rate_other_ratio_unit` | UO:0000191 (ratio) | Hit rate for other genes |

#### System Tables (8 renames + 5 new fields across 2 tables)

##### sys_typedef (5 renames + 4 new fields)
| Old Field Name | New Field Name | Description |
|---------------|----------------|-------------|
| `pk` | `is_pk` | Primary key flag (boolean) |
| `upk` | `is_upk` | Unique key flag (boolean) |
| *(new)* | `is_required` | Required field flag (boolean) |
| *(new)* | `units_sys_oterm_name` | Ontology term name for units |
| *(new)* | `type_sys_oterm_name` | Ontology term name for data type |
| *(new)* | `comment` | Additional comments |

##### sys_ddt_typedef (3 renames + 1 new field)
| Old Field Name | New Field Name | Description |
|---------------|----------------|-------------|
| `cdm_column_name` | `berdl_column_name` | BERDL (Brick Entity Relationship Data Layer) column name |
| `cdm_column_data_type` | `berdl_column_data_type` | BERDL column data type |
| `fk` | `foreign_key` | Foreign key reference |
| *(new)* | `original_csv_string` | Original CSV string representation |

**Note**: The "CDM" → "BERDL" rename reflects a new naming convention for brick data schema.

### 3. Data Statistics

| Category | Tables | Columns | Total Rows |
|----------|--------|---------|------------|
| **Static (sdt_*)** | 17 | 106 | 273K |
| **System (sys_*)** | 6 | 69 | 243K |
| **Dynamic (ddt_*)** | 21 | 116 | 2.1M |
| **Total** | 44 | 291 | 2.6M |

**Row Count Changes** (enigma_coral.db vs jmc_coral.db):
- sdt_location: 594 → 596 (+2)
- sdt_sample: 4,346 → 4,330 (-16)
- sdt_reads: 19,592 → 19,307 (-285)
- sys_process: 84,527 → 142,958 (+58K) ⚠️ significant increase

## Files Modified

### Schema Files
1. `src/linkml_coral/schema/cdm/cdm_static_entities.yaml` - 19 field renames across 9 classes
2. `src/linkml_coral/schema/cdm/cdm_system_tables.yaml` - 8 renames + 5 new fields

### Loader Scripts
3. `scripts/cdm_analysis/load_cdm_parquet_to_store.py` - Updated computed field references (lines 260, 273)

### Documentation
4. `README.md` - Updated database paths and examples
5. `CLAUDE.md` - Updated database paths
6. `project.justfile` - Updated all just command defaults (8 references)
7. `docs/CDM_DATA_DICTIONARY.md` - Regenerated with new field names
8. `docs/cdm_data_dictionary.html` - Interactive dictionary updated
9. All `docs/*.md` files - Database path references updated

### Metadata Catalogs
10. `data/cdm_metadata/static_tables_metadata.json` - Re-extracted from enigma_coral.db
11. `data/cdm_metadata/system_tables_metadata.json` - Re-extracted from enigma_coral.db
12. `data/cdm_metadata/dynamic_tables_metadata.json` - Re-extracted from enigma_coral.db
13. `data/cdm_metadata/column_catalog.json` - Regenerated (291 → 293 columns)
14. `data/cdm_metadata/table_catalog.json` - Regenerated (44 tables)
15. Other catalogs: validation_catalog.json, microtype_catalog.json, relationship_catalog.json

## Migration Process

### Phase 1: Metadata Extraction ✅
- Extracted metadata from all 44 tables in enigma_coral.db
- Validated all 30+ field renames exist in source data
- Confirmed data integrity

### Phase 2: Metadata Catalog Generation ✅
- Generated unified metadata catalogs
- 293 columns (up from 291)
- 44 tables fully documented

### Phase 3: Schema Updates ✅
- Updated cdm_static_entities.yaml (19 field renames)
- Updated cdm_system_tables.yaml (8 renames + 5 new fields)
- Added `original_name` annotations to preserve old names

### Phase 4: Validation ✅
- linkml-lint: No errors
- Schema sync tool: Confirmed no additional changes needed

### Phase 5: Loader Script Updates ✅
- Updated field references for computed fields
- Tested read_count_count_unit and n_contigs_count_unit

### Phase 6: Path Migration ✅
- Updated all jmc_coral.db → enigma_coral.db references
- Changed to relative paths (data/enigma_coral.db)

### Phase 7: Project Regeneration ✅
- Regenerated Python dataclasses
- Regenerated data dictionary (HTML + Markdown)
- Updated all generated documentation

### Phase 8: Integration Testing ✅
- Successfully loaded 490K records from enigma_coral.db
- Verified all field renames in parquet data
- Confirmed computed fields work correctly

### Phase 9: Documentation ✅
- Created this migration summary
- All documentation updated

## Breaking Changes

⚠️ **Users must update their code and queries**:

### 1. Query Updates Required

**Old Query**:
```python
samples = collection.find({"depth": {"$gt": 10}})
reads = collection.find({"read_count": {"$gte": 50000}})
locations = collection.find({"latitude": {"$gte": 37.0}})
```

**New Query**:
```python
samples = collection.find({"depth_meter": {"$gt": 10}})
reads = collection.find({"read_count_count_unit": {"$gte": 50000}})
locations = collection.find({"latitude_degree": {"$gte": 37.0}})
```

### 2. Database Reload Required

Users must:
1. Re-extract data from enigma_coral.db (not jmc_coral.db)
2. Update all field names in custom queries
3. Rebuild linkml-store databases with new schema

### 3. Loader Script Changes

**Old**:
```bash
just load-cdm-store /path/to/jmc_coral.db output.db
```

**New**:
```bash
just load-cdm-store data/enigma_coral.db output.db
```

## Upgrade Guide

### For Data Users

1. **Update database path**:
   ```bash
   # Use enigma_coral.db instead of jmc_coral.db
   export CDM_DB=data/enigma_coral.db
   ```

2. **Update field names in queries**: See field mapping table above

3. **Reload databases**:
   ```bash
   just load-cdm-store
   ```

### For Schema Developers

1. **Pull latest schema changes**:
   ```bash
   git pull origin linkml-coral-cdm
   ```

2. **Regenerate project files**:
   ```bash
   just gen-project
   just site
   ```

3. **Update any custom code** with new field names

## Benefits of This Migration

1. **Explicit Units**: Field names now clearly indicate measurement units (_degree, _meter, _count_unit, _byte)
2. **Better Clarity**: BERDL naming better describes brick data layer architecture
3. **Improved Metadata**: Added fields for better documentation (units_sys_oterm_name, type_sys_oterm_name, comment)
4. **Consistent Naming**: All measurement fields follow standard unit suffix pattern
5. **Enhanced Validation**: More fields with explicit boolean flags (is_pk, is_upk, is_required)

## Rollback Strategy

If needed, rollback to previous state:

```bash
# Restore old schema files
git checkout HEAD~1 -- src/linkml_coral/schema/cdm/

# Regenerate project
just gen-project

# Use old database
just load-cdm-store /old/path/to/jmc_coral.db
```

## Support

For questions or issues:
- GitHub Issues: https://github.com/realmarcin/linkml-coral/issues
- Check CLAUDE.md for updated examples
- Review CDM_DATA_DICTIONARY.md for field reference

---

**Migration Status**: ✅ **Complete**
**Schema Version**: 1.0.0 (enigma_coral.db compatible)
**Date**: 2026-01-20
