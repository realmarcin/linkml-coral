# KBase CDM LinkML Schema Implementation Summary

**Date:** 2025-12-01
**Status:** ✅ COMPLETE - All phases finished
**Schema Validation:** ✅ PASSING

---

## Executive Summary

Successfully created and validated a modular LinkML schema for the KBase Common Data Model (CDM) based on comprehensive analysis of 44 parquet tables containing 83M+ rows of ENIGMA CORAL data.

**Key Achievements:**
- ✅ Analyzed KBase CDM parquet database structure
- ✅ Created reproducible analysis scripts and documentation
- ✅ Implemented modular schema with 4 sub-modules + main schema
- ✅ Defined 17 static entity classes with CDM transformations
- ✅ Defined 6 system table classes for provenance and ontology
- ✅ Defined dynamic data infrastructure for measurement bricks
- ✅ Fixed all slot naming conflicts (FK references use `{entity}_ref` pattern)
- ✅ Fixed duplicate identifier issue (CDMEntity mixin simplified)
- ✅ Schema validation passing (`gen-yaml` successful)
- ✅ Project files generated (Python, JSON Schema, OWL, etc.)

---

## Phase 1: Analysis & Foundation (COMPLETE)

### Analysis Scripts Created
**Location:** `scripts/cdm_analysis/`

1. **analyze_cdm_parquet.py** (14KB)
   - Reads all 44 parquet tables
   - Generates row counts, column metadata, data types
   - Identifies ontology term patterns
   - Outputs comprehensive statistics

2. **generate_cdm_schema_report.py** (11KB)
   - Exports machine-readable JSON schema report
   - Includes type definitions from sys_typedef
   - Documents dynamic data structure
   - Output: `docs/cdm_analysis/cdm_schema_report.json` (238KB)

3. **examine_typedef_details.py** (5.3KB)
   - Extracts field-by-field typedef analysis
   - Documents constraints and FK relationships
   - Shows ontology mappings

### Documentation Generated
**Location:** `docs/cdm_analysis/`

1. **CDM_PARQUET_ANALYSIS_REPORT.md** (22KB)
   - Comprehensive analysis of all 44 tables
   - Ontology term splitting pattern documentation
   - Schema differences from original CORAL
   - Naming conventions and FK relationships
   - Recommendations for Link ML schema

2. **cdm_schema_report.json** (238KB)
   - Machine-readable schema metadata
   - Complete column details for all tables
   - Type definitions and constraints
   - Ready for automated schema generation

### Justfile Targets Added
**Location:** `project.justfile`

```bash
just analyze-cdm              # Analyze KBase CDM parquet tables
just cdm-report               # Generate CDM schema reports
just cdm-compare-schemas      # Compare CORAL vs CDM
just clean-cdm                # Clean CDM outputs
```

### Key Findings from Analysis

**Database Scale:**
- 44 total tables (6 system, 17 static, 21 dynamic)
- 272,934 static entity rows
- 82.6M dynamic data rows (measurements)
- 142,958 provenance records
- 10,594 ontology terms

**Critical Patterns Discovered:**

1. **Ontology Term Splitting** (15 fields across 5 entities)
   ```
   CORAL:  material (enum with ontology constraint)
   CDM:    material_sys_oterm_id + material_sys_oterm_name
   ```
   - Location: 4 fields (continent, country, biome, feature)
   - Sample: 2 fields (material, env_package)
   - Reads: 2 fields (read_type, sequencing_technology)
   - Community: 1 field (community_type)
   - Process: 6 fields (process_type, person, campaign, etc.)

2. **CDM Naming Conventions**
   - Tables: `sdt_<entity>`, `ddt_<entity>`, `sys_<entity>`
   - Primary keys: `sdt_<entity>_id` (pattern: `EntityName\d{7}`)
   - Names: `sdt_<entity>_name` (unique, used for FK)
   - All columns: snake_case with entity prefix

3. **FK References Use Names, Not IDs**
   ```
   Sample.sdt_location_name → Location.sdt_location_name
   ```
   Not: `Sample.location_id → Location.sdt_location_id`

