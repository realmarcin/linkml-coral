# CDM Metadata Catalogs

This directory contains comprehensive metadata extracted from ENIGMA CDM parquet files and prepared for DuckDB loading.

## 📁 Files in This Directory

### Metadata JSON Files
| File | Records | Description |
|------|---------|-------------|
| `static_tables_metadata.json` | 17 tables | All sdt_* static entity tables |
| `system_tables_metadata.json` | 6 tables | All sys_* system tables |
| `dynamic_tables_metadata.json` | 21 tables | ddt_ndarray + 20 brick tables |
| `column_catalog.json` | 291 columns | **DuckDB ready** - All column metadata |
| `table_catalog.json` | 44 tables | **DuckDB ready** - All table metadata |
| `validation_catalog.json` | 46 rules | **DuckDB ready** - Validation rules |
| `microtype_catalog.json` | 69 microtypes | **DuckDB ready** - Microtype usage |
| `relationship_catalog.json` | 108 relationships | **DuckDB ready** - FK relationships |
| `all_catalogs.json` | Combined | All catalogs in one file |

### SQL Files
| File | Description |
|------|-------------|
| `cdm_metadata_schema.sql` | DuckDB DDL for 5 metadata tables + indexes |

---

## 🚀 Quick Start

### Load Metadata into DuckDB

```bash
# 1. Create database with metadata schema
duckdb cdm_with_metadata.db < data/cdm_metadata/cdm_metadata_schema.sql

# 2. Load catalog data
duckdb cdm_with_metadata.db <<EOF
COPY cdm_column_metadata FROM 'data/cdm_metadata/column_catalog.json';
COPY cdm_table_metadata FROM 'data/cdm_metadata/table_catalog.json';
COPY cdm_validation_rules FROM 'data/cdm_metadata/validation_catalog.json';
COPY cdm_microtype_catalog FROM 'data/cdm_metadata/microtype_catalog.json';
COPY cdm_relationship_catalog FROM 'data/cdm_metadata/relationship_catalog.json';
EOF

# 3. Query metadata
duckdb cdm_with_metadata.db "SELECT COUNT(*) FROM cdm_column_metadata;"
```

---

## 📊 Metadata Tables

### 1. `cdm_column_metadata` (291 rows)
Column-level metadata for all tables.

**Schema:**
```sql
CREATE TABLE cdm_column_metadata (
  table_name VARCHAR NOT NULL,
  table_category VARCHAR NOT NULL,
  column_name VARCHAR NOT NULL,
  column_type VARCHAR,
  description TEXT,
  microtype VARCHAR,
  units VARCHAR,
  is_primary_key BOOLEAN,
  is_unique_key BOOLEAN,
  is_foreign_key BOOLEAN,
  fk_references VARCHAR,
  is_required BOOLEAN,
  is_nullable BOOLEAN,
  constraint_pattern VARCHAR,
  original_name VARCHAR,
  field_type VARCHAR,
  PRIMARY KEY (table_name, column_name)
);
```

**Example Queries:**
```sql
-- Find all columns about temperature
SELECT * FROM cdm_column_metadata
WHERE description LIKE '%temperature%';

-- Find all primary key columns
SELECT table_name, column_name, description
FROM cdm_column_metadata
WHERE is_primary_key = TRUE;

-- Find columns with specific microtype
SELECT table_name, column_name, description
FROM cdm_column_metadata
WHERE microtype = 'ME:0000219';  -- Depth measurement
```

### 2. `cdm_table_metadata` (44 rows)
Table-level statistics and metadata.

**Schema:**
```sql
CREATE TABLE cdm_table_metadata (
  table_name VARCHAR PRIMARY KEY,
  table_category VARCHAR NOT NULL,
  total_rows BIGINT,
  num_columns INTEGER,
  num_primary_keys INTEGER,
  num_foreign_keys INTEGER,
  num_unique_keys INTEGER,
  num_required_columns INTEGER,
  description TEXT
);
```

**Example Queries:**
```sql
-- Tables with most FK relationships
SELECT table_name, num_foreign_keys, total_rows
FROM cdm_table_metadata
ORDER BY num_foreign_keys DESC;

-- Static tables summary
SELECT * FROM cdm_table_metadata
WHERE table_category = 'static'
ORDER BY total_rows DESC;
```

### 3. `cdm_validation_rules` (46 rows)
Validation patterns and FK constraints.

**Schema:**
```sql
CREATE TABLE cdm_validation_rules (
  table_name VARCHAR NOT NULL,
  column_name VARCHAR NOT NULL,
  validation_type VARCHAR NOT NULL,
  validation_pattern VARCHAR,
  description TEXT,
  microtype VARCHAR
);
```

**Example Queries:**
```sql
-- All validation rules for a table
SELECT * FROM cdm_validation_rules
WHERE table_name = 'sdt_sample';

-- Find pattern validations
SELECT table_name, column_name, validation_pattern
FROM cdm_validation_rules
WHERE validation_type = 'pattern';
```

### 4. `cdm_microtype_catalog` (69 rows)
Microtype usage statistics.

**Schema:**
```sql
CREATE TABLE cdm_microtype_catalog (
  microtype VARCHAR PRIMARY KEY,
  usage_count INTEGER,
  tables VARCHAR[],
  columns VARCHAR[],
  example_description TEXT
);
```

