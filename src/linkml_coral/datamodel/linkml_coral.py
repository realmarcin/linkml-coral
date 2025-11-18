# Auto generated from linkml_coral.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-11-17T23:27:20
# Schema: enigma-cdm
#
# id: https://w3id.org/enigma/enigma-cdm
# description: LinkML schema for ENIGMA (Environmental Molecular Sciences Laboratory Integrated Genomics Initiative) Common Data Model
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

from linkml_runtime.linkml_model.types import Float, Integer, String

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
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = ENIGMA


# Types
class Date(String):
    """ Date in YYYY-MM-DD format """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "Date"
    type_model_uri = ENIGMA.Date


class Time(String):
    """ Time in HH:MM:SS format """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "Time"
    type_model_uri = ENIGMA.Time


class Link(String):
    """ HTTP/HTTPS URL or file path """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "Link"
    type_model_uri = ENIGMA.Link


class Latitude(Float):
    """ Geographic latitude in decimal degrees """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Latitude"
    type_model_uri = ENIGMA.Latitude


class Longitude(Float):
    """ Geographic longitude in decimal degrees """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Longitude"
    type_model_uri = ENIGMA.Longitude


class Count(Integer):
    """ Non-negative integer count """
    type_class_uri = XSD["integer"]
    type_class_curie = "xsd:integer"
    type_name = "Count"
    type_model_uri = ENIGMA.Count


class Size(Float):
    """ Size measurement (non-negative) """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Size"
    type_model_uri = ENIGMA.Size


class Depth(Float):
    """ Depth measurement """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Depth"
    type_model_uri = ENIGMA.Depth


class Elevation(Float):
    """ Elevation measurement """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Elevation"
    type_model_uri = ENIGMA.Elevation


class Rate(Float):
    """ Rate as a fraction between 0 and 1 """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Rate"
    type_model_uri = ENIGMA.Rate


# Class references
class ProcessProcessId(extended_str):
    pass


class LocationLocationId(extended_str):
    pass


class SampleSampleId(extended_str):
    pass


class TaxonTaxonId(extended_str):
    pass


class OTUOtuId(extended_str):
    pass


class ConditionConditionId(extended_str):
    pass


class StrainStrainId(extended_str):
    pass


class CommunityCommunityId(extended_str):
    pass


class ReadsReadsId(extended_str):
    pass


class AssemblyAssemblyId(extended_str):
    pass


class GenomeGenomeId(extended_str):
    pass


class GeneGeneId(extended_str):
    pass


class BinBinId(extended_str):
    pass


class ProtocolProtocolId(extended_str):
    pass


class ImageImageId(extended_str):
    pass


class TnSeqLibraryTnseqLibraryId(extended_str):
    pass


class DubSeqLibraryDubseqLibraryId(extended_str):
    pass


