# CDM Parquet Validation Guide

## Overview

This guide explains how to validate CDM parquet files against the LinkML schema using the validation tools provided in this repository.

**Key Discovery:** linkml-validate does NOT natively support parquet files. We've implemented a conversion-based approach:
```
Parquet → DataFrame → YAML → linkml-validate → Validation Report
```

## Prerequisites

```bash
# Ensure dependencies are installed
uv sync

# Dependencies used:
# - pandas (DataFrame manipulation)
# - pyarrow (Parquet reading)
# - linkml-validate (Schema validation)
```

## Quick Start

### Validate Single Table

```bash
# Auto-detect class from table name
just validate-cdm-parquet /path/to/sdt_sample

# Or specify class explicitly
just validate-cdm-parquet /path/to/sdt_sample Sample

# Direct Python usage
uv run python scripts/cdm_analysis/validate_parquet_linkml.py \
    /path/to/sdt_sample.parquet \
    --class Sample \
    --verbose
```

### Validate All CDM Tables

```bash
# Using default CDM database path
just validate-all-cdm-parquet

# Or specify custom path
just validate-all-cdm-parquet /custom/path/to/jmc_coral.db
```

## Command-Line Options

### validate_parquet_linkml.py

```
Usage: validate_parquet_linkml.py <parquet_file> [OPTIONS]

Required Arguments:
  parquet_file          Path to parquet file or directory

Optional Arguments:
  --class, -C NAME      LinkML class name (auto-detected if not specified)
  --schema, -s PATH     Path to LinkML schema (default: CDM schema)
  --max-rows N          Maximum rows to validate (default: all)
  --chunk-size N        Validate in chunks of N rows (for large files)
  --verbose, -v         Print detailed validation output
```

### Examples

```bash
# Validate first 1000 rows only
uv run python scripts/cdm_analysis/validate_parquet_linkml.py \
    /path/to/sdt_sample.parquet \
    --max-rows 1000

# Validate in chunks (for large files)
uv run python scripts/cdm_analysis/validate_parquet_linkml.py \
    /path/to/sdt_gene.parquet \
    --chunk-size 10000 \
    --verbose

# Use custom schema
uv run python scripts/cdm_analysis/validate_parquet_linkml.py \
    file.parquet \
    --schema my_schema.yaml \
    --class MyClass
```

## Table-to-Class Mapping

The validation script automatically detects the LinkML class from the table name:

| Table Name | LinkML Class |
|------------|--------------|
| `sdt_location` | Location |
| `sdt_sample` | Sample |
| `sdt_community` | Community |
| `sdt_reads` | Reads |
| `sdt_assembly` | Assembly |
| `sdt_bin` | Bin |
| `sdt_genome` | Genome |
| `sdt_gene` | Gene |
| `sdt_strain` | Strain |
| `sdt_taxon` | Taxon |
| `sdt_asv` | ASV |
| `sdt_protocol` | Protocol |
| `sdt_image` | Image |
| `sdt_condition` | Condition |
| `sdt_dubseq_library` | DubSeqLibrary |
| `sdt_tnseq_library` | TnSeqLibrary |
| `sdt_enigma` | ENIGMA |
| `sys_typedef` | SystemTypedef |
| `sys_ddt_typedef` | SystemDDTTypedef |
| `sys_oterm` | SystemOntologyTerm |
| `sys_process` | SystemProcess |
| `sys_process_input` | SystemProcessInput |
| `sys_process_output` | SystemProcessOutput |
| `ddt_ndarray` | DynamicDataArray |

## Validation Strategies by Table Size

The batch validation script uses different strategies based on table size:

### Small Tables (<100K rows)
**Strategy:** Full validation
**Examples:** Location, Sample, Community, Protocol, ENIGMA

```bash
validate_parquet_linkml.py sdt_location --verbose
```

### Medium Tables (100K-1M rows)
**Strategy:** Chunked validation
**Examples:** Reads, sys_oterm

```bash
validate_parquet_linkml.py sdt_reads --chunk-size 10000
```

### Large Tables (>1M rows)
**Strategy:** Sample validation (first 10K rows)
**Examples:** Gene, sys_process, sys_process_input, sys_process_output

```bash
validate_parquet_linkml.py sdt_gene --max-rows 10000
```

**Rationale:**
- Full validation of 82M+ rows is impractical
- Sample validation catches schema mismatches
- Use `--max-rows` to adjust sample size

## Interpreting Results

### Successful Validation

```
Auto-detected class: Protocol

Validating sdt_protocol
  Class: Protocol
  Total rows: 42
  Validating: 42 rows
No issues found

✅ Validation passed (42 rows)
```

### Validation Errors

```
[ERROR] [/tmp/file.yaml/0] Additional properties are not allowed
    ('unknown_field' was unexpected) in /
[ERROR] [/tmp/file.yaml/1] None is not of type 'string' in /id
[ERROR] [/tmp/file.yaml/2] 'required_field' is a required property in /

❌ Validation failed
```

**Common Error Types:**

