from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "1.0.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'enigma',
     'description': 'LinkML schema for ENIGMA (Environmental Molecular Sciences '
                    'Laboratory Integrated Genomics Initiative) Common Data Model',
     'id': 'https://w3id.org/enigma/enigma-cdm',
     'imports': ['linkml:types'],
     'license': 'MIT',
     'name': 'enigma-cdm',
     'prefixes': {'CONTINENT': {'prefix_prefix': 'CONTINENT',
                                'prefix_reference': 'http://purl.obolibrary.org/obo/CONTINENT_'},
                  'COUNTRY': {'prefix_prefix': 'COUNTRY',
                              'prefix_reference': 'http://purl.obolibrary.org/obo/COUNTRY_'},
                  'DA': {'prefix_prefix': 'DA',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/DA_'},
                  'ENIGMA_TERM': {'prefix_prefix': 'ENIGMA_TERM',
                                  'prefix_reference': 'http://purl.obolibrary.org/obo/ENIGMA_'},
                  'ENVO': {'prefix_prefix': 'ENVO',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/ENVO_'},
                  'ME': {'prefix_prefix': 'ME',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/ME_'},
                  'MIxS': {'prefix_prefix': 'MIxS',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/MIxS_'},
                  'PROCESS': {'prefix_prefix': 'PROCESS',
                              'prefix_reference': 'http://purl.obolibrary.org/obo/PROCESS_'},
                  'UO': {'prefix_prefix': 'UO',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/UO_'},
                  'enigma': {'prefix_prefix': 'enigma',
                             'prefix_reference': 'https://w3id.org/enigma/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'}},
     'source_file': 'src/linkml-coral/schema/linkml-coral.yaml',
     'title': 'ENIGMA Common Data Model'} )


class Process(ConfiguredBaseModel):
    """
    Process entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'term': {'tag': 'term', 'value': 'DA:0000061'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    process_id: str = Field(default=..., description="""id field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000277'}},
         'domain_of': ['Process']} })
    process_process: str = Field(default=..., description="""process field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_process',
         'annotations': {'constraint': {'tag': 'constraint',
                                        'value': 'PROCESS:0000001'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000204'}},
         'domain_of': ['Process']} })
    process_person: str = Field(default=..., description="""person field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_person',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'ENIGMA:0000029'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000205'}},
         'domain_of': ['Process']} })
    process_campaign: str = Field(default=..., description="""campaign field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_campaign',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000206'}},
         'domain_of': ['Process']} })
    process_protocol: Optional[str] = Field(default=None, description="""protocol field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_protocol',
         'annotations': {'foreign_key': {'tag': 'foreign_key',
                                         'value': 'Protocol.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000328'}},
         'domain_of': ['Process']} })
    process_date_start: Optional[str] = Field(default=None, description="""date_start field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_date_start',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000009'}},
         'comments': ['YYYY[-MM[-DD]]'],
         'domain_of': ['Process']} })
    process_date_end: Optional[str] = Field(default=None, description="""date_end field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_date_end',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000009'}},
         'comments': ['YYYY[-MM[-DD]]'],
         'domain_of': ['Process']} })
    process_input_objects: list[str] = Field(default=..., description="""input_objects field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_input_objects',
         'annotations': {'constraint': {'tag': 'constraint', 'value': '[Entity|Brick]'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000207'}},
         'domain_of': ['Process']} })
    process_output_objects: list[str] = Field(default=..., description="""output_objects field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_output_objects',
         'annotations': {'constraint': {'tag': 'constraint', 'value': '[Entity|Brick]'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000208'}},
         'domain_of': ['Process']} })

    @field_validator('process_date_start')
    def pattern_process_date_start(cls, v):
        pattern=re.compile(r"\d\d\d\d(-\d\d(-\d\d)?)?")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid process_date_start format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid process_date_start format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('process_date_end')
    def pattern_process_date_end(cls, v):
        pattern=re.compile(r"\d\d\d\d(-\d\d(-\d\d)?)?")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid process_date_end format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid process_date_end format: {v}"
            raise ValueError(err_msg)
        return v