4. **Centralized Ontology Catalog**
   - sys_oterm table with 10,594 terms
   - Supports multiple ontologies (ME, ENVO, UO, etc.)
   - Hierarchical structure via parent_sys_oterm_id

5. **Denormalized Provenance**
   - sys_process (142K records)
   - sys_process_input (90K records)
   - sys_process_output (38K records)
   - Complete lineage tracking

---

## Phase 2: Modular Schema Creation (COMPLETE - needs minor fixes)

### Schema Module Structure
**Location:** `src/linkml_coral/schema/cdm/`

```
cdm/
├── cdm_base.yaml              # Common types, mixins, patterns (✅ Complete)
├── cdm_static_entities.yaml   # 17 entity classes (⚠️  Needs FK slot fixes)
├── cdm_system_tables.yaml     # 6 system classes (✅ Complete)
├── cdm_dynamic_data.yaml      # Brick infrastructure (✅ Complete)
└── linkml_coral_cdm.yaml      # Main schema entry point (✅ Complete)
```

### 1. cdm_base.yaml (✅ COMPLETE)

**Purpose:** Foundation types, mixins, and patterns

**Contents:**
- 10 semantic types (Date, Time, Link, Latitude, Longitude, Count, Size, Rate, Depth, Elevation)
- 2 new types (OntologyTermID, EntityName)
- 3 mixins:
  - `OntologyTermPair` - Pattern for ontology term splitting
  - `CDMEntity` - Base for all sdt_* entities
  - `SystemEntity` - Base for all sys_* tables
- Common slots (sys_oterm_id, sys_oterm_name, link)

**Key Pattern - OntologyTermPair Mixin:**
```yaml
OntologyTermPair:
  mixin: true
  description: |
    Mixin for ontology-constrained fields in KBase CDM.

    The CDM splits each ontology-controlled field into two columns:
    - {field}_sys_oterm_id: CURIE identifier (FK to sys_oterm)
    - {field}_sys_oterm_name: Human-readable term name
```

**Key Pattern - CDMEntity Mixin:**
```yaml
CDMEntity:
  mixin: true
  attributes:
    id:
      identifier: true
      required: true
      comments:
        - Format: EntityName followed by 7 digits
        - Corresponds to sdt_{entity}_id column
    name:
      range: EntityName
      required: true
      comments:
        - Corresponds to sdt_{entity}_name column
        - Used for FK references instead of ID
```

### 2. cdm_static_entities.yaml (⚠️ NEEDS FK SLOT FIXES)

**Purpose:** 17 core scientific entity classes

**Classes Defined:**
1. Location - Sampling locations with geography
2. Sample - Environmental samples
3. Community - Microbial communities
4. Reads - Sequencing reads datasets
5. Assembly - Genome assemblies
6. Bin - Metagenomic bins
7. Genome - Assembled genomes
8. Gene - Annotated genes
9. Strain - Microbial strains
10. Taxon - Taxonomic classifications
11. ASV - Amplicon Sequence Variants (renamed from OTU)
12. Protocol - Experimental protocols
13. Image - Microscopy images
14. Condition - Growth conditions
15. DubSeqLibrary - DubSeq libraries
16. TnSeqLibrary - TnSeq libraries
17. ENIGMA - Root entity (singleton)

**Transformation Example - Location:**
```yaml
Location:
  mixins:
    - CDMEntity
  slots:
    - sdt_location_id
    - sdt_location_name
    - latitude
    - longitude
    - continent_sys_oterm_id      # Split ontology term
    - continent_sys_oterm_name
    - country_sys_oterm_id        # Split ontology term
    - country_sys_oterm_name
    - biome_sys_oterm_id          # Split ontology term
    - biome_sys_oterm_name
    - feature_sys_oterm_id        # Split ontology term
    - feature_sys_oterm_name
```

**Known Issue:**
- Duplicate slot names between entity's own `sdt_{entity}_name` and FK references
- **Solution:** Rename FK reference slots to use `{entity}_ref` pattern
  - Example: `Sample.location_ref` instead of `Sample.sdt_location_name`
