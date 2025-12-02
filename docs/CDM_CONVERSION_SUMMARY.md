# CDM Conversion Summary

## Overview

Successfully implemented a LinkML to CDM table converter that applies ENIGMA Common Data Model naming conventions to the CORAL LinkML schema.

## Files Created

### 1. **linkml_to_cdm.py** (551 lines)
Python tool that converts LinkML schema to CDM table definitions.

**Features:**
- Reads LinkML YAML schema
- Optionally reads typedef.json for preferred_name support
- Applies CDM naming conventions (sdt_ prefix, snake_case, <table>_id pattern)
- Generates JSON schema and text reports
- Detects and reports potential schema issues
- Preserves all metadata (ontology terms, constraints, provenance)

### 2. **cdm_schema.json**
Machine-readable CDM schema in JSON format.

**Includes:**
- 17 table definitions
- Column specifications with data types
- Foreign key relationships
- Constraints and validation rules
- Ontology term annotations
- Provenance metadata

### 3. **cdm_report.txt**
Human-readable report showing:
- Table structure
- Column details with flags (PK, FK, REQ, UNQ, ARRAY)
- Foreign key targets
- Constraints and comments
- Original LinkML slot names

### 4. **CDM_NAMING_CONVENTIONS.md**
Complete documentation of the naming conventions and conversion process.

## CDM Naming Conventions Applied

### ✅ Table Names
- **Format**: `sdt_<snake_case_name>`
- **Example**: `Location` → `sdt_location`
- **Example**: `TnSeq_Library` → `sdt_tn_seq_library`
- **With preferred_name**: `OTU` (preferred: "ASV") → `sdt_asv`

### ✅ Primary Key Columns
- **Format**: `<table>_id`
- **Example**: `sdt_sample` → `sample_id`
- **Example**: `sdt_tn_seq_library` → `tn_seq_library_id`

### ✅ Foreign Key Columns
- **Single-valued**: `<referenced_table>_id`
  - `community_sample` → `sample_id` (references `sdt_sample.sample_id`)
- **Multi-valued**: `<referenced_table>_ids`
  - `community_defined_strains` → `strain_ids` (array, references `sdt_strain.strain_id`)

### ✅ Regular Columns
- **Format**: `snake_case`
- All lowercase, underscores only
- Examples: `read_count`, `n_contigs`, `sequencing_technology`
- Special case: `MIME type` → `mime_type`

## Conversion Examples

### Example 1: Sample Table

**LinkML Class:** `Sample`
**CDM Table:** `sdt_sample`

| LinkML Slot | CDM Column | Type | FK Target |
|-------------|------------|------|-----------|
| sample_id | sample_id | text | (PK) |
| sample_name | sample_name | text | - |
| sample_location | location_id | text | sdt_location.location_id |
| sample_depth | sample_depth | float | - |
| sample_material | sample_material | text | - |

### Example 2: Community Table with Array FK

**LinkML Class:** `Community`
**CDM Table:** `sdt_community`

| LinkML Slot | CDM Column | Type | FK Target |
|-------------|------------|------|-----------|
| community_id | community_id | text | (PK) |
| community_defined_strains | strain_ids | [text] | sdt_strain.strain_id |

### Example 3: Process Table

**LinkML Class:** `Process`
**CDM Table:** `sdt_process`

| LinkML Slot | CDM Column | Type | FK Target |
|-------------|------------|------|-----------|
| process_id | process_id | text | (PK) |
| process_protocol | protocol_id | text | sdt_protocol.protocol_id |
| process_input_objects | process_input_objects | [text] | - |
| process_output_objects | process_output_objects | [text] | - |

## Verification Results

### ✅ All Tables Converted
**Total:** 17 tables successfully converted

