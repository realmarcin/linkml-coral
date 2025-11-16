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
     'source_file': 'src/linkml_coral/schema/linkml_coral.yaml',
     'title': 'ENIGMA Common Data Model',
     'types': {'Count': {'annotations': {'microtype': {'tag': 'microtype',
                                                       'value': 'ME:0000126'},
                                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                                 'value': 'int'},
                                         'units_term': {'tag': 'units_term',
                                                        'value': 'UO:0000189'}},
                         'description': 'Non-negative integer count',
                         'from_schema': 'https://w3id.org/enigma/enigma-cdm',
                         'minimum_value': 0,
                         'name': 'Count',
                         'typeof': 'integer'},
               'Date': {'annotations': {'microtype': {'tag': 'microtype',
                                                      'value': 'ME:0000009'},
                                        'microtype_data_type': {'tag': 'microtype_data_type',
                                                                'value': 'string'}},
                        'description': 'Date in YYYY-MM-DD format',
                        'from_schema': 'https://w3id.org/enigma/enigma-cdm',
                        'name': 'Date',
                        'pattern': '\\d\\d\\d\\d(-\\d\\d(-\\d\\d)?)?',
                        'typeof': 'string'},
               'Depth': {'annotations': {'microtype': {'tag': 'microtype',
                                                       'value': 'ME:0000219'},
                                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                                 'value': 'float'},
                                         'units_term': {'tag': 'units_term',
                                                        'value': 'UO:0000008'}},
                         'description': 'Depth measurement',
                         'from_schema': 'https://w3id.org/enigma/enigma-cdm',
                         'name': 'Depth',
                         'typeof': 'float'},
               'Elevation': {'annotations': {'microtype': {'tag': 'microtype',
                                                           'value': 'ME:0000220'},
                                             'microtype_data_type': {'tag': 'microtype_data_type',
                                                                     'value': 'float'},
                                             'units_term': {'tag': 'units_term',
                                                            'value': 'UO:0000008'}},
                             'description': 'Elevation measurement',
                             'from_schema': 'https://w3id.org/enigma/enigma-cdm',
                             'name': 'Elevation',
                             'typeof': 'float'},
               'Latitude': {'annotations': {'microtype': {'tag': 'microtype',
                                                          'value': 'ME:0000211'},
                                            'microtype_data_type': {'tag': 'microtype_data_type',
                                                                    'value': 'float'},
                                            'units_term': {'tag': 'units_term',
                                                           'value': 'UO:0000185'}},
                            'description': 'Geographic latitude in decimal degrees',
                            'from_schema': 'https://w3id.org/enigma/enigma-cdm',
                            'maximum_value': 90,
                            'minimum_value': -90,
                            'name': 'Latitude',
                            'typeof': 'float'},
               'Link': {'annotations': {'microtype': {'tag': 'microtype',
                                                      'value': 'ME:0000203'},
                                        'microtype_data_type': {'tag': 'microtype_data_type',
                                                                'value': 'string'}},
                        'description': 'HTTP/HTTPS URL',
                        'from_schema': 'https://w3id.org/enigma/enigma-cdm',
                        'name': 'Link',
                        'pattern': 'http.*',
                        'typeof': 'string'},
               'Longitude': {'annotations': {'microtype': {'tag': 'microtype',
                                                           'value': 'ME:0000212'},
                                             'microtype_data_type': {'tag': 'microtype_data_type',
                                                                     'value': 'float'},
                                             'units_term': {'tag': 'units_term',
                                                            'value': 'UO:0000185'}},
                             'description': 'Geographic longitude in decimal '
                                            'degrees',
                             'from_schema': 'https://w3id.org/enigma/enigma-cdm',
                             'maximum_value': 180,
                             'minimum_value': -180,
                             'name': 'Longitude',
                             'typeof': 'float'},
               'Rate': {'annotations': {'microtype': {'tag': 'microtype',
                                                      'value': 'ME:0000264'},
                                        'microtype_data_type': {'tag': 'microtype_data_type',
                                                                'value': 'float'}},
                        'description': 'Rate as a fraction between 0 and 1',
                        'from_schema': 'https://w3id.org/enigma/enigma-cdm',
                        'maximum_value': 1,
                        'minimum_value': 0,
                        'name': 'Rate',
                        'typeof': 'float'},
               'Size': {'annotations': {'microtype': {'tag': 'microtype',
                                                      'value': 'ME:0000128'},
                                        'microtype_data_type': {'tag': 'microtype_data_type',
                                                                'value': 'float'}},
                        'description': 'Size measurement (non-negative)',
                        'from_schema': 'https://w3id.org/enigma/enigma-cdm',
                        'minimum_value': 0,
                        'name': 'Size',
                        'typeof': 'float'},
               'Time': {'annotations': {'microtype': {'tag': 'microtype',
                                                      'value': 'ME:0000010'},
                                        'microtype_data_type': {'tag': 'microtype_data_type',
                                                                'value': 'string'}},
                        'description': 'Time in HH:MM:SS format',
                        'from_schema': 'https://w3id.org/enigma/enigma-cdm',
                        'name': 'Time',
                        'pattern': '\\d(\\d)?(:\\d\\d(:\\d\\d)?)?\\s*([apAP][mM])?',
                        'typeof': 'string'}}} )

