# KBase CDM Parquet Database Analysis Report

**Database Location:** `/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db`

**Analysis Date:** 2025-12-01

---

## Executive Summary

The KBase CDM (Common Data Model) database contains **44 tables** organized into three categories:
- **6 system tables** (`sys_*`): Metadata, type definitions, provenance, and ontology catalogs
- **17 static data tables** (`sdt_*`): Core scientific entities (samples, assemblies, genomes, etc.)
- **21 dynamic data tables** (`ddt_*`): Measurement arrays stored as "bricks" with flexible schemas

**Total Data Volume:**
- **272,934 rows** across static data tables
- **82.6 million rows** across dynamic data tables (bricks)
- **142,958 process records** tracking provenance
- **10,594 ontology terms** in catalog

---

## 1. System Tables Analysis

### 1.1 sys_typedef (118 rows)
**Purpose:** Maps CORAL static types to CDM table/column names with constraints

**Key Columns:**
- `type_name`: CORAL entity type (e.g., "Gene", "Bin", "Assembly")
- `field_name`: Original CORAL field name
- `cdm_column_name`: Mapped CDM column name (snake_case with prefixes)
- `scalar_type`: Data type (text, int, float, [text] for arrays)
- `pk`, `upk`, `fk`: Primary key, unique key, foreign key flags
- `constraint`: Validation patterns or ontology constraints
- `units_sys_oterm_id`, `type_sys_oterm_id`: Ontology term references

**Key Findings:**
- Defines schema for 18 entity types
- Documents field transformations from CORAL to CDM
- Includes validation constraints and ontology mappings
- Foreign key relationships explicitly defined

### 1.2 sys_ddt_typedef (101 rows)
**Purpose:** Defines dynamic data table schemas (bricks and microtypes)

**Key Columns:**
- `ddt_ndarray_id`: Brick identifier (e.g., "Brick0000010")
- `cdm_column_name`: Column name in brick table
- `cdm_column_data_type`: "variable", "dimension_variable", or "dimension_index"
- `scalar_type`: Data type (float, object_ref, oterm_ref, text, int, bool)
- `dimension_number`, `variable_number`: Position in N-dimensional array
- `dimension_oterm_id/name`, `variable_oterm_id/name`: Semantic metadata
- `unit_sys_oterm_id/name`: Measurement units

**Key Findings:**
- 20 brick types defined with varying dimensionality
- Supports complex multi-dimensional arrays (e.g., [209, 52, 3, 3])
- Dimension semantics (Environmental Sample, Molecule, State, Statistic)
- Variable semantics (Concentration, Molecular Weight, etc.)

### 1.3 sys_oterm (10,594 rows)
**Purpose:** Central ontology term catalog

**Key Columns:**
- `sys_oterm_id`: CURIE (e.g., "ME:0000129", "ENVO:00002041")
- `sys_oterm_name`: Human-readable term name
- `sys_oterm_ontology`: Source ontology
- `parent_sys_oterm_id`: Hierarchical relationships
- `sys_oterm_definition`: Term definitions
- `sys_oterm_synonyms`, `sys_oterm_links`, `sys_oterm_properties`: Additional metadata

**Key Findings:**
- Centralized ontology management
- Primary ontology: `context_measurement_ontology` (custom ENIGMA ontology)
- Supports ENVO, UO (units), PROCESS, CONTINENT, COUNTRY, MIxS, and other standard ontologies
- Hierarchical structure with parent references

### 1.4 sys_process (142,958 rows)
**Purpose:** Provenance tracking for all data transformations

**Key Columns:**
- `sys_process_id`: Unique process identifier
- `process_sys_oterm_id/name`: Process type (e.g., "Assay Growth", "Sequencing")
- `person_sys_oterm_id/name`: Person who performed the process
- `campaign_sys_oterm_id/name`: Research campaign
- `sdt_protocol_name`: Protocol used
- `date_start`, `date_end`: Temporal metadata
- `input_objects`, `output_objects`: Arrays of entity references (type:id format)

**Key Findings:**
- Complete provenance lineage for all data
- Links processes to protocols, people, and campaigns
- Input/output tracking enables full dependency graph
- Supports multiple inputs and outputs per process

### 1.5 sys_process_input (90,395 rows)
**Purpose:** Normalized process input relationships

