# ENIGMA CDM Data Dictionary

**Generated:** 2026-01-20 22:59:36

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
- **Total Columns:** 293
- **Total Rows:** 328,442,906
- **Microtypes Used:** 69
- **FK Relationships:** 61

---

## Static Tables

Static entity tables (sdt_*) store core domain entities.

### sdt_assembly

**Rows:** 3,427 | **Columns:** 5

_static table with 5 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| link | string | Reference to the actual assembly data |  |
| n_contigs_count_unit | integer | Number of contigs in the assembly |  |
| sdt_assembly_id | string | Unique text identifier for the assembly (Primary key) |  |
| sdt_assembly_name | string | Unique name for the assembly |  |
| sdt_strain_name | string | Strain name from which the assembly was derived (foreign key to Strain.name). | FK→Strain.name |

### sdt_asv

**Rows:** 213,044 | **Columns:** 2

_static table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_id | string | Unique identifier for each ASV/OTU (Primary key) |  |
| sdt_asv_name | string | Unique name assigned to the ASV/OTU, usually md5sum |  |

### sdt_bin

**Rows:** 623 | **Columns:** 4

_static table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| contigs | {'type': 'array', 'elementType': 'string', 'containsNull': True} | Array of contig identifiers included in the bin |  |
| sdt_assembly_name | string | Identifier of the metagenomic assembly that the bin belongs to (foreign key to Assembly.name) | FK→Assembly |
| sdt_bin_id | string | Unique identifier for the bin (Primary key) |  |
| sdt_bin_name | string | Human-readable, unique name for the bin |  |

### sdt_community

**Rows:** 2,209 | **Columns:** 9

_static table with 9 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| community_type_sys_oterm_id | string | Type of community, e.g., isolate or enrichment, ontology term CURIE | FK→sys_oterm.id |
| community_type_sys_oterm_name | string | Type of community, e.g., isolate or enrichment |  |
| defined_sdt_strain_names | {'type': 'array', 'elementType': 'string', 'containsNull': True} | List of strains that comprise the community, if the community is defined | FK→[Strain.name] |
| parent_sdt_community_name | string | Reference to the name of a parent community, establishing hierarchical relationships | FK→Community.name |
| sdt_community_description | string | Free-text field providing additional details or notes about the community |  |
| sdt_community_id | string | Unique internal identifier for the community (Primary key) |  |
| sdt_community_name | string | Unique name of the community |  |
| sdt_condition_name | string | Reference to the experimental or environmental condition associated with the community | FK→Condition.name |
| sdt_sample_name | string | Reference to the Sample from which the community was obtained. | FK→Sample.name |

### sdt_condition

**Rows:** 1,046 | **Columns:** 2

_static table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_condition_id | string | Unique identifier for the condition (Primary key) |  |
| sdt_condition_name | string | Unique text name describing the condition |  |

### sdt_dubseq_library

**Rows:** 3 | **Columns:** 4

_static table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| n_fragments_count_unit | integer | Number of unique DNA fragments in the library |  |
| sdt_dubseq_library_id | string | Unique DubSeq library identifier (Primary key) |  |
| sdt_dubseq_library_name | string | Unique, human-readable name of the DubSeq library |  |
| sdt_genome_name | string | Foreign key to the associated genome (Genome.name) from which the library was derived | FK→Genome |

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
| contig_number_count_unit | integer | Contigs are indexed starting at 1, as in KBase |  |
| function | string | Annotated biological function of the gene |  |
| sdt_gene_id | string | Unique internal identifier for the gene (Primary key) |  |
| sdt_gene_name | string | Unique external identifier for the gene |  |
| sdt_genome_name | string | Name of the genome to which the gene belongs (foreign key) | FK→Genome |
| start_base_pair | integer | Genomic start coordinate on the contig, indexed starting at 1 as in KBase |  |
| stop_base_pair | integer | Genomic stop coordinate in base pairs |  |
| strand | string | DNA strand of the gene (+ for forward, - for reverse) |  |

### sdt_genome

**Rows:** 6,705 | **Columns:** 6

_static table with 6 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| link | string | Link to where the genome itself is actually stored |  |
| n_contigs_count_unit | integer | Number of contigs in the genome assembly |  |
| n_features_count_unit | integer | Number of annotated features (e.g., genes) in the genome |  |
| sdt_genome_id | string | Unique identifier for the genome (Primary key) |  |
| sdt_genome_name | string | Unique name of the genome |  |
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
| sdt_image_id | string | Unique identifier for each image (Primary key) |  |
| sdt_image_name | string | Unique name (e.g., filename) for the image. |  |
| size_byte | integer | File size of the image measured in bytes |  |