class ExperimentalContextEnum(str, Enum):
    """
    Context describing experimental design.
    """
    Series_Type = "series_type"
    """
    Context describing the purpose of a series.
    """
    Condition = "condition"
    """
    A human-readable description of an experimental condition.
    """
    Method = "method"
    """
    A description of one or more methods used in an experiment.
    """
    Algorithm_Parameter = "algorithm_parameter"
    """
    A description of one or more algorithm parameters.
    """
    Date = "date"
    """
    A date, formatted as YYYY-MM-DD.
    """
    Time = "time"
    """
    A time, formatted as HH:MM (see DateTime to include the date).
    """
    Comment = "comment"
    """
    A human-readable comment.
    """
    Instrument = "instrument"
    """
    A description of instrument(s) used.
    """
    Category = "category"
    """
    A human-readable description of a category.
    """
    Homogenized = "homogenized"
    """
    Homogenized.
    """
    Anaerobic = "anaerobic"
    """
    Anaerobic.
    """
    Aerobic = "aerobic"
    """
    Aerobic.
    """
    Undisturbed = "undisturbed"
    """
    Undisturbed.
    """
    DateTime = "datetime"
    """
    DateTime.
    """
    Time_Zone = "time_zone"
    """
    Time Zone, e.g., PDT
    """
    Description = "description"
    """
    Description.
    """
    Link = "link"
    """
    Link to other data, e.g., a DOI or URL.
    """
    Experimental_Process = "experimental_process"
    """
    Category of experimental process used to create a dataset.
    """
    Person = "person"
    """
    Name of a person.  Note that ENIGMA people should be listed as 'ENIGMA personnel' instead.
    """
    Campaign = "campaign"
    """
    Campaign.
    """
    Input = "input"
    """
    Input.
    """
    Output = "output"
    """
    Output.
    """
    Control = "control"
    """
    Control.
    """
    Replicate = "replicate"
    """
    Replicate.
    """
    Subsample = "subsample"
    """
    Subsample.
    """
    Protocol = "protocol"
    """
    Protocol.
    """
    Availability = "availability"
    """
    Boolean property indicating whether something is available.
    """
    Ionization_Mode = "ionization_mode"
    """
    Ionization mode used in a mass spec experiment.
    """
    Usability = "usability"
    """
    Usability.
    """
    Barcode = "barcode"
    """
    Barcode.
    """
    Microplate_Name = "microplate_name"
    """
    Microplate Name.
    """
    Microplate_Well_Name = "microplate_well_name"
    """
    Microplate Well Name.
    """
    Microplate = "microplate"
    """
    Microplate.
    """
    Publication = "publication"
    """
    Publication.
    """
    Database = "database"
    """
    Database.
    """
    Obsolete = "obsolete"
    """
    Obsolete.
    """
    Index = "index"
    """
    Index.
    """
    Internal_Standard = "internal_standard"
    """
    Internal Standard.
    """


class SeriesTypeEnum(str, Enum):
    """
    Context describing the purpose of a series.
    """
    Time_Series = "time_series"
    """
    A time series, in which a series of measurements was taken at different timepoints.
    """
    Replicate_Series = "replicate_series"
    """
    A replicate series, e.g., biological or technical replicates.
    """


class MathematicalContextEnum(str, Enum):
    """
    Microtypes that provide mathematical context.
    """
    Normalized = "normalized"
    """
    Normalized; describe how in the Method or Protocol.
    """
    Relative = "relative"
    """
    Human-readable context saying what another microtype is measured relative to.
    """
    Increase = "increase"
    """
    Increase.
    """
    Decrease = "decrease"
    """
    Decrease.
    """
    Gain = "gain"
    """
    Gain.
    """
    Loss = "loss"
    """
    Loss.
    """
    Nearest = "nearest"
    """
    Nearest.
    """
    Variable_Name = "variable_name"
    """
    Variable Name.
    """
    Variable_Type = "variable_type"
    """
    Variable Type.
    """
    Dimension = "dimension"
    """
    Dimension.
    """
    High = "high"
    """
    High.
    """
    Low = "low"
    """
    Low.
    """
    Numerator = "numerator"
    """
    Numerator.
    """
    Denominator = "denominator"
    """
    Denominator.
    """
    Cumulative = "cumulative"
    """
    Cumulative.
    """


class ChemicalContextEnum(str, Enum):
    """
    Describes the context of a molecule in a chemical reaction or experiment.
    """
    Molecule = "molecule"
    """
    Use when the type of molecule varies along a dimension.
    """
    Reaction = "reaction"
    """
    Human-readable description of a chemical reaction.
    """
    Surface_Type = "surface_type"
    """
    Human-readable description of a type of surface.
    """
    Bead_Type = "bead_type"
    """
    Human-readable description of the type of bead used in a (geo)chemical experiment.
    """
    Bead_Size = "bead_size"
    """
    Size of a bead used in a (geo)chemical experiment.
    """
    Thermodynamic_Context = "thermodynamic_context"
    """
    Thermodynamic context for a reaction.
    """
    Specific_Activity = "specific_activity"
    """
    Rate of reaction multiplied by the volume, divided by mass of protein.
    """
    Wavelength = "wavelength"
    """
    Wavelength of radiation.
    """
    Physiochemical_State = "physiochemical_state"
    """
    Human-readable context for the state or type of matter, e.g., dissolved, or in soil
    """
    Detection_Limit = "detection_limit"
    """
    Detection limit for an instrument or experiment.
    """
    Reagent = "reagent"
    """
    Reagent.
    """
    Organic = "organic"
    """
    Use as context, for example, to label inorganic or organic carbon.
    """
    Molecular_Weight = "molecular_weight"
    """
    Molecular Weight.
    """
    Reference_Compound = "reference_compound"
    """
    Reference Compound.
    """
    Isotope = "isotope"
    """
    Isotope.
    """
    Redox = "redox"
    """
    Redox.
    """
    Exact_Mass = "exact_mass"
    """
    Exact Mass.
    """