- Status: Partially implemented, needs completion

### 3. cdm_system_tables.yaml (✅ COMPLETE)

**Purpose:** System tables for metadata, provenance, and ontology

**Classes Defined:**
1. **SystemTypedef** - Type definitions (equivalent to typedef.json)
   - Maps CORAL entity types to CDM table/column names
   - 118 rows defining static entity schema

2. **SystemDDTTypedef** - Dynamic data type definitions
   - Defines brick schemas (dimensions, variables, units)
   - 101 rows defining 20 brick types

3. **SystemOntologyTerm** - Centralized ontology catalog
   - 10,594 ontology terms from multiple sources
   - Hierarchical structure with parent references

4. **SystemProcess** - Provenance tracking
   - 142,958 process records
   - Links inputs → process → outputs
   - Temporal metadata and protocol references

5. **SystemProcessInput** - Normalized inputs
   - 90,395 rows
   - Denormalizes input_objects array for queries

6. **SystemProcessOutput** - Normalized outputs
   - 38,228 rows
   - Denormalizes output_objects array for queries

### 4. cdm_dynamic_data.yaml (✅ COMPLETE)

**Purpose:** Brick infrastructure for N-dimensional measurement arrays

**Classes Defined:**
1. **DynamicDataArray** - Brick index (ddt_ndarray)
   - Catalogs 20 available bricks
   - Stores shape metadata and entity associations

2. **BrickDimension** (abstract)
   - Template for dimension metadata
   - Semantic meaning via ontology terms

3. **BrickVariable** (abstract)
   - Template for variable metadata
   - Data types, units, constraints

4. **Brick** (abstract)
   - Base for all ddt_brick* tables
   - Heterogeneous schemas defined in sys_ddt_typedef

**Example Brick Structure:**
```
Brick0000010:
  Dimensions: [Environmental Sample (209), Molecule (52), State (3), Statistic (3)]
  Total rows: 209 × 52 × 3 × 3 = 52,884
  Variables: Concentration, Molecular Weight
  Units: Tracked via sys_oterm
```

**Enums Defined:**
- BrickDataType: float, int, bool, text, oterm_ref, object_ref
- DimensionSemantics: 8 common dimension types
- VariableSemantics: 8 common variable types

### 5. linkml_coral_cdm.yaml (✅ COMPLETE)

**Purpose:** Main schema entry point with imports

**Features:**
- Imports all 4 sub-modules
- Redefines key enums from original CORAL
- Comprehensive documentation and annotations
- Schema-level metadata (data volumes, dates, etc.)

**Enums Included:**
- StrandEnum (forward, reverse_complement)
- ReadTypeEnum (paired_end, single_end)
- SequencingTechnologyEnum (illumina, pacbio, nanopore, sanger)
- CommunityTypeEnum (isolate, enrichment, assemblage, environmental, active_fraction)
- MaterialEnum, BiomeEnum

---

## Schema Statistics

### Classes
- **Base/Mixins:** 3 (OntologyTermPair, CDMEntity, SystemEntity)
- **Static Entities:** 17 (Location, Sample, Gene, etc.)
- **System Tables:** 6 (SystemTypedef, SystemOntologyTerm, SystemProcess, etc.)
- **Dynamic Data:** 3 abstract (DynamicDataArray, BrickDimension, BrickVariable)
- **Total:** 29 classes

### Types
- **From CORAL:** 10 (Date, Time, Link, Latitude, Longitude, Count, Size, Rate, Depth, Elevation)
- **CDM-specific:** 2 (OntologyTermID, EntityName)
- **Total:** 12 types

### Slots
- **Base slots:** 3 (sys_oterm_id, sys_oterm_name, link)
- **Static entity slots:** ~100 (includes all entity-specific fields)
- **System table slots:** ~40
- **Dynamic data slots:** ~15
- **Total:** ~158 slots

