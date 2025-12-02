
# Class: SystemTypedef

Type definitions for static entity tables (equivalent to typedef.json).

Maps CORAL entity types and fields to CDM table/column names with
constraints, data types, and ontology references.

This table documents the schema transformation from CORAL to CDM and
enables automated validation and migration.

URI: [kbase_cdm:SystemTypedef](https://w3id.org/enigma/kbase-cdm/SystemTypedef)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemTypedef&#124;type_name:string;field_name:string;cdm_column_name:string;scalar_type:string%20%3F;pk:boolean%20%3F;upk:boolean%20%3F;fk:string%20%3F;constraint:string%20%3F;units_sys_oterm_id:OntologyTermID%20%3F;type_sys_oterm_id:OntologyTermID%20%3F]uses%20-.->[SystemEntity],[SystemEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemTypedef&#124;type_name:string;field_name:string;cdm_column_name:string;scalar_type:string%20%3F;pk:boolean%20%3F;upk:boolean%20%3F;fk:string%20%3F;constraint:string%20%3F;units_sys_oterm_id:OntologyTermID%20%3F;type_sys_oterm_id:OntologyTermID%20%3F]uses%20-.->[SystemEntity],[SystemEntity])

## Uses Mixin

 *  mixin: [SystemEntity](SystemEntity.md) - Base mixin for CDM system tables (sys_*).

## Attributes


### Own

 * [type_name](type_name.md)  <sub>1..1</sub>
     * Description: CORAL entity type name (e.g., "Gene", "Sample")
     * Range: [String](types/String.md)
 * [field_name](field_name.md)  <sub>1..1</sub>
     * Description: Original CORAL field name
     * Range: [String](types/String.md)
 * [cdm_column_name](cdm_column_name.md)  <sub>1..1</sub>
     * Description: Mapped CDM column name (snake_case with prefixes)
     * Range: [String](types/String.md)
 * [scalar_type](scalar_type.md)  <sub>0..1</sub>
     * Description: Data type (text, int, float, [text] for arrays)
     * Range: [String](types/String.md)
 * [pk](pk.md)  <sub>0..1</sub>
     * Description: Primary key flag
     * Range: [Boolean](types/Boolean.md)
 * [upk](upk.md)  <sub>0..1</sub>
     * Description: Unique key flag
     * Range: [Boolean](types/Boolean.md)
 * [fk](fk.md)  <sub>0..1</sub>
     * Description: Foreign key reference
     * Range: [String](types/String.md)
 * [constraint](constraint.md)  <sub>0..1</sub>
     * Description: Validation pattern or ontology constraint
     * Range: [String](types/String.md)
 * [units_sys_oterm_id](units_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Ontology term for measurement units
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [type_sys_oterm_id](type_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Ontology term for data type
     * Range: [OntologyTermID](types/OntologyTermID.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | kbase_cdm:SystemTypedef |
