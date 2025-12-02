
# kbase-cdm


**metamodel version:** 1.7.0

**version:** 1.0.0


LinkML schema for KBase Common Data Model (CDM) representing ENIGMA CORAL data.

This schema is derived from the original CORAL LinkML schema but includes
transformations specific to the KBase CDM implementation:

**Key CDM Patterns:**

1. **Ontology Term Splitting**
   - CORAL: Single field with ontology constraint
   - CDM: Two fields (ID + name) for each ontology term
   - Example: `material` → `material_sys_oterm_id` + `material_sys_oterm_name`
   - Enables FK validation + human-readable labels without joins

2. **CDM Naming Conventions**
   - Tables: `sdt_*` (static), `ddt_*` (dynamic), `sys_*` (system)
   - IDs: `sdt_{entity}_id` with pattern `EntityName\d{7}`
   - Names: `sdt_{entity}_name` (unique, used for FK references)
   - All columns: snake_case with entity prefix

3. **Centralized Ontology Catalog**
   - All ontology terms stored in `sys_oterm` table
   - 10,594 terms from multiple ontologies (ME, ENVO, UO, etc.)
   - Hierarchical relationships via `parent_sys_oterm_id`
   - Single source of truth for semantic metadata

4. **Denormalized Provenance Model**
   - Process workflows stored in `sys_process` table
   - Input/output relationships in `sys_process_input`, `sys_process_output`
   - Complete lineage tracing from samples to analyses
   - 142,958 process records documenting all transformations

5. **Dynamic Data Bricks**
   - N-dimensional measurement arrays in `ddt_brick*` tables
   - Flexible schema defined in `sys_ddt_typedef`
   - Semantic dimensions and variables via ontology terms
   - 82.6M rows across 20 brick tables

**Schema Organization:**

This schema is modular, organized into:
- `cdm_base.yaml`: Common types, mixins, validation patterns
- `cdm_static_entities.yaml`: 17 sdt_* entity classes
- `cdm_system_tables.yaml`: 6 sys_* system classes
- `cdm_dynamic_data.yaml`: Brick infrastructure (ddt_*)
- `linkml_coral_cdm.yaml`: Main schema (this file)

**Data Volume:**
- 272,934 rows across 17 static entity tables
- 142,958 process records (provenance)
- 10,594 ontology terms
- 82.6M rows in dynamic data tables

**Comparison to Original CORAL:**
- Maintains same 17 core entity types
- Adds 6 new system table classes
- Preserves provenance annotations
- Extends with CDM-specific patterns

**Documentation:**
- Analysis Report: `docs/cdm_analysis/CDM_PARQUET_ANALYSIS_REPORT.md`
- Schema Comparison: `docs/CORAL_TO_CDM_MAPPING.md`
- Validation Guide: `docs/CDM_VALIDATION_GUIDE.md`


### Classes

 * [ASV](ASV.md) - Amplicon Sequence Variant (formerly OTU).
 * [Assembly](Assembly.md) - Genome assembly from sequencing reads.
 * [Bin](Bin.md) - Genome bin extracted from metagenomic assembly.
 * [Brick](Brick.md) - Abstract base for all brick data tables (ddt_brick*).
 * [BrickDimension](BrickDimension.md) - Abstract base for brick dimension metadata.
 * [BrickVariable](BrickVariable.md) - Abstract base for brick variable metadata.
 * [Community](Community.md) - Microbial community (isolate, enrichment, assemblage, or environmental).
 * [Condition](Condition.md) - Growth or experimental condition.
 * [DubSeqLibrary](DubSeqLibrary.md) - Dual Barcoded Sequencing (DubSeq) library.
 * [DynamicDataArray](DynamicDataArray.md) - Brick index table (ddt_ndarray).
 * [ENIGMA](ENIGMA.md) - Root entity (database singleton).
 * [Gene](Gene.md) - Annotated gene within a genome.
 * [Genome](Genome.md) - Assembled and annotated genome.
 * [Image](Image.md) - Microscopy or other image data.
 * [Location](Location.md) - Sampling location with geographic coordinates and environmental context.
 * [Protocol](Protocol.md) - Experimental protocol.
 * [Reads](Reads.md) - Sequencing reads dataset.
 * [Sample](Sample.md) - Environmental sample collected from a location.
 * [Strain](Strain.md) - Microbial strain (isolated or derived).
 * [SystemDDTTypedef](SystemDDTTypedef.md) - Type definitions for dynamic data tables (bricks).
 * [SystemOntologyTerm](SystemOntologyTerm.md) - Centralized ontology term catalog.
 * [SystemProcess](SystemProcess.md) - Provenance tracking for all data transformations.
 * [SystemProcessInput](SystemProcessInput.md) - Normalized process input relationships.
 * [SystemProcessOutput](SystemProcessOutput.md) - Normalized process output relationships.
 * [SystemTypedef](SystemTypedef.md) - Type definitions for static entity tables (equivalent to typedef.json).
 * [Taxon](Taxon.md) - Taxonomic classification.
 * [TnSeqLibrary](TnSeqLibrary.md) - Transposon Sequencing (TnSeq) library.

