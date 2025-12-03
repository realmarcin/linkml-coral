-- # Abstract Class: OntologyTermPair Description: Mixin for ontology-constrained fields in KBase CDM.The CDM splits each ontology-controlled field into two columns:- {field}_sys_oterm_id: CURIE identifier (FK to sys_oterm)- {field}_sys_oterm_name: Human-readable term nameThis pattern enables:- Ontology validation via FK constraint- Human-readable labels without joins- Ontology evolution without data migrationExamples:- material → material_sys_oterm_id + material_sys_oterm_name- biome → biome_sys_oterm_id + biome_sys_oterm_name- read_type → read_type_sys_oterm_id + read_type_sys_oterm_name
--     * Slot: id
-- # Abstract Class: CDMEntity Description: Base mixin for all CDM static data tables (sdt_*).Enforces CDM naming conventions:- Primary key: sdt_{entity}_id with pattern EntityName\d{7}- Name field: sdt_{entity}_name (unique, used for FK references)- All columns use snake_case with entity prefixExample:- Location: sdt_location_id, sdt_location_name- Sample: sdt_sample_id, sdt_sample_nameNote: Each entity class must define its own id and name slotswith entity-specific names (e.g., sdt_location_id, sdt_location_name).
--     * Slot: id
-- # Abstract Class: SystemEntity Description: Base mixin for CDM system tables (sys_*).System tables provide metadata, type definitions, provenance tracking,and ontology catalogs. They support the static and dynamic data tablesbut are not directly linked to experimental entities.System tables: sys_typedef, sys_ddt_typedef, sys_oterm, sys_process,sys_process_input, sys_process_output
--     * Slot: id
-- # Class: Location Description: Sampling location with geographic coordinates and environmental context.CDM changes from CORAL:- 4 ontology term fields split into ID+name pairs:  continent, country, biome, feature
--     * Slot: sdt_location_id Description: Unique identifier for Location
--     * Slot: sdt_location_name Description: Name of location
--     * Slot: latitude Description: Latitude in decimal degrees
--     * Slot: longitude Description: Longitude in decimal degrees
--     * Slot: continent_sys_oterm_id Description: Continent ontology term ID
--     * Slot: continent_sys_oterm_name Description: Continent ontology term name
--     * Slot: country_sys_oterm_id Description: Country ontology term ID
--     * Slot: country_sys_oterm_name Description: Country ontology term name
--     * Slot: region Description: Geographic region
--     * Slot: biome_sys_oterm_id Description: Biome ontology term ID (ENVO)
--     * Slot: biome_sys_oterm_name Description: Biome ontology term name
--     * Slot: feature_sys_oterm_id Description: Environmental feature ontology term ID
--     * Slot: feature_sys_oterm_name Description: Environmental feature ontology term name
-- # Class: Sample Description: Environmental sample collected from a location.CDM changes from CORAL:- 2 ontology term fields split: material, env_package- FK reference: location → location_ref
--     * Slot: sdt_sample_id Description: Unique identifier for Sample
--     * Slot: sdt_sample_name Description: Name of sample
--     * Slot: location_ref Description: Reference to location name (FK to Location.sdt_location_name)
--     * Slot: depth Description: Depth in meters
--     * Slot: elevation Description: Elevation in meters
--     * Slot: date Description: Collection date
--     * Slot: time Description: Collection time
--     * Slot: timezone Description: Timezone
--     * Slot: material_sys_oterm_id Description: Material type ontology term ID
--     * Slot: material_sys_oterm_name Description: Material type ontology term name
--     * Slot: env_package_sys_oterm_id Description: Environment package ontology term ID
--     * Slot: env_package_sys_oterm_name Description: Environment package ontology term name
--     * Slot: description Description: Free text description
-- # Class: Community Description: Microbial community (isolate, enrichment, assemblage, or environmental).CDM changes from CORAL:- 1 ontology term field split: community_type- FK references: sample → sample_ref, parent_community → parent_community_ref- Multivalued FK: defined_strains → defined_strains_ref
--     * Slot: sdt_community_id Description: Unique identifier for Community
--     * Slot: sdt_community_name Description: Name of community
--     * Slot: community_type_sys_oterm_id Description: Community type ontology term ID
--     * Slot: community_type_sys_oterm_name Description: Community type ontology term name
--     * Slot: sample_ref Description: Reference to sample name (FK to Sample.sdt_sample_name)
--     * Slot: parent_community_ref Description: Reference to parent community name (FK, self-referential to Community.sdt_community_name)
-- # Class: Reads Description: Sequencing reads dataset.CDM changes from CORAL:- 2 ontology term fields split: read_type, sequencing_technology- Added 'link' field for external data references
--     * Slot: sdt_reads_id Description: Unique identifier for Reads
--     * Slot: sdt_reads_name Description: Name of reads dataset
--     * Slot: read_count Description: Number of reads
--     * Slot: base_count Description: Total number of bases
--     * Slot: read_type_sys_oterm_id Description: Read type ontology term ID (e.g., paired-end, single-end)
--     * Slot: read_type_sys_oterm_name Description: Read type ontology term name
--     * Slot: sequencing_technology_sys_oterm_id Description: Sequencing technology ontology term ID
--     * Slot: sequencing_technology_sys_oterm_name Description: Sequencing technology ontology term name
--     * Slot: link Description: External reference URL or file path
-- # Class: Assembly Description: Genome assembly from sequencing reads.CDM changes from CORAL:- FK reference: strain → strain_ref- Added 'link' field
--     * Slot: sdt_assembly_id Description: Unique identifier for Assembly
--     * Slot: sdt_assembly_name Description: Name of assembly
--     * Slot: strain_ref Description: Reference to strain name (FK to Strain.sdt_strain_name)
--     * Slot: n_contigs Description: Number of contigs
--     * Slot: total_size Description: Total assembly size in base pairs
--     * Slot: link Description: External reference URL or file path
-- # Class: Bin Description: Genome bin extracted from metagenomic assembly.CDM changes from CORAL:- FK reference: assembly → assembly_ref- contigs field contains comma-separated contig names
--     * Slot: sdt_bin_id Description: Unique identifier for Bin
--     * Slot: sdt_bin_name Description: Name of bin
--     * Slot: assembly_ref Description: Reference to assembly name (FK to Assembly.sdt_assembly_name)
--     * Slot: contigs Description: Comma-separated list of contig names
-- # Class: Genome Description: Assembled and annotated genome.CDM changes from CORAL:- FK reference: strain → strain_ref- Added 'link' field
--     * Slot: sdt_genome_id Description: Unique identifier for Genome
--     * Slot: sdt_genome_name Description: Name of genome
--     * Slot: strain_ref Description: Reference to strain name (FK to Strain.sdt_strain_name)
--     * Slot: n_contigs Description: Number of contigs
--     * Slot: n_features Description: Number of annotated features
--     * Slot: total_size Description: Total assembly size in base pairs
--     * Slot: link Description: External reference URL or file path
-- # Class: Gene Description: Annotated gene within a genome.CDM changes from CORAL:- FK reference: genome → genome_ref- Gene ID convention: GeneName{genome_name}_{contig}_{start}_{stop}
--     * Slot: sdt_gene_id Description: Unique identifier for Gene
--     * Slot: sdt_gene_name Description: Name of gene
--     * Slot: genome_ref Description: Reference to genome name (FK to Genome.sdt_genome_name)
--     * Slot: contig_number Description: Contig number where gene is located
--     * Slot: strand Description: DNA strand (+ or -)
--     * Slot: start Description: Start position on contig
--     * Slot: stop Description: Stop position on contig
--     * Slot: function Description: Predicted gene function
-- # Class: Strain Description: Microbial strain (isolated or derived).CDM changes from CORAL:- FK references: genome → genome_ref, derived_from → derived_from_strain_ref- Self-referential for strain derivation lineage
--     * Slot: sdt_strain_id Description: Unique identifier for Strain
--     * Slot: sdt_strain_name Description: Name of strain
--     * Slot: genome_ref Description: Reference to genome name (FK to Genome.sdt_genome_name)
--     * Slot: derived_from_strain_ref Description: Reference to parent strain name (FK, self-referential to Strain.sdt_strain_name)
-- # Class: Taxon Description: Taxonomic classification.
--     * Slot: sdt_taxon_id Description: Unique identifier for Taxon
--     * Slot: sdt_taxon_name Description: Taxonomic name
--     * Slot: ncbi_taxid Description: NCBI Taxonomy ID
-- # Class: ASV Description: Amplicon Sequence Variant (formerly OTU).CDM changes from CORAL:- Entity renamed from OTU to ASV (Amplicon Sequence Variant)- Table name: sdt_asv
--     * Slot: sdt_asv_id Description: Unique identifier for ASV
--     * Slot: sdt_asv_name Description: Name of ASV
--     * Slot: sequence Description: DNA sequence
-- # Class: Protocol Description: Experimental protocol.CDM changes from CORAL:- Added 'link' field for protocol documents
--     * Slot: sdt_protocol_id Description: Unique identifier for Protocol
--     * Slot: sdt_protocol_name Description: Name of protocol
--     * Slot: description Description: Free text description
--     * Slot: link Description: External reference URL or file path
-- # Class: Image Description: Microscopy or other image data.CDM changes from CORAL:- Added 'link' field for image files
--     * Slot: sdt_image_id Description: Unique identifier for Image
--     * Slot: sdt_image_name Description: Name of image
--     * Slot: mime_type Description: MIME type of image
--     * Slot: size Description: File size in bytes
--     * Slot: dimensions Description: Image dimensions (e.g., "1024x768")
--     * Slot: link Description: External reference URL or file path
-- # Class: Condition Description: Growth or experimental condition.
--     * Slot: sdt_condition_id Description: Unique identifier for Condition
--     * Slot: sdt_condition_name Description: Name of condition
-- # Class: DubSeqLibrary Description: Dual Barcoded Sequencing (DubSeq) library.CDM changes from CORAL:- FK reference: genome → genome_ref
--     * Slot: sdt_dubseq_library_id Description: Unique identifier for DubSeqLibrary
--     * Slot: sdt_dubseq_library_name Description: Name of DubSeq library
--     * Slot: genome_ref Description: Reference to genome name (FK to Genome.sdt_genome_name)
--     * Slot: n_fragments Description: Number of fragments
-- # Class: TnSeqLibrary Description: Transposon Sequencing (TnSeq) library.CDM changes from CORAL:- FK reference: genome → genome_ref
--     * Slot: sdt_tnseq_library_id Description: Unique identifier for TnSeqLibrary
--     * Slot: sdt_tnseq_library_name Description: Name of TnSeq library
--     * Slot: genome_ref Description: Reference to genome name (FK to Genome.sdt_genome_name)
--     * Slot: primers_model Description: Primers model used
--     * Slot: n_mapped_reads Description: Number of mapped reads
--     * Slot: n_good_reads Description: Number of good quality reads
--     * Slot: n_genes_hit Description: Number of genes with transposon insertions
-- # Class: ENIGMA Description: Root entity (database singleton).
--     * Slot: sdt_enigma_id Description: Unique identifier for ENIGMA root entity
-- # Class: SystemTypedef Description: Type definitions for static entity tables (equivalent to typedef.json).Maps CORAL entity types and fields to CDM table/column names withconstraints, data types, and ontology references.This table documents the schema transformation from CORAL to CDM andenables automated validation and migration.
--     * Slot: id
--     * Slot: type_name Description: CORAL entity type name (e.g., "Gene", "Sample")
--     * Slot: field_name Description: Original CORAL field name
--     * Slot: cdm_column_name Description: Mapped CDM column name (snake_case with prefixes)
--     * Slot: scalar_type Description: Data type (text, int, float, [text] for arrays)
--     * Slot: pk Description: Primary key flag
--     * Slot: upk Description: Unique key flag
--     * Slot: fk Description: Foreign key reference
--     * Slot: constraint Description: Validation pattern or ontology constraint
--     * Slot: units_sys_oterm_id Description: Ontology term for measurement units
--     * Slot: type_sys_oterm_id Description: Ontology term for data type
-- # Class: SystemDDTTypedef Description: Type definitions for dynamic data tables (bricks).Defines schema for N-dimensional measurement arrays including:- Dimension semantics (Environmental Sample, Molecule, State, Statistic)- Variable semantics (Concentration, Molecular Weight, etc.)- Data types and units- Brick structure metadataEach brick can have different dimensionality and variable sets,enabling flexible storage of heterogeneous measurement data.
--     * Slot: id
--     * Slot: ddt_ndarray_id Description: Brick identifier (e.g., "Brick0000010")
--     * Slot: cdm_column_name Description: Mapped CDM column name (snake_case with prefixes)
--     * Slot: cdm_column_data_type Description: Column type (variable, dimension_variable, or dimension_index)
--     * Slot: scalar_type Description: Data type (text, int, float, [text] for arrays)
--     * Slot: dimension_number Description: Position in N-dimensional array (0-indexed)
--     * Slot: variable_number Description: Variable index in brick
--     * Slot: dimension_oterm_id Description: Dimension semantic ontology term ID
--     * Slot: dimension_oterm_name Description: Dimension semantic ontology term name
--     * Slot: variable_oterm_id Description: Variable semantic ontology term ID
--     * Slot: variable_oterm_name Description: Variable semantic ontology term name
--     * Slot: unit_sys_oterm_id Description: Measurement unit ontology term ID
--     * Slot: unit_sys_oterm_name Description: Measurement unit ontology term name
-- # Class: SystemOntologyTerm Description: Centralized ontology term catalog.Stores all ontology terms used across the CDM with:- CURIE identifiers (ME:, ENVO:, UO:, etc.)- Human-readable names- Hierarchical relationships (parent terms)- Definitions, synonyms, and external linksBenefits:- Single source of truth for ontology terms- Supports ontology evolution without data migration- Enables semantic queries and reasoning- Foreign key target for all *_sys_oterm_id columns
--     * Slot: sys_oterm_id Description: Ontology term identifier (CURIE format)
--     * Slot: sys_oterm_name Description: Human-readable ontology term name
--     * Slot: sys_oterm_ontology Description: Source ontology name
--     * Slot: parent_sys_oterm_id Description: Parent term in ontology hierarchy (FK to sys_oterm)
--     * Slot: sys_oterm_definition Description: Formal term definition
--     * Slot: sys_oterm_synonyms Description: Alternative term names (pipe-separated)
--     * Slot: sys_oterm_links Description: External links (URLs, pipe-separated)
--     * Slot: sys_oterm_properties Description: Additional term properties (JSON or key=value pairs)
-- # Class: SystemProcess Description: Provenance tracking for all data transformations.Records experimental processes with:- Process type (Assay Growth, Sequencing, etc.)- People, protocols, campaigns- Temporal metadata (start/end dates)- Input/output relationships (denormalized arrays)Enables complete lineage tracing from raw samples to final analyses.
--     * Slot: sys_process_id Description: Unique process identifier
--     * Slot: process_type_sys_oterm_id Description: Process type ontology term ID
--     * Slot: process_type_sys_oterm_name Description: Process type ontology term name
--     * Slot: person_sys_oterm_id Description: Person who performed process (ontology term ID)
--     * Slot: person_sys_oterm_name Description: Person who performed process (ontology term name)
--     * Slot: campaign_sys_oterm_id Description: Research campaign ontology term ID
--     * Slot: campaign_sys_oterm_name Description: Research campaign ontology term name
--     * Slot: sdt_protocol_name Description: Name of protocol
--     * Slot: date_start Description: Process start date
--     * Slot: date_end Description: Process end date
-- # Class: SystemProcessInput Description: Normalized process input relationships.Denormalizes the input_objects array from sys_process for efficientquerying. Each row represents one input entity to one process.Enables queries like:- "Find all processes that used this sample"- "What samples were used in sequencing processes?"
--     * Slot: id
--     * Slot: sys_process_id Description: Unique process identifier
--     * Slot: input_object_type Description: Type of input entity (e.g., "Sample", "Reads")
--     * Slot: input_object_name Description: Name of input entity
--     * Slot: input_index Description: Index in input_objects array
-- # Class: SystemProcessOutput Description: Normalized process output relationships.Denormalizes the output_objects array from sys_process for efficientquerying. Each row represents one output entity from one process.Enables queries like:- "What process created this assembly?"- "Find all assemblies from sequencing processes"
--     * Slot: id
--     * Slot: sys_process_id Description: Unique process identifier
--     * Slot: output_object_type Description: Type of output entity (e.g., "Assembly", "Genome")
--     * Slot: output_object_name Description: Name of output entity
--     * Slot: output_index Description: Index in output_objects array
-- # Class: DynamicDataArray Description: Brick index table (ddt_ndarray).Catalogs all available measurement bricks with:- Brick identifiers (Brick0000001, Brick0000002, etc.)- Shape metadata (dimensions and sizes)- Entity relationships (which samples, communities, etc.)- Semantic metadata (measurement types, units)Each brick corresponds to:- One ddt_brick* table with actual measurement data- Multiple rows in sys_ddt_typedef defining brick schema
--     * Slot: ddt_ndarray_id Description: Brick identifier (e.g., "Brick0000010")
--     * Slot: brick_table_name Description: Name of brick table (e.g., "ddt_brick0000010")
--     * Slot: n_dimensions Description: Number of dimensions in array
--     * Slot: dimension_sizes Description: Comma-separated dimension sizes (e.g., "209,52,3,3")
--     * Slot: n_variables Description: Number of measured variables
--     * Slot: total_rows Description: Total number of data rows in brick table
--     * Slot: associated_entity_type Description: Type of entities measured (e.g., "Sample", "Community")
--     * Slot: measurement_type_sys_oterm_id Description: Type of measurement ontology term ID
--     * Slot: measurement_type_sys_oterm_name Description: Type of measurement ontology term name
--     * Slot: creation_date Description: Date brick was created
--     * Slot: description Description: Free text description
-- # Abstract Class: BrickDimension Description: Abstract base for brick dimension metadata.Dimensions define the axes of N-dimensional measurement arrays:- Environmental Sample: Different samples measured- Molecule: Different molecules/compounds measured- State: Different conditions (e.g., time points, treatments)- Statistic: Different statistical measures (mean, std, etc.)Each dimension has:- Semantic meaning (ontology term)- Size (number of values along axis)- Index values (entity names or numeric indices)
--     * Slot: id
--     * Slot: dimension_number Description: Position in N-dimensional array (0-indexed)
--     * Slot: dimension_oterm_id Description: Dimension semantic ontology term ID
--     * Slot: dimension_oterm_name Description: Dimension semantic ontology term name
--     * Slot: dimension_size Description: Number of values along this dimension
--     * Slot: dimension_values Description: Comma-separated dimension value labels
-- # Abstract Class: BrickVariable Description: Abstract base for brick variable metadata.Variables define what is measured at each point in the N-dimensional array:- Concentration (with units: mg/L, µM, etc.)- Molecular Weight (with units: Da, kDa, etc.)- Activity Rate (with units: nmol/min, etc.)- Expression Level (with units: RPKM, TPM, etc.)Each variable has:- Semantic meaning (ontology term)- Data type (float, int, bool, oterm_ref, object_ref)- Units (ontology term)- Value range constraints
--     * Slot: id
--     * Slot: variable_number Description: Variable index in brick
--     * Slot: variable_oterm_id Description: Variable semantic ontology term ID
--     * Slot: variable_oterm_name Description: Variable semantic ontology term name
--     * Slot: variable_data_type Description: Data type of variable (float, int, bool, oterm_ref, object_ref)
--     * Slot: unit_sys_oterm_id Description: Measurement unit ontology term ID
--     * Slot: unit_sys_oterm_name Description: Measurement unit ontology term name
--     * Slot: min_value Description: Minimum allowed value (for numeric variables)
--     * Slot: max_value Description: Maximum allowed value (for numeric variables)
-- # Abstract Class: Brick Description: Abstract base for all brick data tables (ddt_brick*).Each brick table stores measurement values in a denormalized formatwhere each row represents one cell in the N-dimensional array.Common structure:- Dimension indices (dim0_index, dim1_index, dim2_index, ...)- Dimension values (dim0_value, dim1_value, dim2_value, ...)- Variable values (var0_value, var1_value, var2_value, ...)Schema is defined in sys_ddt_typedef and varies per brick.Note: Individual brick classes (Brick0000001, Brick0000002, etc.)are not explicitly defined in this schema because they haveheterogeneous structures. They should be validated againstsys_ddt_typedef at runtime.
--     * Slot: id
-- # Class: Community_defined_strains_ref
--     * Slot: Community_sdt_community_id Description: Autocreated FK slot
--     * Slot: defined_strains_ref Description: References to defined strain names (multivalued FK to Strain.sdt_strain_name)
-- # Class: Strain_gene_names_changed
--     * Slot: Strain_sdt_strain_id Description: Autocreated FK slot
--     * Slot: gene_names_changed Description: Names of genes that were changed
-- # Class: SystemProcess_input_objects
--     * Slot: SystemProcess_sys_process_id Description: Autocreated FK slot
--     * Slot: input_objects Description: Array of input entity references (type:name format)
-- # Class: SystemProcess_output_objects
--     * Slot: SystemProcess_sys_process_id Description: Autocreated FK slot
--     * Slot: output_objects Description: Array of output entity references (type:name format)
-- # Class: DynamicDataArray_associated_entity_names
--     * Slot: DynamicDataArray_ddt_ndarray_id Description: Autocreated FK slot
--     * Slot: associated_entity_names Description: Names of entities associated with this brick