**Key Columns:**
- `sys_process_id`: Process reference
- `sdt_<entity>_id`: Foreign keys to input entities (Assembly, Bin, Community, Genome, Location, Reads, Sample, Strain, TnSeq_Library)

**Key Findings:**
- One row per (process, input) pair
- Denormalized for query performance
- Null columns for entities not involved in specific process

### 1.6 sys_process_output (38,228 rows)
**Purpose:** Normalized process output relationships

**Key Columns:**
- `sys_process_id`: Process reference
- Entity ID columns for outputs (including `ddt_ndarray_id` for brick outputs)

**Key Findings:**
- Similar structure to sys_process_input
- Includes dynamic data (bricks) as outputs
- Enables forward and backward provenance queries

---

## 2. Static Data Tables (sdt_*)

### 2.1 Naming Conventions

**Table Names:** `sdt_<snake_case_entity_name>`
- Original CORAL "OTU" → `sdt_asv` (preferred name)
- "TnSeq Library" → `sdt_tnseq_library`

**Column Names:**
- Primary keys: `sdt_<entity>_id` (e.g., `sdt_sample_id`)
- Names: `sdt_<entity>_name` (e.g., `sdt_sample_name`)
- Foreign keys: `sdt_<referenced_entity>_name` (uses name, not ID for FKs)
- Ontology term splitting: `<field>_sys_oterm_id` + `<field>_sys_oterm_name`

### 2.2 Ontology Term Splitting Pattern

**Original CORAL fields with ontology constraints are split into two columns:**

Example from `sdt_sample`:
- `material` → `material_sys_oterm_id` (CURIE) + `material_sys_oterm_name` (label)
- `env_package` → `env_package_sys_oterm_id` + `env_package_sys_oterm_name`

Example from `sdt_location`:
- `continent` → `continent_sys_oterm_id` + `continent_sys_oterm_name`
- `country` → `country_sys_oterm_id` + `country_sys_oterm_name`
- `biome` → `biome_sys_oterm_id` + `biome_sys_oterm_name`
- `feature` → `feature_sys_oterm_id` + `feature_sys_oterm_name`

Example from `sdt_reads`:
- `read_type` → `read_type_sys_oterm_id` + `read_type_sys_oterm_name`
- `sequencing_technology` → `sequencing_technology_sys_oterm_id` + `sequencing_technology_sys_oterm_name`

Example from `sdt_community`:
- `community_type` → `community_type_sys_oterm_id` + `community_type_sys_oterm_name`

**Benefits:**
- Enables ontology validation via FK to sys_oterm
- Preserves human-readable labels for queries
- Supports ontology evolution without data migration

### 2.3 Table Inventory and Sizes

| Table | Rows | Key Columns | Notes |
|-------|------|-------------|-------|
| **sdt_asv** | 213,044 | sdt_asv_id, sdt_asv_name | ASV (Amplicon Sequence Variant) sequences |
| **sdt_reads** | 19,307 | sdt_reads_id, sdt_reads_name, read_count, read_type_*, sequencing_technology_*, link | Sequencing reads with ontology terms |
| **sdt_gene** | 15,015 | sdt_gene_id, sdt_gene_name, sdt_genome_name, contig_number, strand, start, stop, function | Gene annotations |
| **sdt_genome** | 6,688 | sdt_genome_id, sdt_genome_name, sdt_strain_name, n_contigs, n_features, link | Assembled genomes |
| **sdt_sample** | 4,330 | sdt_sample_id, sdt_sample_name, sdt_location_name, depth, elevation, date, material_*, env_package_* | Environmental samples with spatial/temporal metadata |
| **sdt_assembly** | 3,427 | sdt_assembly_id, sdt_assembly_name, sdt_strain_name, n_contigs, link | Sequence assemblies |
| **sdt_taxon** | 3,276 | sdt_taxon_id, sdt_taxon_name, ncbi_taxid | Taxonomic classifications |
| **sdt_strain** | 3,110 | sdt_strain_id, sdt_strain_name, sdt_genome_name, derived_from_sdt_strain_name, sdt_gene_names_changed | Microbial strains |
| **sdt_community** | 2,209 | sdt_community_id, sdt_community_name, community_type_*, sdt_sample_name, parent_sdt_community_name, defined_sdt_strain_names | Microbial communities |
| **sdt_condition** | 1,046 | sdt_condition_id, sdt_condition_name | Growth conditions |
| **sdt_location** | 594 | sdt_location_id, sdt_location_name, latitude, longitude, continent_*, country_*, region, biome_*, feature_* | Sampling locations |
| **sdt_bin** | 623 | sdt_bin_id, sdt_bin_name, sdt_assembly_name, contigs | Genome bins from metagenomes |
| **sdt_image** | 218 | sdt_image_id, sdt_image_name, mime_type, size, dimensions, link | Microscopy and other images |
| **sdt_protocol** | 42 | sdt_protocol_id, sdt_protocol_name, description, link | Experimental protocols |
| **sdt_dubseq_library** | 3 | sdt_dubseq_library_id, sdt_dubseq_library_name, sdt_genome_name, n_fragments | DubSeq libraries |
| **sdt_tnseq_library** | 1 | sdt_tnseq_library_id, sdt_tnseq_library_name, sdt_genome_name, primers_model, n_mapped_reads, etc. | TnSeq library |
| **sdt_enigma** | 1 | sdt_enigma_id | Root entity (database singleton) |