### Mixins

 * [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).
 * [OntologyTermPair](OntologyTermPair.md) - Mixin for ontology-constrained fields in KBase CDM.
 * [SystemEntity](SystemEntity.md) - Base mixin for CDM system tables (sys_*).

### Slots

 * [assembly_ref](assembly_ref.md) - Reference to assembly name (FK to Assembly.sdt_assembly_name)
 * [associated_entity_names](associated_entity_names.md) - Names of entities associated with this brick
 * [associated_entity_type](associated_entity_type.md) - Type of entities measured (e.g., "Sample", "Community")
 * [base_count](base_count.md) - Total number of bases
 * [biome_sys_oterm_id](biome_sys_oterm_id.md) - Biome ontology term ID (ENVO)
 * [biome_sys_oterm_name](biome_sys_oterm_name.md) - Biome ontology term name
 * [brick_table_name](brick_table_name.md) - Name of brick table (e.g., "ddt_brick0000010")
 * [campaign_sys_oterm_id](campaign_sys_oterm_id.md) - Research campaign ontology term ID
 * [campaign_sys_oterm_name](campaign_sys_oterm_name.md) - Research campaign ontology term name
 * [cdm_column_data_type](cdm_column_data_type.md) - Column type (variable, dimension_variable, or dimension_index)
 * [cdm_column_name](cdm_column_name.md) - Mapped CDM column name (snake_case with prefixes)
 * [community_type_sys_oterm_id](community_type_sys_oterm_id.md) - Community type ontology term ID
 * [community_type_sys_oterm_name](community_type_sys_oterm_name.md) - Community type ontology term name
 * [constraint](constraint.md) - Validation pattern or ontology constraint
 * [contig_number](contig_number.md) - Contig number where gene is located
 * [contigs](contigs.md) - Comma-separated list of contig names
 * [continent_sys_oterm_id](continent_sys_oterm_id.md) - Continent ontology term ID
 * [continent_sys_oterm_name](continent_sys_oterm_name.md) - Continent ontology term name
 * [country_sys_oterm_id](country_sys_oterm_id.md) - Country ontology term ID
 * [country_sys_oterm_name](country_sys_oterm_name.md) - Country ontology term name
 * [creation_date](creation_date.md) - Date brick was created
 * [date](date.md) - Collection date
 * [date_end](date_end.md) - Process end date
 * [date_start](date_start.md) - Process start date
 * [ddt_ndarray_id](ddt_ndarray_id.md) - Brick identifier (e.g., "Brick0000010")
     * [DynamicDataArray➞ddt_ndarray_id](DynamicDataArray_ddt_ndarray_id.md)
 * [defined_strains_ref](defined_strains_ref.md) - References to defined strain names (multivalued FK to Strain.sdt_strain_name)
 * [depth](depth.md) - Depth in meters
 * [derived_from_strain_ref](derived_from_strain_ref.md) - Reference to parent strain name (FK, self-referential to Strain.sdt_strain_name)
 * [description](description.md) - Free text description
 * [dimension_number](dimension_number.md) - Position in N-dimensional array (0-indexed)
 * [dimension_oterm_id](dimension_oterm_id.md) - Dimension semantic ontology term ID
 * [dimension_oterm_name](dimension_oterm_name.md) - Dimension semantic ontology term name
 * [dimension_size](dimension_size.md) - Number of values along this dimension
 * [dimension_sizes](dimension_sizes.md) - Comma-separated dimension sizes (e.g., "209,52,3,3")
 * [dimension_values](dimension_values.md) - Comma-separated dimension value labels
 * [dimensions](dimensions.md) - Image dimensions (e.g., "1024x768")
 * [elevation](elevation.md) - Elevation in meters
 * [env_package_sys_oterm_id](env_package_sys_oterm_id.md) - Environment package ontology term ID
 * [env_package_sys_oterm_name](env_package_sys_oterm_name.md) - Environment package ontology term name
 * [feature_sys_oterm_id](feature_sys_oterm_id.md) - Environmental feature ontology term ID
 * [feature_sys_oterm_name](feature_sys_oterm_name.md) - Environmental feature ontology term name
 * [field_name](field_name.md) - Original CORAL field name
 * [fk](fk.md) - Foreign key reference
 * [function](function.md) - Predicted gene function
 * [gene_names_changed](gene_names_changed.md) - Names of genes that were changed
 * [genome_ref](genome_ref.md) - Reference to genome name (FK to Genome.sdt_genome_name)
 * [input_index](input_index.md) - Index in input_objects array
 * [input_object_name](input_object_name.md) - Name of input entity
 * [input_object_type](input_object_type.md) - Type of input entity (e.g., "Sample", "Reads")
 * [input_objects](input_objects.md) - Array of input entity references (type:name format)
 * [latitude](latitude.md) - Latitude in decimal degrees
 * [link](link.md) - External reference URL or file path
 * [location_ref](location_ref.md) - Reference to location name (FK to Location.sdt_location_name)
 * [longitude](longitude.md) - Longitude in decimal degrees
 * [material_sys_oterm_id](material_sys_oterm_id.md) - Material type ontology term ID
 * [material_sys_oterm_name](material_sys_oterm_name.md) - Material type ontology term name
 * [max_value](max_value.md) - Maximum allowed value (for numeric variables)
 * [measurement_type_sys_oterm_id](measurement_type_sys_oterm_id.md) - Type of measurement ontology term ID
 * [measurement_type_sys_oterm_name](measurement_type_sys_oterm_name.md) - Type of measurement ontology term name
 * [mime_type](mime_type.md) - MIME type of image
 * [min_value](min_value.md) - Minimum allowed value (for numeric variables)
 * [n_contigs](n_contigs.md) - Number of contigs
 * [n_dimensions](n_dimensions.md) - Number of dimensions in array
 * [n_features](n_features.md) - Number of annotated features
 * [n_fragments](n_fragments.md) - Number of fragments
 * [n_genes_hit](n_genes_hit.md) - Number of genes with transposon insertions
 * [n_good_reads](n_good_reads.md) - Number of good quality reads
 * [n_mapped_reads](n_mapped_reads.md) - Number of mapped reads
 * [n_variables](n_variables.md) - Number of measured variables
 * [ncbi_taxid](ncbi_taxid.md) - NCBI Taxonomy ID
 * [output_index](output_index.md) - Index in output_objects array
 * [output_object_name](output_object_name.md) - Name of output entity
 * [output_object_type](output_object_type.md) - Type of output entity (e.g., "Assembly", "Genome")
 * [output_objects](output_objects.md) - Array of output entity references (type:name format)
 * [parent_community_ref](parent_community_ref.md) - Reference to parent community name (FK, self-referential to Community.sdt_community_name)
 * [parent_sys_oterm_id](parent_sys_oterm_id.md) - Parent term in ontology hierarchy (FK to sys_oterm)
 * [person_sys_oterm_id](person_sys_oterm_id.md) - Person who performed process (ontology term ID)
 * [person_sys_oterm_name](person_sys_oterm_name.md) - Person who performed process (ontology term name)
 * [pk](pk.md) - Primary key flag
 * [primers_model](primers_model.md) - Primers model used
 * [process_type_sys_oterm_id](process_type_sys_oterm_id.md) - Process type ontology term ID
 * [process_type_sys_oterm_name](process_type_sys_oterm_name.md) - Process type ontology term name
 * [read_count](read_count.md) - Number of reads
 * [read_type_sys_oterm_id](read_type_sys_oterm_id.md) - Read type ontology term ID (e.g., paired-end, single-end)
 * [read_type_sys_oterm_name](read_type_sys_oterm_name.md) - Read type ontology term name
 * [region](region.md) - Geographic region
 * [sample_ref](sample_ref.md) - Reference to sample name (FK to Sample.sdt_sample_name)
 * [scalar_type](scalar_type.md) - Data type (text, int, float, [text] for arrays)
 * [sdt_assembly_id](sdt_assembly_id.md) - Unique identifier for Assembly
 * [sdt_assembly_name](sdt_assembly_name.md) - Name of assembly
 * [sdt_asv_id](sdt_asv_id.md) - Unique identifier for ASV
 * [sdt_asv_name](sdt_asv_name.md) - Name of ASV
 * [sdt_bin_id](sdt_bin_id.md) - Unique identifier for Bin
 * [sdt_bin_name](sdt_bin_name.md) - Name of bin
 * [sdt_community_id](sdt_community_id.md) - Unique identifier for Community
 * [sdt_community_name](sdt_community_name.md) - Name of community
 * [sdt_condition_id](sdt_condition_id.md) - Unique identifier for Condition
 * [sdt_condition_name](sdt_condition_name.md) - Name of condition
 * [sdt_dubseq_library_id](sdt_dubseq_library_id.md) - Unique identifier for DubSeqLibrary
 * [sdt_dubseq_library_name](sdt_dubseq_library_name.md) - Name of DubSeq library
 * [sdt_enigma_id](sdt_enigma_id.md) - Unique identifier for ENIGMA root entity
 * [sdt_gene_id](sdt_gene_id.md) - Unique identifier for Gene
 * [sdt_gene_name](sdt_gene_name.md) - Name of gene
 * [sdt_genome_id](sdt_genome_id.md) - Unique identifier for Genome
 * [sdt_genome_name](sdt_genome_name.md) - Name of genome
 * [sdt_image_id](sdt_image_id.md) - Unique identifier for Image
 * [sdt_image_name](sdt_image_name.md) - Name of image
 * [sdt_location_id](sdt_location_id.md) - Unique identifier for Location
 * [sdt_location_name](sdt_location_name.md) - Name of location
 * [sdt_protocol_id](sdt_protocol_id.md) - Unique identifier for Protocol
 * [sdt_protocol_name](sdt_protocol_name.md) - Name of protocol
 * [sdt_reads_id](sdt_reads_id.md) - Unique identifier for Reads
 * [sdt_reads_name](sdt_reads_name.md) - Name of reads dataset
 * [sdt_sample_id](sdt_sample_id.md) - Unique identifier for Sample
 * [sdt_sample_name](sdt_sample_name.md) - Name of sample
 * [sdt_strain_id](sdt_strain_id.md) - Unique identifier for Strain
 * [sdt_strain_name](sdt_strain_name.md) - Name of strain
 * [sdt_taxon_id](sdt_taxon_id.md) - Unique identifier for Taxon
 * [sdt_taxon_name](sdt_taxon_name.md) - Taxonomic name
 * [sdt_tnseq_library_id](sdt_tnseq_library_id.md) - Unique identifier for TnSeqLibrary
 * [sdt_tnseq_library_name](sdt_tnseq_library_name.md) - Name of TnSeq library
 * [sequence](sequence.md) - DNA sequence
 * [sequencing_technology_sys_oterm_id](sequencing_technology_sys_oterm_id.md) - Sequencing technology ontology term ID
 * [sequencing_technology_sys_oterm_name](sequencing_technology_sys_oterm_name.md) - Sequencing technology ontology term name
 * [size](size.md) - File size in bytes
 * [start](start.md) - Start position on contig
 * [stop](stop.md) - Stop position on contig
 * [strain_ref](strain_ref.md) - Reference to strain name (FK to Strain.sdt_strain_name)
 * [strand](strand.md) - DNA strand (+ or -)
 * [sys_oterm_definition](sys_oterm_definition.md) - Formal term definition
 * [sys_oterm_id](sys_oterm_id.md) - Ontology term identifier (CURIE format)
     * [SystemOntologyTerm➞sys_oterm_id](SystemOntologyTerm_sys_oterm_id.md)
 * [sys_oterm_links](sys_oterm_links.md) - External links (URLs, pipe-separated)
 * [sys_oterm_name](sys_oterm_name.md) - Human-readable ontology term name
 * [sys_oterm_ontology](sys_oterm_ontology.md) - Source ontology name
 * [sys_oterm_properties](sys_oterm_properties.md) - Additional term properties (JSON or key=value pairs)
 * [sys_oterm_synonyms](sys_oterm_synonyms.md) - Alternative term names (pipe-separated)
 * [sys_process_id](sys_process_id.md) - Unique process identifier
     * [SystemProcess➞sys_process_id](SystemProcess_sys_process_id.md)
 * [time](time.md) - Collection time
 * [timezone](timezone.md) - Timezone
 * [total_rows](total_rows.md) - Total number of data rows in brick table
 * [total_size](total_size.md) - Total assembly size in base pairs
 * [type_name](type_name.md) - CORAL entity type name (e.g., "Gene", "Sample")
 * [type_sys_oterm_id](type_sys_oterm_id.md) - Ontology term for data type
 * [unit_sys_oterm_id](unit_sys_oterm_id.md) - Measurement unit ontology term ID
 * [unit_sys_oterm_name](unit_sys_oterm_name.md) - Measurement unit ontology term name
 * [units_sys_oterm_id](units_sys_oterm_id.md) - Ontology term for measurement units
 * [upk](upk.md) - Unique key flag
 * [variable_data_type](variable_data_type.md) - Data type of variable (float, int, bool, oterm_ref, object_ref)
 * [variable_number](variable_number.md) - Variable index in brick
 * [variable_oterm_id](variable_oterm_id.md) - Variable semantic ontology term ID
 * [variable_oterm_name](variable_oterm_name.md) - Variable semantic ontology term name