### sdt_location

**Rows:** 596 | **Columns:** 13

_static table with 13 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| biome_sys_oterm_id | string | Biome classification of the location, ontology term CURIE | FK→sys_oterm.id |
| biome_sys_oterm_name | string | Biome classification of the location |  |
| continent_sys_oterm_id | string | Continent where the location is situated, ontology term CURIE | FK→sys_oterm.id |
| continent_sys_oterm_name | string | Continent where the location is situated |  |
| country_sys_oterm_id | string | Country of the location, ontology term CURIE | FK→sys_oterm.id |
| country_sys_oterm_name | string | Country of the location |  |
| feature_sys_oterm_id | string | Environmental or geographic feature at the location, ontology term CURIE | FK→sys_oterm.id |
| feature_sys_oterm_name | string | Environmental or geographic feature at the location |  |
| latitude_degree | double | Latitude of the location in decimal degrees |  |
| longitude_degree | double | Longitude of the location in decimal degrees |  |
| region | string | Specific local region name(s) |  |
| sdt_location_id | string | Unique identifier for the location (Primary key) |  |
| sdt_location_name | string | Unique name of the location |  |

### sdt_protocol

**Rows:** 51 | **Columns:** 4

_static table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| link | string | URL linking to additional documentation of the protocol, such as protocols.io |  |
| sdt_protocol_description | string | Detailed description of the protocol |  |
| sdt_protocol_id | string | Unique identifier for the protocol (Primary key) |  |
| sdt_protocol_name | string | Unique, human-readable name of the protocol |  |

### sdt_reads

**Rows:** 19,592 | **Columns:** 8

_static table with 8 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| link | string | Link to the reads file (e.g., fastq) |  |
| read_count_count_unit | integer | Number of reads |  |
| read_type_sys_oterm_id | string | Category of reads (e.g., single-end, paired-end), ontology term CURIE | FK→sys_oterm.id |
| read_type_sys_oterm_name | string | Category of reads (e.g., single-end, paired-end) |  |
| sdt_reads_id | string | Unique identifier for each reads dataset (Primary key) |  |
| sdt_reads_name | string | Unique name for the reads |  |
| sequencing_technology_sys_oterm_id | string | Sequencing technology used (e.g., Illumina), ontology term CURIE | FK→sys_oterm.id |
| sequencing_technology_sys_oterm_name | string | Sequencing technology used (e.g., Illumina) |  |

### sdt_sample

**Rows:** 4,346 | **Columns:** 13

_static table with 13 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| date | string | YYYY[-MM[-DD]] |  |
| depth_meter | double | For below-ground samples, the average distance below ground level in meters where the sample was tak |  |
| elevation_meter | double | For above-ground samples, the average distance above ground level in meters where the sample was tak |  |
| env_package_sys_oterm_id | string | MIxS environmental package classification of the sample, ontology term CURIE | FK→sys_oterm.id |
| env_package_sys_oterm_name | string | MIxS environmental package classification of the sample |  |
| material_sys_oterm_id | string | Material type of the sample, ontology term CURIE | FK→sys_oterm.id |
| material_sys_oterm_name | string | Material type of the sample |  |
| sdt_location_name | string | Location where the sample was collected (Foreign key) | FK→Location.name |
| sdt_sample_description | string | Free-form description or notes about the sample |  |
| sdt_sample_id | string | Unique identifier for the sample (Primary key) |  |
| sdt_sample_name | string | Unique name of the sample |  |
| time | string | HH[:MM[:SS]] [AM|PM] |  |
| timezone | string | ISO8601 compliant format, ie. UTC-7 |  |

### sdt_strain

**Rows:** 3,154 | **Columns:** 6

_static table with 6 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| derived_from_sdt_strain_name | string | Name of the parent strain from which this strain was derived, if created by genetic modification or  | FK→Strain.name |
| sdt_gene_names_changed | {'type': 'array', 'elementType': 'string', 'containsNull': True} | List of gene identifiers that have been altered in this strain, if created by genetic modification,  | FK→[Gene.gene_id] |
| sdt_genome_name | string | Genome object for sequenced, wild type strains | FK→Genome.name |
| sdt_strain_description | string | Free-text description of the strain |  |
| sdt_strain_id | string | Unique identifier for each strain (Primary key) |  |
| sdt_strain_name | string | Unique name of the strain |  |