class Location(ConfiguredBaseModel):
    """
    Location entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['ENIGMA']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000028']},
                         'term': {'tag': 'term', 'value': 'DA:0000041'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    location_id: str = Field(default=..., description="""id field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000266'}},
         'domain_of': ['Location']} })
    location_name: str = Field(default=..., description="""name field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000228'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Location']} })
    location_latitude: float = Field(default=..., description="""latitude field for Location""", ge=-90, le=90, json_schema_extra = { "linkml_meta": {'alias': 'location_latitude',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000211'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000185'}},
         'domain_of': ['Location']} })
    location_longitude: float = Field(default=..., description="""longitude field for Location""", ge=-180, le=180, json_schema_extra = { "linkml_meta": {'alias': 'location_longitude',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000212'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000185'}},
         'domain_of': ['Location']} })
    location_continent: str = Field(default=..., description="""continent field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_continent',
         'annotations': {'constraint': {'tag': 'constraint',
                                        'value': 'CONTINENT:0000001'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000213'}},
         'domain_of': ['Location']} })
    location_country: str = Field(default=..., description="""country field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_country',
         'annotations': {'constraint': {'tag': 'constraint',
                                        'value': 'COUNTRY:0000001'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000214'}},
         'domain_of': ['Location']} })
    location_region: str = Field(default=..., description="""region field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_region',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000215'}},
         'comments': ['specific local region name(s)'],
         'domain_of': ['Location']} })
    location_biome: str = Field(default=..., description="""biome field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_biome',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'ENVO:01000254'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000216'}},
         'domain_of': ['Location']} })
    location_feature: Optional[str] = Field(default=None, description="""feature field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_feature',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'ENVO:00002297'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000217'}},
         'domain_of': ['Location']} })


class Sample(ConfiguredBaseModel):
    """
    Sample entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['Location']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000002']},
                         'term': {'tag': 'term', 'value': 'DA:0000042'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    sample_id: str = Field(default=..., description="""id field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000267'}},
         'domain_of': ['Sample']} })
    sample_name: str = Field(default=..., description="""name field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000102'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Sample']} })
    sample_location: str = Field(default=..., description="""location field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_location',
         'annotations': {'foreign_key': {'tag': 'foreign_key',
                                         'value': 'Location.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000228'}},
         'domain_of': ['Sample']} })
    sample_depth: Optional[float] = Field(default=None, description="""depth field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_depth',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000219'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000008'}},
         'comments': ['in meters below ground level'],
         'domain_of': ['Sample']} })
    sample_elevation: Optional[float] = Field(default=None, description="""elevation field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_elevation',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000220'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000008'}},
         'comments': ['in meters above ground level'],
         'domain_of': ['Sample']} })
    sample_date: str = Field(default=..., description="""date field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_date',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000009'}},
         'comments': ['YYYY[-MM[-DD]]'],
         'domain_of': ['Sample']} })
    sample_time: Optional[str] = Field(default=None, description="""time field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_time',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000010'}},
         'comments': ['HH[:MM[:SS]] [AM|PM]'],
         'domain_of': ['Sample']} })
    sample_timezone: Optional[str] = Field(default=None, description="""timezone field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_timezone',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000201'}},
         'comments': ['ISO8601 compliant format, ie. UTC-7'],
         'domain_of': ['Sample']} })
    sample_material: Optional[str] = Field(default=None, description="""material field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_material',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'ENVO:00010483'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000230'}},
         'domain_of': ['Sample']} })
    sample_env_package: str = Field(default=..., description="""env_package field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_env_package',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'MIxS:0000002'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000229'}},
         'domain_of': ['Sample']} })
    sample_description: Optional[str] = Field(default=None, description="""description field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_description',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000202'}},
         'domain_of': ['Sample']} })

    @field_validator('sample_date')
    def pattern_sample_date(cls, v):
        pattern=re.compile(r"\d\d\d\d(-\d\d(-\d\d)?)?")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid sample_date format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid sample_date format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('sample_time')
    def pattern_sample_time(cls, v):
        pattern=re.compile(r"\d(\d)?(:\d\d(:\d\d)?)?\s*([apAP][mM])?")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid sample_time format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid sample_time format: {v}"
            raise ValueError(err_msg)
        return v


