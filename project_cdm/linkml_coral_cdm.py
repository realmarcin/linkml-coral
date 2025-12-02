# Auto generated from linkml_coral_cdm.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-12-01T21:40:09
# Schema: kbase-cdm
#
# id: https://w3id.org/enigma/kbase-cdm
# description: LinkML schema for KBase Common Data Model (CDM) representing ENIGMA CORAL data.
#
#   This schema is derived from the original CORAL LinkML schema but includes
#   transformations specific to the KBase CDM implementation:
#
#   **Key CDM Patterns:**
#
#   1. **Ontology Term Splitting**
#      - CORAL: Single field with ontology constraint
#      - CDM: Two fields (ID + name) for each ontology term
#      - Example: `material` → `material_sys_oterm_id` + `material_sys_oterm_name`
#      - Enables FK validation + human-readable labels without joins
#
#   2. **CDM Naming Conventions**
#      - Tables: `sdt_*` (static), `ddt_*` (dynamic), `sys_*` (system)
#      - IDs: `sdt_{entity}_id` with pattern `EntityName\d{7}`
#      - Names: `sdt_{entity}_name` (unique, used for FK references)
#      - All columns: snake_case with entity prefix
#
#   3. **Centralized Ontology Catalog**
#      - All ontology terms stored in `sys_oterm` table
#      - 10,594 terms from multiple ontologies (ME, ENVO, UO, etc.)
#      - Hierarchical relationships via `parent_sys_oterm_id`
#      - Single source of truth for semantic metadata
#
#   4. **Denormalized Provenance Model**
#      - Process workflows stored in `sys_process` table
#      - Input/output relationships in `sys_process_input`, `sys_process_output`
#      - Complete lineage tracing from samples to analyses
#      - 142,958 process records documenting all transformations
#
#   5. **Dynamic Data Bricks**
#      - N-dimensional measurement arrays in `ddt_brick*` tables
#      - Flexible schema defined in `sys_ddt_typedef`
#      - Semantic dimensions and variables via ontology terms
#      - 82.6M rows across 20 brick tables
#
#   **Schema Organization:**
#
#   This schema is modular, organized into:
#   - `cdm_base.yaml`: Common types, mixins, validation patterns
#   - `cdm_static_entities.yaml`: 17 sdt_* entity classes
#   - `cdm_system_tables.yaml`: 6 sys_* system classes
#   - `cdm_dynamic_data.yaml`: Brick infrastructure (ddt_*)
#   - `linkml_coral_cdm.yaml`: Main schema (this file)
#
#   **Data Volume:**
#   - 272,934 rows across 17 static entity tables
#   - 142,958 process records (provenance)
#   - 10,594 ontology terms
#   - 82.6M rows in dynamic data tables
#
#   **Comparison to Original CORAL:**
#   - Maintains same 17 core entity types
#   - Adds 6 new system table classes
#   - Preserves provenance annotations
#   - Extends with CDM-specific patterns
#
#   **Documentation:**
#   - Analysis Report: `docs/cdm_analysis/CDM_PARQUET_ANALYSIS_REPORT.md`
#   - Schema Comparison: `docs/CORAL_TO_CDM_MAPPING.md`
#   - Validation Guide: `docs/CDM_VALIDATION_GUIDE.md`
#
# license: MIT

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Float, Integer, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = "1.0.0"