Tables:
1. sdt_assembly
2. sdt_bin
3. sdt_community
4. sdt_condition
5. sdt_dub_seq_library
6. sdt_gene
7. sdt_genome
8. sdt_image
9. sdt_location
10. sdt_otu
11. sdt_process
12. sdt_protocol
13. sdt_reads
14. sdt_sample
15. sdt_strain
16. sdt_taxon
17. sdt_tn_seq_library

### ✅ No Schema Issues Detected
The converter found no issues requiring LinkML schema changes. All foreign keys are valid, all naming is consistent.

### ✅ Metadata Preserved
All annotations preserved:
- Ontology terms (DA:*, ME:*, ENVO:*, etc.)
- Constraints (patterns, ranges, enums)
- Units (UO:* terms)
- Comments and descriptions
- Provenance metadata

## Usage

### Generate CDM Schema

```bash
# With typedef.json for preferred_name support
python linkml_to_cdm.py \
  src/linkml_coral/schema/linkml_coral.yaml \
  --typedef data/typedef.json \
  --json-output cdm_schema.json \
  --report-output cdm_report.txt
```

### Check for Schema Issues

```bash
python linkml_to_cdm.py \
  src/linkml_coral/schema/linkml_coral.yaml \
  --check-only
```

### View Report

```bash
# Human-readable report
cat cdm_report.txt

# JSON schema
cat cdm_schema.json | jq .
```

## Key Design Decisions

### 1. **Non-Destructive Approach**
- Does NOT modify the LinkML schema
- Generates CDM definitions as separate outputs
- Preserves full LinkML semantics

### 2. **Metadata Preservation**
- All ontology terms preserved
- Constraints maintained
- Comments and descriptions retained
- Provenance information included

### 3. **Preferred Name Support**
- Checks typedef.json for `preferred_name` field
- Currently no preferred names defined
- Ready to use when added (e.g., OTU → ASV)

### 4. **Issue Detection**
- Reports any inconsistencies
- Validates foreign key references
- Checks naming patterns
- No LinkML schema changes required

## Next Steps (If Needed)

### To Enable Preferred Names

Add to `data/typedef.json`:

```json
{
  "static_types": [
    {
      "name": "OTU",
      "preferred_name": "ASV",
      "term": "DA:0000063",
      "fields": [ ... ]
    }
  ]
}
```

This would change:
- Table: `sdt_otu` → `sdt_asv`
- Primary key: `otu_id` → `asv_id`
- FK references: `otu_id` → `asv_id`

### To Generate SQL DDL

Future enhancement: Add SQL DDL generation to create actual database tables.

```python
# Potential addition to linkml_to_cdm.py
def generate_sql_ddl(tables: List[CDMTable]) -> str:
    # Generate CREATE TABLE statements
    # Include PRIMARY KEY constraints
    # Include FOREIGN KEY constraints
    # Include CHECK constraints for patterns/ranges
```

## Integration with Existing Tools

### Compatible With:
- **linkml-store**: CDM naming can be mapped back to LinkML for querying
- **TSV loaders**: Column names match CDM conventions
- **Query system**: Table names align with `sdt_*` pattern

### Documentation Updated:
- CLAUDE.md - Added CDM conversion tool info
- CDM_NAMING_CONVENTIONS.md - Complete specification
- CDM_CONVERSION_SUMMARY.md - This summary

## Testing

```bash
# Test conversion
uv run python linkml_to_cdm.py \
  src/linkml_coral/schema/linkml_coral.yaml \
  --typedef data/typedef.json \
  --check-only

# Output:
# ✓ Converted 17 tables
# ✓ No LinkML schema issues detected
```

## Summary

Successfully created a comprehensive LinkML to CDM conversion tool that:

✅ Applies all required naming conventions
✅ Preserves semantic information
✅ Generates both machine and human-readable outputs
✅ Reports any potential issues
✅ Requires no changes to the LinkML schema
✅ Ready for preferred_name support when configured

The tool serves as both a validator and a documentation generator for the CDM table structure derived from the CORAL LinkML schema.