class Taxon(ConfiguredBaseModel):
    """
    Taxon entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['ENIGMA']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000029']},
                         'term': {'tag': 'term', 'value': 'DA:0000037'}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    taxon_id: str = Field(default=..., description="""id field for Taxon""", json_schema_extra = { "linkml_meta": {'alias': 'taxon_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000268'}},
         'domain_of': ['Taxon']} })
    taxon_name: str = Field(default=..., description="""name field for Taxon""", json_schema_extra = { "linkml_meta": {'alias': 'taxon_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000047'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Taxon']} })
    taxon_ncbi_taxid: Optional[str] = Field(default=None, description="""ncbi_taxid field for Taxon""", json_schema_extra = { "linkml_meta": {'alias': 'taxon_ncbi_taxid',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000223'}},
         'domain_of': ['Taxon']} })


class OTU(ConfiguredBaseModel):
    """
    OTU entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['Reads']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000031']},
                         'term': {'tag': 'term', 'value': 'DA:0000063'}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    otu_id: str = Field(default=..., description="""id field for OTU""", json_schema_extra = { "linkml_meta": {'alias': 'otu_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000269'}},
         'domain_of': ['OTU']} })
    otu_name: str = Field(default=..., description="""name field for OTU""", json_schema_extra = { "linkml_meta": {'alias': 'otu_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000222'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['OTU']} })


