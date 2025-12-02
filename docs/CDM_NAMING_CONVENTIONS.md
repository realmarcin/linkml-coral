# CDM Naming Conventions for CORAL LinkML Schema

## Overview

This document describes the Common Data Model (CDM) naming conventions applied when converting the CORAL LinkML schema to CDM table definitions.

## Key Behaviors

### Table Naming

**Base Rule**: All tables are prefixed with `sdt_` and use `snake_case`.

```
LinkML Class → CDM Table
Location     → sdt_location
TnSeq_Library → sdt_tn_seq_library
```

**With Preferred Name**: If a type defines `preferred_name` in typedef.json, the CDM table uses that name.

```
# Example (if configured):
OTU → preferred_name: "ASV" → sdt_asv
```

### Column Naming

All column names are **lowercase snake_case** (underscores only, no hyphens or camelCase).

#### Primary Key Columns

Format: `<table>_id`

```
Table: sdt_sample
Primary Key: sample_id

Table: sdt_tn_seq_library
Primary Key: tn_seq_library_id
```

When a preferred_name is used, the primary key reflects the preferred name:

```
# If OTU has preferred_name "ASV"
Table: sdt_asv
Primary Key: asv_id  (not otu_id)
```

#### Foreign Key Columns

**Single-valued FK**: `<referenced_table>_id`

```
LinkML:
  community_sample:
    range: string
    annotations:
      foreign_key: Sample.name

CDM:
  Column: sample_id
  FK Target: sdt_sample.sample_id
```

**Multi-valued FK**: `<referenced_table>_ids` (plural)

```
LinkML:
  community_defined_strains:
    range: string
    multivalued: true
    annotations:
      foreign_key: Strain.name

CDM:
  Column: strain_ids
  FK Target: sdt_strain.strain_id
  Type: [text]
```

#### Regular Columns

All other columns use snake_case derived from the LinkML slot name:

```
LinkML Slot       → CDM Column
read_count        → read_count
n_contigs         → n_contigs
sequencing_technology → sequencing_technology
MIME type         → mime_type
```

### Foreign Key Value Rewriting

**Important**: When preferred names are used, the stored ID values must also be rewritten:

```
# If OTU → ASV with preferred_name
Original ID in data: "OTU000001"
Rewritten ID:        "ASV000001"

# FK columns referencing this table also use the new prefix
```

## Conversion Tool: `linkml_to_cdm.py`

### Usage

```bash
# Basic conversion (outputs to stdout)
python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml

# With typedef.json for preferred_name support
python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml \
  --typedef data/typedef.json

# Generate JSON schema
python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml \
  --typedef data/typedef.json \
  --json-output cdm_schema.json

# Generate text report
python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml \
  --typedef data/typedef.json \
  --report-output cdm_report.txt

# Check for LinkML schema issues only
python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml \
  --check-only
```

### Output Formats

#### JSON Schema (`cdm_schema.json`)

Complete machine-readable schema including:
- Table definitions
- Column specifications
- Data types
- Constraints
- Foreign key relationships
- Ontology term annotations
- Provenance metadata

#### Text Report (`cdm_report.txt`)

Human-readable summary with:
- Table listings
- Column details
- FK relationships
- Constraints and comments
- Any detected issues

## Complete Example: Sample Table

### LinkML Schema

```yaml
Sample:
  slots:
  - sample_id
  - sample_name
  - sample_location
  - sample_depth
  - sample_description

slots:
  sample_id:
    range: string
    identifier: true
    required: true

  sample_name:
    range: string
    required: true
    annotations:
      unique: true

  sample_location:
    range: string
    required: true
    annotations:
      foreign_key: Location.name

  sample_depth:
    range: float
    annotations:
      units_term: UO:0000008
    comments:
    - in meters below ground level

  sample_description:
    range: string
```

### CDM Table Definition

```
Table: sdt_sample

Columns:
  sample_id             text     PK, REQ
  sample_name           text     REQ, UNQ
  location_id           text     FK, REQ    → sdt_location.location_id
  sample_depth          float    -
  sample_description    text     -
```

### Key Transformations

1. **Class name**: `Sample` → `sdt_sample`
2. **Primary key**: `sample_id` → `sample_id` (stays same, already correct format)
3. **Foreign key**: `sample_location` → `location_id` (references sdt_location table)
4. **Regular fields**: Keep snake_case as-is

## Adding Preferred Names

To enable preferred name support, add to typedef.json:

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

This will cause:
- Table: `sdt_asv` (not `sdt_otu`)
- Primary key: `asv_id` (not `otu_id`)
- FK columns referencing it: `asv_id` or `asv_ids`

## Data Type Mappings

| LinkML Type | CDM Type | Notes |
|-------------|----------|-------|
| string      | text     | Default for text fields |
| integer     | int      | Whole numbers |
| float       | float    | Decimal numbers |
| double      | float    | Treated same as float |
| boolean     | boolean  | True/false |
| date        | text     | ISO 8601 format |
| datetime    | text     | ISO 8601 format |
| uri         | text     | URLs and URIs |

**Multivalued fields**: Wrapped in brackets `[type]`
```
multivalued: true, range: string → [text]
```

## Constraint Preservation

The converter preserves all LinkML constraints:

- **Pattern validation**: Regular expressions
- **Range constraints**: min/max values for numbers
- **Enum constraints**: Controlled vocabularies
- **Ontology constraints**: Term references (e.g., ENVO:00010483)

Example:
```yaml
LinkML:
  latitude:
    range: float
    minimum_value: -90
    maximum_value: 90

CDM:
  Column: location_latitude
  Type: float
  Constraint: [-90, 90]
```

## Issues and Recommendations Report

The tool generates a report of any potential issues:

### Example Issues

```
⚠️ Community: typedef.json has typo with FK pointing to [Strain.Name]
   with capital N - Using lowercase name to match actual Strain field
```

These issues are informational and show where the LinkML schema has already compensated for inconsistencies in the original typedef.json.

## Provenance Metadata

Tables include provenance metadata from the LinkML schema:

- `used_for_provenance`: Whether table is used in provenance tracking
- `process_types`: Associated PROCESS ontology terms
- `process_inputs`: Expected input entity types

This metadata is preserved in the JSON output but not required for basic table creation.

## See Also

- [linkml_to_cdm.py](linkml_to_cdm.py) - Conversion tool source code
- [cdm_schema.json](cdm_schema.json) - Generated CDM schema (JSON format)
- [cdm_report.txt](cdm_report.txt) - Generated CDM report (human-readable)
- [LINKML_STORE_USAGE.md](LINKML_STORE_USAGE.md) - Using the data with linkml-store