### Enums
- **From CORAL:** 5 main enums
- **CDM-specific:** 2 (BrickDataType, DimensionSemantics, VariableSemantics)
- **Total:** ~8 enums

---

## Key Transformations from CORAL to CDM

### 1. Ontology Term Splitting
**Impact:** 15 fields across 5 entity types

| Entity | Fields Split | Example |
|--------|-------------|---------|
| Location | 4 | `biome` → `biome_sys_oterm_id` + `biome_sys_oterm_name` |
| Sample | 2 | `material` → `material_sys_oterm_id` + `material_sys_oterm_name` |
| Reads | 2 | `read_type` → `read_type_sys_oterm_id` + `read_type_sys_oterm_name` |
| Community | 1 | `community_type` → `community_type_sys_oterm_id` + `community_type_sys_oterm_name` |
| Process | 6 | `process_type`, `person`, `campaign`, etc. |

### 2. Naming Convention Changes

| Original CORAL | KBase CDM | Pattern |
|----------------|-----------|---------|
| `id` | `sdt_{entity}_id` | EntityName\d{7} |
| `name` | `sdt_{entity}_name` | Unique, used for FK |
| `location` (FK) | `sdt_location_name` (FK) | References name, not ID |

### 3. New Fields Added

| Entity | New Field | Purpose |
|--------|-----------|---------|
| Assembly, Genome, Reads, Image, Protocol | `link` | External data references |
| All ontology fields | `*_sys_oterm_id`, `*_sys_oterm_name` | Ontology term pairs |

### 4. Entity Renames

| Original | CDM | Reason |
|----------|-----|--------|
| OTU | ASV | Preferred terminology (Amplicon Sequence Variant) |

---

## Issues Resolved

### Fixed Issues

1. **Duplicate Slot Names** (✅ RESOLVED)
   - Problem: Entity's own `sdt_{entity}_name` conflicted with FK reference slots
   - Solution: Renamed all FK slots to `{entity}_ref` pattern
   - Fixed slots:
     - `location_ref` (Sample → Location)
     - `sample_ref` (Community → Sample)
     - `parent_community_ref` (Community → Community, self-referential)
     - `defined_strains_ref` (Community → Strain, multivalued)
     - `strain_ref` (Assembly, Genome → Strain)
     - `assembly_ref` (Bin → Assembly)
     - `genome_ref` (Gene, Strain, DubSeqLibrary, TnSeqLibrary → Genome)
     - `derived_from_strain_ref` (Strain → Strain, self-referential)
   - Status: ✅ Complete, all conflicts resolved

2. **Duplicate Identifier Issue** (✅ RESOLVED)
   - Problem: CDMEntity mixin defined `id` attribute with `identifier: true`, conflicting with entity-specific ID slots
   - Error: `ValueError: Class "Location" - multiple keys/identifiers not allowed`
   - Solution: Simplified CDMEntity mixin to not define slots, only used for documentation/grouping
   - Status: ✅ Complete, schema validates successfully

3. **Schema Validation** (✅ PASSING)
   - `gen-yaml` runs successfully with only minor warnings (date/time type overlap)
   - `gen-project` generates all output formats (Python, JSON Schema, OWL, GraphQL, etc.)
   - Python dataclasses generated correctly (112KB file)
   - Status: ✅ Complete

### Next Steps (Optional Enhancements)

1. **Create Additional Documentation** (2-3 hours)
   - docs/CORAL_TO_CDM_MAPPING.md - Detailed field transformation guide
   - docs/CDM_VALIDATION_GUIDE.md - How to validate data against CDM schema
   - Update CLAUDE.md with CDM schema usage instructions

4. **Create Validation Examples** (1 hour)
   - tests/data/cdm/valid/ - Valid examples for each entity
   - tests/data/cdm/invalid/ - Negative test cases
   - Demonstrate ontology term splitting, FK references, etc.

5. **Generate Visualizations** (1 hour)
   - CDM ER diagrams
   - Relationship graphs
   - HTML viewer for CDM schema