class Condition(ConfiguredBaseModel):
    """
    Condition entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['ENIGMA']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000032']},
                         'term': {'tag': 'term', 'value': 'DA:0000045'}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    condition_id: str = Field(default=..., description="""id field for Condition""", json_schema_extra = { "linkml_meta": {'alias': 'condition_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000270'}},
         'domain_of': ['Condition']} })
    condition_name: str = Field(default=..., description="""name field for Condition""", json_schema_extra = { "linkml_meta": {'alias': 'condition_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000200'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Condition']} })


class Strain(ConfiguredBaseModel):
    """
    Strain entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['Sample'], ['Strain']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000015',
                                                     'PROCESS:0000030']},
                         'term': {'tag': 'term', 'value': 'DA:0000062'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    strain_id: str = Field(default=..., description="""id field for Strain""", json_schema_extra = { "linkml_meta": {'alias': 'strain_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000271'}},
         'domain_of': ['Strain']} })
    strain_name: str = Field(default=..., description="""name field for Strain""", json_schema_extra = { "linkml_meta": {'alias': 'strain_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000044'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Strain']} })
    strain_description: Optional[str] = Field(default=None, description="""description field for Strain""", json_schema_extra = { "linkml_meta": {'alias': 'strain_description',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000202'}},
         'domain_of': ['Strain']} })
    strain_genome: Optional[str] = Field(default=None, description="""genome field for Strain""", json_schema_extra = { "linkml_meta": {'alias': 'strain_genome',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Genome.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000246'}},
         'comments': ['genome object for sequenced, WT strains'],
         'domain_of': ['Strain']} })
    strain_derived_from: Optional[str] = Field(default=None, description="""derived_from field for Strain""", json_schema_extra = { "linkml_meta": {'alias': 'strain_derived_from',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Strain.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000044'}},
         'domain_of': ['Strain']} })
    strain_genes_changed: Optional[list[str]] = Field(default=None, description="""genes_changed field for Strain""", json_schema_extra = { "linkml_meta": {'alias': 'strain_genes_changed',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Gene.gene_id'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000091'}},
         'domain_of': ['Strain']} })


class Community(ConfiguredBaseModel):
    """
    Community entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['Sample'], ['Community']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000015',
                                                     'PROCESS:0000016',
                                                     'PROCESS:0000011']},
                         'term': {'tag': 'term', 'value': 'DA:0000048'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    community_id: str = Field(default=..., description="""id field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000272'}},
         'domain_of': ['Community']} })
    community_name: str = Field(default=..., description="""name field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000233'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Community']} })
    community_community_type: str = Field(default=..., description="""community_type field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_community_type',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'ME:0000234'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000234'}},
         'domain_of': ['Community']} })
    community_sample: Optional[str] = Field(default=None, description="""sample field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_sample',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Sample.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000102'}},
         'domain_of': ['Community']} })
    community_parent_community: Optional[str] = Field(default=None, description="""parent_community field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_parent_community',
         'annotations': {'foreign_key': {'tag': 'foreign_key',
                                         'value': 'Community.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000233'}},
         'domain_of': ['Community']} })
    community_condition: Optional[str] = Field(default=None, description="""condition field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_condition',
         'annotations': {'foreign_key': {'tag': 'foreign_key',
                                         'value': 'Condition.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000200'}},
         'domain_of': ['Community']} })
    community_defined_strains: Optional[list[str]] = Field(default=None, description="""defined_strains field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_defined_strains',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Strain.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000044'}},
         'comments': ['typedef.json has typo with FK pointing to [Strain.Name] with '
                      'capital N',
                      'Using lowercase name to match actual Strain field'],
         'domain_of': ['Community']} })
    community_description: Optional[str] = Field(default=None, description="""description field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_description',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000202'}},
         'domain_of': ['Community']} })


class Reads(ConfiguredBaseModel):
    """
    Reads entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['Sample'], ['Community']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000017']},
                         'term': {'tag': 'term', 'value': 'DA:0000054'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    reads_id: str = Field(default=..., description="""id field for Reads""", json_schema_extra = { "linkml_meta": {'alias': 'reads_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000273'}},
         'domain_of': ['Reads']} })
    reads_name: str = Field(default=..., description="""name field for Reads""", json_schema_extra = { "linkml_meta": {'alias': 'reads_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000248'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Reads']} })
    reads_read_count: int = Field(default=..., description="""read_count field for Reads""", json_schema_extra = { "linkml_meta": {'alias': 'reads_read_count',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['Reads']} })
    reads_read_type: str = Field(default=..., description="""read_type field for Reads""", json_schema_extra = { "linkml_meta": {'alias': 'reads_read_type',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'ME:0000112'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000112'}},
         'domain_of': ['Reads']} })
    reads_sequencing_technology: str = Field(default=..., description="""sequencing_technology field for Reads""", json_schema_extra = { "linkml_meta": {'alias': 'reads_sequencing_technology',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'ME:0000116'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000116'}},
         'domain_of': ['Reads']} })
    reads_link: str = Field(default=..., description="""link field for Reads""", json_schema_extra = { "linkml_meta": {'alias': 'reads_link',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000203'}},
         'domain_of': ['Reads']} })


class Assembly(ConfiguredBaseModel):
    """
    Assembly entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['Reads'], ['Reads']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000023',
                                                     'PROCESS:0000024']},
                         'term': {'tag': 'term', 'value': 'DA:0000066'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    assembly_id: str = Field(default=..., description="""id field for Assembly""", json_schema_extra = { "linkml_meta": {'alias': 'assembly_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000281'}},
         'domain_of': ['Assembly']} })
    assembly_name: str = Field(default=..., description="""name field for Assembly""", json_schema_extra = { "linkml_meta": {'alias': 'assembly_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000280'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Assembly']} })
    assembly_strain: Optional[str] = Field(default=None, description="""strain field for Assembly""", json_schema_extra = { "linkml_meta": {'alias': 'assembly_strain',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Strain.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000044'}},
         'domain_of': ['Assembly']} })
    assembly_n_contigs: int = Field(default=..., description="""n_contigs field for Assembly""", json_schema_extra = { "linkml_meta": {'alias': 'assembly_n_contigs',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['Assembly']} })
    assembly_link: str = Field(default=..., description="""link field for Assembly""", json_schema_extra = { "linkml_meta": {'alias': 'assembly_link',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000203'}},
         'domain_of': ['Assembly']} })


class Genome(ConfiguredBaseModel):
    """
    Genome entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['Assembly'], ['Bin']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000034',
                                                     'PROCESS:0000045']},
                         'term': {'tag': 'term', 'value': 'DA:0000039'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    genome_id: str = Field(default=..., description="""id field for Genome""", json_schema_extra = { "linkml_meta": {'alias': 'genome_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000274'}},
         'domain_of': ['Genome']} })
    genome_name: str = Field(default=..., description="""name field for Genome""", json_schema_extra = { "linkml_meta": {'alias': 'genome_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000246'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Genome']} })
    genome_strain: Optional[str] = Field(default=None, description="""strain field for Genome""", json_schema_extra = { "linkml_meta": {'alias': 'genome_strain',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Strain.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000044'}},
         'domain_of': ['Genome']} })
    genome_n_contigs: int = Field(default=..., description="""n_contigs field for Genome""", json_schema_extra = { "linkml_meta": {'alias': 'genome_n_contigs',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['Genome']} })
    genome_n_features: int = Field(default=..., description="""n_features field for Genome""", json_schema_extra = { "linkml_meta": {'alias': 'genome_n_features',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['Genome']} })
    genome_link: str = Field(default=..., description="""link field for Genome""", json_schema_extra = { "linkml_meta": {'alias': 'genome_link',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000203'}},
         'domain_of': ['Genome']} })


class Gene(ConfiguredBaseModel):
    """
    Gene entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['Assembly']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000034']},
                         'term': {'tag': 'term', 'value': 'DA:0000040'}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    gene_id: str = Field(default=..., description="""id field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000275'}},
         'domain_of': ['Gene']} })
    gene_gene_id: str = Field(default=..., description="""gene_id field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_gene_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000224'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Gene']} })
    gene_genome: str = Field(default=..., description="""genome field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_genome',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Genome.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000246'}},
         'comments': ['typedef.json has FK pointing to Genome without specifying '
                      'target field',
                      'Assumed to reference Genome.name based on pattern'],
         'domain_of': ['Gene']} })
    gene_aliases: Optional[list[str]] = Field(default=None, description="""aliases field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_aliases',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000060'}},
         'domain_of': ['Gene']} })
    gene_contig_number: int = Field(default=..., description="""contig_number field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_contig_number',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'comments': ['indexed starting at 1, as in KBase'],
         'domain_of': ['Gene']} })
    gene_strand: str = Field(default=..., description="""strand field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_strand',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000186'}},
         'domain_of': ['Gene']} })
    gene_start: int = Field(default=..., description="""start field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_start',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000242'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000244'}},
         'comments': ['indexed starting at 1, as in KBase'],
         'domain_of': ['Gene']} })
    gene_stop: int = Field(default=..., description="""stop field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_stop',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000243'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000244'}},
         'domain_of': ['Gene']} })
    gene_function: Optional[str] = Field(default=None, description="""function field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_function',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000250'}},
         'domain_of': ['Gene']} })

    @field_validator('gene_strand')
    def pattern_gene_strand(cls, v):
        pattern=re.compile(r"[+-]")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid gene_strand format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid gene_strand format: {v}"
            raise ValueError(err_msg)
        return v