CREATE TABLE "OntologyTermPair" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);CREATE INDEX "ix_OntologyTermPair_id" ON "OntologyTermPair" (id);
CREATE TABLE "CDMEntity" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);CREATE INDEX "ix_CDMEntity_id" ON "CDMEntity" (id);
CREATE TABLE "SystemEntity" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);CREATE INDEX "ix_SystemEntity_id" ON "SystemEntity" (id);
CREATE TABLE "Location" (
	sdt_location_id TEXT NOT NULL,
	sdt_location_name TEXT NOT NULL,
	latitude TEXT,
	longitude TEXT,
	continent_sys_oterm_id TEXT,
	continent_sys_oterm_name TEXT,
	country_sys_oterm_id TEXT,
	country_sys_oterm_name TEXT,
	region TEXT,
	biome_sys_oterm_id TEXT,
	biome_sys_oterm_name TEXT,
	feature_sys_oterm_id TEXT,
	feature_sys_oterm_name TEXT,
	PRIMARY KEY (sdt_location_id)
);CREATE INDEX "ix_Location_sdt_location_id" ON "Location" (sdt_location_id);
CREATE TABLE "Sample" (
	sdt_sample_id TEXT NOT NULL,
	sdt_sample_name TEXT NOT NULL,
	location_ref TEXT,
	depth TEXT,
	elevation TEXT,
	date TEXT,
	time TEXT,
	timezone TEXT,
	material_sys_oterm_id TEXT,
	material_sys_oterm_name TEXT,
	env_package_sys_oterm_id TEXT,
	env_package_sys_oterm_name TEXT,
	description TEXT,
	PRIMARY KEY (sdt_sample_id)
);CREATE INDEX "ix_Sample_sdt_sample_id" ON "Sample" (sdt_sample_id);
CREATE TABLE "Community" (
	sdt_community_id TEXT NOT NULL,
	sdt_community_name TEXT NOT NULL,
	community_type_sys_oterm_id TEXT,
	community_type_sys_oterm_name TEXT,
	sample_ref TEXT,
	parent_community_ref TEXT,
	PRIMARY KEY (sdt_community_id)
);CREATE INDEX "ix_Community_sdt_community_id" ON "Community" (sdt_community_id);
CREATE TABLE "Reads" (
	sdt_reads_id TEXT NOT NULL,
	sdt_reads_name TEXT NOT NULL,
	read_count TEXT,
	base_count TEXT,
	read_type_sys_oterm_id TEXT,
	read_type_sys_oterm_name TEXT,
	sequencing_technology_sys_oterm_id TEXT,
	sequencing_technology_sys_oterm_name TEXT,
	link TEXT,
	PRIMARY KEY (sdt_reads_id)
);CREATE INDEX "ix_Reads_sdt_reads_id" ON "Reads" (sdt_reads_id);
CREATE TABLE "Assembly" (
	sdt_assembly_id TEXT NOT NULL,
	sdt_assembly_name TEXT NOT NULL,
	strain_ref TEXT,
	n_contigs TEXT,
	total_size TEXT,
	link TEXT,
	PRIMARY KEY (sdt_assembly_id)
);CREATE INDEX "ix_Assembly_sdt_assembly_id" ON "Assembly" (sdt_assembly_id);
CREATE TABLE "Bin" (
	sdt_bin_id TEXT NOT NULL,
	sdt_bin_name TEXT NOT NULL,
	assembly_ref TEXT,
	contigs TEXT,
	PRIMARY KEY (sdt_bin_id)
);CREATE INDEX "ix_Bin_sdt_bin_id" ON "Bin" (sdt_bin_id);
CREATE TABLE "Genome" (
	sdt_genome_id TEXT NOT NULL,
	sdt_genome_name TEXT NOT NULL,
	strain_ref TEXT,
	n_contigs TEXT,
	n_features TEXT,
	total_size TEXT,
	link TEXT,
	PRIMARY KEY (sdt_genome_id)
);CREATE INDEX "ix_Genome_sdt_genome_id" ON "Genome" (sdt_genome_id);
CREATE TABLE "Gene" (
	sdt_gene_id TEXT NOT NULL,
	sdt_gene_name TEXT NOT NULL,
	genome_ref TEXT,
	contig_number INTEGER,
	strand TEXT,
	start INTEGER,
	stop INTEGER,
	function TEXT,
	PRIMARY KEY (sdt_gene_id)
);CREATE INDEX "ix_Gene_sdt_gene_id" ON "Gene" (sdt_gene_id);
CREATE TABLE "Strain" (
	sdt_strain_id TEXT NOT NULL,
	sdt_strain_name TEXT NOT NULL,
	genome_ref TEXT,
	derived_from_strain_ref TEXT,
	PRIMARY KEY (sdt_strain_id)
);CREATE INDEX "ix_Strain_sdt_strain_id" ON "Strain" (sdt_strain_id);
CREATE TABLE "Taxon" (
	sdt_taxon_id TEXT NOT NULL,
	sdt_taxon_name TEXT NOT NULL,
	ncbi_taxid INTEGER,
	PRIMARY KEY (sdt_taxon_id)
);CREATE INDEX "ix_Taxon_sdt_taxon_id" ON "Taxon" (sdt_taxon_id);
CREATE TABLE "ASV" (
	sdt_asv_id TEXT NOT NULL,
	sdt_asv_name TEXT NOT NULL,
	sequence TEXT,
	PRIMARY KEY (sdt_asv_id)
);CREATE INDEX "ix_ASV_sdt_asv_id" ON "ASV" (sdt_asv_id);
CREATE TABLE "Protocol" (
	sdt_protocol_id TEXT NOT NULL,
	sdt_protocol_name TEXT NOT NULL,
	description TEXT,
	link TEXT,
	PRIMARY KEY (sdt_protocol_id)
);CREATE INDEX "ix_Protocol_sdt_protocol_id" ON "Protocol" (sdt_protocol_id);
CREATE TABLE "Image" (
	sdt_image_id TEXT NOT NULL,
	sdt_image_name TEXT NOT NULL,
	mime_type TEXT,
	size TEXT,
	dimensions TEXT,
	link TEXT,
	PRIMARY KEY (sdt_image_id)
);CREATE INDEX "ix_Image_sdt_image_id" ON "Image" (sdt_image_id);
CREATE TABLE "Condition" (
	sdt_condition_id TEXT NOT NULL,
	sdt_condition_name TEXT NOT NULL,
	PRIMARY KEY (sdt_condition_id)
);CREATE INDEX "ix_Condition_sdt_condition_id" ON "Condition" (sdt_condition_id);
CREATE TABLE "DubSeqLibrary" (
	sdt_dubseq_library_id TEXT NOT NULL,
	sdt_dubseq_library_name TEXT NOT NULL,
	genome_ref TEXT,
	n_fragments TEXT,
	PRIMARY KEY (sdt_dubseq_library_id)
);CREATE INDEX "ix_DubSeqLibrary_sdt_dubseq_library_id" ON "DubSeqLibrary" (sdt_dubseq_library_id);
CREATE TABLE "TnSeqLibrary" (
	sdt_tnseq_library_id TEXT NOT NULL,
	sdt_tnseq_library_name TEXT NOT NULL,
	genome_ref TEXT,
	primers_model TEXT,
	n_mapped_reads TEXT,
	n_good_reads TEXT,
	n_genes_hit TEXT,
	PRIMARY KEY (sdt_tnseq_library_id)
);CREATE INDEX "ix_TnSeqLibrary_sdt_tnseq_library_id" ON "TnSeqLibrary" (sdt_tnseq_library_id);
CREATE TABLE "ENIGMA" (
	sdt_enigma_id TEXT NOT NULL,
	PRIMARY KEY (sdt_enigma_id)
);CREATE INDEX "ix_ENIGMA_sdt_enigma_id" ON "ENIGMA" (sdt_enigma_id);
CREATE TABLE "SystemTypedef" (
	id INTEGER NOT NULL,
	type_name TEXT NOT NULL,
	field_name TEXT NOT NULL,
	cdm_column_name TEXT NOT NULL,
	scalar_type TEXT,
	pk BOOLEAN,
	upk BOOLEAN,
	fk TEXT,
	"constraint" TEXT,
	units_sys_oterm_id TEXT,
	type_sys_oterm_id TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_SystemTypedef_id" ON "SystemTypedef" (id);
CREATE TABLE "SystemDDTTypedef" (
	id INTEGER NOT NULL,
	ddt_ndarray_id TEXT NOT NULL,
	cdm_column_name TEXT NOT NULL,
	cdm_column_data_type TEXT,
	scalar_type TEXT,
	dimension_number INTEGER,
	variable_number INTEGER,
	dimension_oterm_id TEXT,
	dimension_oterm_name TEXT,
	variable_oterm_id TEXT,
	variable_oterm_name TEXT,
	unit_sys_oterm_id TEXT,
	unit_sys_oterm_name TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_SystemDDTTypedef_id" ON "SystemDDTTypedef" (id);
CREATE TABLE "SystemOntologyTerm" (
	sys_oterm_id TEXT NOT NULL,
	sys_oterm_name TEXT,
	sys_oterm_ontology TEXT,
	parent_sys_oterm_id TEXT,
	sys_oterm_definition TEXT,
	sys_oterm_synonyms TEXT,
	sys_oterm_links TEXT,
	sys_oterm_properties TEXT,
	PRIMARY KEY (sys_oterm_id)
);CREATE INDEX "ix_SystemOntologyTerm_sys_oterm_id" ON "SystemOntologyTerm" (sys_oterm_id);
CREATE TABLE "SystemProcess" (
	sys_process_id TEXT NOT NULL,
	process_type_sys_oterm_id TEXT,
	process_type_sys_oterm_name TEXT,
	person_sys_oterm_id TEXT,
	person_sys_oterm_name TEXT,
	campaign_sys_oterm_id TEXT,
	campaign_sys_oterm_name TEXT,
	sdt_protocol_name TEXT NOT NULL,
	date_start TEXT,
	date_end TEXT,
	PRIMARY KEY (sys_process_id)
);CREATE INDEX "ix_SystemProcess_sys_process_id" ON "SystemProcess" (sys_process_id);
CREATE TABLE "SystemProcessInput" (
	id INTEGER NOT NULL,
	sys_process_id TEXT NOT NULL,
	input_object_type TEXT,
	input_object_name TEXT,
	input_index INTEGER,
	PRIMARY KEY (id)
);CREATE INDEX "ix_SystemProcessInput_id" ON "SystemProcessInput" (id);
CREATE TABLE "SystemProcessOutput" (
	id INTEGER NOT NULL,
	sys_process_id TEXT NOT NULL,
	output_object_type TEXT,
	output_object_name TEXT,
	output_index INTEGER,
	PRIMARY KEY (id)
);CREATE INDEX "ix_SystemProcessOutput_id" ON "SystemProcessOutput" (id);
CREATE TABLE "DynamicDataArray" (
	ddt_ndarray_id TEXT NOT NULL,
	brick_table_name TEXT,
	n_dimensions INTEGER,
	dimension_sizes TEXT,
	n_variables INTEGER,
	total_rows INTEGER,
	associated_entity_type TEXT,
	measurement_type_sys_oterm_id TEXT,
	measurement_type_sys_oterm_name TEXT,
	creation_date TEXT,
	description TEXT,
	PRIMARY KEY (ddt_ndarray_id)
);CREATE INDEX "ix_DynamicDataArray_ddt_ndarray_id" ON "DynamicDataArray" (ddt_ndarray_id);
CREATE TABLE "BrickDimension" (
	id INTEGER NOT NULL,
	dimension_number INTEGER,
	dimension_oterm_id TEXT,
	dimension_oterm_name TEXT,
	dimension_size INTEGER,
	dimension_values TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_BrickDimension_id" ON "BrickDimension" (id);
CREATE TABLE "BrickVariable" (
	id INTEGER NOT NULL,
	variable_number INTEGER,
	variable_oterm_id TEXT,
	variable_oterm_name TEXT,
	variable_data_type TEXT,
	unit_sys_oterm_id TEXT,
	unit_sys_oterm_name TEXT,
	min_value FLOAT,
	max_value FLOAT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_BrickVariable_id" ON "BrickVariable" (id);
CREATE TABLE "Brick" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Brick_id" ON "Brick" (id);
CREATE TABLE "Community_defined_strains_ref" (
	"Community_sdt_community_id" TEXT,
	defined_strains_ref TEXT,
	PRIMARY KEY ("Community_sdt_community_id", defined_strains_ref),
	FOREIGN KEY("Community_sdt_community_id") REFERENCES "Community" (sdt_community_id)
);CREATE INDEX "ix_Community_defined_strains_ref_Community_sdt_community_id" ON "Community_defined_strains_ref" ("Community_sdt_community_id");CREATE INDEX "ix_Community_defined_strains_ref_defined_strains_ref" ON "Community_defined_strains_ref" (defined_strains_ref);
CREATE TABLE "Strain_gene_names_changed" (
	"Strain_sdt_strain_id" TEXT,
	gene_names_changed TEXT,
	PRIMARY KEY ("Strain_sdt_strain_id", gene_names_changed),
	FOREIGN KEY("Strain_sdt_strain_id") REFERENCES "Strain" (sdt_strain_id)
);CREATE INDEX "ix_Strain_gene_names_changed_gene_names_changed" ON "Strain_gene_names_changed" (gene_names_changed);CREATE INDEX "ix_Strain_gene_names_changed_Strain_sdt_strain_id" ON "Strain_gene_names_changed" ("Strain_sdt_strain_id");
CREATE TABLE "SystemProcess_input_objects" (
	"SystemProcess_sys_process_id" TEXT,
	input_objects TEXT,
	PRIMARY KEY ("SystemProcess_sys_process_id", input_objects),
	FOREIGN KEY("SystemProcess_sys_process_id") REFERENCES "SystemProcess" (sys_process_id)
);CREATE INDEX "ix_SystemProcess_input_objects_input_objects" ON "SystemProcess_input_objects" (input_objects);CREATE INDEX "ix_SystemProcess_input_objects_SystemProcess_sys_process_id" ON "SystemProcess_input_objects" ("SystemProcess_sys_process_id");
CREATE TABLE "SystemProcess_output_objects" (
	"SystemProcess_sys_process_id" TEXT,
	output_objects TEXT,
	PRIMARY KEY ("SystemProcess_sys_process_id", output_objects),
	FOREIGN KEY("SystemProcess_sys_process_id") REFERENCES "SystemProcess" (sys_process_id)
);CREATE INDEX "ix_SystemProcess_output_objects_output_objects" ON "SystemProcess_output_objects" (output_objects);CREATE INDEX "ix_SystemProcess_output_objects_SystemProcess_sys_process_id" ON "SystemProcess_output_objects" ("SystemProcess_sys_process_id");
CREATE TABLE "DynamicDataArray_associated_entity_names" (
	"DynamicDataArray_ddt_ndarray_id" TEXT,
	associated_entity_names TEXT,
	PRIMARY KEY ("DynamicDataArray_ddt_ndarray_id", associated_entity_names),
	FOREIGN KEY("DynamicDataArray_ddt_ndarray_id") REFERENCES "DynamicDataArray" (ddt_ndarray_id)
);CREATE INDEX "ix_DynamicDataArray_associated_entity_names_associated_entity_names" ON "DynamicDataArray_associated_entity_names" (associated_entity_names);CREATE INDEX "ix_DynamicDataArray_associated_entity_names_DynamicDataArray_ddt_ndarray_id" ON "DynamicDataArray_associated_entity_names" ("DynamicDataArray_ddt_ndarray_id");