### 2.4 Foreign Key Relationships

**Key Patterns:**
- FKs use `_name` suffix, not `_id` (e.g., `sdt_location_name` in Sample references Location.name)
- Self-referential relationships: Community.parent_sdt_community_name, Strain.derived_from_sdt_strain_name
- Many-to-many via arrays: Community.defined_sdt_strain_names (array of strain names)

**Relationship Graph:**
```
Location
  └─ Sample
      ├─ Community
      │   └─ (parent_community, defined_strains)
      └─ Reads
          └─ Assembly
              ├─ Bin
              │   └─ Genome
              │       ├─ Gene
              │       ├─ DubSeq_Library
              │       └─ TnSeq_Library
              └─ Genome

Strain
  ├─ Assembly
  ├─ Genome
  └─ (derived_from relationship)

Image (standalone, linked via sys_process)
Protocol (referenced by sys_process)
Condition (referenced by Community)
Taxon (standalone)
ASV (standalone, linked via bricks)
```

### 2.5 Schema Differences from Original CORAL

**New Fields:**
- `link`: External URLs/references (Assembly, Genome, Reads, Image, Protocol)
- Ontology term splitting (see section 2.2)
- `sdt_` prefix on all ID and name columns

**Renamed Fields:**
- `id` → `sdt_<entity>_id`
- `name` → `sdt_<entity>_name`
- Foreign key references use `sdt_<entity>_name` convention

**Split Fields:**
- All ontology-constrained fields split into `_sys_oterm_id` + `_sys_oterm_name` pairs

**Normalized Structures:**
- Process inputs/outputs denormalized into separate tables for query performance

---

## 3. Dynamic Data Tables (ddt_*)

### 3.1 ddt_ndarray (Brick Index) - 20 rows

**Purpose:** Index of all measurement bricks with metadata

**Key Columns:**
- `ddt_ndarray_id`: Brick identifier (e.g., "Brick0000010")
- `ddt_ndarray_name`: Descriptive name (e.g., "adams_metals_100ws.ndarray")
- `ddt_ndarray_description`: Full description
- `ddt_ndarray_type_sys_oterm_id/name`: Brick type (e.g., "Chemical Measurement")
- `ddt_ndarray_shape`: Array dimensions (e.g., [209, 52, 3, 3])
- `ddt_ndarray_dimension_types_sys_oterm_id/name`: Dimension semantics (arrays)
- `ddt_ndarray_dimension_variable_types_sys_oterm_id/name`: Variables per dimension
- `ddt_ndarray_variable_types_sys_oterm_id/name`: Value variables
- `withdrawn_date`, `superceded_by_ddt_ndarray_id`: Versioning metadata

**Example Brick:**
```
Brick0000010: adams_metals_100ws.ndarray
  Description: Adams Lab Metals Measurements for 100 Well Survey
  Type: Chemical Measurement (DA:0000005)
  Shape: [209, 52, 3, 3]
  Dimensions:
    1. Environmental Sample (DA:0000042) - variables: Environmental Sample ID
    2. Molecule (ME:0000027) - variables: Molecule from list, Molecular Weight, Algorithm Parameter, Detection Limit
    3. State (ME:0000037) - (no variables listed)
    4. Replicate Series (ME:0000???) - variables: Count Unit
  Values: Concentration (ME:0000129) in micromolar (UO:0000064)
```