@dataclass(repr=False)
class Process(YAMLRoot):
    """
    Process entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Process"]
    class_class_curie: ClassVar[str] = "enigma:Process"
    class_name: ClassVar[str] = "Process"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Process

    process_id: Union[str, ProcessProcessId] = None
    process_process: str = None
    process_person: str = None
    process_campaign: str = None
    process_input_objects: Union[str, list[str]] = None
    process_output_objects: Union[str, list[str]] = None
    process_protocol: Optional[Union[str, ProtocolProtocolId]] = None
    process_date_start: Optional[Union[str, Date]] = None
    process_date_end: Optional[Union[str, Date]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.process_id):
            self.MissingRequiredField("process_id")
        if not isinstance(self.process_id, ProcessProcessId):
            self.process_id = ProcessProcessId(self.process_id)

        if self._is_empty(self.process_process):
            self.MissingRequiredField("process_process")
        if not isinstance(self.process_process, str):
            self.process_process = str(self.process_process)

        if self._is_empty(self.process_person):
            self.MissingRequiredField("process_person")
        if not isinstance(self.process_person, str):
            self.process_person = str(self.process_person)

        if self._is_empty(self.process_campaign):
            self.MissingRequiredField("process_campaign")
        if not isinstance(self.process_campaign, str):
            self.process_campaign = str(self.process_campaign)

        if self._is_empty(self.process_input_objects):
            self.MissingRequiredField("process_input_objects")
        if not isinstance(self.process_input_objects, list):
            self.process_input_objects = [self.process_input_objects] if self.process_input_objects is not None else []
        self.process_input_objects = [v if isinstance(v, str) else str(v) for v in self.process_input_objects]

        if self._is_empty(self.process_output_objects):
            self.MissingRequiredField("process_output_objects")
        if not isinstance(self.process_output_objects, list):
            self.process_output_objects = [self.process_output_objects] if self.process_output_objects is not None else []
        self.process_output_objects = [v if isinstance(v, str) else str(v) for v in self.process_output_objects]

        if self.process_protocol is not None and not isinstance(self.process_protocol, ProtocolProtocolId):
            self.process_protocol = ProtocolProtocolId(self.process_protocol)

        if self.process_date_start is not None and not isinstance(self.process_date_start, Date):
            self.process_date_start = Date(self.process_date_start)

        if self.process_date_end is not None and not isinstance(self.process_date_end, Date):
            self.process_date_end = Date(self.process_date_end)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Location(YAMLRoot):
    """
    Location entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Location"]
    class_class_curie: ClassVar[str] = "enigma:Location"
    class_name: ClassVar[str] = "Location"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Location

    location_id: Union[str, LocationLocationId] = None
    location_name: str = None
    location_latitude: Union[float, Latitude] = None
    location_longitude: Union[float, Longitude] = None
    location_continent: str = None
    location_country: str = None
    location_region: str = None
    location_biome: str = None
    location_feature: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.location_id):
            self.MissingRequiredField("location_id")
        if not isinstance(self.location_id, LocationLocationId):
            self.location_id = LocationLocationId(self.location_id)

        if self._is_empty(self.location_name):
            self.MissingRequiredField("location_name")
        if not isinstance(self.location_name, str):
            self.location_name = str(self.location_name)

        if self._is_empty(self.location_latitude):
            self.MissingRequiredField("location_latitude")
        if not isinstance(self.location_latitude, Latitude):
            self.location_latitude = Latitude(self.location_latitude)

        if self._is_empty(self.location_longitude):
            self.MissingRequiredField("location_longitude")
        if not isinstance(self.location_longitude, Longitude):
            self.location_longitude = Longitude(self.location_longitude)

        if self._is_empty(self.location_continent):
            self.MissingRequiredField("location_continent")
        if not isinstance(self.location_continent, str):
            self.location_continent = str(self.location_continent)

        if self._is_empty(self.location_country):
            self.MissingRequiredField("location_country")
        if not isinstance(self.location_country, str):
            self.location_country = str(self.location_country)

        if self._is_empty(self.location_region):
            self.MissingRequiredField("location_region")
        if not isinstance(self.location_region, str):
            self.location_region = str(self.location_region)

        if self._is_empty(self.location_biome):
            self.MissingRequiredField("location_biome")
        if not isinstance(self.location_biome, str):
            self.location_biome = str(self.location_biome)

        if self.location_feature is not None and not isinstance(self.location_feature, str):
            self.location_feature = str(self.location_feature)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Sample(YAMLRoot):
    """
    Sample entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Sample"]
    class_class_curie: ClassVar[str] = "enigma:Sample"
    class_name: ClassVar[str] = "Sample"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Sample

    sample_id: Union[str, SampleSampleId] = None
    sample_name: str = None
    sample_location: Union[str, LocationLocationId] = None
    sample_date: Union[str, Date] = None
    sample_env_package: str = None
    sample_depth: Optional[Union[float, Depth]] = None
    sample_elevation: Optional[Union[float, Elevation]] = None
    sample_time: Optional[Union[str, Time]] = None
    sample_timezone: Optional[Union[str, Time]] = None
    sample_material: Optional[str] = None
    sample_description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sample_id):
            self.MissingRequiredField("sample_id")
        if not isinstance(self.sample_id, SampleSampleId):
            self.sample_id = SampleSampleId(self.sample_id)

        if self._is_empty(self.sample_name):
            self.MissingRequiredField("sample_name")
        if not isinstance(self.sample_name, str):
            self.sample_name = str(self.sample_name)

        if self._is_empty(self.sample_location):
            self.MissingRequiredField("sample_location")
        if not isinstance(self.sample_location, LocationLocationId):
            self.sample_location = LocationLocationId(self.sample_location)

        if self._is_empty(self.sample_date):
            self.MissingRequiredField("sample_date")
        if not isinstance(self.sample_date, Date):
            self.sample_date = Date(self.sample_date)

        if self._is_empty(self.sample_env_package):
            self.MissingRequiredField("sample_env_package")
        if not isinstance(self.sample_env_package, str):
            self.sample_env_package = str(self.sample_env_package)

        if self.sample_depth is not None and not isinstance(self.sample_depth, Depth):
            self.sample_depth = Depth(self.sample_depth)

        if self.sample_elevation is not None and not isinstance(self.sample_elevation, Elevation):
            self.sample_elevation = Elevation(self.sample_elevation)

        if self.sample_time is not None and not isinstance(self.sample_time, Time):
            self.sample_time = Time(self.sample_time)

        if self.sample_timezone is not None and not isinstance(self.sample_timezone, Time):
            self.sample_timezone = Time(self.sample_timezone)

        if self.sample_material is not None and not isinstance(self.sample_material, str):
            self.sample_material = str(self.sample_material)

        if self.sample_description is not None and not isinstance(self.sample_description, str):
            self.sample_description = str(self.sample_description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Taxon(YAMLRoot):
    """
    Taxon entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Taxon"]
    class_class_curie: ClassVar[str] = "enigma:Taxon"
    class_name: ClassVar[str] = "Taxon"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Taxon

    taxon_id: Union[str, TaxonTaxonId] = None
    taxon_name: str = None
    taxon_ncbi_taxid: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.taxon_id):
            self.MissingRequiredField("taxon_id")
        if not isinstance(self.taxon_id, TaxonTaxonId):
            self.taxon_id = TaxonTaxonId(self.taxon_id)

        if self._is_empty(self.taxon_name):
            self.MissingRequiredField("taxon_name")
        if not isinstance(self.taxon_name, str):
            self.taxon_name = str(self.taxon_name)

        if self.taxon_ncbi_taxid is not None and not isinstance(self.taxon_ncbi_taxid, str):
            self.taxon_ncbi_taxid = str(self.taxon_ncbi_taxid)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OTU(YAMLRoot):
    """
    OTU entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["OTU"]
    class_class_curie: ClassVar[str] = "enigma:OTU"
    class_name: ClassVar[str] = "OTU"
    class_model_uri: ClassVar[URIRef] = ENIGMA.OTU

    otu_id: Union[str, OTUOtuId] = None
    otu_name: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.otu_id):
            self.MissingRequiredField("otu_id")
        if not isinstance(self.otu_id, OTUOtuId):
            self.otu_id = OTUOtuId(self.otu_id)

        if self._is_empty(self.otu_name):
            self.MissingRequiredField("otu_name")
        if not isinstance(self.otu_name, str):
            self.otu_name = str(self.otu_name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Condition(YAMLRoot):
    """
    Condition entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Condition"]
    class_class_curie: ClassVar[str] = "enigma:Condition"
    class_name: ClassVar[str] = "Condition"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Condition

    condition_id: Union[str, ConditionConditionId] = None
    condition_name: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.condition_id):
            self.MissingRequiredField("condition_id")
        if not isinstance(self.condition_id, ConditionConditionId):
            self.condition_id = ConditionConditionId(self.condition_id)

        if self._is_empty(self.condition_name):
            self.MissingRequiredField("condition_name")
        if not isinstance(self.condition_name, str):
            self.condition_name = str(self.condition_name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Strain(YAMLRoot):
    """
    Strain entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Strain"]
    class_class_curie: ClassVar[str] = "enigma:Strain"
    class_name: ClassVar[str] = "Strain"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Strain

    strain_id: Union[str, StrainStrainId] = None
    strain_name: str = None
    strain_description: Optional[str] = None
    strain_genome: Optional[Union[str, GenomeGenomeId]] = None
    strain_derived_from: Optional[Union[str, StrainStrainId]] = None
    strain_genes_changed: Optional[Union[Union[str, GeneGeneId], list[Union[str, GeneGeneId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.strain_id):
            self.MissingRequiredField("strain_id")
        if not isinstance(self.strain_id, StrainStrainId):
            self.strain_id = StrainStrainId(self.strain_id)

        if self._is_empty(self.strain_name):
            self.MissingRequiredField("strain_name")
        if not isinstance(self.strain_name, str):
            self.strain_name = str(self.strain_name)

        if self.strain_description is not None and not isinstance(self.strain_description, str):
            self.strain_description = str(self.strain_description)

        if self.strain_genome is not None and not isinstance(self.strain_genome, GenomeGenomeId):
            self.strain_genome = GenomeGenomeId(self.strain_genome)

        if self.strain_derived_from is not None and not isinstance(self.strain_derived_from, StrainStrainId):
            self.strain_derived_from = StrainStrainId(self.strain_derived_from)

        if not isinstance(self.strain_genes_changed, list):
            self.strain_genes_changed = [self.strain_genes_changed] if self.strain_genes_changed is not None else []
        self.strain_genes_changed = [v if isinstance(v, GeneGeneId) else GeneGeneId(v) for v in self.strain_genes_changed]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Community(YAMLRoot):
    """
    Community entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Community"]
    class_class_curie: ClassVar[str] = "enigma:Community"
    class_name: ClassVar[str] = "Community"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Community

    community_id: Union[str, CommunityCommunityId] = None
    community_name: str = None
    community_community_type: Union[str, "CommunityTypeEnum"] = None
    community_sample: Optional[Union[str, SampleSampleId]] = None
    community_parent_community: Optional[Union[str, CommunityCommunityId]] = None
    community_condition: Optional[Union[str, ConditionConditionId]] = None
    community_defined_strains: Optional[Union[str, StrainStrainId]] = None
    community_description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.community_id):
            self.MissingRequiredField("community_id")
        if not isinstance(self.community_id, CommunityCommunityId):
            self.community_id = CommunityCommunityId(self.community_id)

        if self._is_empty(self.community_name):
            self.MissingRequiredField("community_name")
        if not isinstance(self.community_name, str):
            self.community_name = str(self.community_name)

        if self._is_empty(self.community_community_type):
            self.MissingRequiredField("community_community_type")
        if not isinstance(self.community_community_type, CommunityTypeEnum):
            self.community_community_type = CommunityTypeEnum(self.community_community_type)

        if self.community_sample is not None and not isinstance(self.community_sample, SampleSampleId):
            self.community_sample = SampleSampleId(self.community_sample)

        if self.community_parent_community is not None and not isinstance(self.community_parent_community, CommunityCommunityId):
            self.community_parent_community = CommunityCommunityId(self.community_parent_community)

        if self.community_condition is not None and not isinstance(self.community_condition, ConditionConditionId):
            self.community_condition = ConditionConditionId(self.community_condition)

        if self.community_defined_strains is not None and not isinstance(self.community_defined_strains, StrainStrainId):
            self.community_defined_strains = StrainStrainId(self.community_defined_strains)

        if self.community_description is not None and not isinstance(self.community_description, str):
            self.community_description = str(self.community_description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Reads(YAMLRoot):
    """
    Reads entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Reads"]
    class_class_curie: ClassVar[str] = "enigma:Reads"
    class_name: ClassVar[str] = "Reads"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Reads

    reads_id: Union[str, ReadsReadsId] = None
    reads_name: str = None
    reads_read_count: Union[int, Count] = None
    reads_read_type: Union[str, "ReadTypeEnum"] = None
    reads_sequencing_technology: Union[str, "SequencingTechnologyEnum"] = None
    reads_link: Union[str, Link] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.reads_id):
            self.MissingRequiredField("reads_id")
        if not isinstance(self.reads_id, ReadsReadsId):
            self.reads_id = ReadsReadsId(self.reads_id)

        if self._is_empty(self.reads_name):
            self.MissingRequiredField("reads_name")
        if not isinstance(self.reads_name, str):
            self.reads_name = str(self.reads_name)

        if self._is_empty(self.reads_read_count):
            self.MissingRequiredField("reads_read_count")
        if not isinstance(self.reads_read_count, Count):
            self.reads_read_count = Count(self.reads_read_count)

        if self._is_empty(self.reads_read_type):
            self.MissingRequiredField("reads_read_type")
        if not isinstance(self.reads_read_type, ReadTypeEnum):
            self.reads_read_type = ReadTypeEnum(self.reads_read_type)

        if self._is_empty(self.reads_sequencing_technology):
            self.MissingRequiredField("reads_sequencing_technology")
        if not isinstance(self.reads_sequencing_technology, SequencingTechnologyEnum):
            self.reads_sequencing_technology = SequencingTechnologyEnum(self.reads_sequencing_technology)

        if self._is_empty(self.reads_link):
            self.MissingRequiredField("reads_link")
        if not isinstance(self.reads_link, Link):
            self.reads_link = Link(self.reads_link)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Assembly(YAMLRoot):
    """
    Assembly entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Assembly"]
    class_class_curie: ClassVar[str] = "enigma:Assembly"
    class_name: ClassVar[str] = "Assembly"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Assembly

    assembly_id: Union[str, AssemblyAssemblyId] = None
    assembly_name: str = None
    assembly_n_contigs: Union[int, Count] = None
    assembly_strain: Optional[Union[str, StrainStrainId]] = None
    assembly_link: Optional[Union[str, Link]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.assembly_id):
            self.MissingRequiredField("assembly_id")
        if not isinstance(self.assembly_id, AssemblyAssemblyId):
            self.assembly_id = AssemblyAssemblyId(self.assembly_id)

        if self._is_empty(self.assembly_name):
            self.MissingRequiredField("assembly_name")
        if not isinstance(self.assembly_name, str):
            self.assembly_name = str(self.assembly_name)

        if self._is_empty(self.assembly_n_contigs):
            self.MissingRequiredField("assembly_n_contigs")
        if not isinstance(self.assembly_n_contigs, Count):
            self.assembly_n_contigs = Count(self.assembly_n_contigs)

        if self.assembly_strain is not None and not isinstance(self.assembly_strain, StrainStrainId):
            self.assembly_strain = StrainStrainId(self.assembly_strain)

        if self.assembly_link is not None and not isinstance(self.assembly_link, Link):
            self.assembly_link = Link(self.assembly_link)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Genome(YAMLRoot):
    """
    Genome entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Genome"]
    class_class_curie: ClassVar[str] = "enigma:Genome"
    class_name: ClassVar[str] = "Genome"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Genome

    genome_id: Union[str, GenomeGenomeId] = None
    genome_name: str = None
    genome_n_contigs: Union[int, Count] = None
    genome_n_features: Union[int, Count] = None
    genome_link: Union[str, Link] = None
    genome_strain: Optional[Union[str, StrainStrainId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.genome_id):
            self.MissingRequiredField("genome_id")
        if not isinstance(self.genome_id, GenomeGenomeId):
            self.genome_id = GenomeGenomeId(self.genome_id)

        if self._is_empty(self.genome_name):
            self.MissingRequiredField("genome_name")
        if not isinstance(self.genome_name, str):
            self.genome_name = str(self.genome_name)

        if self._is_empty(self.genome_n_contigs):
            self.MissingRequiredField("genome_n_contigs")
        if not isinstance(self.genome_n_contigs, Count):
            self.genome_n_contigs = Count(self.genome_n_contigs)

        if self._is_empty(self.genome_n_features):
            self.MissingRequiredField("genome_n_features")
        if not isinstance(self.genome_n_features, Count):
            self.genome_n_features = Count(self.genome_n_features)

        if self._is_empty(self.genome_link):
            self.MissingRequiredField("genome_link")
        if not isinstance(self.genome_link, Link):
            self.genome_link = Link(self.genome_link)

        if self.genome_strain is not None and not isinstance(self.genome_strain, StrainStrainId):
            self.genome_strain = StrainStrainId(self.genome_strain)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Gene(YAMLRoot):
    """
    Gene entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Gene"]
    class_class_curie: ClassVar[str] = "enigma:Gene"
    class_name: ClassVar[str] = "Gene"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Gene

    gene_id: Union[str, GeneGeneId] = None
    gene_gene_id: str = None
    gene_genome: Union[str, GenomeGenomeId] = None
    gene_contig_number: int = None
    gene_strand: Union[str, "StrandEnum"] = None
    gene_start: int = None
    gene_stop: int = None
    gene_aliases: Optional[Union[str, list[str]]] = empty_list()
    gene_function: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.gene_id):
            self.MissingRequiredField("gene_id")
        if not isinstance(self.gene_id, GeneGeneId):
            self.gene_id = GeneGeneId(self.gene_id)

        if self._is_empty(self.gene_gene_id):
            self.MissingRequiredField("gene_gene_id")
        if not isinstance(self.gene_gene_id, str):
            self.gene_gene_id = str(self.gene_gene_id)

        if self._is_empty(self.gene_genome):
            self.MissingRequiredField("gene_genome")
        if not isinstance(self.gene_genome, GenomeGenomeId):
            self.gene_genome = GenomeGenomeId(self.gene_genome)

        if self._is_empty(self.gene_contig_number):
            self.MissingRequiredField("gene_contig_number")
        if not isinstance(self.gene_contig_number, int):
            self.gene_contig_number = int(self.gene_contig_number)

        if self._is_empty(self.gene_strand):
            self.MissingRequiredField("gene_strand")
        if not isinstance(self.gene_strand, StrandEnum):
            self.gene_strand = StrandEnum(self.gene_strand)

        if self._is_empty(self.gene_start):
            self.MissingRequiredField("gene_start")
        if not isinstance(self.gene_start, int):
            self.gene_start = int(self.gene_start)

        if self._is_empty(self.gene_stop):
            self.MissingRequiredField("gene_stop")
        if not isinstance(self.gene_stop, int):
            self.gene_stop = int(self.gene_stop)

        if not isinstance(self.gene_aliases, list):
            self.gene_aliases = [self.gene_aliases] if self.gene_aliases is not None else []
        self.gene_aliases = [v if isinstance(v, str) else str(v) for v in self.gene_aliases]

        if self.gene_function is not None and not isinstance(self.gene_function, str):
            self.gene_function = str(self.gene_function)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Bin(YAMLRoot):
    """
    Bin entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Bin"]
    class_class_curie: ClassVar[str] = "enigma:Bin"
    class_name: ClassVar[str] = "Bin"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Bin

    bin_id: Union[str, BinBinId] = None
    bin_name: str = None
    bin_assembly: Union[str, AssemblyAssemblyId] = None
    bin_contigs: Union[str, list[str]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.bin_id):
            self.MissingRequiredField("bin_id")
        if not isinstance(self.bin_id, BinBinId):
            self.bin_id = BinBinId(self.bin_id)

        if self._is_empty(self.bin_name):
            self.MissingRequiredField("bin_name")
        if not isinstance(self.bin_name, str):
            self.bin_name = str(self.bin_name)

        if self._is_empty(self.bin_assembly):
            self.MissingRequiredField("bin_assembly")
        if not isinstance(self.bin_assembly, AssemblyAssemblyId):
            self.bin_assembly = AssemblyAssemblyId(self.bin_assembly)

        if self._is_empty(self.bin_contigs):
            self.MissingRequiredField("bin_contigs")
        if not isinstance(self.bin_contigs, list):
            self.bin_contigs = [self.bin_contigs] if self.bin_contigs is not None else []
        self.bin_contigs = [v if isinstance(v, str) else str(v) for v in self.bin_contigs]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Protocol(YAMLRoot):
    """
    Protocol entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Protocol"]
    class_class_curie: ClassVar[str] = "enigma:Protocol"
    class_name: ClassVar[str] = "Protocol"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Protocol

    protocol_id: Union[str, ProtocolProtocolId] = None
    protocol_name: str = None
    protocol_description: Optional[str] = None
    protocol_link: Optional[Union[str, Link]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.protocol_id):
            self.MissingRequiredField("protocol_id")
        if not isinstance(self.protocol_id, ProtocolProtocolId):
            self.protocol_id = ProtocolProtocolId(self.protocol_id)

        if self._is_empty(self.protocol_name):
            self.MissingRequiredField("protocol_name")
        if not isinstance(self.protocol_name, str):
            self.protocol_name = str(self.protocol_name)

        if self.protocol_description is not None and not isinstance(self.protocol_description, str):
            self.protocol_description = str(self.protocol_description)

        if self.protocol_link is not None and not isinstance(self.protocol_link, Link):
            self.protocol_link = Link(self.protocol_link)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Image(YAMLRoot):
    """
    Image entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["Image"]
    class_class_curie: ClassVar[str] = "enigma:Image"
    class_name: ClassVar[str] = "Image"
    class_model_uri: ClassVar[URIRef] = ENIGMA.Image

    image_id: Union[str, ImageImageId] = None
    image_name: str = None
    image_description: Optional[str] = None
    image_MIME_type: Optional[str] = None
    image_size: Optional[Union[float, Size]] = None
    image_dimensions: Optional[str] = None
    image_link: Optional[Union[str, Link]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.image_id):
            self.MissingRequiredField("image_id")
        if not isinstance(self.image_id, ImageImageId):
            self.image_id = ImageImageId(self.image_id)

        if self._is_empty(self.image_name):
            self.MissingRequiredField("image_name")
        if not isinstance(self.image_name, str):
            self.image_name = str(self.image_name)

        if self.image_description is not None and not isinstance(self.image_description, str):
            self.image_description = str(self.image_description)

        if self.image_MIME_type is not None and not isinstance(self.image_MIME_type, str):
            self.image_MIME_type = str(self.image_MIME_type)

        if self.image_size is not None and not isinstance(self.image_size, Size):
            self.image_size = Size(self.image_size)

        if self.image_dimensions is not None and not isinstance(self.image_dimensions, str):
            self.image_dimensions = str(self.image_dimensions)

        if self.image_link is not None and not isinstance(self.image_link, Link):
            self.image_link = Link(self.image_link)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TnSeqLibrary(YAMLRoot):
    """
    TnSeq_Library entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["TnSeqLibrary"]
    class_class_curie: ClassVar[str] = "enigma:TnSeqLibrary"
    class_name: ClassVar[str] = "TnSeq_Library"
    class_model_uri: ClassVar[URIRef] = ENIGMA.TnSeqLibrary

    tnseq_library_id: Union[str, TnSeqLibraryTnseqLibraryId] = None
    tnseq_library_name: str = None
    tnseq_library_genome: Union[str, GenomeGenomeId] = None
    tnseq_library_primers_model: str = None
    tnseq_library_n_mapped_reads: Optional[int] = None
    tnseq_library_n_barcodes: Optional[int] = None
    tnseq_library_n_usable_barcodes: Optional[int] = None
    tnseq_library_n_insertion_locations: Optional[int] = None
    tnseq_library_hit_rate_essential: Optional[Union[float, Rate]] = None
    tnseq_library_hit_rate_other: Optional[Union[float, Rate]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.tnseq_library_id):
            self.MissingRequiredField("tnseq_library_id")
        if not isinstance(self.tnseq_library_id, TnSeqLibraryTnseqLibraryId):
            self.tnseq_library_id = TnSeqLibraryTnseqLibraryId(self.tnseq_library_id)

        if self._is_empty(self.tnseq_library_name):
            self.MissingRequiredField("tnseq_library_name")
        if not isinstance(self.tnseq_library_name, str):
            self.tnseq_library_name = str(self.tnseq_library_name)

        if self._is_empty(self.tnseq_library_genome):
            self.MissingRequiredField("tnseq_library_genome")
        if not isinstance(self.tnseq_library_genome, GenomeGenomeId):
            self.tnseq_library_genome = GenomeGenomeId(self.tnseq_library_genome)

        if self._is_empty(self.tnseq_library_primers_model):
            self.MissingRequiredField("tnseq_library_primers_model")
        if not isinstance(self.tnseq_library_primers_model, str):
            self.tnseq_library_primers_model = str(self.tnseq_library_primers_model)

        if self.tnseq_library_n_mapped_reads is not None and not isinstance(self.tnseq_library_n_mapped_reads, int):
            self.tnseq_library_n_mapped_reads = int(self.tnseq_library_n_mapped_reads)

        if self.tnseq_library_n_barcodes is not None and not isinstance(self.tnseq_library_n_barcodes, int):
            self.tnseq_library_n_barcodes = int(self.tnseq_library_n_barcodes)

        if self.tnseq_library_n_usable_barcodes is not None and not isinstance(self.tnseq_library_n_usable_barcodes, int):
            self.tnseq_library_n_usable_barcodes = int(self.tnseq_library_n_usable_barcodes)

        if self.tnseq_library_n_insertion_locations is not None and not isinstance(self.tnseq_library_n_insertion_locations, int):
            self.tnseq_library_n_insertion_locations = int(self.tnseq_library_n_insertion_locations)

        if self.tnseq_library_hit_rate_essential is not None and not isinstance(self.tnseq_library_hit_rate_essential, Rate):
            self.tnseq_library_hit_rate_essential = Rate(self.tnseq_library_hit_rate_essential)

        if self.tnseq_library_hit_rate_other is not None and not isinstance(self.tnseq_library_hit_rate_other, Rate):
            self.tnseq_library_hit_rate_other = Rate(self.tnseq_library_hit_rate_other)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DubSeqLibrary(YAMLRoot):
    """
    DubSeq_Library entity in the ENIGMA data model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENIGMA["DubSeqLibrary"]
    class_class_curie: ClassVar[str] = "enigma:DubSeqLibrary"
    class_name: ClassVar[str] = "DubSeq_Library"
    class_model_uri: ClassVar[URIRef] = ENIGMA.DubSeqLibrary

    dubseq_library_id: Union[str, DubSeqLibraryDubseqLibraryId] = None
    dubseq_library_name: str = None
    dubseq_library_genome: Union[str, GenomeGenomeId] = None
    dubseq_library_n_fragments: Optional[Union[int, Count]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.dubseq_library_id):
            self.MissingRequiredField("dubseq_library_id")
        if not isinstance(self.dubseq_library_id, DubSeqLibraryDubseqLibraryId):
            self.dubseq_library_id = DubSeqLibraryDubseqLibraryId(self.dubseq_library_id)

        if self._is_empty(self.dubseq_library_name):
            self.MissingRequiredField("dubseq_library_name")
        if not isinstance(self.dubseq_library_name, str):
            self.dubseq_library_name = str(self.dubseq_library_name)

        if self._is_empty(self.dubseq_library_genome):
            self.MissingRequiredField("dubseq_library_genome")
        if not isinstance(self.dubseq_library_genome, GenomeGenomeId):
            self.dubseq_library_genome = GenomeGenomeId(self.dubseq_library_genome)

        if self.dubseq_library_n_fragments is not None and not isinstance(self.dubseq_library_n_fragments, Count):
            self.dubseq_library_n_fragments = Count(self.dubseq_library_n_fragments)

        super().__post_init__(**kwargs)


# Enumerations
class ExperimentalContextEnum(EnumDefinitionImpl):
    """
    Context describing experimental design.
    """
    series_type = PermissibleValue(
        text="series_type",
        title="Series Type",
        description="Context describing the purpose of a series.")
    condition = PermissibleValue(
        text="condition",
        title="Condition",
        description="A human-readable description of an experimental condition.")
    method = PermissibleValue(
        text="method",
        title="Method",
        description="A description of one or more methods used in an experiment.")
    algorithm_parameter = PermissibleValue(
        text="algorithm_parameter",
        title="Algorithm Parameter",
        description="A description of one or more algorithm parameters.")
    date = PermissibleValue(
        text="date",
        title="Date",
        description="A date, formatted as YYYY-MM-DD.")
    time = PermissibleValue(
        text="time",
        title="Time",
        description="A time, formatted as HH:MM (see DateTime to include the date).")
    comment = PermissibleValue(
        text="comment",
        title="Comment",
        description="A human-readable comment.")
    instrument = PermissibleValue(
        text="instrument",
        title="Instrument",
        description="A description of instrument(s) used.")
    category = PermissibleValue(
        text="category",
        title="Category",
        description="A human-readable description of a category.")
    homogenized = PermissibleValue(
        text="homogenized",
        title="Homogenized",
        description="Homogenized.")
    anaerobic = PermissibleValue(
        text="anaerobic",
        title="Anaerobic",
        description="Anaerobic.")
    aerobic = PermissibleValue(
        text="aerobic",
        title="Aerobic",
        description="Aerobic.")
    undisturbed = PermissibleValue(
        text="undisturbed",
        title="Undisturbed",
        description="Undisturbed.")
    datetime = PermissibleValue(
        text="datetime",
        title="DateTime",
        description="DateTime.")
    time_zone = PermissibleValue(
        text="time_zone",
        title="Time Zone",
        description="Time Zone, e.g., PDT")
    description = PermissibleValue(
        text="description",
        title="Description",
        description="Description.")
    link = PermissibleValue(
        text="link",
        title="Link",
        description="Link to other data, e.g., a DOI or URL.")
    experimental_process = PermissibleValue(
        text="experimental_process",
        title="Experimental Process",
        description="Category of experimental process used to create a dataset.")
    person = PermissibleValue(
        text="person",
        title="Person",
        description="Name of a person.  Note that ENIGMA people should be listed as 'ENIGMA personnel' instead.")
    campaign = PermissibleValue(
        text="campaign",
        title="Campaign",
        description="Campaign.")
    input = PermissibleValue(
        text="input",
        title="Input",
        description="Input.")
    output = PermissibleValue(
        text="output",
        title="Output",
        description="Output.")
    control = PermissibleValue(
        text="control",
        title="Control",
        description="Control.")
    replicate = PermissibleValue(
        text="replicate",
        title="Replicate",
        description="Replicate.")
    subsample = PermissibleValue(
        text="subsample",
        title="Subsample",
        description="Subsample.")
    protocol = PermissibleValue(
        text="protocol",
        title="Protocol",
        description="Protocol.")
    availability = PermissibleValue(
        text="availability",
        title="Availability",
        description="Boolean property indicating whether something is available.")
    ionization_mode = PermissibleValue(
        text="ionization_mode",
        title="Ionization Mode",
        description="Ionization mode used in a mass spec experiment.")
    usability = PermissibleValue(
        text="usability",
        title="Usability",
        description="Usability.")
    barcode = PermissibleValue(
        text="barcode",
        title="Barcode",
        description="Barcode.")
    microplate_name = PermissibleValue(
        text="microplate_name",
        title="Microplate Name",
        description="Microplate Name.")
    microplate_well_name = PermissibleValue(
        text="microplate_well_name",
        title="Microplate Well Name",
        description="Microplate Well Name.")
    microplate = PermissibleValue(
        text="microplate",
        title="Microplate",
        description="Microplate.")
    publication = PermissibleValue(
        text="publication",
        title="Publication",
        description="Publication.")
    database = PermissibleValue(
        text="database",
        title="Database",
        description="Database.")
    obsolete = PermissibleValue(
        text="obsolete",
        title="Obsolete",
        description="Obsolete.")
    index = PermissibleValue(
        text="index",
        title="Index",
        description="Index.")
    internal_standard = PermissibleValue(
        text="internal_standard",
        title="Internal Standard",
        description="Internal Standard.")

    _defn = EnumDefinition(
        name="ExperimentalContextEnum",
        description="Context describing experimental design.",
    )

class SeriesTypeEnum(EnumDefinitionImpl):
    """
    Context describing the purpose of a series.
    """
    time_series = PermissibleValue(
        text="time_series",
        title="Time Series",
        description="A time series, in which a series of measurements was taken at different timepoints.")
    replicate_series = PermissibleValue(
        text="replicate_series",
        title="Replicate Series",
        description="A replicate series, e.g., biological or technical replicates.")

    _defn = EnumDefinition(
        name="SeriesTypeEnum",
        description="Context describing the purpose of a series.",
    )

class MathematicalContextEnum(EnumDefinitionImpl):
    """
    Microtypes that provide mathematical context.
    """
    normalized = PermissibleValue(
        text="normalized",
        title="Normalized",
        description="Normalized; describe how in the Method or Protocol.")
    relative = PermissibleValue(
        text="relative",
        title="Relative",
        description="Human-readable context saying what another microtype is measured relative to.")
    increase = PermissibleValue(
        text="increase",
        title="Increase",
        description="Increase.")
    decrease = PermissibleValue(
        text="decrease",
        title="Decrease",
        description="Decrease.")
    gain = PermissibleValue(
        text="gain",
        title="Gain",
        description="Gain.")
    loss = PermissibleValue(
        text="loss",
        title="Loss",
        description="Loss.")
    nearest = PermissibleValue(
        text="nearest",
        title="Nearest",
        description="Nearest.")
    variable_name = PermissibleValue(
        text="variable_name",
        title="Variable Name",
        description="Variable Name.")
    variable_type = PermissibleValue(
        text="variable_type",
        title="Variable Type",
        description="Variable Type.")
    dimension = PermissibleValue(
        text="dimension",
        title="Dimension",
        description="Dimension.")
    high = PermissibleValue(
        text="high",
        title="High",
        description="High.")
    low = PermissibleValue(
        text="low",
        title="Low",
        description="Low.")
    numerator = PermissibleValue(
        text="numerator",
        title="Numerator",
        description="Numerator.")
    denominator = PermissibleValue(
        text="denominator",
        title="Denominator",
        description="Denominator.")
    cumulative = PermissibleValue(
        text="cumulative",
        title="Cumulative",
        description="Cumulative.")

    _defn = EnumDefinition(
        name="MathematicalContextEnum",
        description="Microtypes that provide mathematical context.",
    )

class ChemicalContextEnum(EnumDefinitionImpl):
    """
    Describes the context of a molecule in a chemical reaction or experiment.
    """
    molecule = PermissibleValue(
        text="molecule",
        title="Molecule",
        description="Use when the type of molecule varies along a dimension.")
    reaction = PermissibleValue(
        text="reaction",
        title="Reaction",
        description="Human-readable description of a chemical reaction.")
    surface_type = PermissibleValue(
        text="surface_type",
        title="Surface Type",
        description="Human-readable description of a type of surface.")
    bead_type = PermissibleValue(
        text="bead_type",
        title="Bead Type",
        description="Human-readable description of the type of bead used in a (geo)chemical experiment.")
    bead_size = PermissibleValue(
        text="bead_size",
        title="Bead Size",
        description="Size of a bead used in a (geo)chemical experiment.")
    thermodynamic_context = PermissibleValue(
        text="thermodynamic_context",
        title="Thermodynamic Context",
        description="Thermodynamic context for a reaction.")
    specific_activity = PermissibleValue(
        text="specific_activity",
        title="Specific Activity",
        description="Rate of reaction multiplied by the volume, divided by mass of protein.")
    wavelength = PermissibleValue(
        text="wavelength",
        title="Wavelength",
        description="Wavelength of radiation.")
    physiochemical_state = PermissibleValue(
        text="physiochemical_state",
        title="Physiochemical State",
        description="Human-readable context for the state or type of matter, e.g., dissolved, or in soil")
    detection_limit = PermissibleValue(
        text="detection_limit",
        title="Detection Limit",
        description="Detection limit for an instrument or experiment.")
    reagent = PermissibleValue(
        text="reagent",
        title="Reagent",
        description="Reagent.")
    organic = PermissibleValue(
        text="organic",
        title="Organic",
        description="Use as context, for example, to label inorganic or organic carbon.")
    molecular_weight = PermissibleValue(
        text="molecular_weight",
        title="Molecular Weight",
        description="Molecular Weight.")
    reference_compound = PermissibleValue(
        text="reference_compound",
        title="Reference Compound",
        description="Reference Compound.")
    isotope = PermissibleValue(
        text="isotope",
        title="Isotope",
        description="Isotope.")
    redox = PermissibleValue(
        text="redox",
        title="Redox",
        description="Redox.")
    exact_mass = PermissibleValue(
        text="exact_mass",
        title="Exact Mass",
        description="Exact Mass.")

    _defn = EnumDefinition(
        name="ChemicalContextEnum",
        description="Describes the context of a molecule in a chemical reaction or experiment.",
    )

class BiologicalContextEnum(EnumDefinitionImpl):
    """
    Biological Context.
    """
    cell = PermissibleValue(
        text="cell",
        title="Cell",
        description="Cell.")
    colony = PermissibleValue(
        text="colony",
        title="Colony",
        description="Colony.")
    strain = PermissibleValue(
        text="strain",
        title="Strain",
        description="Strain of microbe, or isolate ID.")
    taxon = PermissibleValue(
        text="taxon",
        title="Taxon",
        description="Taxon.")
    media = PermissibleValue(
        text="media",
        title="Media",
        description="Media type.")
    metabolite = PermissibleValue(
        text="metabolite",
        title="Metabolite",
        description="Metabolite.")
    enzyme_substrate = PermissibleValue(
        text="enzyme_substrate",
        title="Enzyme Substrate",
        description="Enzyme Substrate.")
    gene = PermissibleValue(
        text="gene",
        title="Gene",
        description="Gene.")
    protein = PermissibleValue(
        text="protein",
        title="Protein",
        description="Protein.")
    protein_annotation = PermissibleValue(
        text="protein_annotation",
        title="Protein Annotation",
        description="Protein Annotation.")
    operon = PermissibleValue(
        text="operon",
        title="Operon",
        description="Operon.")
    ribosome = PermissibleValue(
        text="ribosome",
        title="Ribosome",
        description="Ribosome.")
    growth_parameter = PermissibleValue(
        text="growth_parameter",
        title="Growth Parameter",
        description="Growth Parameter.")
    gene_regulation = PermissibleValue(
        text="gene_regulation",
        title="Gene Regulation",
        description="Gene Regulation.")
    taxonomic_level = PermissibleValue(
        text="taxonomic_level",
        title="Taxonomic Level",
        description="Taxonomic Level.")
    strain_change = PermissibleValue(
        text="strain_change",
        title="Strain Change",
        description="Strain Change.")
    knockout = PermissibleValue(
        text="knockout",
        title="Knockout",
        description="Knockout.")
    environment = PermissibleValue(
        text="environment",
        title="Environment",
        description="Environment.")
    ecology = PermissibleValue(
        text="ecology",
        title="Ecology",
        description="Ecology.")
    sequencing = PermissibleValue(
        text="sequencing",
        title="Sequencing",
        description="Sequencing.")
    asv = PermissibleValue(
        text="asv",
        title="ASV",
        description="Amplicon Sequence Variant.")
    esv = PermissibleValue(
        text="esv",
        title="ESV",
        description="ESV.")
    community = PermissibleValue(
        text="community",
        title="Community",
        description="Community.")
    genome = PermissibleValue(
        text="genome",
        title="Genome",
        description="Genome.")
    gene_annotation = PermissibleValue(
        text="gene_annotation",
        title="Gene Annotation",
        description="Gene Annotation.")
    knockout_library = PermissibleValue(
        text="knockout_library",
        title="Knockout Library",
        description="Knockout Library.")
    assembly = PermissibleValue(
        text="assembly",
        title="Assembly",
        description="Assembly.")
    bin = PermissibleValue(
        text="bin",
        title="Bin",
        description="Bin (metagenomic).")
    overexpression_library = PermissibleValue(
        text="overexpression_library",
        title="Overexpression Library",
        description="Overexpression Library.")
    growth_stage = PermissibleValue(
        text="growth_stage",
        title="Growth Stage",
        description="Growth Stage.")
    otu = PermissibleValue(
        text="otu",
        title="OTU",
        description="OTU.")

    _defn = EnumDefinition(
        name="BiologicalContextEnum",
        description="Biological Context.",
    )

class TaxonomicLevelEnum(EnumDefinitionImpl):
    """
    Taxonomic Level.
    """
    kingdom = PermissibleValue(
        text="kingdom",
        title="Kingdom",
        description="Kingdom.")
    phylum = PermissibleValue(
        text="phylum",
        title="Phylum",
        description="Phylum.")
    order = PermissibleValue(
        text="order",
        title="Order",
        description="Order.")
    family = PermissibleValue(
        text="family",
        title="Family",
        description="Family.")
    genus = PermissibleValue(
        text="genus",
        title="Genus",
        description="Genus.")
    species = PermissibleValue(
        text="species",
        title="Species",
        description="Species.")
    taxonomic_domain = PermissibleValue(
        text="taxonomic_domain",
        title="Taxonomic Domain",
        description="Taxonomic Domain.")

    _defn = EnumDefinition(
        name="TaxonomicLevelEnum",
        description="Taxonomic Level.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "class",
            PermissibleValue(
                text="class",
                title="Class",
                description="Class."))

class StrainChangeEffectEnum(EnumDefinitionImpl):
    """
    Strain Change Effect.
    """
    synonymous = PermissibleValue(
        text="synonymous",
        title="Synonymous",
        description="Synonymous.")
    non_synonymous = PermissibleValue(
        text="non_synonymous",
        title="Non-Synonymous",
        description="Non-Synonymous.")
    frameshift = PermissibleValue(
        text="frameshift",
        title="Frameshift",
        description="Frameshift.")
    stop = PermissibleValue(
        text="stop",
        title="Stop",
        description="Stop.")

    _defn = EnumDefinition(
        name="StrainChangeEffectEnum",
        description="Strain Change Effect.",
    )

class CommunityAssemblyProcessEnum(EnumDefinitionImpl):
    """
    Community Assembly Process.
    """
    variable_selection = PermissibleValue(
        text="variable_selection",
        title="Variable Selection",
        description="Variable Selection.")
    homogenous_selection = PermissibleValue(
        text="homogenous_selection",
        title="Homogenous Selection",
        description="Homogenous Selection.")
    dispersal_limitation = PermissibleValue(
        text="dispersal_limitation",
        title="Dispersal Limitation",
        description="Dispersal Limitation.")
    homogenizing_dispersal = PermissibleValue(
        text="homogenizing_dispersal",
        title="Homogenizing Dispersal",
        description="Homogenizing Dispersal.")
    undominated = PermissibleValue(
        text="undominated",
        title="Undominated",
        description="Undominated.")

    _defn = EnumDefinition(
        name="CommunityAssemblyProcessEnum",
        description="Community Assembly Process.",
    )

class ReadTypeEnum(EnumDefinitionImpl):
    """
    Read Type.
    """
    paired_end_read = PermissibleValue(
        text="paired_end_read",
        title="Paired End Read",
        description="Paired End Read.")
    single_end_read = PermissibleValue(
        text="single_end_read",
        title="Single End Read",
        description="Single End Read.")

    _defn = EnumDefinition(
        name="ReadTypeEnum",
        description="Read Type.",
    )

class SequencingTechnologyEnum(EnumDefinitionImpl):
    """
    Sequencing Technology.
    """
    illumina = PermissibleValue(
        text="illumina",
        title="Illumina",
        description="Illumina.")
    pacbio = PermissibleValue(
        text="pacbio",
        title="Pacbio",
        description="Pacbio.")
    oxford_nanopore = PermissibleValue(
        text="oxford_nanopore",
        title="Oxford Nanopore",
        description="Oxford Nanopore.")

    _defn = EnumDefinition(
        name="SequencingTechnologyEnum",
        description="Sequencing Technology.",
    )

class MeasurementEnum(EnumDefinitionImpl):
    """
    Measurement.
    """
    ph = PermissibleValue(
        text="ph",
        title="pH",
        description="pH.")
    time_elapsed = PermissibleValue(
        text="time_elapsed",
        title="Time Elapsed",
        description="Time Elapsed.")
    temperature = PermissibleValue(
        text="temperature",
        title="Temperature",
        description="Temperature.")
    conductivity = PermissibleValue(
        text="conductivity",
        title="Conductivity",
        description="Conductivity.")
    redox_potential = PermissibleValue(
        text="redox_potential",
        title="Redox Potential",
        description="Redox Potential.")
    count = PermissibleValue(
        text="count",
        title="Count",
        description="Count.")
    optical_density = PermissibleValue(
        text="optical_density",
        title="Optical Density",
        description="Optical Density.")
    size = PermissibleValue(
        text="size",
        title="Size",
        description="Size.")
    concentration = PermissibleValue(
        text="concentration",
        title="Concentration",
        description="Concentration.")
    hybridization_intensity = PermissibleValue(
        text="hybridization_intensity",
        title="Hybridization Intensity",
        description="Hybridization Intensity.")
    expression_level = PermissibleValue(
        text="expression_level",
        title="Expression Level",
        description="Expression Level.")
    enzyme_activity = PermissibleValue(
        text="enzyme_activity",
        title="Enzyme Activity",
        description="Enzyme Activity.")
    absorbance = PermissibleValue(
        text="absorbance",
        title="Absorbance",
        description="Absorbance.")
    heat = PermissibleValue(
        text="heat",
        title="Heat",
        description="Heat.")
    mass = PermissibleValue(
        text="mass",
        title="Mass",
        description="Mass.")
    fitness_score = PermissibleValue(
        text="fitness_score",
        title="Fitness Score",
        description="Fitness Score.")
    genetic_interaction_score = PermissibleValue(
        text="genetic_interaction_score",
        title="Genetic Interaction Score",
        description="Genetic Interaction Score.")
    stoichiometric_ratio = PermissibleValue(
        text="stoichiometric_ratio",
        title="Stoichiometric Ratio",
        description="Stoichiometric Ratio.")
    relative_abundance = PermissibleValue(
        text="relative_abundance",
        title="Relative Abundance",
        description="Relative amounts of multiple categories of the same object.")
    binary = PermissibleValue(
        text="binary",
        title="Binary",
        description="Binary.")
    pressure = PermissibleValue(
        text="pressure",
        title="Pressure",
        description="Pressure.")
    turbidity = PermissibleValue(
        text="turbidity",
        title="Turbidity",
        description="Turbidity.")
    rate = PermissibleValue(
        text="rate",
        title="Rate",
        description="Rate.")
    sequence = PermissibleValue(
        text="sequence",
        title="Sequence",
        description="Sequence.")
    salinity = PermissibleValue(
        text="salinity",
        title="Salinity",
        description="Salinity.")
    resistivity = PermissibleValue(
        text="resistivity",
        title="Resistivity",
        description="Resistivity.")
    saturation = PermissibleValue(
        text="saturation",
        title="Saturation",
        description="Saturation.")
    density = PermissibleValue(
        text="density",
        title="Density",
        description="Density.")
    charge = PermissibleValue(
        text="charge",
        title="Charge",
        description="Charge.")
    wind_speed = PermissibleValue(
        text="wind_speed",
        title="Wind Speed",
        description="Wind Speed.")
    solar_radiation = PermissibleValue(
        text="solar_radiation",
        title="Solar Radiation",
        description="Solar Radiation.")
    rainfall = PermissibleValue(
        text="rainfall",
        title="Rainfall",
        description="Rainfall.")
    wind_direction = PermissibleValue(
        text="wind_direction",
        title="Wind Direction",
        description="Wind Direction.")
    relative_humidity = PermissibleValue(
        text="relative_humidity",
        title="Relative Humidity",
        description="Relative Humidity.")
    error_range = PermissibleValue(
        text="error_range",
        title="Error Range",
        description="Error Range.")
    ion_intensity = PermissibleValue(
        text="ion_intensity",
        title="Ion Intensity",
        description="Ion Intensity.")
    amount = PermissibleValue(
        text="amount",
        title="Amount",
        description="Absolute amount of a substance, such as an element.  See also: concentration.")
    isotope_ratio = PermissibleValue(
        text="isotope_ratio",
        title="Isotope Ratio",
        description="Isotope Ratio.")
    sequence_identity = PermissibleValue(
        text="sequence_identity",
        title="Sequence Identity",
        description="Sequence Identity.")
    sequence_similarity = PermissibleValue(
        text="sequence_similarity",
        title="Sequence Similarity",
        description="Sequence Similarity.")
    relative_evolutionary_divergence = PermissibleValue(
        text="relative_evolutionary_divergence",
        title="Relative Evolutionary Divergence",
        description="Relative Evolutionary Divergence.")
    genome_quality = PermissibleValue(
        text="genome_quality",
        title="Genome Quality",
        description="Genome Quality.")
    jukes_cantor_distance = PermissibleValue(
        text="jukes_cantor_distance",
        title="Jukes-Cantor Distance",
        description="Jukes-Cantor Distance.")
    dew_point = PermissibleValue(
        text="dew_point",
        title="Dew Point",
        description="Dew Point.")
    fluorescence = PermissibleValue(
        text="fluorescence",
        title="Fluorescence",
        description="Fluorescence.")

    _defn = EnumDefinition(
        name="MeasurementEnum",
        description="Measurement.",
    )

class StatisticEnum(EnumDefinitionImpl):
    """
    Statistic.
    """
    average = PermissibleValue(
        text="average",
        title="Average",
        description="Average.")
    difference = PermissibleValue(
        text="difference",
        title="Difference",
        description="Difference.")
    standard_deviation = PermissibleValue(
        text="standard_deviation",
        title="Standard Deviation",
        description="Standard Deviation.")
    standard_error = PermissibleValue(
        text="standard_error",
        title="Standard Error",
        description="Standard Error.")
    minimum = PermissibleValue(
        text="minimum",
        title="Minimum",
        description="Minimum.")
    maximum = PermissibleValue(
        text="maximum",
        title="Maximum",
        description="Maximum.")
    median = PermissibleValue(
        text="median",
        title="Median",
        description="Median.")
    ratio = PermissibleValue(
        text="ratio",
        title="Ratio",
        description="Ratio.")
    log_ratio = PermissibleValue(
        text="log_ratio",
        title="Log Ratio",
        description="Log Ratio.")
    p_value = PermissibleValue(
        text="p_value",
        title="p Value",
        description="p Value.")
    t_score = PermissibleValue(
        text="t_score",
        title="T Score",
        description="T Score.")
    frequency = PermissibleValue(
        text="frequency",
        title="Frequency",
        description="Frequency.")
    fold_enrichment = PermissibleValue(
        text="fold_enrichment",
        title="Fold Enrichment",
        description="Fold Enrichment.")
    confidence = PermissibleValue(
        text="confidence",
        title="Confidence",
        description="Confidence.")
    evaluation = PermissibleValue(
        text="evaluation",
        title="Evaluation",
        description="Evaluation.")
    correlation = PermissibleValue(
        text="correlation",
        title="Correlation",
        description="Correlation.")
    multivariate_analysis = PermissibleValue(
        text="multivariate_analysis",
        title="Multivariate Analysis",
        description="Multivariate Analysis.")
    coefficient_of_variation = PermissibleValue(
        text="coefficient_of_variation",
        title="Coefficient of Variation",
        description="Coefficient of Variation.")

    _defn = EnumDefinition(
        name="StatisticEnum",
        description="Statistic.",
    )

class StrandEnum(EnumDefinitionImpl):
    """
    Strand of DNA
    """
    forward = PermissibleValue(
        text="forward",
        title="Forward",
        description="Forward.")
    reverse_complement = PermissibleValue(
        text="reverse_complement",
        title="Reverse Complement",
        description="Reverse Complement.")

    _defn = EnumDefinition(
        name="StrandEnum",
        description="Strand of DNA",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "+",
            PermissibleValue(
                text="+",
                title="Forward (symbol notation)",
                description="Forward strand using + symbol notation.",
                meaning=ME["0000187"]))
        setattr(cls, "-",
            PermissibleValue(
                text="-",
                title="Reverse Complement (symbol notation)",
                description="Reverse complement strand using - symbol notation.",
                meaning=ME["0000188"]))

class SequenceTypeEnum(EnumDefinitionImpl):
    """
    Sequence Type.
    """
    its_sequence = PermissibleValue(
        text="its_sequence",
        title="ITS Sequence",
        description="ITS Sequence.")
    genome_sequence = PermissibleValue(
        text="genome_sequence",
        title="Genome Sequence",
        description="Genome Sequence.")

    _defn = EnumDefinition(
        name="SequenceTypeEnum",
        description="Sequence Type.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "16s_sequence",
            PermissibleValue(
                text="16s_sequence",
                title="16S Sequence",
                description="16S Sequence."))
        setattr(cls, "18s_sequence",
            PermissibleValue(
                text="18s_sequence",
                title="18S Sequence",
                description="18S Sequence."))

class StrainChangeTypeEnum(EnumDefinitionImpl):
    """
    Strain Change Type.
    """
    insertion = PermissibleValue(
        text="insertion",
        title="Insertion",
        description="Insertion.")
    deletion = PermissibleValue(
        text="deletion",
        title="Deletion",
        description="Deletion.")
    substitution = PermissibleValue(
        text="substitution",
        title="Substitution",
        description="Substitution.")

    _defn = EnumDefinition(
        name="StrainChangeTypeEnum",
        description="Strain Change Type.",
    )

class CommunityTypeEnum(EnumDefinitionImpl):
    """
    Community Type.
    """
    isolate_community = PermissibleValue(
        text="isolate_community",
        title="Isolate Community",
        description="Isolate Community.")
    enrichment = PermissibleValue(
        text="enrichment",
        title="Enrichment",
        description="Enrichment.")
    active_fraction = PermissibleValue(
        text="active_fraction",
        title="Active Fraction",
        description="Active Fraction.")
    assemblage = PermissibleValue(
        text="assemblage",
        title="Assemblage",
        description="Assemblage.")
    environmental_community = PermissibleValue(
        text="environmental_community",
        title="Environmental Community",
        description="Environmental Community.")

    _defn = EnumDefinition(
        name="CommunityTypeEnum",
        description="Community Type.",
    )

class ControlEnum(EnumDefinitionImpl):
    """
    Control.
    """
    negative_control = PermissibleValue(
        text="negative_control",
        title="Negative Control",
        description="Negative Control.")
    positive_control = PermissibleValue(
        text="positive_control",
        title="Positive Control",
        description="Positive Control.")
    low_control = PermissibleValue(
        text="low_control",
        title="Low Control",
        description="Low Control.")
    high_control = PermissibleValue(
        text="high_control",
        title="High Control",
        description="High Control.")
    control_name = PermissibleValue(
        text="control_name",
        title="Control Name",
        description="Control Name.")

    _defn = EnumDefinition(
        name="ControlEnum",
        description="Control.",
    )

class PositionEnum(EnumDefinitionImpl):
    """
    Position.
    """
    top = PermissibleValue(
        text="top",
        title="Top",
        description="Use as context for locations, e.g., the top end of a depth measurement.")
    bottom = PermissibleValue(
        text="bottom",
        title="Bottom",
        description="Use as context for locations, e.g., the bottom end of a depth measurement.")
    upper = PermissibleValue(
        text="upper",
        title="Upper",
        description="Upper.")
    lower = PermissibleValue(
        text="lower",
        title="Lower",
        description="Lower.")
    middle = PermissibleValue(
        text="middle",
        title="Middle",
        description="Middle.")

    _defn = EnumDefinition(
        name="PositionEnum",
        description="Position.",
    )

class IonizationModeEnum(EnumDefinitionImpl):
    """
    Ionization mode used in a mass spec experiment.
    """
    positive_polarity = PermissibleValue(
        text="positive_polarity",
        title="Positive Polarity",
        description="Positive Polarity (ionization mode for MS experiment).")
    negative_polarity = PermissibleValue(
        text="negative_polarity",
        title="Negative Polarity",
        description="Negative Polarity (ionization mode for MS experiment).")

    _defn = EnumDefinition(
        name="IonizationModeEnum",
        description="Ionization mode used in a mass spec experiment.",
    )

class GeologicZoneEnum(EnumDefinitionImpl):
    """
    Geologic Zone.
    """
    vadose_zone = PermissibleValue(
        text="vadose_zone",
        title="Vadose Zone",
        description="Vadose Zone.")
    variably_saturated_zone = PermissibleValue(
        text="variably_saturated_zone",
        title="Variably Saturated Zone",
        description="Variably Saturated Zone.")
    saturated_zone = PermissibleValue(
        text="saturated_zone",
        title="Saturated Zone",
        description="Saturated Zone.")

    _defn = EnumDefinition(
        name="GeologicZoneEnum",
        description="Geologic Zone.",
    )

class GrowthStageEnum(EnumDefinitionImpl):
    """
    Growth Stage.
    """
    enrichment_growth = PermissibleValue(
        text="enrichment_growth",
        title="Enrichment Growth",
        description="Preincubation or enrichment of a microbial sample before plating for colony picking/isolation.")
    inoculation = PermissibleValue(
        text="inoculation",
        title="Inoculation",
        description="Inoculation.")
    lag_phase = PermissibleValue(
        text="lag_phase",
        title="Lag Phase",
        description="Lag Phase.")
    exponential_phase = PermissibleValue(
        text="exponential_phase",
        title="Exponential Phase",
        description="Exponential Phase.")
    stationary_phase = PermissibleValue(
        text="stationary_phase",
        title="Stationary Phase",
        description="Stationary Phase.")
    colony_formation_on_solid_media = PermissibleValue(
        text="colony_formation_on_solid_media",
        title="Colony Formation on Solid Media",
        description="Colony formation on solid media, during the process of microbial isolation")
    single_colony_growth_in_liquid_media = PermissibleValue(
        text="single_colony_growth_in_liquid_media",
        title="Single Colony Growth in Liquid Media",
        description="Single colony growth in liquid media, after microbial isolation")

    _defn = EnumDefinition(
        name="GrowthStageEnum",
        description="Growth Stage.",
    )

class FlagellarArrangementEnum(EnumDefinitionImpl):
    """
    Flagellar Arrangement.
    """
    monotrichous = PermissibleValue(
        text="monotrichous",
        title="Monotrichous",
        description="A single flagellum extending from one end of the cell.")
    amphitrichous = PermissibleValue(
        text="amphitrichous",
        title="Amphitrichous",
        description="Single or multiple flagella extending from both ends of the cell.")
    lophotrichous = PermissibleValue(
        text="lophotrichous",
        title="Lophotrichous",
        description="Tuft of flagella extending from one end or both ends of the cell.")
    peritrichous = PermissibleValue(
        text="peritrichous",
        title="Peritrichous",
        description="Multiple flagella distributed over the entire cell.")

    _defn = EnumDefinition(
        name="FlagellarArrangementEnum",
        description="Flagellar Arrangement.",
    )

class CellShapeEnum(EnumDefinitionImpl):
    """
    Cell Shape.
    """
    rod = PermissibleValue(
        text="rod",
        title="Rod",
        description="Rod.")
    rod_vibrio = PermissibleValue(
        text="rod_vibrio",
        title="Rod-vibrio",
        description="Rod-vibrio.")
    oval = PermissibleValue(
        text="oval",
        title="Oval",
        description="Oval.")
    irregular_oval = PermissibleValue(
        text="irregular_oval",
        title="Irregular Oval",
        description="Irregular Oval.")
    spherical = PermissibleValue(
        text="spherical",
        title="Spherical",
        description="Spherical.")
    pleomorphic = PermissibleValue(
        text="pleomorphic",
        title="Pleomorphic",
        description="Pleomorphic.")

    _defn = EnumDefinition(
        name="CellShapeEnum",
        description="Cell Shape.",
    )

# Slots
class slots:
    pass

slots.process_id = Slot(uri=ENIGMA.process_id, name="process_id", curie=ENIGMA.curie('process_id'),
                   model_uri=ENIGMA.process_id, domain=None, range=URIRef)

slots.process_process = Slot(uri=ENIGMA.process_process, name="process_process", curie=ENIGMA.curie('process_process'),
                   model_uri=ENIGMA.process_process, domain=None, range=str)

slots.process_person = Slot(uri=ENIGMA.process_person, name="process_person", curie=ENIGMA.curie('process_person'),
                   model_uri=ENIGMA.process_person, domain=None, range=str)

slots.process_campaign = Slot(uri=ENIGMA.process_campaign, name="process_campaign", curie=ENIGMA.curie('process_campaign'),
                   model_uri=ENIGMA.process_campaign, domain=None, range=str)

slots.process_protocol = Slot(uri=ENIGMA.process_protocol, name="process_protocol", curie=ENIGMA.curie('process_protocol'),
                   model_uri=ENIGMA.process_protocol, domain=None, range=Optional[Union[str, ProtocolProtocolId]])

slots.process_date_start = Slot(uri=ENIGMA.process_date_start, name="process_date_start", curie=ENIGMA.curie('process_date_start'),
                   model_uri=ENIGMA.process_date_start, domain=None, range=Optional[Union[str, Date]])

slots.process_date_end = Slot(uri=ENIGMA.process_date_end, name="process_date_end", curie=ENIGMA.curie('process_date_end'),
                   model_uri=ENIGMA.process_date_end, domain=None, range=Optional[Union[str, Date]])

slots.process_input_objects = Slot(uri=ENIGMA.process_input_objects, name="process_input_objects", curie=ENIGMA.curie('process_input_objects'),
                   model_uri=ENIGMA.process_input_objects, domain=None, range=Union[str, list[str]])

slots.process_output_objects = Slot(uri=ENIGMA.process_output_objects, name="process_output_objects", curie=ENIGMA.curie('process_output_objects'),
                   model_uri=ENIGMA.process_output_objects, domain=None, range=Union[str, list[str]])

slots.location_id = Slot(uri=ENIGMA.location_id, name="location_id", curie=ENIGMA.curie('location_id'),
                   model_uri=ENIGMA.location_id, domain=None, range=URIRef)

slots.location_name = Slot(uri=ENIGMA.location_name, name="location_name", curie=ENIGMA.curie('location_name'),
                   model_uri=ENIGMA.location_name, domain=None, range=str)

slots.location_latitude = Slot(uri=ENIGMA.location_latitude, name="location_latitude", curie=ENIGMA.curie('location_latitude'),
                   model_uri=ENIGMA.location_latitude, domain=None, range=Union[float, Latitude])

slots.location_longitude = Slot(uri=ENIGMA.location_longitude, name="location_longitude", curie=ENIGMA.curie('location_longitude'),
                   model_uri=ENIGMA.location_longitude, domain=None, range=Union[float, Longitude])

slots.location_continent = Slot(uri=ENIGMA.location_continent, name="location_continent", curie=ENIGMA.curie('location_continent'),
                   model_uri=ENIGMA.location_continent, domain=None, range=str)

slots.location_country = Slot(uri=ENIGMA.location_country, name="location_country", curie=ENIGMA.curie('location_country'),
                   model_uri=ENIGMA.location_country, domain=None, range=str)

slots.location_region = Slot(uri=ENIGMA.location_region, name="location_region", curie=ENIGMA.curie('location_region'),
                   model_uri=ENIGMA.location_region, domain=None, range=str)

slots.location_biome = Slot(uri=ENIGMA.location_biome, name="location_biome", curie=ENIGMA.curie('location_biome'),
                   model_uri=ENIGMA.location_biome, domain=None, range=str)

slots.location_feature = Slot(uri=ENIGMA.location_feature, name="location_feature", curie=ENIGMA.curie('location_feature'),
                   model_uri=ENIGMA.location_feature, domain=None, range=Optional[str])

slots.sample_id = Slot(uri=ENIGMA.sample_id, name="sample_id", curie=ENIGMA.curie('sample_id'),
                   model_uri=ENIGMA.sample_id, domain=None, range=URIRef)

slots.sample_name = Slot(uri=ENIGMA.sample_name, name="sample_name", curie=ENIGMA.curie('sample_name'),
                   model_uri=ENIGMA.sample_name, domain=None, range=str)

slots.sample_location = Slot(uri=ENIGMA.sample_location, name="sample_location", curie=ENIGMA.curie('sample_location'),
                   model_uri=ENIGMA.sample_location, domain=None, range=Union[str, LocationLocationId])

slots.sample_depth = Slot(uri=ENIGMA.sample_depth, name="sample_depth", curie=ENIGMA.curie('sample_depth'),
                   model_uri=ENIGMA.sample_depth, domain=None, range=Optional[Union[float, Depth]])

slots.sample_elevation = Slot(uri=ENIGMA.sample_elevation, name="sample_elevation", curie=ENIGMA.curie('sample_elevation'),
                   model_uri=ENIGMA.sample_elevation, domain=None, range=Optional[Union[float, Elevation]])

slots.sample_date = Slot(uri=ENIGMA.sample_date, name="sample_date", curie=ENIGMA.curie('sample_date'),
                   model_uri=ENIGMA.sample_date, domain=None, range=Union[str, Date])

slots.sample_time = Slot(uri=ENIGMA.sample_time, name="sample_time", curie=ENIGMA.curie('sample_time'),
                   model_uri=ENIGMA.sample_time, domain=None, range=Optional[Union[str, Time]])

slots.sample_timezone = Slot(uri=ENIGMA.sample_timezone, name="sample_timezone", curie=ENIGMA.curie('sample_timezone'),
                   model_uri=ENIGMA.sample_timezone, domain=None, range=Optional[Union[str, Time]])

slots.sample_material = Slot(uri=ENIGMA.sample_material, name="sample_material", curie=ENIGMA.curie('sample_material'),
                   model_uri=ENIGMA.sample_material, domain=None, range=Optional[str])

slots.sample_env_package = Slot(uri=ENIGMA.sample_env_package, name="sample_env_package", curie=ENIGMA.curie('sample_env_package'),
                   model_uri=ENIGMA.sample_env_package, domain=None, range=str)

slots.sample_description = Slot(uri=ENIGMA.sample_description, name="sample_description", curie=ENIGMA.curie('sample_description'),
                   model_uri=ENIGMA.sample_description, domain=None, range=Optional[str])

slots.taxon_id = Slot(uri=ENIGMA.taxon_id, name="taxon_id", curie=ENIGMA.curie('taxon_id'),
                   model_uri=ENIGMA.taxon_id, domain=None, range=URIRef)

slots.taxon_name = Slot(uri=ENIGMA.taxon_name, name="taxon_name", curie=ENIGMA.curie('taxon_name'),
                   model_uri=ENIGMA.taxon_name, domain=None, range=str)

slots.taxon_ncbi_taxid = Slot(uri=ENIGMA.taxon_ncbi_taxid, name="taxon_ncbi_taxid", curie=ENIGMA.curie('taxon_ncbi_taxid'),
                   model_uri=ENIGMA.taxon_ncbi_taxid, domain=None, range=Optional[str])

slots.otu_id = Slot(uri=ENIGMA.otu_id, name="otu_id", curie=ENIGMA.curie('otu_id'),
                   model_uri=ENIGMA.otu_id, domain=None, range=URIRef)

slots.otu_name = Slot(uri=ENIGMA.otu_name, name="otu_name", curie=ENIGMA.curie('otu_name'),
                   model_uri=ENIGMA.otu_name, domain=None, range=str)

slots.condition_id = Slot(uri=ENIGMA.condition_id, name="condition_id", curie=ENIGMA.curie('condition_id'),
                   model_uri=ENIGMA.condition_id, domain=None, range=URIRef)

slots.condition_name = Slot(uri=ENIGMA.condition_name, name="condition_name", curie=ENIGMA.curie('condition_name'),
                   model_uri=ENIGMA.condition_name, domain=None, range=str)

slots.strain_id = Slot(uri=ENIGMA.strain_id, name="strain_id", curie=ENIGMA.curie('strain_id'),
                   model_uri=ENIGMA.strain_id, domain=None, range=URIRef)

slots.strain_name = Slot(uri=ENIGMA.strain_name, name="strain_name", curie=ENIGMA.curie('strain_name'),
                   model_uri=ENIGMA.strain_name, domain=None, range=str)

slots.strain_description = Slot(uri=ENIGMA.strain_description, name="strain_description", curie=ENIGMA.curie('strain_description'),
                   model_uri=ENIGMA.strain_description, domain=None, range=Optional[str])

slots.strain_genome = Slot(uri=ENIGMA.strain_genome, name="strain_genome", curie=ENIGMA.curie('strain_genome'),
                   model_uri=ENIGMA.strain_genome, domain=None, range=Optional[Union[str, GenomeGenomeId]])

slots.strain_derived_from = Slot(uri=ENIGMA.strain_derived_from, name="strain_derived_from", curie=ENIGMA.curie('strain_derived_from'),
                   model_uri=ENIGMA.strain_derived_from, domain=None, range=Optional[Union[str, StrainStrainId]])

slots.strain_genes_changed = Slot(uri=ENIGMA.strain_genes_changed, name="strain_genes_changed", curie=ENIGMA.curie('strain_genes_changed'),
                   model_uri=ENIGMA.strain_genes_changed, domain=None, range=Optional[Union[Union[str, GeneGeneId], list[Union[str, GeneGeneId]]]])

slots.community_id = Slot(uri=ENIGMA.community_id, name="community_id", curie=ENIGMA.curie('community_id'),
                   model_uri=ENIGMA.community_id, domain=None, range=URIRef)

slots.community_name = Slot(uri=ENIGMA.community_name, name="community_name", curie=ENIGMA.curie('community_name'),
                   model_uri=ENIGMA.community_name, domain=None, range=str)

slots.community_community_type = Slot(uri=ENIGMA.community_community_type, name="community_community_type", curie=ENIGMA.curie('community_community_type'),
                   model_uri=ENIGMA.community_community_type, domain=None, range=Union[str, "CommunityTypeEnum"])

slots.community_sample = Slot(uri=ENIGMA.community_sample, name="community_sample", curie=ENIGMA.curie('community_sample'),
                   model_uri=ENIGMA.community_sample, domain=None, range=Optional[Union[str, SampleSampleId]])

slots.community_parent_community = Slot(uri=ENIGMA.community_parent_community, name="community_parent_community", curie=ENIGMA.curie('community_parent_community'),
                   model_uri=ENIGMA.community_parent_community, domain=None, range=Optional[Union[str, CommunityCommunityId]])

slots.community_condition = Slot(uri=ENIGMA.community_condition, name="community_condition", curie=ENIGMA.curie('community_condition'),
                   model_uri=ENIGMA.community_condition, domain=None, range=Optional[Union[str, ConditionConditionId]])

slots.community_defined_strains = Slot(uri=ENIGMA.community_defined_strains, name="community_defined_strains", curie=ENIGMA.curie('community_defined_strains'),
                   model_uri=ENIGMA.community_defined_strains, domain=None, range=Optional[Union[str, StrainStrainId]])

slots.community_description = Slot(uri=ENIGMA.community_description, name="community_description", curie=ENIGMA.curie('community_description'),
                   model_uri=ENIGMA.community_description, domain=None, range=Optional[str])

slots.reads_id = Slot(uri=ENIGMA.reads_id, name="reads_id", curie=ENIGMA.curie('reads_id'),
                   model_uri=ENIGMA.reads_id, domain=None, range=URIRef)

slots.reads_name = Slot(uri=ENIGMA.reads_name, name="reads_name", curie=ENIGMA.curie('reads_name'),
                   model_uri=ENIGMA.reads_name, domain=None, range=str)

slots.reads_read_count = Slot(uri=ENIGMA.reads_read_count, name="reads_read_count", curie=ENIGMA.curie('reads_read_count'),
                   model_uri=ENIGMA.reads_read_count, domain=None, range=Union[int, Count])

slots.reads_read_type = Slot(uri=ENIGMA.reads_read_type, name="reads_read_type", curie=ENIGMA.curie('reads_read_type'),
                   model_uri=ENIGMA.reads_read_type, domain=None, range=Union[str, "ReadTypeEnum"])

slots.reads_sequencing_technology = Slot(uri=ENIGMA.reads_sequencing_technology, name="reads_sequencing_technology", curie=ENIGMA.curie('reads_sequencing_technology'),
                   model_uri=ENIGMA.reads_sequencing_technology, domain=None, range=Union[str, "SequencingTechnologyEnum"])

slots.reads_link = Slot(uri=ENIGMA.reads_link, name="reads_link", curie=ENIGMA.curie('reads_link'),
                   model_uri=ENIGMA.reads_link, domain=None, range=Union[str, Link])

slots.assembly_id = Slot(uri=ENIGMA.assembly_id, name="assembly_id", curie=ENIGMA.curie('assembly_id'),
                   model_uri=ENIGMA.assembly_id, domain=None, range=URIRef)

slots.assembly_name = Slot(uri=ENIGMA.assembly_name, name="assembly_name", curie=ENIGMA.curie('assembly_name'),
                   model_uri=ENIGMA.assembly_name, domain=None, range=str)

slots.assembly_strain = Slot(uri=ENIGMA.assembly_strain, name="assembly_strain", curie=ENIGMA.curie('assembly_strain'),
                   model_uri=ENIGMA.assembly_strain, domain=None, range=Optional[Union[str, StrainStrainId]])

slots.assembly_n_contigs = Slot(uri=ENIGMA.assembly_n_contigs, name="assembly_n_contigs", curie=ENIGMA.curie('assembly_n_contigs'),
                   model_uri=ENIGMA.assembly_n_contigs, domain=None, range=Union[int, Count])

slots.assembly_link = Slot(uri=ENIGMA.assembly_link, name="assembly_link", curie=ENIGMA.curie('assembly_link'),
                   model_uri=ENIGMA.assembly_link, domain=None, range=Optional[Union[str, Link]])

slots.genome_id = Slot(uri=ENIGMA.genome_id, name="genome_id", curie=ENIGMA.curie('genome_id'),
                   model_uri=ENIGMA.genome_id, domain=None, range=URIRef)

slots.genome_name = Slot(uri=ENIGMA.genome_name, name="genome_name", curie=ENIGMA.curie('genome_name'),
                   model_uri=ENIGMA.genome_name, domain=None, range=str)

slots.genome_strain = Slot(uri=ENIGMA.genome_strain, name="genome_strain", curie=ENIGMA.curie('genome_strain'),
                   model_uri=ENIGMA.genome_strain, domain=None, range=Optional[Union[str, StrainStrainId]])

slots.genome_n_contigs = Slot(uri=ENIGMA.genome_n_contigs, name="genome_n_contigs", curie=ENIGMA.curie('genome_n_contigs'),
                   model_uri=ENIGMA.genome_n_contigs, domain=None, range=Union[int, Count])

slots.genome_n_features = Slot(uri=ENIGMA.genome_n_features, name="genome_n_features", curie=ENIGMA.curie('genome_n_features'),
                   model_uri=ENIGMA.genome_n_features, domain=None, range=Union[int, Count])

slots.genome_link = Slot(uri=ENIGMA.genome_link, name="genome_link", curie=ENIGMA.curie('genome_link'),
                   model_uri=ENIGMA.genome_link, domain=None, range=Union[str, Link])

slots.gene_id = Slot(uri=ENIGMA.gene_id, name="gene_id", curie=ENIGMA.curie('gene_id'),
                   model_uri=ENIGMA.gene_id, domain=None, range=URIRef)

slots.gene_gene_id = Slot(uri=ENIGMA.gene_gene_id, name="gene_gene_id", curie=ENIGMA.curie('gene_gene_id'),
                   model_uri=ENIGMA.gene_gene_id, domain=None, range=str)

slots.gene_genome = Slot(uri=ENIGMA.gene_genome, name="gene_genome", curie=ENIGMA.curie('gene_genome'),
                   model_uri=ENIGMA.gene_genome, domain=None, range=Union[str, GenomeGenomeId])

slots.gene_aliases = Slot(uri=ENIGMA.gene_aliases, name="gene_aliases", curie=ENIGMA.curie('gene_aliases'),
                   model_uri=ENIGMA.gene_aliases, domain=None, range=Optional[Union[str, list[str]]])

slots.gene_contig_number = Slot(uri=ENIGMA.gene_contig_number, name="gene_contig_number", curie=ENIGMA.curie('gene_contig_number'),
                   model_uri=ENIGMA.gene_contig_number, domain=None, range=int)

slots.gene_strand = Slot(uri=ENIGMA.gene_strand, name="gene_strand", curie=ENIGMA.curie('gene_strand'),
                   model_uri=ENIGMA.gene_strand, domain=None, range=Union[str, "StrandEnum"])

slots.gene_start = Slot(uri=ENIGMA.gene_start, name="gene_start", curie=ENIGMA.curie('gene_start'),
                   model_uri=ENIGMA.gene_start, domain=None, range=int)

slots.gene_stop = Slot(uri=ENIGMA.gene_stop, name="gene_stop", curie=ENIGMA.curie('gene_stop'),
                   model_uri=ENIGMA.gene_stop, domain=None, range=int)

slots.gene_function = Slot(uri=ENIGMA.gene_function, name="gene_function", curie=ENIGMA.curie('gene_function'),
                   model_uri=ENIGMA.gene_function, domain=None, range=Optional[str])

slots.bin_id = Slot(uri=ENIGMA.bin_id, name="bin_id", curie=ENIGMA.curie('bin_id'),
                   model_uri=ENIGMA.bin_id, domain=None, range=URIRef)

slots.bin_name = Slot(uri=ENIGMA.bin_name, name="bin_name", curie=ENIGMA.curie('bin_name'),
                   model_uri=ENIGMA.bin_name, domain=None, range=str)

slots.bin_assembly = Slot(uri=ENIGMA.bin_assembly, name="bin_assembly", curie=ENIGMA.curie('bin_assembly'),
                   model_uri=ENIGMA.bin_assembly, domain=None, range=Union[str, AssemblyAssemblyId])

slots.bin_contigs = Slot(uri=ENIGMA.bin_contigs, name="bin_contigs", curie=ENIGMA.curie('bin_contigs'),
                   model_uri=ENIGMA.bin_contigs, domain=None, range=Union[str, list[str]])

slots.protocol_id = Slot(uri=ENIGMA.protocol_id, name="protocol_id", curie=ENIGMA.curie('protocol_id'),
                   model_uri=ENIGMA.protocol_id, domain=None, range=URIRef)

slots.protocol_name = Slot(uri=ENIGMA.protocol_name, name="protocol_name", curie=ENIGMA.curie('protocol_name'),
                   model_uri=ENIGMA.protocol_name, domain=None, range=str)

slots.protocol_description = Slot(uri=ENIGMA.protocol_description, name="protocol_description", curie=ENIGMA.curie('protocol_description'),
                   model_uri=ENIGMA.protocol_description, domain=None, range=Optional[str])

slots.protocol_link = Slot(uri=ENIGMA.protocol_link, name="protocol_link", curie=ENIGMA.curie('protocol_link'),
                   model_uri=ENIGMA.protocol_link, domain=None, range=Optional[Union[str, Link]])

slots.image_id = Slot(uri=ENIGMA.image_id, name="image_id", curie=ENIGMA.curie('image_id'),
                   model_uri=ENIGMA.image_id, domain=None, range=URIRef)

slots.image_name = Slot(uri=ENIGMA.image_name, name="image_name", curie=ENIGMA.curie('image_name'),
                   model_uri=ENIGMA.image_name, domain=None, range=str)

slots.image_description = Slot(uri=ENIGMA.image_description, name="image_description", curie=ENIGMA.curie('image_description'),
                   model_uri=ENIGMA.image_description, domain=None, range=Optional[str])

slots.image_MIME_type = Slot(uri=ENIGMA.image_MIME_type, name="image_MIME_type", curie=ENIGMA.curie('image_MIME_type'),
                   model_uri=ENIGMA.image_MIME_type, domain=None, range=Optional[str])

slots.image_size = Slot(uri=ENIGMA.image_size, name="image_size", curie=ENIGMA.curie('image_size'),
                   model_uri=ENIGMA.image_size, domain=None, range=Optional[Union[float, Size]])

slots.image_dimensions = Slot(uri=ENIGMA.image_dimensions, name="image_dimensions", curie=ENIGMA.curie('image_dimensions'),
                   model_uri=ENIGMA.image_dimensions, domain=None, range=Optional[str])

slots.image_link = Slot(uri=ENIGMA.image_link, name="image_link", curie=ENIGMA.curie('image_link'),
                   model_uri=ENIGMA.image_link, domain=None, range=Optional[Union[str, Link]])

slots.tnseq_library_id = Slot(uri=ENIGMA.tnseq_library_id, name="tnseq_library_id", curie=ENIGMA.curie('tnseq_library_id'),
                   model_uri=ENIGMA.tnseq_library_id, domain=None, range=URIRef)

slots.tnseq_library_name = Slot(uri=ENIGMA.tnseq_library_name, name="tnseq_library_name", curie=ENIGMA.curie('tnseq_library_name'),
                   model_uri=ENIGMA.tnseq_library_name, domain=None, range=str)

slots.tnseq_library_genome = Slot(uri=ENIGMA.tnseq_library_genome, name="tnseq_library_genome", curie=ENIGMA.curie('tnseq_library_genome'),
                   model_uri=ENIGMA.tnseq_library_genome, domain=None, range=Union[str, GenomeGenomeId])

slots.tnseq_library_primers_model = Slot(uri=ENIGMA.tnseq_library_primers_model, name="tnseq_library_primers_model", curie=ENIGMA.curie('tnseq_library_primers_model'),
                   model_uri=ENIGMA.tnseq_library_primers_model, domain=None, range=str)

slots.tnseq_library_n_mapped_reads = Slot(uri=ENIGMA.tnseq_library_n_mapped_reads, name="tnseq_library_n_mapped_reads", curie=ENIGMA.curie('tnseq_library_n_mapped_reads'),
                   model_uri=ENIGMA.tnseq_library_n_mapped_reads, domain=None, range=Optional[int])

slots.tnseq_library_n_barcodes = Slot(uri=ENIGMA.tnseq_library_n_barcodes, name="tnseq_library_n_barcodes", curie=ENIGMA.curie('tnseq_library_n_barcodes'),
                   model_uri=ENIGMA.tnseq_library_n_barcodes, domain=None, range=Optional[int])

slots.tnseq_library_n_usable_barcodes = Slot(uri=ENIGMA.tnseq_library_n_usable_barcodes, name="tnseq_library_n_usable_barcodes", curie=ENIGMA.curie('tnseq_library_n_usable_barcodes'),
                   model_uri=ENIGMA.tnseq_library_n_usable_barcodes, domain=None, range=Optional[int])

slots.tnseq_library_n_insertion_locations = Slot(uri=ENIGMA.tnseq_library_n_insertion_locations, name="tnseq_library_n_insertion_locations", curie=ENIGMA.curie('tnseq_library_n_insertion_locations'),
                   model_uri=ENIGMA.tnseq_library_n_insertion_locations, domain=None, range=Optional[int])

slots.tnseq_library_hit_rate_essential = Slot(uri=ENIGMA.tnseq_library_hit_rate_essential, name="tnseq_library_hit_rate_essential", curie=ENIGMA.curie('tnseq_library_hit_rate_essential'),
                   model_uri=ENIGMA.tnseq_library_hit_rate_essential, domain=None, range=Optional[Union[float, Rate]])

slots.tnseq_library_hit_rate_other = Slot(uri=ENIGMA.tnseq_library_hit_rate_other, name="tnseq_library_hit_rate_other", curie=ENIGMA.curie('tnseq_library_hit_rate_other'),
                   model_uri=ENIGMA.tnseq_library_hit_rate_other, domain=None, range=Optional[Union[float, Rate]])

slots.dubseq_library_id = Slot(uri=ENIGMA.dubseq_library_id, name="dubseq_library_id", curie=ENIGMA.curie('dubseq_library_id'),
                   model_uri=ENIGMA.dubseq_library_id, domain=None, range=URIRef)

slots.dubseq_library_name = Slot(uri=ENIGMA.dubseq_library_name, name="dubseq_library_name", curie=ENIGMA.curie('dubseq_library_name'),
                   model_uri=ENIGMA.dubseq_library_name, domain=None, range=str)

slots.dubseq_library_genome = Slot(uri=ENIGMA.dubseq_library_genome, name="dubseq_library_genome", curie=ENIGMA.curie('dubseq_library_genome'),
                   model_uri=ENIGMA.dubseq_library_genome, domain=None, range=Union[str, GenomeGenomeId])

slots.dubseq_library_n_fragments = Slot(uri=ENIGMA.dubseq_library_n_fragments, name="dubseq_library_n_fragments", curie=ENIGMA.curie('dubseq_library_n_fragments'),
                   model_uri=ENIGMA.dubseq_library_n_fragments, domain=None, range=Optional[Union[int, Count]])