class BiologicalContextEnum(str, Enum):
    """
    Biological Context.
    """
    Cell = "cell"
    """
    Cell.
    """
    Colony = "colony"
    """
    Colony.
    """
    Strain = "strain"
    """
    Strain of microbe, or isolate ID.
    """
    Taxon = "taxon"
    """
    Taxon.
    """
    Media = "media"
    """
    Media type.
    """
    Metabolite = "metabolite"
    """
    Metabolite.
    """
    Enzyme_Substrate = "enzyme_substrate"
    """
    Enzyme Substrate.
    """
    Gene = "gene"
    """
    Gene.
    """
    Protein = "protein"
    """
    Protein.
    """
    Protein_Annotation = "protein_annotation"
    """
    Protein Annotation.
    """
    Operon = "operon"
    """
    Operon.
    """
    Ribosome = "ribosome"
    """
    Ribosome.
    """
    Growth_Parameter = "growth_parameter"
    """
    Growth Parameter.
    """
    Gene_Regulation = "gene_regulation"
    """
    Gene Regulation.
    """
    Taxonomic_Level = "taxonomic_level"
    """
    Taxonomic Level.
    """
    Strain_Change = "strain_change"
    """
    Strain Change.
    """
    Knockout = "knockout"
    """
    Knockout.
    """
    Environment = "environment"
    """
    Environment.
    """
    Ecology = "ecology"
    """
    Ecology.
    """
    Sequencing = "sequencing"
    """
    Sequencing.
    """
    ASV = "asv"
    """
    Amplicon Sequence Variant.
    """
    ESV = "esv"
    """
    ESV.
    """
    Community = "community"
    """
    Community.
    """
    Genome = "genome"
    """
    Genome.
    """
    Gene_Annotation = "gene_annotation"
    """
    Gene Annotation.
    """
    Knockout_Library = "knockout_library"
    """
    Knockout Library.
    """
    Assembly = "assembly"
    """
    Assembly.
    """
    Bin = "bin"
    """
    Bin (metagenomic).
    """
    Overexpression_Library = "overexpression_library"
    """
    Overexpression Library.
    """
    Growth_Stage = "growth_stage"
    """
    Growth Stage.
    """
    OTU = "otu"
    """
    OTU.
    """


class TaxonomicLevelEnum(str, Enum):
    """
    Taxonomic Level.
    """
    Kingdom = "kingdom"
    """
    Kingdom.
    """
    Phylum = "phylum"
    """
    Phylum.
    """
    Class = "class"
    """
    Class.
    """
    Order = "order"
    """
    Order.
    """
    Family = "family"
    """
    Family.
    """
    Genus = "genus"
    """
    Genus.
    """
    Species = "species"
    """
    Species.
    """
    Taxonomic_Domain = "taxonomic_domain"
    """
    Taxonomic Domain.
    """


class StrainChangeEffectEnum(str, Enum):
    """
    Strain Change Effect.
    """
    Synonymous = "synonymous"
    """
    Synonymous.
    """
    Non_Synonymous = "non_synonymous"
    """
    Non-Synonymous.
    """
    Frameshift = "frameshift"
    """
    Frameshift.
    """
    Stop = "stop"
    """
    Stop.
    """


class CommunityAssemblyProcessEnum(str, Enum):
    """
    Community Assembly Process.
    """
    Variable_Selection = "variable_selection"
    """
    Variable Selection.
    """
    Homogenous_Selection = "homogenous_selection"
    """
    Homogenous Selection.
    """
    Dispersal_Limitation = "dispersal_limitation"
    """
    Dispersal Limitation.
    """
    Homogenizing_Dispersal = "homogenizing_dispersal"
    """
    Homogenizing Dispersal.
    """
    Undominated = "undominated"
    """
    Undominated.
    """


class ReadTypeEnum(str, Enum):
    """
    Read Type.
    """
    Paired_End_Read = "paired_end_read"
    """
    Paired End Read.
    """
    Single_End_Read = "single_end_read"
    """
    Single End Read.
    """


class SequencingTechnologyEnum(str, Enum):
    """
    Sequencing Technology.
    """
    Illumina = "illumina"
    """
    Illumina.
    """
    Pacbio = "pacbio"
    """
    Pacbio.
    """
    Oxford_Nanopore = "oxford_nanopore"
    """
    Oxford Nanopore.
    """