### 3.2 Brick Tables (20 tables)

**Table Naming:** `ddt_brick<7-digit-id>` (e.g., `ddt_brick0000010`)

**Column Structure:**
- **Dimension variables:** Reference columns (e.g., `sdt_sample_name`, `molecule_from_list_sys_oterm_id`)
- **Dimension metadata:** Properties (e.g., `molecule_molecular_weight_dalton`, `state`)
- **Value variables:** Measurements (e.g., `concentration_micromolar`)

**Example Brick Schemas:**

**ddt_brick0000010** (52,884 rows):
```
- sdt_sample_name (dimension 1: Environmental Sample)
- molecule_from_list_sys_oterm_id (dimension 2: Molecule)
- molecule_from_list_sys_oterm_name
- molecule_molecular_weight_dalton
- molecule_algorithm_parameter
- molecule_detection_limit_micromolar
- state (dimension 3: State)
- replicate_series_count_unit (dimension 4)
- concentration_micromolar (value variable)
```

**ddt_brick0000452** (113,741 rows):
```
- sdt_asv_name
- sequence_sequence_type_16s_sequence
```

**ddt_brick0000080** (98,176 rows):
```
- sdt_sample_name
- molecule_from_list_sys_oterm_id
- molecule_from_list_sys_oterm_name
- molecule_molecular_weight_dalton
- molecule_presence_molecule_from_list_helium_0
- concentration_statistic_average_parts_per_billion
- concentration_statistic_standard_deviation_parts_per_billion
- detection_limit_parts_per_billion
```

**Key Findings:**
- Flexible schema supports different measurement types
- Ontology terms embedded for molecules and other categorical dimensions
- Statistical aggregates (mean, std dev) stored in same row
- Detection limits and quality metadata included
- Large data volume: 82+ million rows across 20 bricks

---

## 4. Key Schema Patterns

### 4.1 Identifier Conventions

- **System IDs:** `sys_<entity>_id` (e.g., `sys_process_id`, `sys_oterm_id`)
- **Static Data IDs:** `sdt_<entity>_id` (e.g., `sdt_sample_id`)
- **Dynamic Data IDs:** `ddt_ndarray_id` (for bricks)
- **All IDs:** Zero-padded sequential (e.g., "Assembly0000001", "Process0122921")

### 4.2 Ontology Integration

**Three Types of Ontology References:**
1. **Direct term usage:** `field_sys_oterm_id` + `field_sys_oterm_name` pairs
2. **Metadata annotations:** `units_sys_oterm_id`, `type_sys_oterm_id` in sys_typedef
3. **Semantic dimensions:** Dimension and variable ontology terms in sys_ddt_typedef

**Ontology Namespaces:**
- `ME:*` - ENIGMA Measurement/Context Ontology (custom)
- `ENVO:*` - Environment Ontology
- `UO:*` - Units of Measurement Ontology
- `DA:*` - Data Array Ontology (custom)
- `PROCESS:*` - Process Types (custom)
- `ENIGMA:*` - People and Campaigns (custom)
- `CONTINENT:*`, `COUNTRY:*` - Geography (custom)
- `MIxS:*` - Minimum Information Standards

### 4.3 Provenance Model

**Hierarchical Tracking:**
```
sys_process (workflow step)
  ├─ inputs (sys_process_input)
  │   ├─ Static entities (sdt_*)
  │   └─ Dynamic arrays (ddt_*)
  ├─ outputs (sys_process_output)
  │   ├─ Static entities (sdt_*)
  │   └─ Dynamic arrays (ddt_*)
  └─ metadata
      ├─ Process type (ontology)
      ├─ Person (ontology)
      ├─ Campaign (ontology)
      ├─ Protocol (reference)
      └─ Dates
```

**Query Capabilities:**
- Forward lineage: "What was derived from this sample?"
- Backward lineage: "What inputs created this assembly?"
- Process-centric: "Show all sequencing processes by person X"
- Campaign tracking: "All data from Metal Metabolism campaign"