### sdt_taxon

**Rows:** 3,365 | **Columns:** 3

_static table with 3 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| ncbi_taxid | string | NCBI taxonomy identifier for the taxon, if available |  |
| sdt_taxon_id | string | Unique identifier for a taxon record (Primary key) |  |
| sdt_taxon_name | string | Unique taxon name, typically the scientific name |  |

### sdt_tnseq_library

**Rows:** 1 | **Columns:** 10

_static table with 10 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| hit_rate_essential_ratio_unit | double | Proportion of essential genes with at least one transposon insertion |  |
| hit_rate_other_ratio_unit | double | Proportion of non-essential (other) genes with at least one transposon insertion |  |
| n_barcodes_count_unit | integer | Total number of distinct barcode sequences detected in the library |  |
| n_insertion_locations_count_unit | integer | Number of distinct transposon insertion sites identified in the library |  |
| n_mapped_reads_count_unit | integer | Number of reads that mapped to the reference genome |  |
| n_usable_barcodes_count_unit | integer | Number of barcodes deemed usable after quality filtering |  |
| primers_model | string | Type of primers used to generate the library |  |
| sdt_genome_name | string | Foreign key to the associated genome (Genome.name) from which the library was derived | FK→Genome |
| sdt_tnseq_library_id | string | Unique TnSeq library identifier (Primary key) |  |
| sdt_tnseq_library_name | string | Unique, human-readable name of the TnSeq library |  |

## System Tables

System tables (sys_*) store metadata and provenance information.

### sys_ddt_typedef

**Rows:** 606 | **Columns:** 15

_system table with 15 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| berdl_column_data_type | string |  |  |
| berdl_column_name | string |  |  |
| comment | string |  |  |
| ddt_ndarray_id | string |  |  |
| dimension_number | integer |  |  |
| dimension_oterm_id | string |  |  |
| dimension_oterm_name | string |  |  |
| foreign_key | string |  |  |
| original_csv_string | string |  |  |
| scalar_type | string |  |  |
| unit_sys_oterm_id | string |  |  |
| unit_sys_oterm_name | string |  |  |
| variable_number | integer |  |  |
| variable_oterm_id | string |  |  |
| variable_oterm_name | string |  |  |

### sys_oterm

**Rows:** 10,600 | **Columns:** 8

_system table with 8 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| parent_sys_oterm_id | string | Parent term identifier |  |
| sys_oterm_definition | string | Term definition |  |
| sys_oterm_id | string | Term identifier, aka CURIE (Primary key) |  |
| sys_oterm_links | {'type': 'array', 'elementType': 'string', 'containsNull': True} | Indicates that values are links to other tables (Ref) or ontological terms (ORef) |  |
| sys_oterm_name | string | Term name |  |
| sys_oterm_ontology | string | Ontology that each term is from |  |
| sys_oterm_properties | {'type': 'map', 'keyType': 'string', 'valueType': 'string', 'valueContainsNull': True} | Semicolon-separated map of properties to values for terms that are CORAL microtypes, including scala |  |
| sys_oterm_synonyms | {'type': 'array', 'elementType': 'string', 'containsNull': True} | List of synonyms for a term |  |

### sys_process

**Rows:** 84,527 | **Columns:** 12

_system table with 12 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| campaign_sys_oterm_id | string | Reference to the ENIGMA campaign under which the data were generated, ontology term CURIE | FK→sys_oterm.id |
| campaign_sys_oterm_name | string | Reference to the ENIGMA campaign under which the data were generated |  |
| date_end | string | YYYY[-MM[-DD]] |  |
| date_start | string | YYYY[-MM[-DD]] |  |
| input_objects | {'type': 'array', 'elementType': 'string', 'containsNull': True} | List of references to data that were input to this process |  |
| output_objects | {'type': 'array', 'elementType': 'string', 'containsNull': True} | List of references to data that were produced by this process |  |
| person_sys_oterm_id | string | Reference to the person or lab that performed the process, ontology term CURIE | FK→sys_oterm.id |
| person_sys_oterm_name | string | Reference to the person or lab that performed the process |  |
| process_sys_oterm_id | string | Reference to the specific process type used to generate the outputs, ontology term CURIE | FK→sys_oterm.id |
| process_sys_oterm_name | string | Reference to the specific process type used to generate the outputs |  |
| sdt_protocol_name | string | Protocol used in this process (foreign key to Protocol.name) | FK→Protocol.name |
| sys_process_id | string | Unique identifier for each process record (Primary key) |  |