class MeasurementEnum(str, Enum):
    """
    Measurement.
    """
    pH = "ph"
    """
    pH.
    """
    Time_Elapsed = "time_elapsed"
    """
    Time Elapsed.
    """
    Temperature = "temperature"
    """
    Temperature.
    """
    Conductivity = "conductivity"
    """
    Conductivity.
    """
    Redox_Potential = "redox_potential"
    """
    Redox Potential.
    """
    Count = "count"
    """
    Count.
    """
    Optical_Density = "optical_density"
    """
    Optical Density.
    """
    Size = "size"
    """
    Size.
    """
    Concentration = "concentration"
    """
    Concentration.
    """
    Hybridization_Intensity = "hybridization_intensity"
    """
    Hybridization Intensity.
    """
    Expression_Level = "expression_level"
    """
    Expression Level.
    """
    Enzyme_Activity = "enzyme_activity"
    """
    Enzyme Activity.
    """
    Absorbance = "absorbance"
    """
    Absorbance.
    """
    Heat = "heat"
    """
    Heat.
    """
    Mass = "mass"
    """
    Mass.
    """
    Fitness_Score = "fitness_score"
    """
    Fitness Score.
    """
    Genetic_Interaction_Score = "genetic_interaction_score"
    """
    Genetic Interaction Score.
    """
    Stoichiometric_Ratio = "stoichiometric_ratio"
    """
    Stoichiometric Ratio.
    """
    Relative_Abundance = "relative_abundance"
    """
    Relative amounts of multiple categories of the same object.
    """
    Binary = "binary"
    """
    Binary.
    """
    Pressure = "pressure"
    """
    Pressure.
    """
    Turbidity = "turbidity"
    """
    Turbidity.
    """
    Rate = "rate"
    """
    Rate.
    """
    Sequence = "sequence"
    """
    Sequence.
    """
    Salinity = "salinity"
    """
    Salinity.
    """
    Resistivity = "resistivity"
    """
    Resistivity.
    """
    Saturation = "saturation"
    """
    Saturation.
    """
    Density = "density"
    """
    Density.
    """
    Charge = "charge"
    """
    Charge.
    """
    Wind_Speed = "wind_speed"
    """
    Wind Speed.
    """
    Solar_Radiation = "solar_radiation"
    """
    Solar Radiation.
    """
    Rainfall = "rainfall"
    """
    Rainfall.
    """
    Wind_Direction = "wind_direction"
    """
    Wind Direction.
    """
    Relative_Humidity = "relative_humidity"
    """
    Relative Humidity.
    """
    Error_Range = "error_range"
    """
    Error Range.
    """
    Ion_Intensity = "ion_intensity"
    """
    Ion Intensity.
    """
    Amount = "amount"
    """
    Absolute amount of a substance, such as an element.  See also: concentration.
    """
    Isotope_Ratio = "isotope_ratio"
    """
    Isotope Ratio.
    """
    Sequence_Identity = "sequence_identity"
    """
    Sequence Identity.
    """
    Sequence_Similarity = "sequence_similarity"
    """
    Sequence Similarity.
    """
    Relative_Evolutionary_Divergence = "relative_evolutionary_divergence"
    """
    Relative Evolutionary Divergence.
    """
    Genome_Quality = "genome_quality"
    """
    Genome Quality.
    """
    Jukes_Cantor_Distance = "jukes_cantor_distance"
    """
    Jukes-Cantor Distance.
    """
    Dew_Point = "dew_point"
    """
    Dew Point.
    """
    Fluorescence = "fluorescence"
    """
    Fluorescence.
    """


class StatisticEnum(str, Enum):
    """
    Statistic.
    """
    Average = "average"
    """
    Average.
    """
    Difference = "difference"
    """
    Difference.
    """
    Standard_Deviation = "standard_deviation"
    """
    Standard Deviation.
    """
    Standard_Error = "standard_error"
    """
    Standard Error.
    """
    Minimum = "minimum"
    """
    Minimum.
    """
    Maximum = "maximum"
    """
    Maximum.
    """
    Median = "median"
    """
    Median.
    """
    Ratio = "ratio"
    """
    Ratio.
    """
    Log_Ratio = "log_ratio"
    """
    Log Ratio.
    """
    p_Value = "p_value"
    """
    p Value.
    """
    T_Score = "t_score"
    """
    T Score.
    """
    Frequency = "frequency"
    """
    Frequency.
    """
    Fold_Enrichment = "fold_enrichment"
    """
    Fold Enrichment.
    """
    Confidence = "confidence"
    """
    Confidence.
    """
    Evaluation = "evaluation"
    """
    Evaluation.
    """
    Correlation = "correlation"
    """
    Correlation.
    """
    Multivariate_Analysis = "multivariate_analysis"
    """
    Multivariate Analysis.
    """
    Coefficient_of_Variation = "coefficient_of_variation"
    """
    Coefficient of Variation.
    """


class StrandEnum(str, Enum):
    """
    Strand of DNA
    """
    Forward = "forward"
    """
    Forward.
    """
    Reverse_Complement = "reverse_complement"
    """
    Reverse Complement.
    """


class SequenceTypeEnum(str, Enum):
    """
    Sequence Type.
    """
    number_16S_Sequence = "16s_sequence"
    """
    16S Sequence.
    """
    number_18S_Sequence = "18s_sequence"
    """
    18S Sequence.
    """
    ITS_Sequence = "its_sequence"
    """
    ITS Sequence.
    """
    Genome_Sequence = "genome_sequence"
    """
    Genome Sequence.
    """


class StrainChangeTypeEnum(str, Enum):
    """
    Strain Change Type.
    """
    Insertion = "insertion"
    """
    Insertion.
    """
    Deletion = "deletion"
    """
    Deletion.
    """
    Substitution = "substitution"
    """
    Substitution.
    """


class CommunityTypeEnum(str, Enum):
    """
    Community Type.
    """
    Isolate_Community = "isolate_community"
    """
    Isolate Community.
    """
    Enrichment = "enrichment"
    """
    Enrichment.
    """
    Assemblage = "assemblage"
    """
    Assemblage.
    """
    Environmental_Community = "environmental_community"
    """
    Environmental Community.
    """


class ControlEnum(str, Enum):
    """
    Control.
    """
    Negative_Control = "negative_control"
    """
    Negative Control.
    """
    Positive_Control = "positive_control"
    """
    Positive Control.
    """
    Low_Control = "low_control"
    """
    Low Control.
    """
    High_Control = "high_control"
    """
    High Control.
    """
    Control_Name = "control_name"
    """
    Control Name.
    """