### 4.4 Delta Lake Format

**All tables stored as Delta Lake:**
- Directory per table with `_delta_log/` subdirectory
- Parquet files with UUID naming: `part-00000-<uuid>-c000.snappy.parquet`
- ACID transactions and time travel support
- Schema evolution capability

---

## 5. Data Volume Summary

### 5.1 Row Counts by Category

| Category | Table Count | Total Rows |
|----------|-------------|------------|
| System Tables | 6 | 242,176 |
| Static Data | 17 | 272,934 |
| Dynamic Data (Bricks) | 20 | 82,627,111 |
| **Total** | **43** | **83,142,221** |

### 5.2 Top 10 Tables by Size

1. **ddt_brick0000452** - 113,741 rows (ASV sequences)
2. **ddt_brick0000080** - 98,176 rows (molecule concentrations)
3. **ddt_brick0000010** - 52,884 rows (metals measurements)
4. **sdt_asv** - 213,044 rows
5. **sys_process** - 142,958 rows
6. **sys_process_input** - 90,395 rows
7. **sys_process_output** - 38,228 rows
8. **sdt_reads** - 19,307 rows
9. **sdt_gene** - 15,015 rows
10. **sys_oterm** - 10,594 rows

---

## 6. Comparison to Original CORAL Schema

### 6.1 Structural Changes

**Table-Level Changes:**
- Added `sys_*` prefix to all system tables
- Added `sdt_*` prefix to all static data tables
- Added `ddt_*` prefix to all dynamic data tables
- Renamed "OTU" → "ASV" (Amplicon Sequence Variant)

**Column-Level Changes:**
- All ID columns: `id` → `sdt_<entity>_id`
- All name columns: `name` → `sdt_<entity>_name`
- All FK columns: `<entity>` → `sdt_<entity>_name`
- Ontology fields: Split into `_sys_oterm_id` + `_sys_oterm_name` pairs

### 6.2 New Capabilities

**Enhanced Provenance:**
- Denormalized sys_process_input and sys_process_output tables for query performance
- Process linking to protocols, people, and campaigns

**Ontology Management:**
- Centralized sys_oterm catalog
- Foreign key constraints ensure ontology term validity
- Embedded ontology names eliminate joins for display

**Measurement Versioning:**
- `withdrawn_date` and `superceded_by_ddt_ndarray_id` in brick index
- Supports data quality improvements without deletion

**External Linking:**
- `link` fields for URLs to sequence files, images, protocols

### 6.3 Preserved Features

- Core entity model (Sample, Location, Reads, Assembly, Genome, Gene, etc.)
- Multi-dimensional array structure (bricks)
- Process-based provenance
- Flexible ontology annotations

---

## 7. Recommendations for LinkML Schema

### 7.1 Schema Organization

**Proposed Module Structure:**
```
linkml_coral_kbase/
  ├── core/
  │   ├── ontology.yaml          # sys_oterm, ontology term references
  │   ├── provenance.yaml        # sys_process, sys_process_input/output
  │   └── types.yaml             # sys_typedef, sys_ddt_typedef
  ├── static_entities/
  │   ├── location_sample.yaml   # Location, Sample
  │   ├── genomics.yaml          # Assembly, Genome, Gene, Bin
  │   ├── microbiology.yaml      # Strain, Community, Taxon
  │   ├── sequencing.yaml        # Reads, ASV
  │   ├── libraries.yaml         # TnSeq_Library, DubSeq_Library
  │   └── metadata.yaml          # Image, Protocol, Condition
  └── dynamic_arrays/
      └── bricks.yaml            # ddt_ndarray, brick metadata
```

### 7.2 Key Patterns to Implement

**1. Ontology Term Mixin:**
```yaml
mixins:
  OntologyTermPair:
    attributes:
      sys_oterm_id:
        range: OntologyTerm
        required: true
      sys_oterm_name:
        range: string
        required: true
```

**2. Entity Naming Convention:**
```yaml
classes:
  Sample:
    attributes:
      sdt_sample_id:
        identifier: true
        pattern: "^Sample\\d{7}$"
      sdt_sample_name:
        required: true
        unique_key: true
```

**3. Foreign Key Conventions:**
```yaml
attributes:
  sdt_location_name:
    range: Location
    inlined: false  # Reference by name, not inline
```