### sys_process_input

**Rows:** 82,864 | **Columns:** 10

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

**Rows:** 38,594 | **Columns:** 12

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

**Rows:** 118 | **Columns:** 14

_system table with 14 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| cdm_column_name | string |  |  |
| comment | string |  |  |
| constraint | string |  |  |
| field_name | string |  |  |
| fk | string |  |  |
| is_pk | boolean |  |  |
| is_required | boolean |  |  |
| is_upk | boolean |  |  |
| scalar_type | string |  |  |
| type_name | string |  |  |
| type_sys_oterm_id | string |  |  |
| type_sys_oterm_name | string | Term name |  |
| units_sys_oterm_id | string |  |  |
| units_sys_oterm_name | string | Term name |  |

## Dynamic Tables

Dynamic data tables (ddt_*) store measurement arrays in brick format.

### ddt_brick0000010

**Rows:** 158,652 | **Columns:** 9

_dynamic table with 9 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| concentration_micromolar | double |  |  |
| molecule_algorithm_parameter | string |  |  |
| molecule_detection_limit_micromolar | double |  |  |
| molecule_from_list_sys_oterm_id | string |  |  |
| molecule_from_list_sys_oterm_name | string |  |  |
| molecule_molecular_weight_dalton | double |  |  |
| physiochemical_state | string |  |  |
| replicate_series_count_unit | integer |  |  |
| sdt_sample_name | string |  |  |

### ddt_brick0000072

**Rows:** 5,670 | **Columns:** 9

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

**Rows:** 10,692 | **Columns:** 9

_dynamic table with 9 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| concentration_milligram_per_kilogram | double |  |  |
| molecule_from_list_sys_oterm_id | string |  |  |
| molecule_from_list_sys_oterm_name | string |  |  |
| molecule_molecular_weight_dalton | double |  |  |
| molecule_presence_molecule_from_list_helium_0 | boolean |  |  |
| physiochemical_state | string |  |  |
| sdt_sample_name | string |  |  |
| statistic_sys_oterm_id | string |  |  |
| statistic_sys_oterm_name | string |  |  |

### ddt_brick0000080

**Rows:** 294,528 | **Columns:** 8

_dynamic table with 8 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| concentration_statistic_average_parts_per_billion | double |  |  |
| concentration_statistic_standard_deviation_parts_per_billion | double |  |  |
| detection_limit_parts_per_billion | double |  |  |
| molecule_from_list_sys_oterm_id | string |  |  |
| molecule_from_list_sys_oterm_name | string |  |  |
| molecule_molecular_weight_dalton | double |  |  |
| molecule_presence_molecule_from_list_helium_0 | boolean |  |  |
| sdt_sample_name | string |  |  |

### ddt_brick0000452

**Rows:** 341,223 | **Columns:** 2

_dynamic table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string |  |  |
| sequence_sequence_type_16s_sequence | string |  |  |

### ddt_brick0000454

**Rows:** 1,881,723 | **Columns:** 4

_dynamic table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string |  |  |
| sdt_taxon_name | string |  |  |
| taxonomic_level_sys_oterm_id | string |  |  |
| taxonomic_level_sys_oterm_name | string |  |  |

### ddt_brick0000457

**Rows:** 70,374 | **Columns:** 2

_dynamic table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string |  |  |
| sequence_sequence_type_16s_sequence | string |  |  |

### ddt_brick0000458

**Rows:** 326,526 | **Columns:** 4

_dynamic table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string |  |  |
| sdt_taxon_name | string |  |  |
| taxonomic_level_sys_oterm_id | string |  |  |
| taxonomic_level_sys_oterm_name | string |  |  |

### ddt_brick0000459

**Rows:** 2,603,838 | **Columns:** 3

_dynamic table with 3 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| count_count_unit | integer |  |  |
| sdt_asv_name | string |  |  |
| sdt_community_name | string |  |  |

### ddt_brick0000460

**Rows:** 28,296 | **Columns:** 2

_dynamic table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string |  |  |
| sequence_sequence_type_16s_sequence | string |  |  |

### ddt_brick0000461

**Rows:** 170,088 | **Columns:** 5