### Enums

 * [BiomeEnum](BiomeEnum.md) - Environmental biome
 * [BrickDataType](BrickDataType.md) - Data types for brick variables
 * [CommunityTypeEnum](CommunityTypeEnum.md) - Microbial community type
 * [DimensionSemantics](DimensionSemantics.md) - Common dimension semantic types
 * [MaterialEnum](MaterialEnum.md) - Sample material type
 * [ReadTypeEnum](ReadTypeEnum.md) - Sequencing read type
 * [SequencingTechnologyEnum](SequencingTechnologyEnum.md) - Sequencing platform technology
 * [StrandEnum](StrandEnum.md) - DNA strand orientation
 * [VariableSemantics](VariableSemantics.md) - Common variable semantic types

### Subsets


### Types


#### Built in

 * **Bool**
 * **Curie**
 * **Decimal**
 * **ElementIdentifier**
 * **NCName**
 * **NodeIdentifier**
 * **URI**
 * **URIorCURIE**
 * **XSDDate**
 * **XSDDateTime**
 * **XSDTime**
 * **float**
 * **int**
 * **str**

#### Defined

 * [Count](types/Count.md)  ([Integer](types/Integer.md))  - Non-negative integer count
 * [Date](types/Date.md)  ([String](types/String.md))  - ISO 8601 date format (YYYY-MM-DD)
 * [Depth](types/Depth.md)  ([Float](types/Float.md))  - Depth measurement (meters)
 * [Elevation](types/Elevation.md)  ([Float](types/Float.md))  - Elevation measurement (meters)
 * [EntityName](types/EntityName.md)  ([String](types/String.md))  - Human-readable entity name
 * [Latitude](types/Latitude.md)  ([Float](types/Float.md))  - Latitude in decimal degrees
 * [Link](types/Link.md)  ([String](types/String.md))  - HTTP/HTTPS URL or file path
 * [Longitude](types/Longitude.md)  ([Float](types/Float.md))  - Longitude in decimal degrees
 * [OntologyTermID](types/OntologyTermID.md)  ([String](types/String.md))  - CURIE format ontology term identifier (e.g., ME:0000129, ENVO:00002041)
 * [Rate](types/Rate.md)  ([Float](types/Float.md))  - Rate or frequency measurement
 * [Size](types/Size.md)  ([Integer](types/Integer.md))  - Size in bytes
 * [Time](types/Time.md)  ([String](types/String.md))  - Time in HH:MM or HH:MM:SS format
 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [Curie](types/Curie.md)  (**Curie**)  - a compact URI
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [DateOrDatetime](types/DateOrDatetime.md)  (**str**)  - Either a date or a datetime
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Jsonpath](types/Jsonpath.md)  (**str**)  - A string encoding a JSON Path. The value of the string MUST conform to JSON Point syntax and SHOULD dereference to zero or more valid objects within the current instance document when encoded in tree form.
 * [Jsonpointer](types/Jsonpointer.md)  (**str**)  - A string encoding a JSON Pointer. The value of the string MUST conform to JSON Point syntax and SHOULD dereference to a valid object within the current instance document when encoded in tree form.
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [Sparqlpath](types/Sparqlpath.md)  (**str**)  - A string encoding a SPARQL Property Path. The value of the string MUST conform to SPARQL syntax and SHOULD dereference to zero or more valid objects within the current instance document when encoded as RDF.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