class Bin(ConfiguredBaseModel):
    """
    Bin entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['Assembly']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000039']},
                         'term': {'tag': 'term', 'value': 'DA:0000072'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    bin_id: str = Field(default=..., description="""id field for Bin""", json_schema_extra = { "linkml_meta": {'alias': 'bin_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000331'}},
         'domain_of': ['Bin']} })
    bin_name: str = Field(default=..., description="""name field for Bin""", json_schema_extra = { "linkml_meta": {'alias': 'bin_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000330'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Bin']} })
    bin_assembly: str = Field(default=..., description="""assembly field for Bin""", json_schema_extra = { "linkml_meta": {'alias': 'bin_assembly',
         'annotations': {'foreign_key': {'tag': 'foreign_key',
                                         'value': 'Assembly.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000280'}},
         'comments': ['typedef.json has FK pointing to Assembly without specifying '
                      'target field',
                      'Assumed to reference Assembly.name based on pattern'],
         'domain_of': ['Bin']} })
    bin_contigs: list[str] = Field(default=..., description="""contigs field for Bin""", json_schema_extra = { "linkml_meta": {'alias': 'bin_contigs',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000240'}},
         'domain_of': ['Bin']} })


class Protocol(ConfiguredBaseModel):
    """
    Protocol entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['ENIGMA']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000044']},
                         'term': {'tag': 'term', 'value': 'DA:0000073'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    protocol_id: str = Field(default=..., description="""id field for Protocol""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000332'}},
         'domain_of': ['Protocol']} })
    protocol_name: str = Field(default=..., description="""name field for Protocol""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000328'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Protocol']} })
    protocol_description: Optional[str] = Field(default=None, description="""description field for Protocol""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_description',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000202'}},
         'domain_of': ['Protocol']} })
    protocol_link: Optional[str] = Field(default=None, description="""link field for Protocol""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_link',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000203'}},
         'domain_of': ['Protocol']} })

    @field_validator('protocol_link')
    def pattern_protocol_link(cls, v):
        pattern=re.compile(r"http.*")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid protocol_link format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid protocol_link format: {v}"
            raise ValueError(err_msg)
        return v