class PositionEnum(str, Enum):
    """
    Position.
    """
    Top = "top"
    """
    Use as context for locations, e.g., the top end of a depth measurement.
    """
    Bottom = "bottom"
    """
    Use as context for locations, e.g., the bottom end of a depth measurement.
    """
    Upper = "upper"
    """
    Upper.
    """
    Lower = "lower"
    """
    Lower.
    """
    Middle = "middle"
    """
    Middle.
    """


class IonizationModeEnum(str, Enum):
    """
    Ionization mode used in a mass spec experiment.
    """
    Positive_Polarity = "positive_polarity"
    """
    Positive Polarity (ionization mode for MS experiment).
    """
    Negative_Polarity = "negative_polarity"
    """
    Negative Polarity (ionization mode for MS experiment).
    """


class GeologicZoneEnum(str, Enum):
    """
    Geologic Zone.
    """
    Vadose_Zone = "vadose_zone"
    """
    Vadose Zone.
    """
    Variably_Saturated_Zone = "variably_saturated_zone"
    """
    Variably Saturated Zone.
    """
    Saturated_Zone = "saturated_zone"
    """
    Saturated Zone.
    """


class GrowthStageEnum(str, Enum):
    """
    Growth Stage.
    """
    Enrichment_Growth = "enrichment_growth"
    """
    Preincubation or enrichment of a microbial sample before plating for colony picking/isolation.
    """
    Inoculation = "inoculation"
    """
    Inoculation.
    """
    Lag_Phase = "lag_phase"
    """
    Lag Phase.
    """
    Exponential_Phase = "exponential_phase"
    """
    Exponential Phase.
    """
    Stationary_Phase = "stationary_phase"
    """
    Stationary Phase.
    """
    Colony_Formation_on_Solid_Media = "colony_formation_on_solid_media"
    """
    Colony formation on solid media, during the process of microbial isolation
    """
    Single_Colony_Growth_in_Liquid_Media = "single_colony_growth_in_liquid_media"
    """
    Single colony growth in liquid media, after microbial isolation
    """


class FlagellarArrangementEnum(str, Enum):
    """
    Flagellar Arrangement.
    """
    Monotrichous = "monotrichous"
    """
    A single flagellum extending from one end of the cell.
    """
    Amphitrichous = "amphitrichous"
    """
    Single or multiple flagella extending from both ends of the cell.
    """
    Lophotrichous = "lophotrichous"
    """
    Tuft of flagella extending from one end or both ends of the cell.
    """
    Peritrichous = "peritrichous"
    """
    Multiple flagella distributed over the entire cell.
    """


class CellShapeEnum(str, Enum):
    """
    Cell Shape.
    """
    Rod = "rod"
    """
    Rod.
    """
    Rod_vibrio = "rod_vibrio"
    """
    Rod-vibrio.
    """
    Oval = "oval"
    """
    Oval.
    """
    Irregular_Oval = "irregular_oval"
    """
    Irregular Oval.
    """
    Spherical = "spherical"
    """
    Spherical.
    """
    Pleomorphic = "pleomorphic"
    """
    Pleomorphic.
    """



