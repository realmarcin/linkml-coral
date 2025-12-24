# ENIGMA CDM Data Dictionary

**Generated:** 2025-12-23 19:14:02

---

## Table of Contents

- [Overview](#overview)
- [Static Tables (sdt_*)](#static-tables)
- [System Tables (sys_*)](#system-tables)
- [Dynamic Tables (ddt_*)](#dynamic-tables)
- [Microtype Reference](#microtype-reference)
- [Relationship Catalog](#relationship-catalog)

---

## Overview

- **Total Tables:** 44
- **Total Columns:** 291
- **Total Rows:** 83,182,615
- **Microtypes Used:** 69
- **FK Relationships:** 108

---

## Static Tables

Static entity tables (sdt_*) store core domain entities.

### sdt_assembly

**Rows:** 3,427 | **Columns:** 5

_static table with 5 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| link | string | Reference to the actual assembly data | REQUIRED |
| n_contigs | integer | Number of contigs in the assembly | REQUIRED |
| sdt_assembly_id | string | Unique text identifier for the assembly (Primary key) | PK, REQUIRED |
| sdt_assembly_name | string | Unique name for the assembly | UNIQUE, REQUIRED |
| sdt_strain_name | string | Strain name from which the assembly was derived (foreign key to Strain.name). | FK→Strain.name |

### sdt_asv

**Rows:** 213,044 | **Columns:** 2

_static table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_id | string | Unique identifier for each ASV/OTU (Primary key) | PK, REQUIRED |
| sdt_asv_name | string | Unique name assigned to the ASV/OTU, usually md5sum | UNIQUE, REQUIRED |

### sdt_bin

**Rows:** 623 | **Columns:** 4

_static table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| contigs | {'type': 'array', 'elementType': 'string', 'containsNull': True} | Array of contig identifiers included in the bin | REQUIRED |
| sdt_assembly_name | string | Identifier of the metagenomic assembly that the bin belongs to (foreign key to Assembly.name) | FK→Assembly, REQUIRED |
| sdt_bin_id | string | Unique identifier for the bin (Primary key) | PK, REQUIRED |
| sdt_bin_name | string | Human-readable, unique name for the bin | UNIQUE, REQUIRED |

### sdt_community

**Rows:** 2,209 | **Columns:** 9

_static table with 9 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| community_type_sys_oterm_id | string | Type of community, e.g., isolate or enrichment | FK→sys_oterm.id, REQUIRED |
| community_type_sys_oterm_name | string | Type of community, e.g., isolate or enrichment | REQUIRED |
| defined_sdt_strain_names | {'type': 'array', 'elementType': 'string', 'containsNull': True} | List of strains that comprise the community, if the community is defined | FK→[Strain.name] |
| parent_sdt_community_name | string | Reference to the name of a parent community, establishing hierarchical relationships | FK→Community.name |
| sdt_community_description | string | Free-text field providing additional details or notes about the community |  |
| sdt_community_id | string | Unique internal identifier for the community (Primary key) | PK, REQUIRED |
| sdt_community_name | string | Unique name of the community | UNIQUE, REQUIRED |
| sdt_condition_name | string | Reference to the experimental or environmental condition associated with the community | FK→Condition.name |
| sdt_sample_name | string | Reference to the Sample from which the community was obtained. | FK→Sample.name |

### sdt_condition

**Rows:** 1,046 | **Columns:** 2

_static table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_condition_id | string | Unique identifier for the condition (Primary key) | PK, REQUIRED |
| sdt_condition_name | string | Unique text name describing the condition | UNIQUE, REQUIRED |

### sdt_dubseq_library

**Rows:** 3 | **Columns:** 4

_static table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| n_fragments | integer | Number of unique DNA fragments in the library |  |
| sdt_dubseq_library_id | string | Unique DubSeq library identifier (Primary key) | PK, REQUIRED |
| sdt_dubseq_library_name | string | Unique, human-readable name of the DubSeq library | UNIQUE, REQUIRED |
| sdt_genome_name | string | Foreign key to the associated genome (Genome.name) from which the library was derived | FK→Genome, REQUIRED |

### sdt_enigma

**Rows:** 1 | **Columns:** 1

_static table with 1 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_enigma_id | string | Primary key for table `sdt_enigma` |  |

### sdt_gene

**Rows:** 15,015 | **Columns:** 9

_static table with 9 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| aliases | {'type': 'array', 'elementType': 'string', 'containsNull': True} | List of alternative names or identifiers for the gene |  |
| contig_number | integer | Contigs are indexed starting at 1, as in KBase | REQUIRED |
| function | string | Annotated biological function of the gene |  |
| sdt_gene_id | string | Unique internal identifier for the gene (Primary key) | PK, REQUIRED |
| sdt_gene_name | string | Unique external identifier for the gene | UNIQUE, REQUIRED |
| sdt_genome_name | string | Name of the genome to which the gene belongs (foreign key) | FK→Genome, REQUIRED |
| start | integer | Genomic start coordinate on the contig, indexed starting at 1 as in KBase | REQUIRED |
| stop | integer | Genomic stop coordinate in base pairs | REQUIRED |
| strand | string | DNA strand of the gene (+ for forward, - for reverse) | REQUIRED |

### sdt_genome

**Rows:** 6,688 | **Columns:** 6

_static table with 6 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| link | string | Link to where the genome itself is actually stored | REQUIRED |
| n_contigs | integer | Number of contigs in the genome assembly | REQUIRED |
| n_features | integer | Number of annotated features (e.g., genes) in the genome | REQUIRED |
| sdt_genome_id | string | Unique identifier for the genome (Primary key) | PK, REQUIRED |
| sdt_genome_name | string | Unique name of the genome | UNIQUE, REQUIRED |
| sdt_strain_name | string | Name of the microbial strain associated with the genome (foreign key) | FK→Strain.name |

### sdt_image

**Rows:** 218 | **Columns:** 7

_static table with 7 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| dimensions | string | Image dimensions (e.g., width × height) expressed in pixels |  |
| link | string | URL or file path linking to the stored image |  |
| mime_type | string | MIME type specifying the image file format (e.g., image/jpeg) |  |
| sdt_image_description | string | Textual description of the image |  |
| sdt_image_id | string | Unique identifier for each image (Primary key) | PK, REQUIRED |
| sdt_image_name | string | Unique name (e.g., filename) for the image. | UNIQUE, REQUIRED |
| size | integer | File size of the image measured in bytes |  |

### sdt_location

**Rows:** 594 | **Columns:** 13

_static table with 13 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| biome_sys_oterm_id | string | Biome classification of the location | FK→sys_oterm.id, REQUIRED |
| biome_sys_oterm_name | string | Biome classification of the location | REQUIRED |
| continent_sys_oterm_id | string | Continent where the location is situated | FK→sys_oterm.id, REQUIRED |
| continent_sys_oterm_name | string | Continent where the location is situated | REQUIRED |
| country_sys_oterm_id | string | Country of the location | FK→sys_oterm.id, REQUIRED |
| country_sys_oterm_name | string | Country of the location | REQUIRED |
| feature_sys_oterm_id | string | Environmental or geographic feature at the location | FK→sys_oterm.id |
| feature_sys_oterm_name | string | Environmental or geographic feature at the location |  |
| latitude | double | Latitude of the location in decimal degrees | REQUIRED |
| longitude | double | Longitude of the location in decimal degrees | REQUIRED |
| region | string | Specific local region name(s) | REQUIRED |
| sdt_location_id | string | Unique identifier for the location (Primary key) | PK, REQUIRED |
| sdt_location_name | string | Unique name of the location | UNIQUE, REQUIRED |

### sdt_protocol

**Rows:** 42 | **Columns:** 4

_static table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| link | string | URL linking to additional documentation of the protocol, such as protocols.io |  |
| sdt_protocol_description | string | Detailed description of the protocol |  |
| sdt_protocol_id | string | Unique identifier for the protocol (Primary key) | PK, REQUIRED |
| sdt_protocol_name | string | Unique, human-readable name of the protocol | UNIQUE, REQUIRED |

### sdt_reads

**Rows:** 19,307 | **Columns:** 8

_static table with 8 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| link | string | Link to the reads file (e.g., fastq) | REQUIRED |
| read_count | integer | Number of reads | REQUIRED |
| read_type_sys_oterm_id | string | Category of reads (e.g., single-end, paired-end) | FK→sys_oterm.id, REQUIRED |
| read_type_sys_oterm_name | string | Category of reads (e.g., single-end, paired-end) | REQUIRED |
| sdt_reads_id | string | Unique identifier for each reads dataset (Primary key) | PK, REQUIRED |
| sdt_reads_name | string | Unique name for the reads | UNIQUE, REQUIRED |
| sequencing_technology_sys_oterm_id | string | Sequencing technology used (e.g., Illumina) | FK→sys_oterm.id, REQUIRED |
| sequencing_technology_sys_oterm_name | string | Sequencing technology used (e.g., Illumina) | REQUIRED |

### sdt_sample

**Rows:** 4,330 | **Columns:** 13

_static table with 13 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| date | string | YYYY[-MM[-DD]] | REQUIRED |
| depth | double | For below-ground samples, the average distance below ground level in meters where the sample was tak |  |
| elevation | double | For above-ground samples, the average distance above ground level in meters where the sample was tak |  |
| env_package_sys_oterm_id | string | MIxS environmental package classification of the sample | FK→sys_oterm.id, REQUIRED |
| env_package_sys_oterm_name | string | MIxS environmental package classification of the sample | REQUIRED |
| material_sys_oterm_id | string | Material type of the sample | FK→sys_oterm.id |
| material_sys_oterm_name | string | Material type of the sample |  |
| sdt_location_name | string | Location where the sample was collected (Foreign key) | FK→Location.name, REQUIRED |
| sdt_sample_description | string | Free-form description or notes about the sample |  |
| sdt_sample_id | string | Unique identifier for the sample (Primary key) | PK, REQUIRED |
| sdt_sample_name | string | Unique name of the sample | UNIQUE, REQUIRED |
| time | string | HH[:MM[:SS]] [AM|PM] |  |
| timezone | string | ISO8601 compliant format, ie. UTC-7 |  |

### sdt_strain

**Rows:** 3,110 | **Columns:** 6

_static table with 6 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| derived_from_sdt_strain_name | string | Name of the parent strain from which this strain was derived, if created by genetic modification or  | FK→Strain.name |
| sdt_gene_names_changed | {'type': 'array', 'elementType': 'string', 'containsNull': True} | List of gene identifiers that have been altered in this strain, if created by genetic modification,  | FK→[Gene.gene_id] |
| sdt_genome_name | string | Genome object for sequenced, wild type strains | FK→Genome.name |
| sdt_strain_description | string | Free-text description of the strain |  |
| sdt_strain_id | string | Unique identifier for each strain (Primary key) | PK, REQUIRED |
| sdt_strain_name | string | Unique name of the strain | UNIQUE, REQUIRED |

### sdt_taxon

**Rows:** 3,276 | **Columns:** 3

_static table with 3 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| ncbi_taxid | string | NCBI taxonomy identifier for the taxon, if available |  |
| sdt_taxon_id | string | Unique identifier for a taxon record (Primary key) | PK, REQUIRED |
| sdt_taxon_name | string | Unique taxon name, typically the scientific name | UNIQUE, REQUIRED |

### sdt_tnseq_library

**Rows:** 1 | **Columns:** 10

_static table with 10 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| hit_rate_essential | double | Proportion of essential genes with at least one transposon insertion |  |
| hit_rate_other | double | Proportion of non-essential (other) genes with at least one transposon insertion |  |
| n_barcodes | integer | Total number of distinct barcode sequences detected in the library |  |
| n_insertion_locations | integer | Number of distinct transposon insertion sites identified in the library |  |
| n_mapped_reads | integer | Number of reads that mapped to the reference genome |  |
| n_usable_barcodes | integer | Number of barcodes deemed usable after quality filtering |  |
| primers_model | string | Type of primers used to generate the library | REQUIRED |
| sdt_genome_name | string | Foreign key to the associated genome (Genome.name) from which the library was derived | FK→Genome, REQUIRED |
| sdt_tnseq_library_id | string | Unique TnSeq library identifier (Primary key) | PK, REQUIRED |
| sdt_tnseq_library_name | string | Unique, human-readable name of the TnSeq library | UNIQUE, REQUIRED |

## System Tables

System tables (sys_*) store metadata and provenance information.

### sys_ddt_typedef

**Rows:** 101 | **Columns:** 15

_system table with 15 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| cdm_column_data_type | string | CDM column data type, variable or dimension_variable |  |
| cdm_column_name | string | CDM column name |  |
| comment | string | Column comment |  |
| ddt_ndarray_id | string | Key for dynamic data type (N-dimensional array) |  |
| dimension_number | integer | Dimension number, starting at 1, for dimension variables |  |
| dimension_oterm_id | string | Dimension data type, ontology term CURIE |  |
| dimension_oterm_name | string | Dimension data type |  |
| fk | string | Foreign key reference |  |
| original_csv_string | string | Original representation of this variable in the CORAL data dump CSV |  |
| scalar_type | string | Scalar type |  |
| unit_sys_oterm_id | string | Unit, ontology term CURIE |  |
| unit_sys_oterm_name | string | Unit |  |
| variable_number | integer | Variable number within a dimension, numbered starting at 1 |  |
| variable_oterm_id | string | Dimension variable data type, ontology term CURIE |  |
| variable_oterm_name | string | Dimension variable data type |  |

### sys_oterm

**Rows:** 10,594 | **Columns:** 8

_system table with 8 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| parent_sys_oterm_id | string | Parent term identifier |  |
| sys_oterm_definition | string | Term definition |  |
| sys_oterm_id | string | Term identifier, aka CURIE (Primary key) |  |
| sys_oterm_links | {'type': 'array', 'elementType': 'string', 'containsNull': True} | Indicates that values are links to other tables (Ref) or ontological terms (ORef) |  |
| sys_oterm_name | string | Term name |  |
| sys_oterm_ontology | string | Ontology that each term is from |  |
| sys_oterm_properties | {'type': 'map', 'keyType': 'string', 'valueType': 'string', 'valueContainsNull': True} | Semicolon‑separated map of properties to values for terms that are CORAL microtypes, including scala |  |
| sys_oterm_synonyms | {'type': 'array', 'elementType': 'string', 'containsNull': True} | List of synonyms for a term |  |

### sys_process

**Rows:** 142,958 | **Columns:** 12

_system table with 12 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| campaign_sys_oterm_id | string | Reference to the ENIGMA campaign under which the data were generated | FK→sys_oterm.id, REQUIRED |
| campaign_sys_oterm_name | string | Reference to the ENIGMA campaign under which the data were generated | REQUIRED |
| date_end | string | YYYY[-MM[-DD]] |  |
| date_start | string | YYYY[-MM[-DD]] |  |
| input_objects | {'type': 'array', 'elementType': 'string', 'containsNull': True} | List of references to data that were input to this process | REQUIRED |
| output_objects | {'type': 'array', 'elementType': 'string', 'containsNull': True} | List of references to data that were produced by this process | REQUIRED |
| person_sys_oterm_id | string | Reference to the person or lab that performed the process | FK→sys_oterm.id, REQUIRED |
| person_sys_oterm_name | string | Reference to the person or lab that performed the process | REQUIRED |
| process_sys_oterm_id | string | Reference to the specific process type used to generate the outputs | FK→sys_oterm.id, REQUIRED |
| process_sys_oterm_name | string | Reference to the specific process type used to generate the outputs | REQUIRED |
| sdt_protocol_name | string | Protocol used in this process (foreign key to Protocol.name) | FK→Protocol.name |
| sys_process_id | string | Unique identifier for each process record (Primary key) | PK, REQUIRED |

### sys_process_input

**Rows:** 90,395 | **Columns:** 10

_system table with 10 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_assembly_id | string | Input object from sdt_assembly |  |
| sdt_bin_id | string | Input object from sdt_bin |  |
| sdt_community_id | string | Input object from sdt_community |  |
| sdt_genome_id | string | Input object from sdt_genome |  |
| sdt_location_id | string | Input object from sdt_location |  |
| sdt_reads_id | string | Input object from sdt_reads |  |
| sdt_sample_id | string | Input object from sdt_sample |  |
| sdt_strain_id | string | Input object from sdt_strain |  |
| sdt_tnseq_library_id | string | Input object from sdt_tnseq_library |  |
| sys_process_id | string | Foreign key to sys_process |  |

### sys_process_output

**Rows:** 38,228 | **Columns:** 12

_system table with 12 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| ddt_ndarray_id | string | Output object from ddt_ndarray |  |
| sdt_assembly_id | string | Output object from sdt_assembly |  |
| sdt_bin_id | string | Output object from sdt_bin |  |
| sdt_community_id | string | Output object from sdt_community |  |
| sdt_dubseq_library_id | string | Output object from sdt_dubseq_library |  |
| sdt_genome_id | string | Output object from sdt_genome |  |
| sdt_image_id | string | Output object from sdt_image |  |
| sdt_reads_id | string | Output object from sdt_reads |  |
| sdt_sample_id | string | Output object from sdt_sample |  |
| sdt_strain_id | string | Output object from sdt_strain |  |
| sdt_tnseq_library_id | string | Output object from sdt_tnseq_library |  |
| sys_process_id | string | Foreign key to sys_process |  |

### sys_typedef

**Rows:** 118 | **Columns:** 12

_system table with 12 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| cdm_column_name | string |  |  |
| comment | string |  |  |
| constraint | string |  |  |
| field_name | string |  |  |
| fk | string |  |  |
| pk | boolean |  |  |
| required | boolean |  |  |
| scalar_type | string |  |  |
| type_name | string |  |  |
| type_sys_oterm_id | string |  |  |
| units_sys_oterm_id | string |  |  |
| upk | boolean |  |  |

## Dynamic Tables

Dynamic data tables (ddt_*) store measurement arrays in brick format.

### ddt_brick0000010

**Rows:** 52,884 | **Columns:** 9

_dynamic table with 9 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| concentration_micromolar | double | Concentration |  |
| molecule_algorithm_parameter | string | Algorithm Parameter |  |
| molecule_detection_limit_micromolar | double | Detection Limit |  |
| molecule_from_list_sys_oterm_id | string | Molecule from list, ontology term CURIE |  |
| molecule_from_list_sys_oterm_name | string | Molecule from list |  |
| molecule_molecular_weight_dalton | double | Molecular Weight |  |
| replicate_series_count_unit | integer | Replicate Series |  |
| sdt_sample_name | string | Environmental Sample ID |  |
| state | string | State |  |

### ddt_brick0000072

**Rows:** 1,890 | **Columns:** 9

_dynamic table with 9 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| concentration_milligram_per_kilogram | double | Concentration |  |
| molecule_from_list_sys_oterm_id | string | Molecule from list, ontology term CURIE |  |
| molecule_from_list_sys_oterm_name | string | Molecule from list |  |
| molecule_molecular_weight_dalton | double | Molecular Weight |  |
| molecule_presence_molecule_from_list_helium_0 | boolean | Presence, Molecule from list=helium(0) |  |
| sdt_sample_name | string | Environmental Sample ID |  |
| state | string | State |  |
| statistic_sys_oterm_id | string | Statistic, ontology term CURIE |  |
| statistic_sys_oterm_name | string | Statistic |  |

### ddt_brick0000073

**Rows:** 3,564 | **Columns:** 9

_dynamic table with 9 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| concentration_milligram_per_kilogram | double | Concentration |  |
| molecule_from_list_sys_oterm_id | string | Molecule from list, ontology term CURIE |  |
| molecule_from_list_sys_oterm_name | string | Molecule from list |  |
| molecule_molecular_weight_dalton | double | Molecular Weight |  |
| molecule_presence_molecule_from_list_helium_0 | boolean | Presence, Molecule from list=helium(0) |  |
| sdt_sample_name | string | Environmental Sample ID |  |
| state | string | State |  |
| statistic_sys_oterm_id | string | Statistic, ontology term CURIE |  |
| statistic_sys_oterm_name | string | Statistic |  |

### ddt_brick0000080

**Rows:** 98,176 | **Columns:** 8

_dynamic table with 8 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| concentration_statistic_average_parts_per_billion | double | Concentration, Statistic=Average |  |
| concentration_statistic_standard_deviation_parts_per_billion | double | Concentration, Statistic=Standard Deviation |  |
| detection_limit_parts_per_billion | double | Detection Limit |  |
| molecule_from_list_sys_oterm_id | string | Molecule from list, ontology term CURIE |  |
| molecule_from_list_sys_oterm_name | string | Molecule from list |  |
| molecule_molecular_weight_dalton | double | Molecular Weight |  |
| molecule_presence_molecule_from_list_helium_0 | boolean | Presence, Molecule from list=helium(0) |  |
| sdt_sample_name | string | Environmental Sample ID |  |

### ddt_brick0000452

**Rows:** 113,741 | **Columns:** 2

_dynamic table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string | ASV ID |  |
| sequence_sequence_type_16s_sequence | string | Sequence, Sequence Type=16S Sequence |  |

### ddt_brick0000454

**Rows:** 627,241 | **Columns:** 4

_dynamic table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string | ASV ID |  |
| sdt_taxon_name | string | Taxon ID |  |
| taxonomic_level_sys_oterm_id | string | Taxonomic Level, ontology term CURIE |  |
| taxonomic_level_sys_oterm_name | string | Taxonomic Level |  |

### ddt_brick0000457

**Rows:** 23,458 | **Columns:** 2

_dynamic table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string | ASV ID |  |
| sequence_sequence_type_16s_sequence | string | Sequence, Sequence Type=16S Sequence |  |

### ddt_brick0000458

**Rows:** 108,842 | **Columns:** 4

_dynamic table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string | ASV ID |  |
| sdt_taxon_name | string | Taxon ID |  |
| taxonomic_level_sys_oterm_id | string | Taxonomic Level, ontology term CURIE |  |
| taxonomic_level_sys_oterm_name | string | Taxonomic Level |  |

### ddt_brick0000459

**Rows:** 867,946 | **Columns:** 3

_dynamic table with 3 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| count_count_unit | integer | Count |  |
| sdt_asv_name | string | ASV ID |  |
| sdt_community_name | string | Community ID |  |

### ddt_brick0000460

**Rows:** 9,432 | **Columns:** 2

_dynamic table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string | ASV ID |  |
| sequence_sequence_type_16s_sequence | string | Sequence, Sequence Type=16S Sequence |  |

### ddt_brick0000461

**Rows:** 56,696 | **Columns:** 5

_dynamic table with 5 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| confidence_confidence_unit | double | Confidence |  |
| sdt_asv_name | string | ASV ID |  |
| sdt_taxon_name | string | Taxon ID |  |
| taxonomic_level_sys_oterm_id | string | Taxonomic Level, ontology term CURIE |  |
| taxonomic_level_sys_oterm_name | string | Taxonomic Level |  |

### ddt_brick0000462

**Rows:** 132,048 | **Columns:** 3

_dynamic table with 3 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| count_count_unit | integer | Count |  |
| sdt_asv_name | string | ASV ID |  |
| sdt_community_name | string | Community ID |  |

### ddt_brick0000476

**Rows:** 80,070,280 | **Columns:** 4

_dynamic table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| count_count_unit | integer | Count |  |
| replicate_series_count_unit | integer | Replicate Series |  |
| sdt_asv_name | string | ASV ID |  |
| sdt_community_name | string | Community ID |  |

### ddt_brick0000477

**Rows:** 9,398 | **Columns:** 2

_dynamic table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string | ASV ID |  |
| sequence_sequence_type_16s_sequence | string | Sequence, Sequence Type=16S Sequence |  |

### ddt_brick0000478

**Rows:** 56,497 | **Columns:** 5

_dynamic table with 5 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| confidence_confidence_unit | double | Confidence |  |
| sdt_asv_name | string | ASV ID |  |
| sdt_taxon_name | string | Taxon ID |  |
| taxonomic_level_sys_oterm_id | string | Taxonomic Level, ontology term CURIE |  |
| taxonomic_level_sys_oterm_name | string | Taxonomic Level |  |

### ddt_brick0000479

**Rows:** 375,920 | **Columns:** 3

_dynamic table with 3 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| count_count_unit | integer | Count |  |
| sdt_asv_name | string | ASV ID |  |
| sdt_community_name | string | Community ID |  |

### ddt_brick0000495

**Rows:** 8,904 | **Columns:** 5

_dynamic table with 5 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_strain_name | string | Strain ID |  |
| sdt_taxon_name | string | Taxon ID |  |
| strain_relative_evolutionary_divergence_dimensionless_unit | double | Relative Evolutionary Divergence |  |
| taxonomic_level_sys_oterm_id | string | Taxonomic Level, ontology term CURIE |  |
| taxonomic_level_sys_oterm_name | string | Taxonomic Level |  |

### ddt_brick0000501

**Rows:** 3,107 | **Columns:** 10

_dynamic table with 10 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| date_comment_sampling_date | string | Date, Comment=Sampling Date |  |
| description_comment_original_condition_description | string | Description, Comment=Original Condition Description |  |
| enigma_campaign_sys_oterm_id | string | ENIGMA Campaign, ontology term CURIE |  |
| enigma_campaign_sys_oterm_name | string | ENIGMA Campaign |  |
| enigma_labs_and_personnel_comment_contact_person_or_lab_sys_oterm_id | string | ENIGMA Labs and Personnel, Comment=Contact Person or Lab, ontology term CURIE |  |
| enigma_labs_and_personnel_comment_contact_person_or_lab_sys_oterm_name | string | ENIGMA Labs and Personnel, Comment=Contact Person or Lab |  |
| sdt_condition_name | string | Condition ID |  |
| sdt_location_name | string | Environmental Sample Location ID |  |
| sdt_sample_name | string | Environmental Sample ID |  |
| sdt_strain_name | string | Strain ID |  |

### ddt_brick0000507

**Rows:** 3,009 | **Columns:** 6

_dynamic table with 6 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_strain_name | string | Strain ID |  |
| sequence | string | Sequence |  |
| sequence_type_sys_oterm_id | string | Sequence Type, ontology term CURIE |  |
| sequence_type_sys_oterm_name | string | Sequence Type |  |
| strand_sys_oterm_id | string | Strand, ontology term CURIE |  |
| strand_sys_oterm_name | string | Strand |  |

### ddt_brick0000508

**Rows:** 4,234 | **Columns:** 6

_dynamic table with 6 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| read_coverage_comment_percent_of_1kb_chunks_of_genome_covered_by_at_least_one_read_percent | double | Read Coverage, Comment=percent of 1kb chunks of genome covered by at least one read |  |
| read_coverage_statistic_average_comment_cov80_average_coverage_after_trimming_highest_and_lowest_10_percent_count_unit | double | Read Coverage, Statistic=Average, Comment=cov80 average coverage after trimming highest and lowest 1 |  |
| sdt_genome_name | string | Genome ID |  |
| sdt_sample_name | string | Environmental Sample ID |  |
| sdt_strain_name | string | Strain ID |  |
| sequence_identity_statistic_average_comment_average_percent_identity_of_aligned_reads_percent | double | Sequence Identity, Statistic=Average, Comment=average percent identity of aligned reads |  |

### ddt_ndarray

**Rows:** 20 | **Columns:** 15

_dynamic table with 15 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| ddt_ndarray_description | string | Description of the data brick (N-dimensional array) |  |
| ddt_ndarray_dimension_types_sys_oterm_id | {'type': 'array', 'elementType': 'string', 'containsNull': True} | Array of dimension data types, ontology term CURIEs |  |
| ddt_ndarray_dimension_types_sys_oterm_name | {'type': 'array', 'elementType': 'string', 'containsNull': True} | Array of dimension data types |  |
| ddt_ndarray_dimension_variable_types_sys_oterm_id | {'type': 'array', 'elementType': 'string', 'containsNull': True} | Array of dimension variable types, ontology term CURIEs |  |
| ddt_ndarray_dimension_variable_types_sys_oterm_name | {'type': 'array', 'elementType': 'string', 'containsNull': True} | Array of dimension variable types |  |
| ddt_ndarray_id | string | Primary key for dynamic data type (N-dimensional array) |  |
| ddt_ndarray_metadata | string | Metadata for the data brick (N-dimensional array) |  |
| ddt_ndarray_name | string | Name of the data brick (N-dimensional array) |  |
| ddt_ndarray_shape | string | Shape of the N-dimensional array, array with one integer per dimension |  |
| ddt_ndarray_type_sys_oterm_id | string | Data type for this data brick, ontology term CURIE |  |
| ddt_ndarray_type_sys_oterm_name | string | Data type for this data brick |  |
| ddt_ndarray_variable_types_sys_oterm_id | {'type': 'array', 'elementType': 'string', 'containsNull': True} | Array of variable types, ontology term CURIEs |  |
| ddt_ndarray_variable_types_sys_oterm_name | {'type': 'array', 'elementType': 'string', 'containsNull': True} | Array of variable types |  |
| superceded_by_ddt_ndarray_id | string | Dataset that supercedes this one, if the dataset was withdrawn and replaced, or null if the dataset  |  |
| withdrawn_date | string | Date when this dataset was withdrawn, or null if the dataset is currently valid |  |

## Microtype Reference

Semantic type annotations used across the CDM schema.

| Microtype | Usage Count | Example Description |
|-----------|-------------|---------------------|
| ME:0000126 | 10 | Number of contigs in the assembly |
| ME:0000044 | 5 | Strain name from which the assembly was derived (foreign key to Strain.name). |
| ME:0000203 | 5 | Reference to the actual assembly data |
| ME:0000202 | 5 | Free-text field providing additional details or notes about the community |
| ME:0000246 | 5 | Foreign key to the associated genome (Genome.name) from which the library was de |
| ME:0000009 | 3 | YYYY[-MM[-DD]] |
| ME:0000280 | 2 | Unique name for the assembly |
| ME:0000233 | 2 | Unique name of the community |
| ME:0000234 | 2 | Type of community, e.g., isolate or enrichment |
| ME:0000102 | 2 | Reference to the Sample from which the community was obtained. |
| ME:0000200 | 2 | Reference to the experimental or environmental condition associated with the com |
| ME:0000276 | 2 | Unique DubSeq library identifier (Primary key) |
| ME:0000262 | 2 | Unique, human-readable name of the DubSeq library |
| ME:0000228 | 2 | Unique name of the location |
| ME:0000213 | 2 | Continent where the location is situated |
| ME:0000214 | 2 | Country of the location |
| ME:0000216 | 2 | Biome classification of the location |
| ME:0000217 | 2 | Environmental or geographic feature at the location |
| ME:0000328 | 2 | Unique, human-readable name of the protocol |
| ME:0000112 | 2 | Category of reads (e.g., single-end, paired-end) |

*Showing top 20 of 69 microtypes*

## Relationship Catalog

Foreign key relationships between tables.

| Source Table | Source Column | Target Table | Target Column | Required |
|--------------|---------------|--------------|---------------|----------|
| ddt_brick0000010 | sdt_sample_name | sdt_sample | sdt_sample_name |  |
| ddt_brick0000010 | molecule_from_list_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000072 | statistic_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000072 | sdt_sample_name | sdt_sample | sdt_sample_name |  |
| ddt_brick0000072 | molecule_from_list_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000073 | statistic_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000073 | sdt_sample_name | sdt_sample | sdt_sample_name |  |
| ddt_brick0000073 | molecule_from_list_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000080 | sdt_sample_name | sdt_sample | sdt_sample_name |  |
| ddt_brick0000080 | molecule_from_list_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000452 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000454 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000454 | taxonomic_level_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000454 | sdt_taxon_name | sdt_taxon | sdt_taxon_name |  |
| ddt_brick0000457 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000458 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000458 | taxonomic_level_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000458 | sdt_taxon_name | sdt_taxon | sdt_taxon_name |  |
| ddt_brick0000459 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000459 | sdt_community_name | sdt_community | sdt_community_name |  |
| ddt_brick0000460 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000461 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000461 | taxonomic_level_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000461 | sdt_taxon_name | sdt_taxon | sdt_taxon_name |  |
| ddt_brick0000462 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000462 | sdt_community_name | sdt_community | sdt_community_name |  |
| ddt_brick0000476 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000476 | sdt_community_name | sdt_community | sdt_community_name |  |
| ddt_brick0000477 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000478 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000478 | taxonomic_level_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000478 | sdt_taxon_name | sdt_taxon | sdt_taxon_name |  |
| ddt_brick0000479 | sdt_asv_name | sdt_asv | sdt_asv_name |  |
| ddt_brick0000479 | sdt_community_name | sdt_community | sdt_community_name |  |
| ddt_brick0000495 | sdt_strain_name | sdt_strain | sdt_strain_name |  |
| ddt_brick0000495 | taxonomic_level_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000495 | sdt_taxon_name | sdt_taxon | sdt_taxon_name |  |
| ddt_brick0000501 | sdt_strain_name | sdt_strain | sdt_strain_name |  |
| ddt_brick0000501 | sdt_condition_name | sdt_condition | sdt_condition_name |  |
| ddt_brick0000501 | sdt_sample_name | sdt_sample | sdt_sample_name |  |
| ddt_brick0000501 | sdt_location_name | sdt_location | sdt_location_name |  |
| ddt_brick0000501 | enigma_campaign_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000501 | enigma_labs_and_personnel_comment_contact_person_or_lab_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000507 | sdt_strain_name | sdt_strain | sdt_strain_name |  |
| ddt_brick0000507 | sequence_type_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000507 | strand_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000508 | sdt_sample_name | sdt_sample | sdt_sample_name |  |
| ddt_brick0000508 | sdt_strain_name | sdt_strain | sdt_strain_name |  |
| ddt_brick0000508 | sdt_genome_name | sdt_genome | sdt_genome_name |  |
| ddt_ndarray | ddt_ndarray_type_sys_oterm_id | sys_oterm | sys_oterm_id |  |

*Showing 50 of 108 relationships*