# Namespaces
CONTINENT = CurieNamespace('CONTINENT', 'http://purl.obolibrary.org/obo/CONTINENT_')
COUNTRY = CurieNamespace('COUNTRY', 'http://purl.obolibrary.org/obo/COUNTRY_')
DA = CurieNamespace('DA', 'http://purl.obolibrary.org/obo/DA_')
ENIGMA_TERM = CurieNamespace('ENIGMA_TERM', 'http://purl.obolibrary.org/obo/ENIGMA_')
ENVO = CurieNamespace('ENVO', 'http://purl.obolibrary.org/obo/ENVO_')
ME = CurieNamespace('ME', 'http://purl.obolibrary.org/obo/ME_')
MIXS = CurieNamespace('MIxS', 'http://purl.obolibrary.org/obo/MIxS_')
PROCESS = CurieNamespace('PROCESS', 'http://purl.obolibrary.org/obo/PROCESS_')
UO = CurieNamespace('UO', 'http://purl.obolibrary.org/obo/UO_')
ENIGMA = CurieNamespace('enigma', 'https://w3id.org/enigma/')
KBASE_CDM = CurieNamespace('kbase_cdm', 'https://w3id.org/enigma/kbase-cdm/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = KBASE_CDM


# Types
class Date(String):
    """ ISO 8601 date format (YYYY-MM-DD) """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "Date"
    type_model_uri = KBASE_CDM.Date


class Time(String):
    """ Time in HH:MM or HH:MM:SS format """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "Time"
    type_model_uri = KBASE_CDM.Time


class Link(String):
    """ HTTP/HTTPS URL or file path """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "Link"
    type_model_uri = KBASE_CDM.Link


class Latitude(Float):
    """ Latitude in decimal degrees """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Latitude"
    type_model_uri = KBASE_CDM.Latitude


class Longitude(Float):
    """ Longitude in decimal degrees """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Longitude"
    type_model_uri = KBASE_CDM.Longitude


class Count(Integer):
    """ Non-negative integer count """
    type_class_uri = XSD["integer"]
    type_class_curie = "xsd:integer"
    type_name = "Count"
    type_model_uri = KBASE_CDM.Count


class Size(Integer):
    """ Size in bytes """
    type_class_uri = XSD["integer"]
    type_class_curie = "xsd:integer"
    type_name = "Size"
    type_model_uri = KBASE_CDM.Size


class Rate(Float):
    """ Rate or frequency measurement """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Rate"
    type_model_uri = KBASE_CDM.Rate


class Depth(Float):
    """ Depth measurement (meters) """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Depth"
    type_model_uri = KBASE_CDM.Depth


class Elevation(Float):
    """ Elevation measurement (meters) """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Elevation"
    type_model_uri = KBASE_CDM.Elevation


class OntologyTermID(String):
    """ CURIE format ontology term identifier (e.g., ME:0000129, ENVO:00002041) """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "OntologyTermID"
    type_model_uri = KBASE_CDM.OntologyTermID


class EntityName(String):
    """ Human-readable entity name """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "EntityName"
    type_model_uri = KBASE_CDM.EntityName


# Class references
class LocationSdtLocationId(extended_str):
    pass


class SampleSdtSampleId(extended_str):
    pass


class CommunitySdtCommunityId(extended_str):
    pass


class ReadsSdtReadsId(extended_str):
    pass


class AssemblySdtAssemblyId(extended_str):
    pass


class BinSdtBinId(extended_str):
    pass


class GenomeSdtGenomeId(extended_str):
    pass


class GeneSdtGeneId(extended_str):
    pass


class StrainSdtStrainId(extended_str):
    pass


class TaxonSdtTaxonId(extended_str):
    pass


class ASVSdtAsvId(extended_str):
    pass


class ProtocolSdtProtocolId(extended_str):
    pass


class ImageSdtImageId(extended_str):
    pass


class ConditionSdtConditionId(extended_str):
    pass


class DubSeqLibrarySdtDubseqLibraryId(extended_str):
    pass


class TnSeqLibrarySdtTnseqLibraryId(extended_str):
    pass


class ENIGMASdtEnigmaId(extended_str):
    pass


class SystemOntologyTermSysOtermId(OntologyTermID):
    pass


class SystemProcessSysProcessId(extended_str):
    pass


class DynamicDataArrayDdtNdarrayId(extended_str):
    pass


class OntologyTermPair(YAMLRoot):
    """
    Mixin for ontology-constrained fields in KBase CDM.

    The CDM splits each ontology-controlled field into two columns:
    - {field}_sys_oterm_id: CURIE identifier (FK to sys_oterm)
    - {field}_sys_oterm_name: Human-readable term name

    This pattern enables:
    - Ontology validation via FK constraint
    - Human-readable labels without joins
    - Ontology evolution without data migration

    Examples:
    - material → material_sys_oterm_id + material_sys_oterm_name
    - biome → biome_sys_oterm_id + biome_sys_oterm_name
    - read_type → read_type_sys_oterm_id + read_type_sys_oterm_name
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["OntologyTermPair"]
    class_class_curie: ClassVar[str] = "kbase_cdm:OntologyTermPair"
    class_name: ClassVar[str] = "OntologyTermPair"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.OntologyTermPair


class CDMEntity(YAMLRoot):
    """
    Base mixin for all CDM static data tables (sdt_*).

    Enforces CDM naming conventions:
    - Primary key: sdt_{entity}_id with pattern EntityName\d{7}
    - Name field: sdt_{entity}_name (unique, used for FK references)
    - All columns use snake_case with entity prefix

    Example:
    - Location: sdt_location_id, sdt_location_name
    - Sample: sdt_sample_id, sdt_sample_name

    Note: Each entity class must define its own id and name slots
    with entity-specific names (e.g., sdt_location_id, sdt_location_name).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["CDMEntity"]
    class_class_curie: ClassVar[str] = "kbase_cdm:CDMEntity"
    class_name: ClassVar[str] = "CDMEntity"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.CDMEntity


class SystemEntity(YAMLRoot):
    """
    Base mixin for CDM system tables (sys_*).

    System tables provide metadata, type definitions, provenance tracking,
    and ontology catalogs. They support the static and dynamic data tables
    but are not directly linked to experimental entities.

    System tables: sys_typedef, sys_ddt_typedef, sys_oterm, sys_process,
    sys_process_input, sys_process_output
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["SystemEntity"]
    class_class_curie: ClassVar[str] = "kbase_cdm:SystemEntity"
    class_name: ClassVar[str] = "SystemEntity"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.SystemEntity


@dataclass(repr=False)
class Location(YAMLRoot):
    """
    Sampling location with geographic coordinates and environmental context.

    CDM changes from CORAL:
    - 4 ontology term fields split into ID+name pairs:
    continent, country, biome, feature
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Location"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Location"
    class_name: ClassVar[str] = "Location"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Location

    sdt_location_id: Union[str, LocationSdtLocationId] = None
    sdt_location_name: Union[str, EntityName] = None
    latitude: Optional[Union[float, Latitude]] = None
    longitude: Optional[Union[float, Longitude]] = None
    continent_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    continent_sys_oterm_name: Optional[str] = None
    country_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    country_sys_oterm_name: Optional[str] = None
    region: Optional[str] = None
    biome_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    biome_sys_oterm_name: Optional[str] = None
    feature_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    feature_sys_oterm_name: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_location_id):
            self.MissingRequiredField("sdt_location_id")
        if not isinstance(self.sdt_location_id, LocationSdtLocationId):
            self.sdt_location_id = LocationSdtLocationId(self.sdt_location_id)

        if self._is_empty(self.sdt_location_name):
            self.MissingRequiredField("sdt_location_name")
        if not isinstance(self.sdt_location_name, EntityName):
            self.sdt_location_name = EntityName(self.sdt_location_name)

        if self.latitude is not None and not isinstance(self.latitude, Latitude):
            self.latitude = Latitude(self.latitude)

        if self.longitude is not None and not isinstance(self.longitude, Longitude):
            self.longitude = Longitude(self.longitude)

        if self.continent_sys_oterm_id is not None and not isinstance(self.continent_sys_oterm_id, OntologyTermID):
            self.continent_sys_oterm_id = OntologyTermID(self.continent_sys_oterm_id)

        if self.continent_sys_oterm_name is not None and not isinstance(self.continent_sys_oterm_name, str):
            self.continent_sys_oterm_name = str(self.continent_sys_oterm_name)

        if self.country_sys_oterm_id is not None and not isinstance(self.country_sys_oterm_id, OntologyTermID):
            self.country_sys_oterm_id = OntologyTermID(self.country_sys_oterm_id)

        if self.country_sys_oterm_name is not None and not isinstance(self.country_sys_oterm_name, str):
            self.country_sys_oterm_name = str(self.country_sys_oterm_name)

        if self.region is not None and not isinstance(self.region, str):
            self.region = str(self.region)

        if self.biome_sys_oterm_id is not None and not isinstance(self.biome_sys_oterm_id, OntologyTermID):
            self.biome_sys_oterm_id = OntologyTermID(self.biome_sys_oterm_id)

        if self.biome_sys_oterm_name is not None and not isinstance(self.biome_sys_oterm_name, str):
            self.biome_sys_oterm_name = str(self.biome_sys_oterm_name)

        if self.feature_sys_oterm_id is not None and not isinstance(self.feature_sys_oterm_id, OntologyTermID):
            self.feature_sys_oterm_id = OntologyTermID(self.feature_sys_oterm_id)

        if self.feature_sys_oterm_name is not None and not isinstance(self.feature_sys_oterm_name, str):
            self.feature_sys_oterm_name = str(self.feature_sys_oterm_name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Sample(YAMLRoot):
    """
    Environmental sample collected from a location.

    CDM changes from CORAL:
    - 2 ontology term fields split: material, env_package
    - FK reference: location → location_ref
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Sample"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Sample"
    class_name: ClassVar[str] = "Sample"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Sample

    sdt_sample_id: Union[str, SampleSdtSampleId] = None
    sdt_sample_name: Union[str, EntityName] = None
    location_ref: Optional[Union[str, EntityName]] = None
    depth: Optional[Union[float, Depth]] = None
    elevation: Optional[Union[float, Elevation]] = None
    date: Optional[Union[str, Date]] = None
    time: Optional[Union[str, Time]] = None
    timezone: Optional[str] = None
    material_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    material_sys_oterm_name: Optional[str] = None
    env_package_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    env_package_sys_oterm_name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_sample_id):
            self.MissingRequiredField("sdt_sample_id")
        if not isinstance(self.sdt_sample_id, SampleSdtSampleId):
            self.sdt_sample_id = SampleSdtSampleId(self.sdt_sample_id)

        if self._is_empty(self.sdt_sample_name):
            self.MissingRequiredField("sdt_sample_name")
        if not isinstance(self.sdt_sample_name, EntityName):
            self.sdt_sample_name = EntityName(self.sdt_sample_name)

        if self.location_ref is not None and not isinstance(self.location_ref, EntityName):
            self.location_ref = EntityName(self.location_ref)

        if self.depth is not None and not isinstance(self.depth, Depth):
            self.depth = Depth(self.depth)

        if self.elevation is not None and not isinstance(self.elevation, Elevation):
            self.elevation = Elevation(self.elevation)

        if self.date is not None and not isinstance(self.date, Date):
            self.date = Date(self.date)

        if self.time is not None and not isinstance(self.time, Time):
            self.time = Time(self.time)

        if self.timezone is not None and not isinstance(self.timezone, str):
            self.timezone = str(self.timezone)

        if self.material_sys_oterm_id is not None and not isinstance(self.material_sys_oterm_id, OntologyTermID):
            self.material_sys_oterm_id = OntologyTermID(self.material_sys_oterm_id)

        if self.material_sys_oterm_name is not None and not isinstance(self.material_sys_oterm_name, str):
            self.material_sys_oterm_name = str(self.material_sys_oterm_name)

        if self.env_package_sys_oterm_id is not None and not isinstance(self.env_package_sys_oterm_id, OntologyTermID):
            self.env_package_sys_oterm_id = OntologyTermID(self.env_package_sys_oterm_id)

        if self.env_package_sys_oterm_name is not None and not isinstance(self.env_package_sys_oterm_name, str):
            self.env_package_sys_oterm_name = str(self.env_package_sys_oterm_name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Community(YAMLRoot):
    """
    Microbial community (isolate, enrichment, assemblage, or environmental).

    CDM changes from CORAL:
    - 1 ontology term field split: community_type
    - FK references: sample → sample_ref, parent_community → parent_community_ref
    - Multivalued FK: defined_strains → defined_strains_ref
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Community"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Community"
    class_name: ClassVar[str] = "Community"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Community

    sdt_community_id: Union[str, CommunitySdtCommunityId] = None
    sdt_community_name: Union[str, EntityName] = None
    community_type_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    community_type_sys_oterm_name: Optional[str] = None
    sample_ref: Optional[Union[str, EntityName]] = None
    parent_community_ref: Optional[Union[str, EntityName]] = None
    defined_strains_ref: Optional[Union[Union[str, EntityName], list[Union[str, EntityName]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_community_id):
            self.MissingRequiredField("sdt_community_id")
        if not isinstance(self.sdt_community_id, CommunitySdtCommunityId):
            self.sdt_community_id = CommunitySdtCommunityId(self.sdt_community_id)

        if self._is_empty(self.sdt_community_name):
            self.MissingRequiredField("sdt_community_name")
        if not isinstance(self.sdt_community_name, EntityName):
            self.sdt_community_name = EntityName(self.sdt_community_name)

        if self.community_type_sys_oterm_id is not None and not isinstance(self.community_type_sys_oterm_id, OntologyTermID):
            self.community_type_sys_oterm_id = OntologyTermID(self.community_type_sys_oterm_id)

        if self.community_type_sys_oterm_name is not None and not isinstance(self.community_type_sys_oterm_name, str):
            self.community_type_sys_oterm_name = str(self.community_type_sys_oterm_name)

        if self.sample_ref is not None and not isinstance(self.sample_ref, EntityName):
            self.sample_ref = EntityName(self.sample_ref)

        if self.parent_community_ref is not None and not isinstance(self.parent_community_ref, EntityName):
            self.parent_community_ref = EntityName(self.parent_community_ref)

        if not isinstance(self.defined_strains_ref, list):
            self.defined_strains_ref = [self.defined_strains_ref] if self.defined_strains_ref is not None else []
        self.defined_strains_ref = [v if isinstance(v, EntityName) else EntityName(v) for v in self.defined_strains_ref]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Reads(YAMLRoot):
    """
    Sequencing reads dataset.

    CDM changes from CORAL:
    - 2 ontology term fields split: read_type, sequencing_technology
    - Added 'link' field for external data references
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Reads"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Reads"
    class_name: ClassVar[str] = "Reads"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Reads

    sdt_reads_id: Union[str, ReadsSdtReadsId] = None
    sdt_reads_name: Union[str, EntityName] = None
    read_count: Optional[Union[int, Count]] = None
    base_count: Optional[Union[int, Count]] = None
    read_type_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    read_type_sys_oterm_name: Optional[str] = None
    sequencing_technology_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    sequencing_technology_sys_oterm_name: Optional[str] = None
    link: Optional[Union[str, Link]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_reads_id):
            self.MissingRequiredField("sdt_reads_id")
        if not isinstance(self.sdt_reads_id, ReadsSdtReadsId):
            self.sdt_reads_id = ReadsSdtReadsId(self.sdt_reads_id)

        if self._is_empty(self.sdt_reads_name):
            self.MissingRequiredField("sdt_reads_name")
        if not isinstance(self.sdt_reads_name, EntityName):
            self.sdt_reads_name = EntityName(self.sdt_reads_name)

        if self.read_count is not None and not isinstance(self.read_count, Count):
            self.read_count = Count(self.read_count)

        if self.base_count is not None and not isinstance(self.base_count, Count):
            self.base_count = Count(self.base_count)

        if self.read_type_sys_oterm_id is not None and not isinstance(self.read_type_sys_oterm_id, OntologyTermID):
            self.read_type_sys_oterm_id = OntologyTermID(self.read_type_sys_oterm_id)

        if self.read_type_sys_oterm_name is not None and not isinstance(self.read_type_sys_oterm_name, str):
            self.read_type_sys_oterm_name = str(self.read_type_sys_oterm_name)

        if self.sequencing_technology_sys_oterm_id is not None and not isinstance(self.sequencing_technology_sys_oterm_id, OntologyTermID):
            self.sequencing_technology_sys_oterm_id = OntologyTermID(self.sequencing_technology_sys_oterm_id)

        if self.sequencing_technology_sys_oterm_name is not None and not isinstance(self.sequencing_technology_sys_oterm_name, str):
            self.sequencing_technology_sys_oterm_name = str(self.sequencing_technology_sys_oterm_name)

        if self.link is not None and not isinstance(self.link, Link):
            self.link = Link(self.link)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Assembly(YAMLRoot):
    """
    Genome assembly from sequencing reads.

    CDM changes from CORAL:
    - FK reference: strain → strain_ref
    - Added 'link' field
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Assembly"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Assembly"
    class_name: ClassVar[str] = "Assembly"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Assembly

    sdt_assembly_id: Union[str, AssemblySdtAssemblyId] = None
    sdt_assembly_name: Union[str, EntityName] = None
    strain_ref: Optional[Union[str, EntityName]] = None
    n_contigs: Optional[Union[int, Count]] = None
    total_size: Optional[Union[int, Size]] = None
    link: Optional[Union[str, Link]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_assembly_id):
            self.MissingRequiredField("sdt_assembly_id")
        if not isinstance(self.sdt_assembly_id, AssemblySdtAssemblyId):
            self.sdt_assembly_id = AssemblySdtAssemblyId(self.sdt_assembly_id)

        if self._is_empty(self.sdt_assembly_name):
            self.MissingRequiredField("sdt_assembly_name")
        if not isinstance(self.sdt_assembly_name, EntityName):
            self.sdt_assembly_name = EntityName(self.sdt_assembly_name)

        if self.strain_ref is not None and not isinstance(self.strain_ref, EntityName):
            self.strain_ref = EntityName(self.strain_ref)

        if self.n_contigs is not None and not isinstance(self.n_contigs, Count):
            self.n_contigs = Count(self.n_contigs)

        if self.total_size is not None and not isinstance(self.total_size, Size):
            self.total_size = Size(self.total_size)

        if self.link is not None and not isinstance(self.link, Link):
            self.link = Link(self.link)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Bin(YAMLRoot):
    """
    Genome bin extracted from metagenomic assembly.

    CDM changes from CORAL:
    - FK reference: assembly → assembly_ref
    - contigs field contains comma-separated contig names
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Bin"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Bin"
    class_name: ClassVar[str] = "Bin"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Bin

    sdt_bin_id: Union[str, BinSdtBinId] = None
    sdt_bin_name: Union[str, EntityName] = None
    assembly_ref: Optional[Union[str, EntityName]] = None
    contigs: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_bin_id):
            self.MissingRequiredField("sdt_bin_id")
        if not isinstance(self.sdt_bin_id, BinSdtBinId):
            self.sdt_bin_id = BinSdtBinId(self.sdt_bin_id)

        if self._is_empty(self.sdt_bin_name):
            self.MissingRequiredField("sdt_bin_name")
        if not isinstance(self.sdt_bin_name, EntityName):
            self.sdt_bin_name = EntityName(self.sdt_bin_name)

        if self.assembly_ref is not None and not isinstance(self.assembly_ref, EntityName):
            self.assembly_ref = EntityName(self.assembly_ref)

        if self.contigs is not None and not isinstance(self.contigs, str):
            self.contigs = str(self.contigs)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Genome(YAMLRoot):
    """
    Assembled and annotated genome.

    CDM changes from CORAL:
    - FK reference: strain → strain_ref
    - Added 'link' field
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Genome"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Genome"
    class_name: ClassVar[str] = "Genome"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Genome

    sdt_genome_id: Union[str, GenomeSdtGenomeId] = None
    sdt_genome_name: Union[str, EntityName] = None
    strain_ref: Optional[Union[str, EntityName]] = None
    n_contigs: Optional[Union[int, Count]] = None
    n_features: Optional[Union[int, Count]] = None
    total_size: Optional[Union[int, Size]] = None
    link: Optional[Union[str, Link]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_genome_id):
            self.MissingRequiredField("sdt_genome_id")
        if not isinstance(self.sdt_genome_id, GenomeSdtGenomeId):
            self.sdt_genome_id = GenomeSdtGenomeId(self.sdt_genome_id)

        if self._is_empty(self.sdt_genome_name):
            self.MissingRequiredField("sdt_genome_name")
        if not isinstance(self.sdt_genome_name, EntityName):
            self.sdt_genome_name = EntityName(self.sdt_genome_name)

        if self.strain_ref is not None and not isinstance(self.strain_ref, EntityName):
            self.strain_ref = EntityName(self.strain_ref)

        if self.n_contigs is not None and not isinstance(self.n_contigs, Count):
            self.n_contigs = Count(self.n_contigs)

        if self.n_features is not None and not isinstance(self.n_features, Count):
            self.n_features = Count(self.n_features)

        if self.total_size is not None and not isinstance(self.total_size, Size):
            self.total_size = Size(self.total_size)

        if self.link is not None and not isinstance(self.link, Link):
            self.link = Link(self.link)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Gene(YAMLRoot):
    """
    Annotated gene within a genome.

    CDM changes from CORAL:
    - FK reference: genome → genome_ref
    - Gene ID convention: GeneName{genome_name}_{contig}_{start}_{stop}
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Gene"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Gene"
    class_name: ClassVar[str] = "Gene"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Gene

    sdt_gene_id: Union[str, GeneSdtGeneId] = None
    sdt_gene_name: Union[str, EntityName] = None
    genome_ref: Optional[Union[str, EntityName]] = None
    contig_number: Optional[int] = None
    strand: Optional[str] = None
    start: Optional[int] = None
    stop: Optional[int] = None
    function: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_gene_id):
            self.MissingRequiredField("sdt_gene_id")
        if not isinstance(self.sdt_gene_id, GeneSdtGeneId):
            self.sdt_gene_id = GeneSdtGeneId(self.sdt_gene_id)

        if self._is_empty(self.sdt_gene_name):
            self.MissingRequiredField("sdt_gene_name")
        if not isinstance(self.sdt_gene_name, EntityName):
            self.sdt_gene_name = EntityName(self.sdt_gene_name)

        if self.genome_ref is not None and not isinstance(self.genome_ref, EntityName):
            self.genome_ref = EntityName(self.genome_ref)

        if self.contig_number is not None and not isinstance(self.contig_number, int):
            self.contig_number = int(self.contig_number)

        if self.strand is not None and not isinstance(self.strand, str):
            self.strand = str(self.strand)

        if self.start is not None and not isinstance(self.start, int):
            self.start = int(self.start)

        if self.stop is not None and not isinstance(self.stop, int):
            self.stop = int(self.stop)

        if self.function is not None and not isinstance(self.function, str):
            self.function = str(self.function)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Strain(YAMLRoot):
    """
    Microbial strain (isolated or derived).

    CDM changes from CORAL:
    - FK references: genome → genome_ref, derived_from → derived_from_strain_ref
    - Self-referential for strain derivation lineage
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Strain"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Strain"
    class_name: ClassVar[str] = "Strain"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Strain

    sdt_strain_id: Union[str, StrainSdtStrainId] = None
    sdt_strain_name: Union[str, EntityName] = None
    genome_ref: Optional[Union[str, EntityName]] = None
    derived_from_strain_ref: Optional[Union[str, EntityName]] = None
    gene_names_changed: Optional[Union[Union[str, EntityName], list[Union[str, EntityName]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_strain_id):
            self.MissingRequiredField("sdt_strain_id")
        if not isinstance(self.sdt_strain_id, StrainSdtStrainId):
            self.sdt_strain_id = StrainSdtStrainId(self.sdt_strain_id)

        if self._is_empty(self.sdt_strain_name):
            self.MissingRequiredField("sdt_strain_name")
        if not isinstance(self.sdt_strain_name, EntityName):
            self.sdt_strain_name = EntityName(self.sdt_strain_name)

        if self.genome_ref is not None and not isinstance(self.genome_ref, EntityName):
            self.genome_ref = EntityName(self.genome_ref)

        if self.derived_from_strain_ref is not None and not isinstance(self.derived_from_strain_ref, EntityName):
            self.derived_from_strain_ref = EntityName(self.derived_from_strain_ref)

        if not isinstance(self.gene_names_changed, list):
            self.gene_names_changed = [self.gene_names_changed] if self.gene_names_changed is not None else []
        self.gene_names_changed = [v if isinstance(v, EntityName) else EntityName(v) for v in self.gene_names_changed]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Taxon(YAMLRoot):
    """
    Taxonomic classification.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Taxon"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Taxon"
    class_name: ClassVar[str] = "Taxon"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Taxon

    sdt_taxon_id: Union[str, TaxonSdtTaxonId] = None
    sdt_taxon_name: Union[str, EntityName] = None
    ncbi_taxid: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_taxon_id):
            self.MissingRequiredField("sdt_taxon_id")
        if not isinstance(self.sdt_taxon_id, TaxonSdtTaxonId):
            self.sdt_taxon_id = TaxonSdtTaxonId(self.sdt_taxon_id)

        if self._is_empty(self.sdt_taxon_name):
            self.MissingRequiredField("sdt_taxon_name")
        if not isinstance(self.sdt_taxon_name, EntityName):
            self.sdt_taxon_name = EntityName(self.sdt_taxon_name)

        if self.ncbi_taxid is not None and not isinstance(self.ncbi_taxid, int):
            self.ncbi_taxid = int(self.ncbi_taxid)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ASV(YAMLRoot):
    """
    Amplicon Sequence Variant (formerly OTU).

    CDM changes from CORAL:
    - Entity renamed from OTU to ASV (Amplicon Sequence Variant)
    - Table name: sdt_asv
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["ASV"]
    class_class_curie: ClassVar[str] = "kbase_cdm:ASV"
    class_name: ClassVar[str] = "ASV"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.ASV

    sdt_asv_id: Union[str, ASVSdtAsvId] = None
    sdt_asv_name: Union[str, EntityName] = None
    sequence: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_asv_id):
            self.MissingRequiredField("sdt_asv_id")
        if not isinstance(self.sdt_asv_id, ASVSdtAsvId):
            self.sdt_asv_id = ASVSdtAsvId(self.sdt_asv_id)

        if self._is_empty(self.sdt_asv_name):
            self.MissingRequiredField("sdt_asv_name")
        if not isinstance(self.sdt_asv_name, EntityName):
            self.sdt_asv_name = EntityName(self.sdt_asv_name)

        if self.sequence is not None and not isinstance(self.sequence, str):
            self.sequence = str(self.sequence)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Protocol(YAMLRoot):
    """
    Experimental protocol.

    CDM changes from CORAL:
    - Added 'link' field for protocol documents
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Protocol"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Protocol"
    class_name: ClassVar[str] = "Protocol"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Protocol

    sdt_protocol_id: Union[str, ProtocolSdtProtocolId] = None
    sdt_protocol_name: Union[str, EntityName] = None
    description: Optional[str] = None
    link: Optional[Union[str, Link]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_protocol_id):
            self.MissingRequiredField("sdt_protocol_id")
        if not isinstance(self.sdt_protocol_id, ProtocolSdtProtocolId):
            self.sdt_protocol_id = ProtocolSdtProtocolId(self.sdt_protocol_id)

        if self._is_empty(self.sdt_protocol_name):
            self.MissingRequiredField("sdt_protocol_name")
        if not isinstance(self.sdt_protocol_name, EntityName):
            self.sdt_protocol_name = EntityName(self.sdt_protocol_name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.link is not None and not isinstance(self.link, Link):
            self.link = Link(self.link)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Image(YAMLRoot):
    """
    Microscopy or other image data.

    CDM changes from CORAL:
    - Added 'link' field for image files
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Image"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Image"
    class_name: ClassVar[str] = "Image"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Image

    sdt_image_id: Union[str, ImageSdtImageId] = None
    sdt_image_name: Union[str, EntityName] = None
    mime_type: Optional[str] = None
    size: Optional[Union[int, Size]] = None
    dimensions: Optional[str] = None
    link: Optional[Union[str, Link]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_image_id):
            self.MissingRequiredField("sdt_image_id")
        if not isinstance(self.sdt_image_id, ImageSdtImageId):
            self.sdt_image_id = ImageSdtImageId(self.sdt_image_id)

        if self._is_empty(self.sdt_image_name):
            self.MissingRequiredField("sdt_image_name")
        if not isinstance(self.sdt_image_name, EntityName):
            self.sdt_image_name = EntityName(self.sdt_image_name)

        if self.mime_type is not None and not isinstance(self.mime_type, str):
            self.mime_type = str(self.mime_type)

        if self.size is not None and not isinstance(self.size, Size):
            self.size = Size(self.size)

        if self.dimensions is not None and not isinstance(self.dimensions, str):
            self.dimensions = str(self.dimensions)

        if self.link is not None and not isinstance(self.link, Link):
            self.link = Link(self.link)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Condition(YAMLRoot):
    """
    Growth or experimental condition.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Condition"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Condition"
    class_name: ClassVar[str] = "Condition"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Condition

    sdt_condition_id: Union[str, ConditionSdtConditionId] = None
    sdt_condition_name: Union[str, EntityName] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_condition_id):
            self.MissingRequiredField("sdt_condition_id")
        if not isinstance(self.sdt_condition_id, ConditionSdtConditionId):
            self.sdt_condition_id = ConditionSdtConditionId(self.sdt_condition_id)

        if self._is_empty(self.sdt_condition_name):
            self.MissingRequiredField("sdt_condition_name")
        if not isinstance(self.sdt_condition_name, EntityName):
            self.sdt_condition_name = EntityName(self.sdt_condition_name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DubSeqLibrary(YAMLRoot):
    """
    Dual Barcoded Sequencing (DubSeq) library.

    CDM changes from CORAL:
    - FK reference: genome → genome_ref
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["DubSeqLibrary"]
    class_class_curie: ClassVar[str] = "kbase_cdm:DubSeqLibrary"
    class_name: ClassVar[str] = "DubSeqLibrary"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.DubSeqLibrary

    sdt_dubseq_library_id: Union[str, DubSeqLibrarySdtDubseqLibraryId] = None
    sdt_dubseq_library_name: Union[str, EntityName] = None
    genome_ref: Optional[Union[str, EntityName]] = None
    n_fragments: Optional[Union[int, Count]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_dubseq_library_id):
            self.MissingRequiredField("sdt_dubseq_library_id")
        if not isinstance(self.sdt_dubseq_library_id, DubSeqLibrarySdtDubseqLibraryId):
            self.sdt_dubseq_library_id = DubSeqLibrarySdtDubseqLibraryId(self.sdt_dubseq_library_id)

        if self._is_empty(self.sdt_dubseq_library_name):
            self.MissingRequiredField("sdt_dubseq_library_name")
        if not isinstance(self.sdt_dubseq_library_name, EntityName):
            self.sdt_dubseq_library_name = EntityName(self.sdt_dubseq_library_name)

        if self.genome_ref is not None and not isinstance(self.genome_ref, EntityName):
            self.genome_ref = EntityName(self.genome_ref)

        if self.n_fragments is not None and not isinstance(self.n_fragments, Count):
            self.n_fragments = Count(self.n_fragments)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TnSeqLibrary(YAMLRoot):
    """
    Transposon Sequencing (TnSeq) library.

    CDM changes from CORAL:
    - FK reference: genome → genome_ref
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["TnSeqLibrary"]
    class_class_curie: ClassVar[str] = "kbase_cdm:TnSeqLibrary"
    class_name: ClassVar[str] = "TnSeqLibrary"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.TnSeqLibrary

    sdt_tnseq_library_id: Union[str, TnSeqLibrarySdtTnseqLibraryId] = None
    sdt_tnseq_library_name: Union[str, EntityName] = None
    genome_ref: Optional[Union[str, EntityName]] = None
    primers_model: Optional[str] = None
    n_mapped_reads: Optional[Union[int, Count]] = None
    n_good_reads: Optional[Union[int, Count]] = None
    n_genes_hit: Optional[Union[int, Count]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_tnseq_library_id):
            self.MissingRequiredField("sdt_tnseq_library_id")
        if not isinstance(self.sdt_tnseq_library_id, TnSeqLibrarySdtTnseqLibraryId):
            self.sdt_tnseq_library_id = TnSeqLibrarySdtTnseqLibraryId(self.sdt_tnseq_library_id)

        if self._is_empty(self.sdt_tnseq_library_name):
            self.MissingRequiredField("sdt_tnseq_library_name")
        if not isinstance(self.sdt_tnseq_library_name, EntityName):
            self.sdt_tnseq_library_name = EntityName(self.sdt_tnseq_library_name)

        if self.genome_ref is not None and not isinstance(self.genome_ref, EntityName):
            self.genome_ref = EntityName(self.genome_ref)

        if self.primers_model is not None and not isinstance(self.primers_model, str):
            self.primers_model = str(self.primers_model)

        if self.n_mapped_reads is not None and not isinstance(self.n_mapped_reads, Count):
            self.n_mapped_reads = Count(self.n_mapped_reads)

        if self.n_good_reads is not None and not isinstance(self.n_good_reads, Count):
            self.n_good_reads = Count(self.n_good_reads)

        if self.n_genes_hit is not None and not isinstance(self.n_genes_hit, Count):
            self.n_genes_hit = Count(self.n_genes_hit)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ENIGMA(YAMLRoot):
    """
    Root entity (database singleton).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["ENIGMA"]
    class_class_curie: ClassVar[str] = "kbase_cdm:ENIGMA"
    class_name: ClassVar[str] = "ENIGMA"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.ENIGMA

    sdt_enigma_id: Union[str, ENIGMASdtEnigmaId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sdt_enigma_id):
            self.MissingRequiredField("sdt_enigma_id")
        if not isinstance(self.sdt_enigma_id, ENIGMASdtEnigmaId):
            self.sdt_enigma_id = ENIGMASdtEnigmaId(self.sdt_enigma_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SystemTypedef(YAMLRoot):
    """
    Type definitions for static entity tables (equivalent to typedef.json).

    Maps CORAL entity types and fields to CDM table/column names with
    constraints, data types, and ontology references.

    This table documents the schema transformation from CORAL to CDM and
    enables automated validation and migration.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["SystemTypedef"]
    class_class_curie: ClassVar[str] = "kbase_cdm:SystemTypedef"
    class_name: ClassVar[str] = "SystemTypedef"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.SystemTypedef

    type_name: str = None
    field_name: str = None
    cdm_column_name: str = None
    scalar_type: Optional[str] = None
    pk: Optional[Union[bool, Bool]] = None
    upk: Optional[Union[bool, Bool]] = None
    fk: Optional[str] = None
    constraint: Optional[str] = None
    units_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    type_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.type_name):
            self.MissingRequiredField("type_name")
        if not isinstance(self.type_name, str):
            self.type_name = str(self.type_name)

        if self._is_empty(self.field_name):
            self.MissingRequiredField("field_name")
        if not isinstance(self.field_name, str):
            self.field_name = str(self.field_name)

        if self._is_empty(self.cdm_column_name):
            self.MissingRequiredField("cdm_column_name")
        if not isinstance(self.cdm_column_name, str):
            self.cdm_column_name = str(self.cdm_column_name)

        if self.scalar_type is not None and not isinstance(self.scalar_type, str):
            self.scalar_type = str(self.scalar_type)

        if self.pk is not None and not isinstance(self.pk, Bool):
            self.pk = Bool(self.pk)

        if self.upk is not None and not isinstance(self.upk, Bool):
            self.upk = Bool(self.upk)

        if self.fk is not None and not isinstance(self.fk, str):
            self.fk = str(self.fk)

        if self.constraint is not None and not isinstance(self.constraint, str):
            self.constraint = str(self.constraint)

        if self.units_sys_oterm_id is not None and not isinstance(self.units_sys_oterm_id, OntologyTermID):
            self.units_sys_oterm_id = OntologyTermID(self.units_sys_oterm_id)

        if self.type_sys_oterm_id is not None and not isinstance(self.type_sys_oterm_id, OntologyTermID):
            self.type_sys_oterm_id = OntologyTermID(self.type_sys_oterm_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SystemDDTTypedef(YAMLRoot):
    """
    Type definitions for dynamic data tables (bricks).

    Defines schema for N-dimensional measurement arrays including:
    - Dimension semantics (Environmental Sample, Molecule, State, Statistic)
    - Variable semantics (Concentration, Molecular Weight, etc.)
    - Data types and units
    - Brick structure metadata

    Each brick can have different dimensionality and variable sets,
    enabling flexible storage of heterogeneous measurement data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["SystemDDTTypedef"]
    class_class_curie: ClassVar[str] = "kbase_cdm:SystemDDTTypedef"
    class_name: ClassVar[str] = "SystemDDTTypedef"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.SystemDDTTypedef

    ddt_ndarray_id: str = None
    cdm_column_name: str = None
    cdm_column_data_type: Optional[str] = None
    scalar_type: Optional[str] = None
    dimension_number: Optional[int] = None
    variable_number: Optional[int] = None
    dimension_oterm_id: Optional[Union[str, OntologyTermID]] = None
    dimension_oterm_name: Optional[str] = None
    variable_oterm_id: Optional[Union[str, OntologyTermID]] = None
    variable_oterm_name: Optional[str] = None
    unit_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    unit_sys_oterm_name: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.ddt_ndarray_id):
            self.MissingRequiredField("ddt_ndarray_id")
        if not isinstance(self.ddt_ndarray_id, str):
            self.ddt_ndarray_id = str(self.ddt_ndarray_id)

        if self._is_empty(self.cdm_column_name):
            self.MissingRequiredField("cdm_column_name")
        if not isinstance(self.cdm_column_name, str):
            self.cdm_column_name = str(self.cdm_column_name)

        if self.cdm_column_data_type is not None and not isinstance(self.cdm_column_data_type, str):
            self.cdm_column_data_type = str(self.cdm_column_data_type)

        if self.scalar_type is not None and not isinstance(self.scalar_type, str):
            self.scalar_type = str(self.scalar_type)

        if self.dimension_number is not None and not isinstance(self.dimension_number, int):
            self.dimension_number = int(self.dimension_number)

        if self.variable_number is not None and not isinstance(self.variable_number, int):
            self.variable_number = int(self.variable_number)

        if self.dimension_oterm_id is not None and not isinstance(self.dimension_oterm_id, OntologyTermID):
            self.dimension_oterm_id = OntologyTermID(self.dimension_oterm_id)

        if self.dimension_oterm_name is not None and not isinstance(self.dimension_oterm_name, str):
            self.dimension_oterm_name = str(self.dimension_oterm_name)

        if self.variable_oterm_id is not None and not isinstance(self.variable_oterm_id, OntologyTermID):
            self.variable_oterm_id = OntologyTermID(self.variable_oterm_id)

        if self.variable_oterm_name is not None and not isinstance(self.variable_oterm_name, str):
            self.variable_oterm_name = str(self.variable_oterm_name)

        if self.unit_sys_oterm_id is not None and not isinstance(self.unit_sys_oterm_id, OntologyTermID):
            self.unit_sys_oterm_id = OntologyTermID(self.unit_sys_oterm_id)

        if self.unit_sys_oterm_name is not None and not isinstance(self.unit_sys_oterm_name, str):
            self.unit_sys_oterm_name = str(self.unit_sys_oterm_name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SystemOntologyTerm(YAMLRoot):
    """
    Centralized ontology term catalog.

    Stores all ontology terms used across the CDM with:
    - CURIE identifiers (ME:, ENVO:, UO:, etc.)
    - Human-readable names
    - Hierarchical relationships (parent terms)
    - Definitions, synonyms, and external links

    Benefits:
    - Single source of truth for ontology terms
    - Supports ontology evolution without data migration
    - Enables semantic queries and reasoning
    - Foreign key target for all *_sys_oterm_id columns
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["SystemOntologyTerm"]
    class_class_curie: ClassVar[str] = "kbase_cdm:SystemOntologyTerm"
    class_name: ClassVar[str] = "SystemOntologyTerm"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.SystemOntologyTerm

    sys_oterm_id: Union[str, SystemOntologyTermSysOtermId] = None
    sys_oterm_name: Optional[str] = None
    sys_oterm_ontology: Optional[str] = None
    parent_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    sys_oterm_definition: Optional[str] = None
    sys_oterm_synonyms: Optional[str] = None
    sys_oterm_links: Optional[str] = None
    sys_oterm_properties: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sys_oterm_id):
            self.MissingRequiredField("sys_oterm_id")
        if not isinstance(self.sys_oterm_id, SystemOntologyTermSysOtermId):
            self.sys_oterm_id = SystemOntologyTermSysOtermId(self.sys_oterm_id)

        if self.sys_oterm_name is not None and not isinstance(self.sys_oterm_name, str):
            self.sys_oterm_name = str(self.sys_oterm_name)

        if self.sys_oterm_ontology is not None and not isinstance(self.sys_oterm_ontology, str):
            self.sys_oterm_ontology = str(self.sys_oterm_ontology)

        if self.parent_sys_oterm_id is not None and not isinstance(self.parent_sys_oterm_id, OntologyTermID):
            self.parent_sys_oterm_id = OntologyTermID(self.parent_sys_oterm_id)

        if self.sys_oterm_definition is not None and not isinstance(self.sys_oterm_definition, str):
            self.sys_oterm_definition = str(self.sys_oterm_definition)

        if self.sys_oterm_synonyms is not None and not isinstance(self.sys_oterm_synonyms, str):
            self.sys_oterm_synonyms = str(self.sys_oterm_synonyms)

        if self.sys_oterm_links is not None and not isinstance(self.sys_oterm_links, str):
            self.sys_oterm_links = str(self.sys_oterm_links)

        if self.sys_oterm_properties is not None and not isinstance(self.sys_oterm_properties, str):
            self.sys_oterm_properties = str(self.sys_oterm_properties)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SystemProcess(YAMLRoot):
    """
    Provenance tracking for all data transformations.

    Records experimental processes with:
    - Process type (Assay Growth, Sequencing, etc.)
    - People, protocols, campaigns
    - Temporal metadata (start/end dates)
    - Input/output relationships (denormalized arrays)

    Enables complete lineage tracing from raw samples to final analyses.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["SystemProcess"]
    class_class_curie: ClassVar[str] = "kbase_cdm:SystemProcess"
    class_name: ClassVar[str] = "SystemProcess"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.SystemProcess

    sys_process_id: Union[str, SystemProcessSysProcessId] = None
    sdt_protocol_name: Union[str, EntityName] = None
    process_type_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    process_type_sys_oterm_name: Optional[str] = None
    person_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    person_sys_oterm_name: Optional[str] = None
    campaign_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    campaign_sys_oterm_name: Optional[str] = None
    date_start: Optional[Union[str, Date]] = None
    date_end: Optional[Union[str, Date]] = None
    input_objects: Optional[Union[str, list[str]]] = empty_list()
    output_objects: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sys_process_id):
            self.MissingRequiredField("sys_process_id")
        if not isinstance(self.sys_process_id, SystemProcessSysProcessId):
            self.sys_process_id = SystemProcessSysProcessId(self.sys_process_id)

        if self._is_empty(self.sdt_protocol_name):
            self.MissingRequiredField("sdt_protocol_name")
        if not isinstance(self.sdt_protocol_name, EntityName):
            self.sdt_protocol_name = EntityName(self.sdt_protocol_name)

        if self.process_type_sys_oterm_id is not None and not isinstance(self.process_type_sys_oterm_id, OntologyTermID):
            self.process_type_sys_oterm_id = OntologyTermID(self.process_type_sys_oterm_id)

        if self.process_type_sys_oterm_name is not None and not isinstance(self.process_type_sys_oterm_name, str):
            self.process_type_sys_oterm_name = str(self.process_type_sys_oterm_name)

        if self.person_sys_oterm_id is not None and not isinstance(self.person_sys_oterm_id, OntologyTermID):
            self.person_sys_oterm_id = OntologyTermID(self.person_sys_oterm_id)

        if self.person_sys_oterm_name is not None and not isinstance(self.person_sys_oterm_name, str):
            self.person_sys_oterm_name = str(self.person_sys_oterm_name)

        if self.campaign_sys_oterm_id is not None and not isinstance(self.campaign_sys_oterm_id, OntologyTermID):
            self.campaign_sys_oterm_id = OntologyTermID(self.campaign_sys_oterm_id)

        if self.campaign_sys_oterm_name is not None and not isinstance(self.campaign_sys_oterm_name, str):
            self.campaign_sys_oterm_name = str(self.campaign_sys_oterm_name)

        if self.date_start is not None and not isinstance(self.date_start, Date):
            self.date_start = Date(self.date_start)

        if self.date_end is not None and not isinstance(self.date_end, Date):
            self.date_end = Date(self.date_end)

        if not isinstance(self.input_objects, list):
            self.input_objects = [self.input_objects] if self.input_objects is not None else []
        self.input_objects = [v if isinstance(v, str) else str(v) for v in self.input_objects]

        if not isinstance(self.output_objects, list):
            self.output_objects = [self.output_objects] if self.output_objects is not None else []
        self.output_objects = [v if isinstance(v, str) else str(v) for v in self.output_objects]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SystemProcessInput(YAMLRoot):
    """
    Normalized process input relationships.

    Denormalizes the input_objects array from sys_process for efficient
    querying. Each row represents one input entity to one process.

    Enables queries like:
    - "Find all processes that used this sample"
    - "What samples were used in sequencing processes?"
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["SystemProcessInput"]
    class_class_curie: ClassVar[str] = "kbase_cdm:SystemProcessInput"
    class_name: ClassVar[str] = "SystemProcessInput"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.SystemProcessInput

    sys_process_id: str = None
    input_object_type: Optional[str] = None
    input_object_name: Optional[Union[str, EntityName]] = None
    input_index: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sys_process_id):
            self.MissingRequiredField("sys_process_id")
        if not isinstance(self.sys_process_id, str):
            self.sys_process_id = str(self.sys_process_id)

        if self.input_object_type is not None and not isinstance(self.input_object_type, str):
            self.input_object_type = str(self.input_object_type)

        if self.input_object_name is not None and not isinstance(self.input_object_name, EntityName):
            self.input_object_name = EntityName(self.input_object_name)

        if self.input_index is not None and not isinstance(self.input_index, int):
            self.input_index = int(self.input_index)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SystemProcessOutput(YAMLRoot):
    """
    Normalized process output relationships.

    Denormalizes the output_objects array from sys_process for efficient
    querying. Each row represents one output entity from one process.

    Enables queries like:
    - "What process created this assembly?"
    - "Find all assemblies from sequencing processes"
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["SystemProcessOutput"]
    class_class_curie: ClassVar[str] = "kbase_cdm:SystemProcessOutput"
    class_name: ClassVar[str] = "SystemProcessOutput"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.SystemProcessOutput

    sys_process_id: str = None
    output_object_type: Optional[str] = None
    output_object_name: Optional[Union[str, EntityName]] = None
    output_index: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sys_process_id):
            self.MissingRequiredField("sys_process_id")
        if not isinstance(self.sys_process_id, str):
            self.sys_process_id = str(self.sys_process_id)

        if self.output_object_type is not None and not isinstance(self.output_object_type, str):
            self.output_object_type = str(self.output_object_type)

        if self.output_object_name is not None and not isinstance(self.output_object_name, EntityName):
            self.output_object_name = EntityName(self.output_object_name)

        if self.output_index is not None and not isinstance(self.output_index, int):
            self.output_index = int(self.output_index)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DynamicDataArray(YAMLRoot):
    """
    Brick index table (ddt_ndarray).

    Catalogs all available measurement bricks with:
    - Brick identifiers (Brick0000001, Brick0000002, etc.)
    - Shape metadata (dimensions and sizes)
    - Entity relationships (which samples, communities, etc.)
    - Semantic metadata (measurement types, units)

    Each brick corresponds to:
    - One ddt_brick* table with actual measurement data
    - Multiple rows in sys_ddt_typedef defining brick schema
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["DynamicDataArray"]
    class_class_curie: ClassVar[str] = "kbase_cdm:DynamicDataArray"
    class_name: ClassVar[str] = "DynamicDataArray"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.DynamicDataArray

    ddt_ndarray_id: Union[str, DynamicDataArrayDdtNdarrayId] = None
    brick_table_name: Optional[str] = None
    n_dimensions: Optional[int] = None
    dimension_sizes: Optional[str] = None
    n_variables: Optional[int] = None
    total_rows: Optional[int] = None
    associated_entity_type: Optional[str] = None
    associated_entity_names: Optional[Union[Union[str, EntityName], list[Union[str, EntityName]]]] = empty_list()
    measurement_type_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    measurement_type_sys_oterm_name: Optional[str] = None
    creation_date: Optional[Union[str, Date]] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.ddt_ndarray_id):
            self.MissingRequiredField("ddt_ndarray_id")
        if not isinstance(self.ddt_ndarray_id, DynamicDataArrayDdtNdarrayId):
            self.ddt_ndarray_id = DynamicDataArrayDdtNdarrayId(self.ddt_ndarray_id)

        if self.brick_table_name is not None and not isinstance(self.brick_table_name, str):
            self.brick_table_name = str(self.brick_table_name)

        if self.n_dimensions is not None and not isinstance(self.n_dimensions, int):
            self.n_dimensions = int(self.n_dimensions)

        if self.dimension_sizes is not None and not isinstance(self.dimension_sizes, str):
            self.dimension_sizes = str(self.dimension_sizes)

        if self.n_variables is not None and not isinstance(self.n_variables, int):
            self.n_variables = int(self.n_variables)

        if self.total_rows is not None and not isinstance(self.total_rows, int):
            self.total_rows = int(self.total_rows)

        if self.associated_entity_type is not None and not isinstance(self.associated_entity_type, str):
            self.associated_entity_type = str(self.associated_entity_type)

        if not isinstance(self.associated_entity_names, list):
            self.associated_entity_names = [self.associated_entity_names] if self.associated_entity_names is not None else []
        self.associated_entity_names = [v if isinstance(v, EntityName) else EntityName(v) for v in self.associated_entity_names]

        if self.measurement_type_sys_oterm_id is not None and not isinstance(self.measurement_type_sys_oterm_id, OntologyTermID):
            self.measurement_type_sys_oterm_id = OntologyTermID(self.measurement_type_sys_oterm_id)

        if self.measurement_type_sys_oterm_name is not None and not isinstance(self.measurement_type_sys_oterm_name, str):
            self.measurement_type_sys_oterm_name = str(self.measurement_type_sys_oterm_name)

        if self.creation_date is not None and not isinstance(self.creation_date, Date):
            self.creation_date = Date(self.creation_date)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BrickDimension(YAMLRoot):
    """
    Abstract base for brick dimension metadata.

    Dimensions define the axes of N-dimensional measurement arrays:
    - Environmental Sample: Different samples measured
    - Molecule: Different molecules/compounds measured
    - State: Different conditions (e.g., time points, treatments)
    - Statistic: Different statistical measures (mean, std, etc.)

    Each dimension has:
    - Semantic meaning (ontology term)
    - Size (number of values along axis)
    - Index values (entity names or numeric indices)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["BrickDimension"]
    class_class_curie: ClassVar[str] = "kbase_cdm:BrickDimension"
    class_name: ClassVar[str] = "BrickDimension"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.BrickDimension

    dimension_number: Optional[int] = None
    dimension_oterm_id: Optional[Union[str, OntologyTermID]] = None
    dimension_oterm_name: Optional[str] = None
    dimension_size: Optional[int] = None
    dimension_values: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.dimension_number is not None and not isinstance(self.dimension_number, int):
            self.dimension_number = int(self.dimension_number)

        if self.dimension_oterm_id is not None and not isinstance(self.dimension_oterm_id, OntologyTermID):
            self.dimension_oterm_id = OntologyTermID(self.dimension_oterm_id)

        if self.dimension_oterm_name is not None and not isinstance(self.dimension_oterm_name, str):
            self.dimension_oterm_name = str(self.dimension_oterm_name)

        if self.dimension_size is not None and not isinstance(self.dimension_size, int):
            self.dimension_size = int(self.dimension_size)

        if self.dimension_values is not None and not isinstance(self.dimension_values, str):
            self.dimension_values = str(self.dimension_values)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BrickVariable(YAMLRoot):
    """
    Abstract base for brick variable metadata.

    Variables define what is measured at each point in the N-dimensional array:
    - Concentration (with units: mg/L, µM, etc.)
    - Molecular Weight (with units: Da, kDa, etc.)
    - Activity Rate (with units: nmol/min, etc.)
    - Expression Level (with units: RPKM, TPM, etc.)

    Each variable has:
    - Semantic meaning (ontology term)
    - Data type (float, int, bool, oterm_ref, object_ref)
    - Units (ontology term)
    - Value range constraints
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["BrickVariable"]
    class_class_curie: ClassVar[str] = "kbase_cdm:BrickVariable"
    class_name: ClassVar[str] = "BrickVariable"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.BrickVariable

    variable_number: Optional[int] = None
    variable_oterm_id: Optional[Union[str, OntologyTermID]] = None
    variable_oterm_name: Optional[str] = None
    variable_data_type: Optional[str] = None
    unit_sys_oterm_id: Optional[Union[str, OntologyTermID]] = None
    unit_sys_oterm_name: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.variable_number is not None and not isinstance(self.variable_number, int):
            self.variable_number = int(self.variable_number)

        if self.variable_oterm_id is not None and not isinstance(self.variable_oterm_id, OntologyTermID):
            self.variable_oterm_id = OntologyTermID(self.variable_oterm_id)

        if self.variable_oterm_name is not None and not isinstance(self.variable_oterm_name, str):
            self.variable_oterm_name = str(self.variable_oterm_name)

        if self.variable_data_type is not None and not isinstance(self.variable_data_type, str):
            self.variable_data_type = str(self.variable_data_type)

        if self.unit_sys_oterm_id is not None and not isinstance(self.unit_sys_oterm_id, OntologyTermID):
            self.unit_sys_oterm_id = OntologyTermID(self.unit_sys_oterm_id)

        if self.unit_sys_oterm_name is not None and not isinstance(self.unit_sys_oterm_name, str):
            self.unit_sys_oterm_name = str(self.unit_sys_oterm_name)

        if self.min_value is not None and not isinstance(self.min_value, float):
            self.min_value = float(self.min_value)

        if self.max_value is not None and not isinstance(self.max_value, float):
            self.max_value = float(self.max_value)

        super().__post_init__(**kwargs)


class Brick(YAMLRoot):
    """
    Abstract base for all brick data tables (ddt_brick*).

    Each brick table stores measurement values in a denormalized format
    where each row represents one cell in the N-dimensional array.

    Common structure:
    - Dimension indices (dim0_index, dim1_index, dim2_index, ...)
    - Dimension values (dim0_value, dim1_value, dim2_value, ...)
    - Variable values (var0_value, var1_value, var2_value, ...)

    Schema is defined in sys_ddt_typedef and varies per brick.

    Note: Individual brick classes (Brick0000001, Brick0000002, etc.)
    are not explicitly defined in this schema because they have
    heterogeneous structures. They should be validated against
    sys_ddt_typedef at runtime.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KBASE_CDM["Brick"]
    class_class_curie: ClassVar[str] = "kbase_cdm:Brick"
    class_name: ClassVar[str] = "Brick"
    class_model_uri: ClassVar[URIRef] = KBASE_CDM.Brick


# Enumerations
class StrandEnum(EnumDefinitionImpl):
    """
    DNA strand orientation
    """
    forward = PermissibleValue(
        text="forward",
        description="Forward strand (+)",
        meaning=ME["0000193"])
    reverse_complement = PermissibleValue(
        text="reverse_complement",
        description="Reverse complement strand (-)",
        meaning=ME["0000194"])

    _defn = EnumDefinition(
        name="StrandEnum",
        description="DNA strand orientation",
    )

class ReadTypeEnum(EnumDefinitionImpl):
    """
    Sequencing read type
    """
    paired_end = PermissibleValue(
        text="paired_end",
        description="Paired-end reads",
        meaning=ME["0000113"])
    single_end = PermissibleValue(
        text="single_end",
        description="Single-end reads",
        meaning=ME["0000114"])

    _defn = EnumDefinition(
        name="ReadTypeEnum",
        description="Sequencing read type",
    )

class SequencingTechnologyEnum(EnumDefinitionImpl):
    """
    Sequencing platform technology
    """
    illumina = PermissibleValue(
        text="illumina",
        description="Illumina sequencing",
        meaning=ME["0000115"])
    pacbio = PermissibleValue(
        text="pacbio",
        description="PacBio sequencing",
        meaning=ME["0000116"])
    nanopore = PermissibleValue(
        text="nanopore",
        description="Oxford Nanopore sequencing",
        meaning=ME["0000117"])
    sanger = PermissibleValue(
        text="sanger",
        description="Sanger sequencing",
        meaning=ME["0000118"])

    _defn = EnumDefinition(
        name="SequencingTechnologyEnum",
        description="Sequencing platform technology",
    )

class CommunityTypeEnum(EnumDefinitionImpl):
    """
    Microbial community type
    """
    isolate_community = PermissibleValue(
        text="isolate_community",
        description="Isolated single strain",
        meaning=ME["0000200"])
    enrichment = PermissibleValue(
        text="enrichment",
        description="Enrichment culture",
        meaning=ME["0000201"])
    assemblage = PermissibleValue(
        text="assemblage",
        description="Defined assemblage of strains",
        meaning=ME["0000202"])
    environmental_community = PermissibleValue(
        text="environmental_community",
        description="Environmental community (metagenome)",
        meaning=ME["0000203"])
    active_fraction = PermissibleValue(
        text="active_fraction",
        description="Active fraction",
        meaning=ME["0000237"])

    _defn = EnumDefinition(
        name="CommunityTypeEnum",
        description="Microbial community type",
    )

class MaterialEnum(EnumDefinitionImpl):
    """
    Sample material type
    """
    soil = PermissibleValue(
        text="soil",
        description="Soil",
        meaning=ENVO["00001998"])
    sediment = PermissibleValue(
        text="sediment",
        description="Sediment",
        meaning=ENVO["00002007"])
    water = PermissibleValue(
        text="water",
        description="Water",
        meaning=ENVO["00002006"])
    biofilm = PermissibleValue(
        text="biofilm",
        description="Biofilm",
        meaning=ENVO["00002034"])

    _defn = EnumDefinition(
        name="MaterialEnum",
        description="Sample material type",
    )

class BiomeEnum(EnumDefinitionImpl):
    """
    Environmental biome
    """
    terrestrial = PermissibleValue(
        text="terrestrial",
        description="Terrestrial biome",
        meaning=ENVO["00000446"])
    aquatic = PermissibleValue(
        text="aquatic",
        description="Aquatic biome",
        meaning=ENVO["00002030"])
    marine = PermissibleValue(
        text="marine",
        description="Marine biome",
        meaning=ENVO["00000447"])

    _defn = EnumDefinition(
        name="BiomeEnum",
        description="Environmental biome",
    )

class BrickDataType(EnumDefinitionImpl):
    """
    Data types for brick variables
    """
    float = PermissibleValue(
        text="float",
        description="Floating point number")
    int = PermissibleValue(
        text="int",
        description="Integer")
    bool = PermissibleValue(
        text="bool",
        description="Boolean (true/false)")
    text = PermissibleValue(
        text="text",
        description="Free text string")
    oterm_ref = PermissibleValue(
        text="oterm_ref",
        description="Reference to ontology term (sys_oterm_id)")
    object_ref = PermissibleValue(
        text="object_ref",
        description="Reference to entity by name")

    _defn = EnumDefinition(
        name="BrickDataType",
        description="Data types for brick variables",
    )

class DimensionSemantics(EnumDefinitionImpl):
    """
    Common dimension semantic types
    """
    environmental_sample = PermissibleValue(
        text="environmental_sample",
        description="Environmental sample dimension",
        meaning=ME["0000501"])
    molecule = PermissibleValue(
        text="molecule",
        description="Molecule/compound dimension",
        meaning=ME["0000502"])
    state = PermissibleValue(
        text="state",
        description="Experimental state dimension (time, treatment, etc.)",
        meaning=ME["0000503"])
    statistic = PermissibleValue(
        text="statistic",
        description="Statistical measure dimension (mean, std, etc.)",
        meaning=ME["0000504"])
    gene = PermissibleValue(
        text="gene",
        description="Gene dimension",
        meaning=ME["0000505"])
    taxon = PermissibleValue(
        text="taxon",
        description="Taxonomic dimension",
        meaning=ME["0000506"])
    location = PermissibleValue(
        text="location",
        description="Location dimension",
        meaning=ME["0000507"])
    time = PermissibleValue(
        text="time",
        description="Time point dimension",
        meaning=ME["0000508"])

    _defn = EnumDefinition(
        name="DimensionSemantics",
        description="Common dimension semantic types",
    )

class VariableSemantics(EnumDefinitionImpl):
    """
    Common variable semantic types
    """
    concentration = PermissibleValue(
        text="concentration",
        description="Chemical concentration",
        meaning=ME["0000601"])
    molecular_weight = PermissibleValue(
        text="molecular_weight",
        description="Molecular weight",
        meaning=ME["0000602"])
    activity_rate = PermissibleValue(
        text="activity_rate",
        description="Enzymatic or metabolic activity rate",
        meaning=ME["0000603"])
    expression_level = PermissibleValue(
        text="expression_level",
        description="Gene expression level",
        meaning=ME["0000604"])
    abundance = PermissibleValue(
        text="abundance",
        description="Relative or absolute abundance",
        meaning=ME["0000605"])
    ph = PermissibleValue(
        text="ph",
        description="pH measurement",
        meaning=ME["0000606"])
    temperature = PermissibleValue(
        text="temperature",
        description="Temperature",
        meaning=ME["0000607"])
    growth_rate = PermissibleValue(
        text="growth_rate",
        description="Cell or organism growth rate",
        meaning=ME["0000608"])

    _defn = EnumDefinition(
        name="VariableSemantics",
        description="Common variable semantic types",
    )

# Slots
class slots:
    pass

slots.sys_oterm_id = Slot(uri=KBASE_CDM.sys_oterm_id, name="sys_oterm_id", curie=KBASE_CDM.curie('sys_oterm_id'),
                   model_uri=KBASE_CDM.sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.sys_oterm_name = Slot(uri=KBASE_CDM.sys_oterm_name, name="sys_oterm_name", curie=KBASE_CDM.curie('sys_oterm_name'),
                   model_uri=KBASE_CDM.sys_oterm_name, domain=None, range=Optional[str])

slots.link = Slot(uri=KBASE_CDM.link, name="link", curie=KBASE_CDM.curie('link'),
                   model_uri=KBASE_CDM.link, domain=None, range=Optional[Union[str, Link]])

slots.sdt_location_id = Slot(uri=KBASE_CDM.sdt_location_id, name="sdt_location_id", curie=KBASE_CDM.curie('sdt_location_id'),
                   model_uri=KBASE_CDM.sdt_location_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Location\d{7}$'))

slots.sdt_location_name = Slot(uri=KBASE_CDM.sdt_location_name, name="sdt_location_name", curie=KBASE_CDM.curie('sdt_location_name'),
                   model_uri=KBASE_CDM.sdt_location_name, domain=None, range=Union[str, EntityName])

slots.latitude = Slot(uri=KBASE_CDM.latitude, name="latitude", curie=KBASE_CDM.curie('latitude'),
                   model_uri=KBASE_CDM.latitude, domain=None, range=Optional[Union[float, Latitude]])

slots.longitude = Slot(uri=KBASE_CDM.longitude, name="longitude", curie=KBASE_CDM.curie('longitude'),
                   model_uri=KBASE_CDM.longitude, domain=None, range=Optional[Union[float, Longitude]])

slots.continent_sys_oterm_id = Slot(uri=KBASE_CDM.continent_sys_oterm_id, name="continent_sys_oterm_id", curie=KBASE_CDM.curie('continent_sys_oterm_id'),
                   model_uri=KBASE_CDM.continent_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.continent_sys_oterm_name = Slot(uri=KBASE_CDM.continent_sys_oterm_name, name="continent_sys_oterm_name", curie=KBASE_CDM.curie('continent_sys_oterm_name'),
                   model_uri=KBASE_CDM.continent_sys_oterm_name, domain=None, range=Optional[str])

slots.country_sys_oterm_id = Slot(uri=KBASE_CDM.country_sys_oterm_id, name="country_sys_oterm_id", curie=KBASE_CDM.curie('country_sys_oterm_id'),
                   model_uri=KBASE_CDM.country_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.country_sys_oterm_name = Slot(uri=KBASE_CDM.country_sys_oterm_name, name="country_sys_oterm_name", curie=KBASE_CDM.curie('country_sys_oterm_name'),
                   model_uri=KBASE_CDM.country_sys_oterm_name, domain=None, range=Optional[str])

slots.region = Slot(uri=KBASE_CDM.region, name="region", curie=KBASE_CDM.curie('region'),
                   model_uri=KBASE_CDM.region, domain=None, range=Optional[str])

slots.biome_sys_oterm_id = Slot(uri=KBASE_CDM.biome_sys_oterm_id, name="biome_sys_oterm_id", curie=KBASE_CDM.curie('biome_sys_oterm_id'),
                   model_uri=KBASE_CDM.biome_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.biome_sys_oterm_name = Slot(uri=KBASE_CDM.biome_sys_oterm_name, name="biome_sys_oterm_name", curie=KBASE_CDM.curie('biome_sys_oterm_name'),
                   model_uri=KBASE_CDM.biome_sys_oterm_name, domain=None, range=Optional[str])

slots.feature_sys_oterm_id = Slot(uri=KBASE_CDM.feature_sys_oterm_id, name="feature_sys_oterm_id", curie=KBASE_CDM.curie('feature_sys_oterm_id'),
                   model_uri=KBASE_CDM.feature_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.feature_sys_oterm_name = Slot(uri=KBASE_CDM.feature_sys_oterm_name, name="feature_sys_oterm_name", curie=KBASE_CDM.curie('feature_sys_oterm_name'),
                   model_uri=KBASE_CDM.feature_sys_oterm_name, domain=None, range=Optional[str])

slots.sdt_sample_id = Slot(uri=KBASE_CDM.sdt_sample_id, name="sdt_sample_id", curie=KBASE_CDM.curie('sdt_sample_id'),
                   model_uri=KBASE_CDM.sdt_sample_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Sample\d{7}$'))

slots.sdt_sample_name = Slot(uri=KBASE_CDM.sdt_sample_name, name="sdt_sample_name", curie=KBASE_CDM.curie('sdt_sample_name'),
                   model_uri=KBASE_CDM.sdt_sample_name, domain=None, range=Union[str, EntityName])

slots.location_ref = Slot(uri=KBASE_CDM.location_ref, name="location_ref", curie=KBASE_CDM.curie('location_ref'),
                   model_uri=KBASE_CDM.location_ref, domain=None, range=Optional[Union[str, EntityName]])

slots.depth = Slot(uri=KBASE_CDM.depth, name="depth", curie=KBASE_CDM.curie('depth'),
                   model_uri=KBASE_CDM.depth, domain=None, range=Optional[Union[float, Depth]])

slots.elevation = Slot(uri=KBASE_CDM.elevation, name="elevation", curie=KBASE_CDM.curie('elevation'),
                   model_uri=KBASE_CDM.elevation, domain=None, range=Optional[Union[float, Elevation]])

slots.date = Slot(uri=KBASE_CDM.date, name="date", curie=KBASE_CDM.curie('date'),
                   model_uri=KBASE_CDM.date, domain=None, range=Optional[Union[str, Date]])

slots.time = Slot(uri=KBASE_CDM.time, name="time", curie=KBASE_CDM.curie('time'),
                   model_uri=KBASE_CDM.time, domain=None, range=Optional[Union[str, Time]])

slots.timezone = Slot(uri=KBASE_CDM.timezone, name="timezone", curie=KBASE_CDM.curie('timezone'),
                   model_uri=KBASE_CDM.timezone, domain=None, range=Optional[str])

slots.material_sys_oterm_id = Slot(uri=KBASE_CDM.material_sys_oterm_id, name="material_sys_oterm_id", curie=KBASE_CDM.curie('material_sys_oterm_id'),
                   model_uri=KBASE_CDM.material_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.material_sys_oterm_name = Slot(uri=KBASE_CDM.material_sys_oterm_name, name="material_sys_oterm_name", curie=KBASE_CDM.curie('material_sys_oterm_name'),
                   model_uri=KBASE_CDM.material_sys_oterm_name, domain=None, range=Optional[str])

slots.env_package_sys_oterm_id = Slot(uri=KBASE_CDM.env_package_sys_oterm_id, name="env_package_sys_oterm_id", curie=KBASE_CDM.curie('env_package_sys_oterm_id'),
                   model_uri=KBASE_CDM.env_package_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.env_package_sys_oterm_name = Slot(uri=KBASE_CDM.env_package_sys_oterm_name, name="env_package_sys_oterm_name", curie=KBASE_CDM.curie('env_package_sys_oterm_name'),
                   model_uri=KBASE_CDM.env_package_sys_oterm_name, domain=None, range=Optional[str])

slots.description = Slot(uri=KBASE_CDM.description, name="description", curie=KBASE_CDM.curie('description'),
                   model_uri=KBASE_CDM.description, domain=None, range=Optional[str])

slots.sdt_community_id = Slot(uri=KBASE_CDM.sdt_community_id, name="sdt_community_id", curie=KBASE_CDM.curie('sdt_community_id'),
                   model_uri=KBASE_CDM.sdt_community_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Community\d{7}$'))

slots.sdt_community_name = Slot(uri=KBASE_CDM.sdt_community_name, name="sdt_community_name", curie=KBASE_CDM.curie('sdt_community_name'),
                   model_uri=KBASE_CDM.sdt_community_name, domain=None, range=Union[str, EntityName])

slots.community_type_sys_oterm_id = Slot(uri=KBASE_CDM.community_type_sys_oterm_id, name="community_type_sys_oterm_id", curie=KBASE_CDM.curie('community_type_sys_oterm_id'),
                   model_uri=KBASE_CDM.community_type_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.community_type_sys_oterm_name = Slot(uri=KBASE_CDM.community_type_sys_oterm_name, name="community_type_sys_oterm_name", curie=KBASE_CDM.curie('community_type_sys_oterm_name'),
                   model_uri=KBASE_CDM.community_type_sys_oterm_name, domain=None, range=Optional[str])

slots.sample_ref = Slot(uri=KBASE_CDM.sample_ref, name="sample_ref", curie=KBASE_CDM.curie('sample_ref'),
                   model_uri=KBASE_CDM.sample_ref, domain=None, range=Optional[Union[str, EntityName]])

slots.parent_community_ref = Slot(uri=KBASE_CDM.parent_community_ref, name="parent_community_ref", curie=KBASE_CDM.curie('parent_community_ref'),
                   model_uri=KBASE_CDM.parent_community_ref, domain=None, range=Optional[Union[str, EntityName]])

slots.defined_strains_ref = Slot(uri=KBASE_CDM.defined_strains_ref, name="defined_strains_ref", curie=KBASE_CDM.curie('defined_strains_ref'),
                   model_uri=KBASE_CDM.defined_strains_ref, domain=None, range=Optional[Union[Union[str, EntityName], list[Union[str, EntityName]]]])

slots.sdt_reads_id = Slot(uri=KBASE_CDM.sdt_reads_id, name="sdt_reads_id", curie=KBASE_CDM.curie('sdt_reads_id'),
                   model_uri=KBASE_CDM.sdt_reads_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Reads\d{7}$'))

slots.sdt_reads_name = Slot(uri=KBASE_CDM.sdt_reads_name, name="sdt_reads_name", curie=KBASE_CDM.curie('sdt_reads_name'),
                   model_uri=KBASE_CDM.sdt_reads_name, domain=None, range=Union[str, EntityName])

slots.read_count = Slot(uri=KBASE_CDM.read_count, name="read_count", curie=KBASE_CDM.curie('read_count'),
                   model_uri=KBASE_CDM.read_count, domain=None, range=Optional[Union[int, Count]])

slots.base_count = Slot(uri=KBASE_CDM.base_count, name="base_count", curie=KBASE_CDM.curie('base_count'),
                   model_uri=KBASE_CDM.base_count, domain=None, range=Optional[Union[int, Count]])

slots.read_type_sys_oterm_id = Slot(uri=KBASE_CDM.read_type_sys_oterm_id, name="read_type_sys_oterm_id", curie=KBASE_CDM.curie('read_type_sys_oterm_id'),
                   model_uri=KBASE_CDM.read_type_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.read_type_sys_oterm_name = Slot(uri=KBASE_CDM.read_type_sys_oterm_name, name="read_type_sys_oterm_name", curie=KBASE_CDM.curie('read_type_sys_oterm_name'),
                   model_uri=KBASE_CDM.read_type_sys_oterm_name, domain=None, range=Optional[str])

slots.sequencing_technology_sys_oterm_id = Slot(uri=KBASE_CDM.sequencing_technology_sys_oterm_id, name="sequencing_technology_sys_oterm_id", curie=KBASE_CDM.curie('sequencing_technology_sys_oterm_id'),
                   model_uri=KBASE_CDM.sequencing_technology_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.sequencing_technology_sys_oterm_name = Slot(uri=KBASE_CDM.sequencing_technology_sys_oterm_name, name="sequencing_technology_sys_oterm_name", curie=KBASE_CDM.curie('sequencing_technology_sys_oterm_name'),
                   model_uri=KBASE_CDM.sequencing_technology_sys_oterm_name, domain=None, range=Optional[str])

slots.sdt_assembly_id = Slot(uri=KBASE_CDM.sdt_assembly_id, name="sdt_assembly_id", curie=KBASE_CDM.curie('sdt_assembly_id'),
                   model_uri=KBASE_CDM.sdt_assembly_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Assembly\d{7}$'))

slots.sdt_assembly_name = Slot(uri=KBASE_CDM.sdt_assembly_name, name="sdt_assembly_name", curie=KBASE_CDM.curie('sdt_assembly_name'),
                   model_uri=KBASE_CDM.sdt_assembly_name, domain=None, range=Union[str, EntityName])

slots.strain_ref = Slot(uri=KBASE_CDM.strain_ref, name="strain_ref", curie=KBASE_CDM.curie('strain_ref'),
                   model_uri=KBASE_CDM.strain_ref, domain=None, range=Optional[Union[str, EntityName]])

slots.n_contigs = Slot(uri=KBASE_CDM.n_contigs, name="n_contigs", curie=KBASE_CDM.curie('n_contigs'),
                   model_uri=KBASE_CDM.n_contigs, domain=None, range=Optional[Union[int, Count]])

slots.total_size = Slot(uri=KBASE_CDM.total_size, name="total_size", curie=KBASE_CDM.curie('total_size'),
                   model_uri=KBASE_CDM.total_size, domain=None, range=Optional[Union[int, Size]])

slots.sdt_bin_id = Slot(uri=KBASE_CDM.sdt_bin_id, name="sdt_bin_id", curie=KBASE_CDM.curie('sdt_bin_id'),
                   model_uri=KBASE_CDM.sdt_bin_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Bin\d{7}$'))

slots.sdt_bin_name = Slot(uri=KBASE_CDM.sdt_bin_name, name="sdt_bin_name", curie=KBASE_CDM.curie('sdt_bin_name'),
                   model_uri=KBASE_CDM.sdt_bin_name, domain=None, range=Union[str, EntityName])

slots.assembly_ref = Slot(uri=KBASE_CDM.assembly_ref, name="assembly_ref", curie=KBASE_CDM.curie('assembly_ref'),
                   model_uri=KBASE_CDM.assembly_ref, domain=None, range=Optional[Union[str, EntityName]])

slots.contigs = Slot(uri=KBASE_CDM.contigs, name="contigs", curie=KBASE_CDM.curie('contigs'),
                   model_uri=KBASE_CDM.contigs, domain=None, range=Optional[str])

slots.sdt_genome_id = Slot(uri=KBASE_CDM.sdt_genome_id, name="sdt_genome_id", curie=KBASE_CDM.curie('sdt_genome_id'),
                   model_uri=KBASE_CDM.sdt_genome_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Genome\d{7}$'))

slots.sdt_genome_name = Slot(uri=KBASE_CDM.sdt_genome_name, name="sdt_genome_name", curie=KBASE_CDM.curie('sdt_genome_name'),
                   model_uri=KBASE_CDM.sdt_genome_name, domain=None, range=Union[str, EntityName])

slots.genome_ref = Slot(uri=KBASE_CDM.genome_ref, name="genome_ref", curie=KBASE_CDM.curie('genome_ref'),
                   model_uri=KBASE_CDM.genome_ref, domain=None, range=Optional[Union[str, EntityName]])

slots.n_features = Slot(uri=KBASE_CDM.n_features, name="n_features", curie=KBASE_CDM.curie('n_features'),
                   model_uri=KBASE_CDM.n_features, domain=None, range=Optional[Union[int, Count]])

slots.sdt_gene_id = Slot(uri=KBASE_CDM.sdt_gene_id, name="sdt_gene_id", curie=KBASE_CDM.curie('sdt_gene_id'),
                   model_uri=KBASE_CDM.sdt_gene_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Gene\d{7}$'))

slots.sdt_gene_name = Slot(uri=KBASE_CDM.sdt_gene_name, name="sdt_gene_name", curie=KBASE_CDM.curie('sdt_gene_name'),
                   model_uri=KBASE_CDM.sdt_gene_name, domain=None, range=Union[str, EntityName])

slots.contig_number = Slot(uri=KBASE_CDM.contig_number, name="contig_number", curie=KBASE_CDM.curie('contig_number'),
                   model_uri=KBASE_CDM.contig_number, domain=None, range=Optional[int])

slots.strand = Slot(uri=KBASE_CDM.strand, name="strand", curie=KBASE_CDM.curie('strand'),
                   model_uri=KBASE_CDM.strand, domain=None, range=Optional[str],
                   pattern=re.compile(r'^[+-]$'))

slots.start = Slot(uri=KBASE_CDM.start, name="start", curie=KBASE_CDM.curie('start'),
                   model_uri=KBASE_CDM.start, domain=None, range=Optional[int])

slots.stop = Slot(uri=KBASE_CDM.stop, name="stop", curie=KBASE_CDM.curie('stop'),
                   model_uri=KBASE_CDM.stop, domain=None, range=Optional[int])

slots.function = Slot(uri=KBASE_CDM.function, name="function", curie=KBASE_CDM.curie('function'),
                   model_uri=KBASE_CDM.function, domain=None, range=Optional[str])

slots.sdt_strain_id = Slot(uri=KBASE_CDM.sdt_strain_id, name="sdt_strain_id", curie=KBASE_CDM.curie('sdt_strain_id'),
                   model_uri=KBASE_CDM.sdt_strain_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Strain\d{7}$'))

slots.sdt_strain_name = Slot(uri=KBASE_CDM.sdt_strain_name, name="sdt_strain_name", curie=KBASE_CDM.curie('sdt_strain_name'),
                   model_uri=KBASE_CDM.sdt_strain_name, domain=None, range=Union[str, EntityName])

slots.derived_from_strain_ref = Slot(uri=KBASE_CDM.derived_from_strain_ref, name="derived_from_strain_ref", curie=KBASE_CDM.curie('derived_from_strain_ref'),
                   model_uri=KBASE_CDM.derived_from_strain_ref, domain=None, range=Optional[Union[str, EntityName]])

slots.gene_names_changed = Slot(uri=KBASE_CDM.gene_names_changed, name="gene_names_changed", curie=KBASE_CDM.curie('gene_names_changed'),
                   model_uri=KBASE_CDM.gene_names_changed, domain=None, range=Optional[Union[Union[str, EntityName], list[Union[str, EntityName]]]])

slots.sdt_taxon_id = Slot(uri=KBASE_CDM.sdt_taxon_id, name="sdt_taxon_id", curie=KBASE_CDM.curie('sdt_taxon_id'),
                   model_uri=KBASE_CDM.sdt_taxon_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Taxon\d{7}$'))

slots.sdt_taxon_name = Slot(uri=KBASE_CDM.sdt_taxon_name, name="sdt_taxon_name", curie=KBASE_CDM.curie('sdt_taxon_name'),
                   model_uri=KBASE_CDM.sdt_taxon_name, domain=None, range=Union[str, EntityName])

slots.ncbi_taxid = Slot(uri=KBASE_CDM.ncbi_taxid, name="ncbi_taxid", curie=KBASE_CDM.curie('ncbi_taxid'),
                   model_uri=KBASE_CDM.ncbi_taxid, domain=None, range=Optional[int])

slots.sdt_asv_id = Slot(uri=KBASE_CDM.sdt_asv_id, name="sdt_asv_id", curie=KBASE_CDM.curie('sdt_asv_id'),
                   model_uri=KBASE_CDM.sdt_asv_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^ASV\d{7}$'))

slots.sdt_asv_name = Slot(uri=KBASE_CDM.sdt_asv_name, name="sdt_asv_name", curie=KBASE_CDM.curie('sdt_asv_name'),
                   model_uri=KBASE_CDM.sdt_asv_name, domain=None, range=Union[str, EntityName])

slots.sequence = Slot(uri=KBASE_CDM.sequence, name="sequence", curie=KBASE_CDM.curie('sequence'),
                   model_uri=KBASE_CDM.sequence, domain=None, range=Optional[str])

slots.sdt_protocol_id = Slot(uri=KBASE_CDM.sdt_protocol_id, name="sdt_protocol_id", curie=KBASE_CDM.curie('sdt_protocol_id'),
                   model_uri=KBASE_CDM.sdt_protocol_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Protocol\d{7}$'))

slots.sdt_protocol_name = Slot(uri=KBASE_CDM.sdt_protocol_name, name="sdt_protocol_name", curie=KBASE_CDM.curie('sdt_protocol_name'),
                   model_uri=KBASE_CDM.sdt_protocol_name, domain=None, range=Union[str, EntityName])

slots.sdt_image_id = Slot(uri=KBASE_CDM.sdt_image_id, name="sdt_image_id", curie=KBASE_CDM.curie('sdt_image_id'),
                   model_uri=KBASE_CDM.sdt_image_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Image\d{7}$'))

slots.sdt_image_name = Slot(uri=KBASE_CDM.sdt_image_name, name="sdt_image_name", curie=KBASE_CDM.curie('sdt_image_name'),
                   model_uri=KBASE_CDM.sdt_image_name, domain=None, range=Union[str, EntityName])

slots.mime_type = Slot(uri=KBASE_CDM.mime_type, name="mime_type", curie=KBASE_CDM.curie('mime_type'),
                   model_uri=KBASE_CDM.mime_type, domain=None, range=Optional[str])

slots.size = Slot(uri=KBASE_CDM.size, name="size", curie=KBASE_CDM.curie('size'),
                   model_uri=KBASE_CDM.size, domain=None, range=Optional[Union[int, Size]])

slots.dimensions = Slot(uri=KBASE_CDM.dimensions, name="dimensions", curie=KBASE_CDM.curie('dimensions'),
                   model_uri=KBASE_CDM.dimensions, domain=None, range=Optional[str])

slots.sdt_condition_id = Slot(uri=KBASE_CDM.sdt_condition_id, name="sdt_condition_id", curie=KBASE_CDM.curie('sdt_condition_id'),
                   model_uri=KBASE_CDM.sdt_condition_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^Condition\d{7}$'))

slots.sdt_condition_name = Slot(uri=KBASE_CDM.sdt_condition_name, name="sdt_condition_name", curie=KBASE_CDM.curie('sdt_condition_name'),
                   model_uri=KBASE_CDM.sdt_condition_name, domain=None, range=Union[str, EntityName])

slots.sdt_dubseq_library_id = Slot(uri=KBASE_CDM.sdt_dubseq_library_id, name="sdt_dubseq_library_id", curie=KBASE_CDM.curie('sdt_dubseq_library_id'),
                   model_uri=KBASE_CDM.sdt_dubseq_library_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^DubSeqLibrary\d{7}$'))

slots.sdt_dubseq_library_name = Slot(uri=KBASE_CDM.sdt_dubseq_library_name, name="sdt_dubseq_library_name", curie=KBASE_CDM.curie('sdt_dubseq_library_name'),
                   model_uri=KBASE_CDM.sdt_dubseq_library_name, domain=None, range=Union[str, EntityName])

slots.n_fragments = Slot(uri=KBASE_CDM.n_fragments, name="n_fragments", curie=KBASE_CDM.curie('n_fragments'),
                   model_uri=KBASE_CDM.n_fragments, domain=None, range=Optional[Union[int, Count]])

slots.sdt_tnseq_library_id = Slot(uri=KBASE_CDM.sdt_tnseq_library_id, name="sdt_tnseq_library_id", curie=KBASE_CDM.curie('sdt_tnseq_library_id'),
                   model_uri=KBASE_CDM.sdt_tnseq_library_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^TnSeqLibrary\d{7}$'))

slots.sdt_tnseq_library_name = Slot(uri=KBASE_CDM.sdt_tnseq_library_name, name="sdt_tnseq_library_name", curie=KBASE_CDM.curie('sdt_tnseq_library_name'),
                   model_uri=KBASE_CDM.sdt_tnseq_library_name, domain=None, range=Union[str, EntityName])

slots.primers_model = Slot(uri=KBASE_CDM.primers_model, name="primers_model", curie=KBASE_CDM.curie('primers_model'),
                   model_uri=KBASE_CDM.primers_model, domain=None, range=Optional[str])

slots.n_mapped_reads = Slot(uri=KBASE_CDM.n_mapped_reads, name="n_mapped_reads", curie=KBASE_CDM.curie('n_mapped_reads'),
                   model_uri=KBASE_CDM.n_mapped_reads, domain=None, range=Optional[Union[int, Count]])

slots.n_good_reads = Slot(uri=KBASE_CDM.n_good_reads, name="n_good_reads", curie=KBASE_CDM.curie('n_good_reads'),
                   model_uri=KBASE_CDM.n_good_reads, domain=None, range=Optional[Union[int, Count]])

slots.n_genes_hit = Slot(uri=KBASE_CDM.n_genes_hit, name="n_genes_hit", curie=KBASE_CDM.curie('n_genes_hit'),
                   model_uri=KBASE_CDM.n_genes_hit, domain=None, range=Optional[Union[int, Count]])

slots.sdt_enigma_id = Slot(uri=KBASE_CDM.sdt_enigma_id, name="sdt_enigma_id", curie=KBASE_CDM.curie('sdt_enigma_id'),
                   model_uri=KBASE_CDM.sdt_enigma_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^ENIGMA1$'))

slots.type_name = Slot(uri=KBASE_CDM.type_name, name="type_name", curie=KBASE_CDM.curie('type_name'),
                   model_uri=KBASE_CDM.type_name, domain=None, range=str)

slots.field_name = Slot(uri=KBASE_CDM.field_name, name="field_name", curie=KBASE_CDM.curie('field_name'),
                   model_uri=KBASE_CDM.field_name, domain=None, range=str)

slots.cdm_column_name = Slot(uri=KBASE_CDM.cdm_column_name, name="cdm_column_name", curie=KBASE_CDM.curie('cdm_column_name'),
                   model_uri=KBASE_CDM.cdm_column_name, domain=None, range=str)

slots.scalar_type = Slot(uri=KBASE_CDM.scalar_type, name="scalar_type", curie=KBASE_CDM.curie('scalar_type'),
                   model_uri=KBASE_CDM.scalar_type, domain=None, range=Optional[str])

slots.pk = Slot(uri=KBASE_CDM.pk, name="pk", curie=KBASE_CDM.curie('pk'),
                   model_uri=KBASE_CDM.pk, domain=None, range=Optional[Union[bool, Bool]])

slots.upk = Slot(uri=KBASE_CDM.upk, name="upk", curie=KBASE_CDM.curie('upk'),
                   model_uri=KBASE_CDM.upk, domain=None, range=Optional[Union[bool, Bool]])

slots.fk = Slot(uri=KBASE_CDM.fk, name="fk", curie=KBASE_CDM.curie('fk'),
                   model_uri=KBASE_CDM.fk, domain=None, range=Optional[str])

slots.constraint = Slot(uri=KBASE_CDM.constraint, name="constraint", curie=KBASE_CDM.curie('constraint'),
                   model_uri=KBASE_CDM.constraint, domain=None, range=Optional[str])

slots.units_sys_oterm_id = Slot(uri=KBASE_CDM.units_sys_oterm_id, name="units_sys_oterm_id", curie=KBASE_CDM.curie('units_sys_oterm_id'),
                   model_uri=KBASE_CDM.units_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.type_sys_oterm_id = Slot(uri=KBASE_CDM.type_sys_oterm_id, name="type_sys_oterm_id", curie=KBASE_CDM.curie('type_sys_oterm_id'),
                   model_uri=KBASE_CDM.type_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.ddt_ndarray_id = Slot(uri=KBASE_CDM.ddt_ndarray_id, name="ddt_ndarray_id", curie=KBASE_CDM.curie('ddt_ndarray_id'),
                   model_uri=KBASE_CDM.ddt_ndarray_id, domain=None, range=str)

slots.cdm_column_data_type = Slot(uri=KBASE_CDM.cdm_column_data_type, name="cdm_column_data_type", curie=KBASE_CDM.curie('cdm_column_data_type'),
                   model_uri=KBASE_CDM.cdm_column_data_type, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(variable|dimension_variable|dimension_index)$'))

slots.dimension_number = Slot(uri=KBASE_CDM.dimension_number, name="dimension_number", curie=KBASE_CDM.curie('dimension_number'),
                   model_uri=KBASE_CDM.dimension_number, domain=None, range=Optional[int])

slots.variable_number = Slot(uri=KBASE_CDM.variable_number, name="variable_number", curie=KBASE_CDM.curie('variable_number'),
                   model_uri=KBASE_CDM.variable_number, domain=None, range=Optional[int])

slots.dimension_oterm_id = Slot(uri=KBASE_CDM.dimension_oterm_id, name="dimension_oterm_id", curie=KBASE_CDM.curie('dimension_oterm_id'),
                   model_uri=KBASE_CDM.dimension_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.dimension_oterm_name = Slot(uri=KBASE_CDM.dimension_oterm_name, name="dimension_oterm_name", curie=KBASE_CDM.curie('dimension_oterm_name'),
                   model_uri=KBASE_CDM.dimension_oterm_name, domain=None, range=Optional[str])

slots.variable_oterm_id = Slot(uri=KBASE_CDM.variable_oterm_id, name="variable_oterm_id", curie=KBASE_CDM.curie('variable_oterm_id'),
                   model_uri=KBASE_CDM.variable_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.variable_oterm_name = Slot(uri=KBASE_CDM.variable_oterm_name, name="variable_oterm_name", curie=KBASE_CDM.curie('variable_oterm_name'),
                   model_uri=KBASE_CDM.variable_oterm_name, domain=None, range=Optional[str])

slots.unit_sys_oterm_id = Slot(uri=KBASE_CDM.unit_sys_oterm_id, name="unit_sys_oterm_id", curie=KBASE_CDM.curie('unit_sys_oterm_id'),
                   model_uri=KBASE_CDM.unit_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.unit_sys_oterm_name = Slot(uri=KBASE_CDM.unit_sys_oterm_name, name="unit_sys_oterm_name", curie=KBASE_CDM.curie('unit_sys_oterm_name'),
                   model_uri=KBASE_CDM.unit_sys_oterm_name, domain=None, range=Optional[str])

slots.sys_oterm_ontology = Slot(uri=KBASE_CDM.sys_oterm_ontology, name="sys_oterm_ontology", curie=KBASE_CDM.curie('sys_oterm_ontology'),
                   model_uri=KBASE_CDM.sys_oterm_ontology, domain=None, range=Optional[str])

slots.parent_sys_oterm_id = Slot(uri=KBASE_CDM.parent_sys_oterm_id, name="parent_sys_oterm_id", curie=KBASE_CDM.curie('parent_sys_oterm_id'),
                   model_uri=KBASE_CDM.parent_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.sys_oterm_definition = Slot(uri=KBASE_CDM.sys_oterm_definition, name="sys_oterm_definition", curie=KBASE_CDM.curie('sys_oterm_definition'),
                   model_uri=KBASE_CDM.sys_oterm_definition, domain=None, range=Optional[str])

slots.sys_oterm_synonyms = Slot(uri=KBASE_CDM.sys_oterm_synonyms, name="sys_oterm_synonyms", curie=KBASE_CDM.curie('sys_oterm_synonyms'),
                   model_uri=KBASE_CDM.sys_oterm_synonyms, domain=None, range=Optional[str])

slots.sys_oterm_links = Slot(uri=KBASE_CDM.sys_oterm_links, name="sys_oterm_links", curie=KBASE_CDM.curie('sys_oterm_links'),
                   model_uri=KBASE_CDM.sys_oterm_links, domain=None, range=Optional[str])

slots.sys_oterm_properties = Slot(uri=KBASE_CDM.sys_oterm_properties, name="sys_oterm_properties", curie=KBASE_CDM.curie('sys_oterm_properties'),
                   model_uri=KBASE_CDM.sys_oterm_properties, domain=None, range=Optional[str])

slots.sys_process_id = Slot(uri=KBASE_CDM.sys_process_id, name="sys_process_id", curie=KBASE_CDM.curie('sys_process_id'),
                   model_uri=KBASE_CDM.sys_process_id, domain=None, range=str,
                   pattern=re.compile(r'^Process\d{7}$'))

slots.process_type_sys_oterm_id = Slot(uri=KBASE_CDM.process_type_sys_oterm_id, name="process_type_sys_oterm_id", curie=KBASE_CDM.curie('process_type_sys_oterm_id'),
                   model_uri=KBASE_CDM.process_type_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.process_type_sys_oterm_name = Slot(uri=KBASE_CDM.process_type_sys_oterm_name, name="process_type_sys_oterm_name", curie=KBASE_CDM.curie('process_type_sys_oterm_name'),
                   model_uri=KBASE_CDM.process_type_sys_oterm_name, domain=None, range=Optional[str])

slots.person_sys_oterm_id = Slot(uri=KBASE_CDM.person_sys_oterm_id, name="person_sys_oterm_id", curie=KBASE_CDM.curie('person_sys_oterm_id'),
                   model_uri=KBASE_CDM.person_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.person_sys_oterm_name = Slot(uri=KBASE_CDM.person_sys_oterm_name, name="person_sys_oterm_name", curie=KBASE_CDM.curie('person_sys_oterm_name'),
                   model_uri=KBASE_CDM.person_sys_oterm_name, domain=None, range=Optional[str])

slots.campaign_sys_oterm_id = Slot(uri=KBASE_CDM.campaign_sys_oterm_id, name="campaign_sys_oterm_id", curie=KBASE_CDM.curie('campaign_sys_oterm_id'),
                   model_uri=KBASE_CDM.campaign_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.campaign_sys_oterm_name = Slot(uri=KBASE_CDM.campaign_sys_oterm_name, name="campaign_sys_oterm_name", curie=KBASE_CDM.curie('campaign_sys_oterm_name'),
                   model_uri=KBASE_CDM.campaign_sys_oterm_name, domain=None, range=Optional[str])

slots.date_start = Slot(uri=KBASE_CDM.date_start, name="date_start", curie=KBASE_CDM.curie('date_start'),
                   model_uri=KBASE_CDM.date_start, domain=None, range=Optional[Union[str, Date]])

slots.date_end = Slot(uri=KBASE_CDM.date_end, name="date_end", curie=KBASE_CDM.curie('date_end'),
                   model_uri=KBASE_CDM.date_end, domain=None, range=Optional[Union[str, Date]])

slots.input_objects = Slot(uri=KBASE_CDM.input_objects, name="input_objects", curie=KBASE_CDM.curie('input_objects'),
                   model_uri=KBASE_CDM.input_objects, domain=None, range=Optional[Union[str, list[str]]])

slots.output_objects = Slot(uri=KBASE_CDM.output_objects, name="output_objects", curie=KBASE_CDM.curie('output_objects'),
                   model_uri=KBASE_CDM.output_objects, domain=None, range=Optional[Union[str, list[str]]])

slots.input_object_type = Slot(uri=KBASE_CDM.input_object_type, name="input_object_type", curie=KBASE_CDM.curie('input_object_type'),
                   model_uri=KBASE_CDM.input_object_type, domain=None, range=Optional[str])

slots.input_object_name = Slot(uri=KBASE_CDM.input_object_name, name="input_object_name", curie=KBASE_CDM.curie('input_object_name'),
                   model_uri=KBASE_CDM.input_object_name, domain=None, range=Optional[Union[str, EntityName]])

slots.input_index = Slot(uri=KBASE_CDM.input_index, name="input_index", curie=KBASE_CDM.curie('input_index'),
                   model_uri=KBASE_CDM.input_index, domain=None, range=Optional[int])

slots.output_object_type = Slot(uri=KBASE_CDM.output_object_type, name="output_object_type", curie=KBASE_CDM.curie('output_object_type'),
                   model_uri=KBASE_CDM.output_object_type, domain=None, range=Optional[str])

slots.output_object_name = Slot(uri=KBASE_CDM.output_object_name, name="output_object_name", curie=KBASE_CDM.curie('output_object_name'),
                   model_uri=KBASE_CDM.output_object_name, domain=None, range=Optional[Union[str, EntityName]])

slots.output_index = Slot(uri=KBASE_CDM.output_index, name="output_index", curie=KBASE_CDM.curie('output_index'),
                   model_uri=KBASE_CDM.output_index, domain=None, range=Optional[int])

slots.brick_table_name = Slot(uri=KBASE_CDM.brick_table_name, name="brick_table_name", curie=KBASE_CDM.curie('brick_table_name'),
                   model_uri=KBASE_CDM.brick_table_name, domain=None, range=Optional[str],
                   pattern=re.compile(r'^ddt_brick\d{7}$'))

slots.n_dimensions = Slot(uri=KBASE_CDM.n_dimensions, name="n_dimensions", curie=KBASE_CDM.curie('n_dimensions'),
                   model_uri=KBASE_CDM.n_dimensions, domain=None, range=Optional[int])

slots.dimension_sizes = Slot(uri=KBASE_CDM.dimension_sizes, name="dimension_sizes", curie=KBASE_CDM.curie('dimension_sizes'),
                   model_uri=KBASE_CDM.dimension_sizes, domain=None, range=Optional[str],
                   pattern=re.compile(r'^\d+(,\d+)*$'))

slots.n_variables = Slot(uri=KBASE_CDM.n_variables, name="n_variables", curie=KBASE_CDM.curie('n_variables'),
                   model_uri=KBASE_CDM.n_variables, domain=None, range=Optional[int])

slots.total_rows = Slot(uri=KBASE_CDM.total_rows, name="total_rows", curie=KBASE_CDM.curie('total_rows'),
                   model_uri=KBASE_CDM.total_rows, domain=None, range=Optional[int])

slots.associated_entity_type = Slot(uri=KBASE_CDM.associated_entity_type, name="associated_entity_type", curie=KBASE_CDM.curie('associated_entity_type'),
                   model_uri=KBASE_CDM.associated_entity_type, domain=None, range=Optional[str])

slots.associated_entity_names = Slot(uri=KBASE_CDM.associated_entity_names, name="associated_entity_names", curie=KBASE_CDM.curie('associated_entity_names'),
                   model_uri=KBASE_CDM.associated_entity_names, domain=None, range=Optional[Union[Union[str, EntityName], list[Union[str, EntityName]]]])

slots.measurement_type_sys_oterm_id = Slot(uri=KBASE_CDM.measurement_type_sys_oterm_id, name="measurement_type_sys_oterm_id", curie=KBASE_CDM.curie('measurement_type_sys_oterm_id'),
                   model_uri=KBASE_CDM.measurement_type_sys_oterm_id, domain=None, range=Optional[Union[str, OntologyTermID]])

slots.measurement_type_sys_oterm_name = Slot(uri=KBASE_CDM.measurement_type_sys_oterm_name, name="measurement_type_sys_oterm_name", curie=KBASE_CDM.curie('measurement_type_sys_oterm_name'),
                   model_uri=KBASE_CDM.measurement_type_sys_oterm_name, domain=None, range=Optional[str])

slots.creation_date = Slot(uri=KBASE_CDM.creation_date, name="creation_date", curie=KBASE_CDM.curie('creation_date'),
                   model_uri=KBASE_CDM.creation_date, domain=None, range=Optional[Union[str, Date]])

slots.dimension_size = Slot(uri=KBASE_CDM.dimension_size, name="dimension_size", curie=KBASE_CDM.curie('dimension_size'),
                   model_uri=KBASE_CDM.dimension_size, domain=None, range=Optional[int])

slots.dimension_values = Slot(uri=KBASE_CDM.dimension_values, name="dimension_values", curie=KBASE_CDM.curie('dimension_values'),
                   model_uri=KBASE_CDM.dimension_values, domain=None, range=Optional[str])

slots.variable_data_type = Slot(uri=KBASE_CDM.variable_data_type, name="variable_data_type", curie=KBASE_CDM.curie('variable_data_type'),
                   model_uri=KBASE_CDM.variable_data_type, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(float|int|bool|text|oterm_ref|object_ref)$'))

slots.min_value = Slot(uri=KBASE_CDM.min_value, name="min_value", curie=KBASE_CDM.curie('min_value'),
                   model_uri=KBASE_CDM.min_value, domain=None, range=Optional[float])

slots.max_value = Slot(uri=KBASE_CDM.max_value, name="max_value", curie=KBASE_CDM.curie('max_value'),
                   model_uri=KBASE_CDM.max_value, domain=None, range=Optional[float])

slots.SystemOntologyTerm_sys_oterm_id = Slot(uri=KBASE_CDM.sys_oterm_id, name="SystemOntologyTerm_sys_oterm_id", curie=KBASE_CDM.curie('sys_oterm_id'),
                   model_uri=KBASE_CDM.SystemOntologyTerm_sys_oterm_id, domain=SystemOntologyTerm, range=Union[str, SystemOntologyTermSysOtermId])

slots.SystemProcess_sys_process_id = Slot(uri=KBASE_CDM.sys_process_id, name="SystemProcess_sys_process_id", curie=KBASE_CDM.curie('sys_process_id'),
                   model_uri=KBASE_CDM.SystemProcess_sys_process_id, domain=SystemProcess, range=Union[str, SystemProcessSysProcessId],
                   pattern=re.compile(r'^Process\d{7}$'))

slots.DynamicDataArray_ddt_ndarray_id = Slot(uri=KBASE_CDM.ddt_ndarray_id, name="DynamicDataArray_ddt_ndarray_id", curie=KBASE_CDM.curie('ddt_ndarray_id'),
                   model_uri=KBASE_CDM.DynamicDataArray_ddt_ndarray_id, domain=DynamicDataArray, range=Union[str, DynamicDataArrayDdtNdarrayId])