**Example Queries:**
```sql
-- Most used microtypes
SELECT microtype, usage_count, example_description
FROM cdm_microtype_catalog
ORDER BY usage_count DESC
LIMIT 10;

-- Find where a microtype is used
SELECT microtype, unnest(columns) as column_path
FROM cdm_microtype_catalog
WHERE microtype = 'ME:0000102';
```

### 5. `cdm_relationship_catalog` (108 rows)
Foreign key relationships.

**Schema:**
```sql
CREATE TABLE cdm_relationship_catalog (
  source_table VARCHAR NOT NULL,
  source_column VARCHAR NOT NULL,
  target_table VARCHAR NOT NULL,
  target_column VARCHAR,
  relationship_type VARCHAR,
  is_required BOOLEAN,
  description TEXT
);
```

**Example Queries:**
```sql
-- All relationships from a table
SELECT source_column, target_table, target_column
FROM cdm_relationship_catalog
WHERE source_table = 'sdt_sample';

-- Find tables referenced by others
SELECT target_table, COUNT(*) as ref_count
FROM cdm_relationship_catalog
GROUP BY target_table
ORDER BY ref_count DESC;
```

---

## 🔍 Common Query Patterns

### Search Across All Metadata
```sql
-- Find anything related to "sequencing"
SELECT
  'Column' as type,
  table_name,
  column_name as name,
  description
FROM cdm_column_metadata
WHERE description ILIKE '%sequencing%'

UNION ALL

SELECT
  'Table' as type,
  table_name,
  '' as name,
  description
FROM cdm_table_metadata
WHERE description ILIKE '%sequencing%';
```

### Build Table Lineage
```sql
-- Find all tables that reference sdt_sample
WITH RECURSIVE lineage AS (
  SELECT
    source_table,
    target_table,
    1 as depth
  FROM cdm_relationship_catalog
  WHERE target_table = 'sdt_sample'

  UNION ALL

  SELECT
    r.source_table,
    r.target_table,
    l.depth + 1
  FROM cdm_relationship_catalog r
  JOIN lineage l ON r.target_table = l.source_table
  WHERE l.depth < 5
)
SELECT DISTINCT source_table, depth
FROM lineage
ORDER BY depth, source_table;
```

### Validate Schema Completeness
```sql
-- Tables without descriptions
SELECT table_name
FROM cdm_table_metadata
WHERE description IS NULL OR description = '';

-- Columns without descriptions
SELECT table_name, column_name
FROM cdm_column_metadata
WHERE description IS NULL OR description = '';
```

---

## 🛠️ Regenerate Metadata

If parquet files are updated, regenerate metadata:

```bash
# 1. Extract metadata from parquet
uv run python scripts/cdm_analysis/extract_cdm_metadata.py data/jmc_coral.db \
  --category static \
  --output data/cdm_metadata/static_tables_metadata.json

uv run python scripts/cdm_analysis/extract_cdm_metadata.py data/jmc_coral.db \
  --category system \
  --output data/cdm_metadata/system_tables_metadata.json

uv run python scripts/cdm_analysis/extract_cdm_metadata.py data/jmc_coral.db \
  --category dynamic \
  --output data/cdm_metadata/dynamic_tables_metadata.json

# 2. Create catalogs
uv run python scripts/cdm_analysis/create_metadata_catalog.py --generate-ddl

# 3. Regenerate data dictionary
uv run python scripts/cdm_analysis/generate_data_dictionary.py

# 4. Update LinkML schema
uv run python scripts/cdm_analysis/update_schema_with_metadata.py --dry-run  # Check first
uv run python scripts/cdm_analysis/update_schema_with_metadata.py  # Execute
```

---

## 📖 Related Documentation

- **[CDM_PARQUET_METADATA_ANALYSIS.md](../../CDM_PARQUET_METADATA_ANALYSIS.md)** - Detailed metadata analysis
- **[CDM_METADATA_INTEGRATION_SUMMARY.md](../../CDM_METADATA_INTEGRATION_SUMMARY.md)** - Integration summary
- **[docs/CDM_DATA_DICTIONARY.md](../../docs/CDM_DATA_DICTIONARY.md)** - Comprehensive data dictionary
- **[docs/cdm_data_dictionary.html](../../docs/cdm_data_dictionary.html)** - Interactive HTML dictionary

---

## 📝 Metadata Structure

### Column Catalog Example
```json
{
  "table_name": "sdt_sample",
  "table_category": "static",
  "column_name": "sdt_sample_id",
  "column_type": "string",
  "description": "Unique identifier for the sample (Primary key)",
  "microtype": "ME:0000267",
  "units": null,
  "is_primary_key": true,
  "is_unique_key": false,
  "is_foreign_key": false,
  "fk_references": null,
  "is_required": true,
  "is_nullable": true,
  "constraint_pattern": null,
  "original_name": "id",
  "field_type": "primary_key"
}
```

### Microtype Catalog Example
```json
{
  "microtype": "ME:0000219",
  "usage_count": 2,
  "tables": ["sdt_sample", "sdt_location"],
  "columns": ["sdt_sample.depth", "sdt_location.depth"],
  "example_description": "For below-ground samples, the average distance below ground level in meters..."
}
```

---

**Last Updated:** 2025-12-23
**Source:** ENIGMA CDM parquet files (`data/jmc_coral.db`)
**Coverage:** 44 tables, 291 columns, 100% description coverage