**4. Process Tracking:**
```yaml
classes:
  Process:
    attributes:
      sys_process_id:
        identifier: true
      input_objects:
        multivalued: true
        range: string  # Format: "EntityType:EntityID"
      output_objects:
        multivalued: true
        range: string
```

### 7.3 Validation Rules

**Required Constraints:**
- ID format patterns (e.g., `^Assembly\\d{7}$`)
- Latitude range: [-90, 90]
- Longitude range: [-180, 180]
- Ontology term format: `^[A-Z_]+:\\d+$`
- Date format: ISO 8601

**Recommended Enhancements:**
- FK validation against sys_oterm
- Process input/output entity type validation
- Brick dimension/shape validation
- Unit compatibility checks

### 7.4 Documentation Needs

**Critical Documentation:**
- Ontology term splitting pattern explanation
- FK naming convention (uses `_name`, not `_id`)
- Process provenance model
- Brick structure and query patterns
- Delta Lake storage format

**Migration Guide:**
- Original CORAL → KBase CDM mapping
- Field renaming dictionary
- Ontology term migration paths

---

## 8. Next Steps

### 8.1 Immediate Actions

1. **Create LinkML schema modules** following proposed structure
2. **Document ontology term catalog** with term counts and coverage
3. **Map sys_typedef records** to LinkML class definitions
4. **Define process provenance classes** with input/output tracking
5. **Create brick schema templates** from sys_ddt_typedef

### 8.2 Validation Tasks

1. **Cross-validate FKs** between tables
2. **Check ontology term usage** against sys_oterm catalog
3. **Verify process lineage completeness**
4. **Test brick dimension consistency**
5. **Validate ID format patterns**

### 8.3 Query Examples to Develop

1. Sample → Reads → Assembly → Genome lineage
2. Provenance chain for a specific measurement brick
3. All data from a specific geographic location
4. Strain derivation tree
5. Process attribution (who did what when)

---

## Appendix A: Complete Table Listing

### System Tables
- sys_typedef (118 rows)
- sys_ddt_typedef (101 rows)
- sys_oterm (10,594 rows)
- sys_process (142,958 rows)
- sys_process_input (90,395 rows)
- sys_process_output (38,228 rows)

### Static Data Tables
- sdt_assembly (3,427 rows)
- sdt_asv (213,044 rows)
- sdt_bin (623 rows)
- sdt_community (2,209 rows)
- sdt_condition (1,046 rows)
- sdt_dubseq_library (3 rows)
- sdt_enigma (1 row)
- sdt_gene (15,015 rows)
- sdt_genome (6,688 rows)
- sdt_image (218 rows)
- sdt_location (594 rows)
- sdt_protocol (42 rows)
- sdt_reads (19,307 rows)
- sdt_sample (4,330 rows)
- sdt_strain (3,110 rows)
- sdt_taxon (3,276 rows)
- sdt_tnseq_library (1 row)

### Dynamic Data Tables
- ddt_ndarray (20 rows)
- ddt_brick0000010, 0000072, 0000073, 0000080
- ddt_brick0000452, 0000454, 0000457, 0000458, 0000459
- ddt_brick0000460, 0000461, 0000462
- ddt_brick0000476, 0000477, 0000478, 0000479
- ddt_brick0000495, 0000501, 0000507, 0000508

---

## Appendix B: Sample Queries

### Query 1: Find all samples from a location
```sql
SELECT s.*
FROM sdt_sample s
WHERE s.sdt_location_name = 'CPT1'
```

### Query 2: Trace assembly provenance
```sql
SELECT
  p.sys_process_id,
  p.process_sys_oterm_name,
  pi.sdt_reads_id AS input_reads,
  po.sdt_assembly_id AS output_assembly
FROM sys_process p
JOIN sys_process_input pi ON p.sys_process_id = pi.sys_process_id
JOIN sys_process_output po ON p.sys_process_id = po.sys_process_id
WHERE po.sdt_assembly_id = 'Assembly0000001'
```

### Query 3: Find measurements for a sample
```sql
SELECT
  b.*
FROM ddt_brick0000010 b
WHERE b.sdt_sample_name = 'EU02-D01'
```

---

**End of Report**