class Image(ConfiguredBaseModel):
    """
    Image entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['ENIGMA']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000044']},
                         'term': {'tag': 'term', 'value': 'DA:0000074'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    image_id: str = Field(default=..., description="""id field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000356'}},
         'domain_of': ['Image']} })
    image_name: str = Field(default=..., description="""name field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000355'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Image']} })
    image_description: Optional[str] = Field(default=None, description="""description field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_description',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000202'}},
         'domain_of': ['Image']} })
    image_MIME_type: Optional[str] = Field(default=None, description="""MIME type field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_MIME_type',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000357'}},
         'domain_of': ['Image']} })
    image_size: Optional[int] = Field(default=None, description="""size field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_size',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000128'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000233'}},
         'domain_of': ['Image']} })
    image_dimensions: Optional[str] = Field(default=None, description="""dimensions field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_dimensions',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000292'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000236'}},
         'domain_of': ['Image']} })
    image_link: Optional[str] = Field(default=None, description="""link field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_link',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000203'}},
         'domain_of': ['Image']} })


class TnSeqLibrary(ConfiguredBaseModel):
    """
    TnSeq_Library entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['Genome']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000027']},
                         'term': {'tag': 'term', 'value': 'DA:0000060'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    tnseq_library_id: str = Field(default=..., description="""id field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000276'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_name: str = Field(default=..., description="""name field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000262'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_genome: str = Field(default=..., description="""genome field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_genome',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Genome.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000246'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_primers_model: str = Field(default=..., description="""primers_model field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_primers_model',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000263'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_n_mapped_reads: Optional[int] = Field(default=None, description="""n_mapped_reads field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_n_mapped_reads',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_n_barcodes: Optional[int] = Field(default=None, description="""n_barcodes field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_n_barcodes',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_n_usable_barcodes: Optional[int] = Field(default=None, description="""n_usable_barcodes field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_n_usable_barcodes',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_n_insertion_locations: Optional[int] = Field(default=None, description="""n_insertion_locations field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_n_insertion_locations',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_hit_rate_essential: Optional[float] = Field(default=None, description="""hit_rate_essential field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_hit_rate_essential',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000264'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000190'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_hit_rate_other: Optional[float] = Field(default=None, description="""hit_rate_other field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_hit_rate_other',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000264'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000190'}},
         'domain_of': ['TnSeq_Library']} })


class DubSeqLibrary(ConfiguredBaseModel):
    """
    DubSeq_Library entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'process_inputs': {'tag': 'process_inputs',
                                            'value': [['Genome']]},
                         'process_types': {'tag': 'process_types',
                                           'value': ['PROCESS:0000049']},
                         'term': {'tag': 'term', 'value': 'DA:0000075'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    dubseq_library_id: str = Field(default=..., description="""id field for DubSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'dubseq_library_id',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000276'}},
         'domain_of': ['DubSeq_Library']} })
    dubseq_library_name: str = Field(default=..., description="""name field for DubSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'dubseq_library_name',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000262'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['DubSeq_Library']} })
    dubseq_library_genome: str = Field(default=..., description="""genome field for DubSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'dubseq_library_genome',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Genome.name'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000246'}},
         'domain_of': ['DubSeq_Library']} })
    dubseq_library_n_fragments: Optional[int] = Field(default=None, description="""n_fragments field for DubSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'dubseq_library_n_fragments',
         'annotations': {'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['DubSeq_Library']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Process.model_rebuild()
Location.model_rebuild()
Sample.model_rebuild()
Taxon.model_rebuild()
OTU.model_rebuild()
Condition.model_rebuild()
Strain.model_rebuild()
Community.model_rebuild()
Reads.model_rebuild()
Assembly.model_rebuild()
Genome.model_rebuild()
Gene.model_rebuild()
Bin.model_rebuild()
Protocol.model_rebuild()
Image.model_rebuild()
TnSeqLibrary.model_rebuild()
DubSeqLibrary.model_rebuild()