_dynamic table with 5 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| confidence_confidence_unit | double |  |  |
| sdt_asv_name | string |  |  |
| sdt_taxon_name | string |  |  |
| taxonomic_level_sys_oterm_id | string |  |  |
| taxonomic_level_sys_oterm_name | string |  |  |

### ddt_brick0000462

**Rows:** 396,144 | **Columns:** 3

_dynamic table with 3 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| count_count_unit | integer |  |  |
| sdt_asv_name | string |  |  |
| sdt_community_name | string |  |  |

### ddt_brick0000476

**Rows:** 320,281,120 | **Columns:** 4

_dynamic table with 4 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| count_count_unit | integer |  |  |
| replicate_series_count_unit | integer |  |  |
| sdt_asv_name | string |  |  |
| sdt_community_name | string |  |  |

### ddt_brick0000477

**Rows:** 28,194 | **Columns:** 2

_dynamic table with 2 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_asv_name | string |  |  |
| sequence_sequence_type_16s_sequence | string |  |  |

### ddt_brick0000478

**Rows:** 169,491 | **Columns:** 5

_dynamic table with 5 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| confidence_confidence_unit | double |  |  |
| sdt_asv_name | string |  |  |
| sdt_taxon_name | string |  |  |
| taxonomic_level_sys_oterm_id | string |  |  |
| taxonomic_level_sys_oterm_name | string |  |  |

### ddt_brick0000479

**Rows:** 1,127,760 | **Columns:** 3

_dynamic table with 3 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| count_count_unit | integer |  |  |
| sdt_asv_name | string |  |  |
| sdt_community_name | string |  |  |

### ddt_brick0000495

**Rows:** 26,712 | **Columns:** 5

_dynamic table with 5 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| sdt_strain_name | string |  |  |
| sdt_taxon_name | string |  |  |
| strain_relative_evolutionary_divergence_dimensionless_unit | double |  |  |
| taxonomic_level_sys_oterm_id | string |  |  |
| taxonomic_level_sys_oterm_name | string |  |  |

### ddt_brick0000501

**Rows:** 9,321 | **Columns:** 10

_dynamic table with 10 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| date_comment_sampling_date | string |  |  |
| description_comment_original_condition_description | string |  |  |
| enigma_campaign_sys_oterm_id | string |  |  |
| enigma_campaign_sys_oterm_name | string |  |  |
| enigma_labs_and_personnel_comment_contact_person_or_lab_sys_oterm_id | string |  |  |
| enigma_labs_and_personnel_comment_contact_person_or_lab_sys_oterm_name | string |  |  |
| sdt_condition_name | string |  |  |
| sdt_location_name | string |  |  |
| sdt_sample_name | string |  |  |
| sdt_strain_name | string |  |  |

### ddt_brick0000507

**Rows:** 9,027 | **Columns:** 6

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

**Rows:** 12,702 | **Columns:** 6

_dynamic table with 6 columns_

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| read_coverage_comment_percent_of_1kb_chunks_of_genome_covered_by_at_least_one_read_percent | double |  |  |
| read_coverage_statistic_average_comment_cov80_average_coverage_after_trimming_highest_and_lowest_10_percent_count_unit | double |  |  |
| sdt_genome_name | string |  |  |
| sdt_sample_name | string |  |  |
| sdt_strain_name | string |  |  |
| sequence_identity_statistic_average_comment_average_percent_identity_of_aligned_reads_percent | double |  |  |

### ddt_ndarray

**Rows:** 120 | **Columns:** 15

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
| ME:0000234 | 2 | Type of community, e.g., isolate or enrichment, ontology term CURIE |
| ME:0000102 | 2 | Reference to the Sample from which the community was obtained. |
| ME:0000200 | 2 | Reference to the experimental or environmental condition associated with the com |
| ME:0000276 | 2 | Unique DubSeq library identifier (Primary key) |
| ME:0000262 | 2 | Unique, human-readable name of the DubSeq library |
| ME:0000228 | 2 | Unique name of the location |
| ME:0000213 | 2 | Continent where the location is situated, ontology term CURIE |
| ME:0000214 | 2 | Country of the location, ontology term CURIE |
| ME:0000216 | 2 | Biome classification of the location, ontology term CURIE |
| ME:0000217 | 2 | Environmental or geographic feature at the location, ontology term CURIE |
| ME:0000328 | 2 | Unique, human-readable name of the protocol |
| ME:0000112 | 2 | Category of reads (e.g., single-end, paired-end), ontology term CURIE |