1. **Additional properties:** Column in parquet not defined in schema
   - **Fix:** Add missing slot to schema OR remove column from data

2. **Type mismatches:** Value doesn't match expected type
   - **Example:** `None` where `string` required
   - **Fix:** Fix data quality OR make field optional in schema

3. **Required property missing:** Required field has NULL value
   - **Fix:** Populate required fields OR make field optional

## Known Issues and Limitations

### 1. Column Naming Mismatches

**Issue:** Parquet columns may not match schema slot names exactly.

**Example:**
- Schema slot: `description`
- Parquet column: `sdt_protocol_description`

**Solution:** Update schema to match CDM naming conventions (add `sdt_` prefix).

### 2. NULL Values in Required Fields

**Issue:** Some CDM tables have NULL values in fields marked as required.

**Example:** `sdt_enigma` table has `sdt_enigma_id = NULL`

**Solutions:**
- Fix data quality in CDM database
- Make field optional in schema (if appropriate)
- Document known data quality issues

### 3. Large Table Performance

**Issue:** Validating 82M+ rows is memory-intensive and slow.

**Solutions:**
- Use `--chunk-size` for chunked validation
- Use `--max-rows` for sample validation
- Skip brick tables (ddt_brick*) - they have heterogeneous schemas

### 4. Brick Tables

**Issue:** Dynamic data bricks (ddt_brick0000001, etc.) have heterogeneous schemas.

**Status:** Not currently validated - schema varies per brick.

**Future:** Implement custom validation using `sys_ddt_typedef` metadata.

## Validation Reports

### Batch Validation Output

The `validate_all_cdm_parquet.sh` script creates timestamped logs:

```
validation_reports/cdm_parquet/validation_20251201_143022.log
```

### Report Contents

```
================================================
CDM Parquet Validation Report
================================================
Database: /path/to/jmc_coral.db
Log file: validation_20251201_143022.log
Started: Mon Dec 1 14:30:22 PST 2025

=== Static Entity Tables (sdt_*) ===

[1] Validating sdt_location (Location, strategy: full)...
  ✅ PASSED
[2] Validating sdt_sample (Sample, strategy: full)...
  ✅ PASSED
...

================================================
Validation Summary
================================================
Total tables validated: 23
  ✅ Passed: 22
  ❌ Failed: 1
  ⊘ Skipped: 20

Completed: Mon Dec 1 14:35:47 PST 2025
```

## Troubleshooting

### "pandas not installed"

```bash
uv pip install pandas
```

### "pyarrow not installed"

```bash
uv pip install pyarrow
# Or update dependencies
uv sync
```

### "Schema not found"

Ensure you're running from the repository root:
```bash
cd /path/to/linkml-coral
uv run python scripts/cdm_analysis/validate_parquet_linkml.py ...
```

### "Could not infer class name"

Specify `--class` explicitly:
```bash
uv run python scripts/cdm_analysis/validate_parquet_linkml.py \
    my_file.parquet \
    --class MyClassName
```

### Memory Issues with Large Tables

Use chunking or sampling:
```bash
# Chunk-based validation
--chunk-size 10000

# Or sample first N rows
--max-rows 100000
```

## Implementation Details

### Conversion Process

1. **Read Parquet:** Uses `pandas.read_parquet()` or `pyarrow.parquet.ParquetFile`
2. **Convert to YAML:** Uses `yaml.dump()` to create temporary YAML file
3. **Validate:** Calls `linkml-validate` subprocess
4. **Parse Results:** Captures stdout/stderr for reporting

### Delta Lake Support

The script handles Delta Lake format (parquet files in directories):

```python
# Detects directory structure
if parquet_path.is_dir():
    # Read all *.parquet files in directory
    parquet_files = list(parquet_path.glob("*.parquet"))
```

### NaN Handling

Pandas NaN values are converted to YAML `null`:

```python
for record in records:
    for key, value in record.items():
        if pd.isna(value):
            record[key] = None
```

## Next Steps

1. **Fix Schema Mismatches:** Update CDM schema to match parquet column names
2. **Fix Data Quality:** Address NULL values in required fields
3. **Validate All Tables:** Run full batch validation
4. **Document Issues:** Create data quality report
5. **Implement Brick Validation:** Custom validation using sys_ddt_typedef

## Related Documentation

- [CDM Schema Implementation Summary](CDM_SCHEMA_IMPLEMENTATION_SUMMARY.md)
- [CDM Parquet Analysis Report](cdm_analysis/CDM_PARQUET_ANALYSIS_REPORT.md)
- [CORAL to CDM Mapping](CORAL_TO_CDM_MAPPING.md) *(to be created)*
- [LinkML Validation Guide](https://linkml.io/linkml/howtos/validate-data.html)

## References

- LinkML Documentation: https://linkml.io/linkml/
- LinkML Validator: https://github.com/linkml/linkml/tree/main/linkml/validator
- CDM Schema: `src/linkml_coral/schema/cdm/linkml_coral_cdm.yaml`
- Validation Scripts: `scripts/cdm_analysis/`