class Process(ConfiguredBaseModel):
    """
    Process entity in the ENIGMA data model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'term': {'tag': 'term', 'value': 'DA:0000061'},
                         'used_for_provenance': {'tag': 'used_for_provenance',
                                                 'value': True}},
         'from_schema': 'https://w3id.org/enigma/enigma-cdm'})

    process_id: str = Field(default=..., description="""id field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_id',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000277'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000277'}},
         'domain_of': ['Process']} })
    process_process: str = Field(default=..., description="""process field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_process',
         'annotations': {'constraint': {'tag': 'constraint',
                                        'value': 'PROCESS:0000001'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000204'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'oterm_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000204'}},
         'domain_of': ['Process']} })
    process_person: str = Field(default=..., description="""person field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_person',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'ENIGMA:0000029'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000205'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000205'}},
         'domain_of': ['Process']} })
    process_campaign: str = Field(default=..., description="""campaign field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_campaign',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000206'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000206'}},
         'domain_of': ['Process']} })
    process_protocol: Optional[str] = Field(default=None, description="""protocol field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_protocol',
         'annotations': {'foreign_key': {'tag': 'foreign_key',
                                         'value': 'Protocol.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000328'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000328'}},
         'domain_of': ['Process']} })
    process_date_start: Optional[str] = Field(default=None, description="""date_start field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_date_start',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000009'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000009'}},
         'comments': ['YYYY[-MM[-DD]]'],
         'domain_of': ['Process']} })
    process_date_end: Optional[str] = Field(default=None, description="""date_end field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_date_end',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000009'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000009'}},
         'comments': ['YYYY[-MM[-DD]]'],
         'domain_of': ['Process']} })
    process_input_objects: list[str] = Field(default=..., description="""input_objects field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_input_objects',
         'annotations': {'constraint': {'tag': 'constraint', 'value': '[Entity|Brick]'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000207'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000207'}},
         'domain_of': ['Process']} })
    process_output_objects: list[str] = Field(default=..., description="""output_objects field for Process""", json_schema_extra = { "linkml_meta": {'alias': 'process_output_objects',
         'annotations': {'constraint': {'tag': 'constraint', 'value': '[Entity|Brick]'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000208'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000208'}},
         'domain_of': ['Process']} })


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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000266'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000266'}},
         'domain_of': ['Location']} })
    location_name: str = Field(default=..., description="""name field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000228'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000228'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Location']} })
    location_latitude: float = Field(default=..., description="""latitude field for Location""", ge=-90, le=90, json_schema_extra = { "linkml_meta": {'alias': 'location_latitude',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000211'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'float'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000211'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000185'}},
         'domain_of': ['Location']} })
    location_longitude: float = Field(default=..., description="""longitude field for Location""", ge=-180, le=180, json_schema_extra = { "linkml_meta": {'alias': 'location_longitude',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000212'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'float'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000212'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000185'}},
         'domain_of': ['Location']} })
    location_continent: str = Field(default=..., description="""continent field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_continent',
         'annotations': {'constraint': {'tag': 'constraint',
                                        'value': 'CONTINENT:0000001'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000213'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'oterm_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000213'}},
         'domain_of': ['Location']} })
    location_country: str = Field(default=..., description="""country field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_country',
         'annotations': {'constraint': {'tag': 'constraint',
                                        'value': 'COUNTRY:0000001'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000214'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'oterm_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000214'}},
         'domain_of': ['Location']} })
    location_region: str = Field(default=..., description="""region field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_region',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000215'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000215'}},
         'comments': ['specific local region name(s)'],
         'domain_of': ['Location']} })
    location_biome: str = Field(default=..., description="""biome field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_biome',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'ENVO:01000254'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000216'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'oterm_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000216'}},
         'domain_of': ['Location']} })
    location_feature: Optional[str] = Field(default=None, description="""feature field for Location""", json_schema_extra = { "linkml_meta": {'alias': 'location_feature',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'ENVO:00002297'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000217'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'oterm_ref'},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000267'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000267'}},
         'domain_of': ['Sample']} })
    sample_name: str = Field(default=..., description="""name field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000102'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000102'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Sample']} })
    sample_location: str = Field(default=..., description="""location field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_location',
         'annotations': {'foreign_key': {'tag': 'foreign_key',
                                         'value': 'Location.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000228'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000228'}},
         'domain_of': ['Sample']} })
    sample_depth: Optional[float] = Field(default=None, description="""depth field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_depth',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000219'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'float'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000219'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000008'}},
         'comments': ['in meters below ground level'],
         'domain_of': ['Sample']} })
    sample_elevation: Optional[float] = Field(default=None, description="""elevation field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_elevation',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000220'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'float'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000220'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000008'}},
         'comments': ['in meters above ground level'],
         'domain_of': ['Sample']} })
    sample_date: str = Field(default=..., description="""date field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_date',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000009'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000009'}},
         'comments': ['YYYY[-MM[-DD]]'],
         'domain_of': ['Sample']} })
    sample_time: Optional[str] = Field(default=None, description="""time field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_time',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000010'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000010'}},
         'comments': ['HH[:MM[:SS]] [AM|PM]'],
         'domain_of': ['Sample']} })
    sample_timezone: Optional[str] = Field(default=None, description="""timezone field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_timezone',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000201'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000201'}},
         'comments': ['ISO8601 compliant format, ie. UTC-7'],
         'domain_of': ['Sample']} })
    sample_material: Optional[str] = Field(default=None, description="""material field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_material',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'ENVO:00010483'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000230'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'oterm_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000230'}},
         'domain_of': ['Sample']} })
    sample_env_package: str = Field(default=..., description="""env_package field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_env_package',
         'annotations': {'constraint': {'tag': 'constraint', 'value': 'MIxS:0000002'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000229'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'oterm_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000229'}},
         'domain_of': ['Sample']} })
    sample_description: Optional[str] = Field(default=None, description="""description field for Sample""", json_schema_extra = { "linkml_meta": {'alias': 'sample_description',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000202'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000202'}},
         'domain_of': ['Sample']} })


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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000268'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000268'}},
         'domain_of': ['Taxon']} })
    taxon_name: str = Field(default=..., description="""name field for Taxon""", json_schema_extra = { "linkml_meta": {'alias': 'taxon_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000046'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000046'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Taxon']} })
    taxon_ncbi_taxid: Optional[str] = Field(default=None, description="""ncbi_taxid field for Taxon""", json_schema_extra = { "linkml_meta": {'alias': 'taxon_ncbi_taxid',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000047'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000047'}},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000269'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000269'}},
         'domain_of': ['OTU']} })
    otu_name: str = Field(default=..., description="""name field for OTU""", json_schema_extra = { "linkml_meta": {'alias': 'otu_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000221'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000221'},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000270'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000270'}},
         'domain_of': ['Condition']} })
    condition_name: str = Field(default=..., description="""name field for Condition""", json_schema_extra = { "linkml_meta": {'alias': 'condition_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000200'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000200'},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000271'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000271'}},
         'domain_of': ['Strain']} })
    strain_name: str = Field(default=..., description="""name field for Strain""", json_schema_extra = { "linkml_meta": {'alias': 'strain_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000044'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000044'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Strain']} })
    strain_description: Optional[str] = Field(default=None, description="""description field for Strain""", json_schema_extra = { "linkml_meta": {'alias': 'strain_description',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000202'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000202'}},
         'domain_of': ['Strain']} })
    strain_genome: Optional[str] = Field(default=None, description="""genome field for Strain""", json_schema_extra = { "linkml_meta": {'alias': 'strain_genome',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Genome.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000246'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000246'}},
         'comments': ['genome object for sequenced, WT strains'],
         'domain_of': ['Strain']} })
    strain_derived_from: Optional[str] = Field(default=None, description="""derived_from field for Strain""", json_schema_extra = { "linkml_meta": {'alias': 'strain_derived_from',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Strain.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000044'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000044'}},
         'domain_of': ['Strain']} })
    strain_genes_changed: Optional[list[str]] = Field(default=None, description="""genes_changed field for Strain""", json_schema_extra = { "linkml_meta": {'alias': 'strain_genes_changed',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Gene.gene_id'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000091'},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000272'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000272'}},
         'domain_of': ['Community']} })
    community_name: str = Field(default=..., description="""name field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000233'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000233'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Community']} })
    community_community_type: CommunityTypeEnum = Field(default=..., description="""community_type field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_community_type',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000234'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'oterm_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000234'}},
         'domain_of': ['Community']} })
    community_sample: Optional[str] = Field(default=None, description="""sample field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_sample',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Sample.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000102'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000102'}},
         'domain_of': ['Community']} })
    community_parent_community: Optional[str] = Field(default=None, description="""parent_community field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_parent_community',
         'annotations': {'foreign_key': {'tag': 'foreign_key',
                                         'value': 'Community.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000233'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000233'}},
         'domain_of': ['Community']} })
    community_condition: Optional[str] = Field(default=None, description="""condition field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_condition',
         'annotations': {'foreign_key': {'tag': 'foreign_key',
                                         'value': 'Condition.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000200'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000200'}},
         'domain_of': ['Community']} })
    community_defined_strains: Optional[list[str]] = Field(default=None, description="""defined_strains field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_defined_strains',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Strain.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000044'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000044'}},
         'comments': ['typedef.json has typo with FK pointing to [Strain.Name] with '
                      'capital N',
                      'Using lowercase name to match actual Strain field'],
         'domain_of': ['Community']} })
    community_description: Optional[str] = Field(default=None, description="""description field for Community""", json_schema_extra = { "linkml_meta": {'alias': 'community_description',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000202'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000202'}},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000273'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000273'}},
         'domain_of': ['Reads']} })
    reads_name: str = Field(default=..., description="""name field for Reads""", json_schema_extra = { "linkml_meta": {'alias': 'reads_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000248'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000248'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Reads']} })
    reads_read_count: int = Field(default=..., description="""read_count field for Reads""", json_schema_extra = { "linkml_meta": {'alias': 'reads_read_count',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000126'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['Reads']} })
    reads_read_type: ReadTypeEnum = Field(default=..., description="""read_type field for Reads""", json_schema_extra = { "linkml_meta": {'alias': 'reads_read_type',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000112'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'oterm_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000112'}},
         'domain_of': ['Reads']} })
    reads_sequencing_technology: SequencingTechnologyEnum = Field(default=..., description="""sequencing_technology field for Reads""", json_schema_extra = { "linkml_meta": {'alias': 'reads_sequencing_technology',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000116'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'oterm_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000116'}},
         'domain_of': ['Reads']} })
    reads_link: str = Field(default=..., description="""link field for Reads""", json_schema_extra = { "linkml_meta": {'alias': 'reads_link',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000203'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000203'}},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000281'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000281'}},
         'domain_of': ['Assembly']} })
    assembly_name: str = Field(default=..., description="""name field for Assembly""", json_schema_extra = { "linkml_meta": {'alias': 'assembly_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000280'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000280'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Assembly']} })
    assembly_strain: Optional[str] = Field(default=None, description="""strain field for Assembly""", json_schema_extra = { "linkml_meta": {'alias': 'assembly_strain',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Strain.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000044'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000044'}},
         'domain_of': ['Assembly']} })
    assembly_n_contigs: int = Field(default=..., description="""n_contigs field for Assembly""", json_schema_extra = { "linkml_meta": {'alias': 'assembly_n_contigs',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000126'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['Assembly']} })
    assembly_link: str = Field(default=..., description="""link field for Assembly""", json_schema_extra = { "linkml_meta": {'alias': 'assembly_link',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000203'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000203'}},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000274'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000274'}},
         'domain_of': ['Genome']} })
    genome_name: str = Field(default=..., description="""name field for Genome""", json_schema_extra = { "linkml_meta": {'alias': 'genome_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000246'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000246'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Genome']} })
    genome_strain: Optional[str] = Field(default=None, description="""strain field for Genome""", json_schema_extra = { "linkml_meta": {'alias': 'genome_strain',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Strain.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000044'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000044'}},
         'domain_of': ['Genome']} })
    genome_n_contigs: int = Field(default=..., description="""n_contigs field for Genome""", json_schema_extra = { "linkml_meta": {'alias': 'genome_n_contigs',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000126'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['Genome']} })
    genome_n_features: int = Field(default=..., description="""n_features field for Genome""", json_schema_extra = { "linkml_meta": {'alias': 'genome_n_features',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000126'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['Genome']} })
    genome_link: str = Field(default=..., description="""link field for Genome""", json_schema_extra = { "linkml_meta": {'alias': 'genome_link',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000203'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000203'}},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000275'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000275'}},
         'domain_of': ['Gene']} })
    gene_gene_id: str = Field(default=..., description="""gene_id field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_gene_id',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000224'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000224'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Gene']} })
    gene_genome: str = Field(default=..., description="""genome field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_genome',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Genome.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000246'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000246'}},
         'comments': ['typedef.json has FK pointing to Genome without specifying '
                      'target field',
                      'Assumed to reference Genome.name based on pattern'],
         'domain_of': ['Gene']} })
    gene_aliases: Optional[list[str]] = Field(default=None, description="""aliases field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_aliases',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000060'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000060'}},
         'domain_of': ['Gene']} })
    gene_contig_number: int = Field(default=..., description="""contig_number field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_contig_number',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000126'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'comments': ['indexed starting at 1, as in KBase'],
         'domain_of': ['Gene']} })
    gene_strand: StrandEnum = Field(default=..., description="""strand field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_strand',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000186'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'oterm_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000186'}},
         'domain_of': ['Gene']} })
    gene_start: int = Field(default=..., description="""start field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_start',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000242'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000242'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000244'}},
         'comments': ['indexed starting at 1, as in KBase'],
         'domain_of': ['Gene']} })
    gene_stop: int = Field(default=..., description="""stop field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_stop',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000243'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000243'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000244'}},
         'domain_of': ['Gene']} })
    gene_function: Optional[str] = Field(default=None, description="""function field for Gene""", json_schema_extra = { "linkml_meta": {'alias': 'gene_function',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000250'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000250'}},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000331'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000331'}},
         'domain_of': ['Bin']} })
    bin_name: str = Field(default=..., description="""name field for Bin""", json_schema_extra = { "linkml_meta": {'alias': 'bin_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000330'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000330'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Bin']} })
    bin_assembly: str = Field(default=..., description="""assembly field for Bin""", json_schema_extra = { "linkml_meta": {'alias': 'bin_assembly',
         'annotations': {'foreign_key': {'tag': 'foreign_key',
                                         'value': 'Assembly.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000280'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000280'}},
         'comments': ['typedef.json has FK pointing to Assembly without specifying '
                      'target field',
                      'Assumed to reference Assembly.name based on pattern'],
         'domain_of': ['Bin']} })
    bin_contigs: list[str] = Field(default=..., description="""contigs field for Bin""", json_schema_extra = { "linkml_meta": {'alias': 'bin_contigs',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000240'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000240'}},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000332'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000332'}},
         'domain_of': ['Protocol']} })
    protocol_name: str = Field(default=..., description="""name field for Protocol""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000328'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000328'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Protocol']} })
    protocol_description: Optional[str] = Field(default=None, description="""description field for Protocol""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_description',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000202'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000202'}},
         'domain_of': ['Protocol']} })
    protocol_link: Optional[str] = Field(default=None, description="""link field for Protocol""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_link',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000203'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000203'}},
         'domain_of': ['Protocol']} })


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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000356'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000356'}},
         'domain_of': ['Image']} })
    image_name: str = Field(default=..., description="""name field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000355'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000355'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['Image']} })
    image_description: Optional[str] = Field(default=None, description="""description field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_description',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000202'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000202'}},
         'domain_of': ['Image']} })
    image_MIME_type: Optional[str] = Field(default=None, description="""MIME type field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_MIME_type',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000357'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000357'}},
         'domain_of': ['Image']} })
    image_size: Optional[float] = Field(default=None, description="""size field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_size',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000128'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'float'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000128'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000233'}},
         'domain_of': ['Image']} })
    image_dimensions: Optional[str] = Field(default=None, description="""dimensions field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_dimensions',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000292'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000292'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000236'}},
         'domain_of': ['Image']} })
    image_link: Optional[str] = Field(default=None, description="""link field for Image""", json_schema_extra = { "linkml_meta": {'alias': 'image_link',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000203'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000203'}},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000276'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000276'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_name: str = Field(default=..., description="""name field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000262'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000262'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_genome: str = Field(default=..., description="""genome field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_genome',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Genome.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000246'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000246'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_primers_model: str = Field(default=..., description="""primers_model field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_primers_model',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000263'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'string'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000263'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_n_mapped_reads: Optional[int] = Field(default=None, description="""n_mapped_reads field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_n_mapped_reads',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000126'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_n_barcodes: Optional[int] = Field(default=None, description="""n_barcodes field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_n_barcodes',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000126'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_n_usable_barcodes: Optional[int] = Field(default=None, description="""n_usable_barcodes field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_n_usable_barcodes',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000126'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_n_insertion_locations: Optional[int] = Field(default=None, description="""n_insertion_locations field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_n_insertion_locations',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000126'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_hit_rate_essential: Optional[float] = Field(default=None, description="""hit_rate_essential field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_hit_rate_essential',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000264'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'float'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000264'},
                         'units_term': {'tag': 'units_term', 'value': 'UO:0000190'}},
         'domain_of': ['TnSeq_Library']} })
    tnseq_library_hit_rate_other: Optional[float] = Field(default=None, description="""hit_rate_other field for TnSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'tnseq_library_hit_rate_other',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000264'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'float'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000264'},
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
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000276'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000276'}},
         'domain_of': ['DubSeq_Library']} })
    dubseq_library_name: str = Field(default=..., description="""name field for DubSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'dubseq_library_name',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000262'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000262'},
                         'unique': {'tag': 'unique', 'value': True}},
         'domain_of': ['DubSeq_Library']} })
    dubseq_library_genome: str = Field(default=..., description="""genome field for DubSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'dubseq_library_genome',
         'annotations': {'foreign_key': {'tag': 'foreign_key', 'value': 'Genome.name'},
                         'microtype': {'tag': 'microtype', 'value': 'ME:0000246'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'object_ref'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000246'}},
         'domain_of': ['DubSeq_Library']} })
    dubseq_library_n_fragments: Optional[int] = Field(default=None, description="""n_fragments field for DubSeq_Library""", json_schema_extra = { "linkml_meta": {'alias': 'dubseq_library_n_fragments',
         'annotations': {'microtype': {'tag': 'microtype', 'value': 'ME:0000126'},
                         'microtype_data_type': {'tag': 'microtype_data_type',
                                                 'value': 'int'},
                         'type_term': {'tag': 'type_term', 'value': 'ME:0000126'},
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