6. **Commit and Document** (30 min)
   - Git commit with comprehensive message
   - Update project documentation
   - Create migration guide

---

## File Inventory

### Analysis Scripts
```
scripts/cdm_analysis/
├── analyze_cdm_parquet.py           (14KB)
├── generate_cdm_schema_report.py    (11KB)
└── examine_typedef_details.py       (5.3KB)
```

### Documentation
```
docs/
├── cdm_analysis/
│   ├── CDM_PARQUET_ANALYSIS_REPORT.md  (22KB)
│   └── cdm_schema_report.json          (238KB)
└── CDM_SCHEMA_IMPLEMENTATION_SUMMARY.md (this file)
```

### Schema Files
```
src/linkml_coral/schema/cdm/
├── cdm_base.yaml                    (✅ Complete)
├── cdm_static_entities.yaml         (⚠️  Needs FK fixes)
├── cdm_system_tables.yaml           (✅ Complete)
├── cdm_dynamic_data.yaml            (✅ Complete)
└── linkml_coral_cdm.yaml            (✅ Complete)
```

### Configuration
```
project.justfile                     (Updated with CDM targets)
```

---

## Usage Examples

### Analyze CDM Database
```bash
just analyze-cdm
just cdm-report
```

### Generate CDM Schema
```bash
# After fixing duplicate slots:
uv run gen-yaml src/linkml_coral/schema/cdm/linkml_coral_cdm.yaml
uv run gen-project -d project/cdm src/linkml_coral/schema/cdm/linkml_coral_cdm.yaml
```

### Compare Schemas
```bash
just cdm-compare-schemas
# Outputs comparison of CORAL vs CDM
```

---

## Migration Path

### From Original CORAL Data → KBase CDM Format

1. **Split Ontology Fields**
   ```python
   # CORAL format:
   {"biome": "terrestrial biome"}

   # CDM format:
   {
     "biome_sys_oterm_id": "ENVO:00000446",
     "biome_sys_oterm_name": "terrestrial biome"
   }
   ```

2. **Rename ID/Name Fields**
   ```python
   # CORAL format:
   {"id": "Location001", "name": "Site A"}

   # CDM format:
   {
     "sdt_location_id": "Location0000001",
     "sdt_location_name": "Site A"
   }
   ```

3. **Convert FK References**
   ```python
   # CORAL format:
   {"location": "Location001"}  # References ID

   # CDM format:
   {"location_ref": "Site A"}  # References name
   ```

4. **Add External Links**
   ```python
   # CDM adds link fields where applicable:
   {
     "sdt_assembly_id": "Assembly0000001",
     "link": "https://data.kbase.us/assemblies/ASM001"
   }
   ```

---

## Provenance Tracking Example

### Sample → Reads → Assembly → Genome Lineage

```yaml
# sys_process record:
sys_process_id: Process0001234
process_type_sys_oterm_id: ME:0000113  # Sequencing
process_type_sys_oterm_name: "Illumina Sequencing"
input_objects: ["Sample:Sample0000042"]
output_objects: ["Reads:Reads0000123"]
sdt_protocol_name: "Illumina HiSeq Protocol v2.1"
date_start: "2023-05-15"

# Normalized in sys_process_input:
sys_process_id: Process0001234
input_object_type: "Sample"
input_object_name: "Sample0000042"
input_index: 0

# Normalized in sys_process_output:
sys_process_id: Process0001234
output_object_type: "Reads"
output_object_name: "Reads0000123"
output_index: 0
```

---

## Contact & Contribution

**Implementation Date:** 2025-12-01
**LinkML Version:** 1.8.x
**Python Version:** 3.13

**Key Resources:**
- Original CORAL Schema: `src/linkml_coral/schema/linkml_coral.yaml`
- KBase CDM Parquet DB: `/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db`
- Analysis Scripts: `scripts/cdm_analysis/`
- Documentation: `docs/cdm_analysis/`

**Generated with:** Claude Code (Anthropic)
**Project:** ENIGMA linkml-coral
**Repository:** https://github.com/realmarcin/linkml-coral