*Showing top 20 of 69 microtypes*

## Relationship Catalog

Foreign key relationships between tables.

| Source Table | Source Column | Target Table | Target Column | Required |
|--------------|---------------|--------------|---------------|----------|
| ddt_brick0000072 | statistic_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000072 | sdt_sample_name | sdt_sample | sdt_sample_name |  |
| ddt_brick0000072 | molecule_from_list_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000507 | sdt_strain_name | sdt_strain | sdt_strain_name |  |
| ddt_brick0000507 | sequence_type_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_brick0000507 | strand_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_ndarray | ddt_ndarray_type_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| ddt_ndarray | ddt_ndarray_dimension_types_sys_oterm_id | [sys_oterm | sys_oterm_id] |  |
| ddt_ndarray | ddt_ndarray_dimension_variable_types_sys_oterm_id | [sys_oterm | sys_oterm_id] |  |
| ddt_ndarray | ddt_ndarray_variable_types_sys_oterm_id | [sys_oterm | sys_oterm_id] |  |
| ddt_ndarray | superceded_by_ddt_ndarray_id | ddt_ndarray | ddt_ndarray_id |  |
| sdt_assembly | sdt_strain_name | Strain | name |  |
| sdt_bin | sdt_assembly_name | Assembly | (any) |  |
| sdt_community | community_type_sys_oterm_id | sys_oterm | id |  |
| sdt_community | sdt_sample_name | Sample | name |  |
| sdt_community | parent_sdt_community_name | Community | name |  |
| sdt_community | sdt_condition_name | Condition | name |  |
| sdt_community | defined_sdt_strain_names | [Strain | name] |  |
| sdt_dubseq_library | sdt_genome_name | Genome | (any) |  |
| sdt_gene | sdt_genome_name | Genome | (any) |  |
| sdt_genome | sdt_strain_name | Strain | name |  |
| sdt_location | continent_sys_oterm_id | sys_oterm | id |  |
| sdt_location | country_sys_oterm_id | sys_oterm | id |  |
| sdt_location | biome_sys_oterm_id | sys_oterm | id |  |
| sdt_location | feature_sys_oterm_id | sys_oterm | id |  |
| sdt_reads | read_type_sys_oterm_id | sys_oterm | id |  |
| sdt_reads | sequencing_technology_sys_oterm_id | sys_oterm | id |  |
| sdt_sample | sdt_location_name | Location | name |  |
| sdt_sample | material_sys_oterm_id | sys_oterm | id |  |
| sdt_sample | env_package_sys_oterm_id | sys_oterm | id |  |
| sdt_strain | sdt_genome_name | Genome | name |  |
| sdt_strain | derived_from_sdt_strain_name | Strain | name |  |
| sdt_strain | sdt_gene_names_changed | [Gene | gene_id] |  |
| sdt_tnseq_library | sdt_genome_name | Genome | (any) |  |
| sys_oterm | parent_sys_oterm_id | sys_oterm | sys_oterm_id |  |
| sys_process | process_sys_oterm_id | sys_oterm | id |  |
| sys_process | person_sys_oterm_id | sys_oterm | id |  |
| sys_process | campaign_sys_oterm_id | sys_oterm | id |  |
| sys_process | sdt_protocol_name | Protocol | name |  |
| sys_process_input | sys_process_id | sys_process | sys_process_id |  |
| sys_process_input | sdt_assembly_id | sdt_assembly | sdt_assembly_id |  |
| sys_process_input | sdt_bin_id | sdt_bin | sdt_bin_id |  |
| sys_process_input | sdt_community_id | sdt_community | sdt_community_id |  |
| sys_process_input | sdt_genome_id | sdt_genome | sdt_genome_id |  |
| sys_process_input | sdt_location_id | sdt_location | sdt_location_id |  |
| sys_process_input | sdt_reads_id | sdt_reads | sdt_reads_id |  |
| sys_process_input | sdt_sample_id | sdt_sample | sdt_sample_id |  |
| sys_process_input | sdt_strain_id | sdt_strain | sdt_strain_id |  |
| sys_process_input | sdt_tnseq_library_id | sdt_tnseq_library | sdt_tnseq_library_id |  |
| sys_process_output | sys_process_id | sys_process | sys_process_id |  |

*Showing 50 of 61 relationships*
