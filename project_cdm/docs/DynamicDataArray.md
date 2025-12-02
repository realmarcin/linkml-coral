
# Class: DynamicDataArray

Brick index table (ddt_ndarray).

Catalogs all available measurement bricks with:
- Brick identifiers (Brick0000001, Brick0000002, etc.)
- Shape metadata (dimensions and sizes)
- Entity relationships (which samples, communities, etc.)
- Semantic metadata (measurement types, units)

Each brick corresponds to:
- One ddt_brick* table with actual measurement data
- Multiple rows in sys_ddt_typedef defining brick schema

URI: [kbase_cdm:DynamicDataArray](https://w3id.org/enigma/kbase-cdm/DynamicDataArray)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemEntity],[DynamicDataArray&#124;ddt_ndarray_id:string;brick_table_name:string%20%3F;n_dimensions:integer%20%3F;dimension_sizes:string%20%3F;n_variables:integer%20%3F;total_rows:integer%20%3F;associated_entity_type:string%20%3F;associated_entity_names:EntityName%20*;measurement_type_sys_oterm_id:OntologyTermID%20%3F;measurement_type_sys_oterm_name:string%20%3F;creation_date:Date%20%3F;description:string%20%3F]uses%20-.->[SystemEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemEntity],[DynamicDataArray&#124;ddt_ndarray_id:string;brick_table_name:string%20%3F;n_dimensions:integer%20%3F;dimension_sizes:string%20%3F;n_variables:integer%20%3F;total_rows:integer%20%3F;associated_entity_type:string%20%3F;associated_entity_names:EntityName%20*;measurement_type_sys_oterm_id:OntologyTermID%20%3F;measurement_type_sys_oterm_name:string%20%3F;creation_date:Date%20%3F;description:string%20%3F]uses%20-.->[SystemEntity])

## Uses Mixin

 *  mixin: [SystemEntity](SystemEntity.md) - Base mixin for CDM system tables (sys_*).

## Referenced by Class


## Attributes


### Own

 * [DynamicDataArray➞ddt_ndarray_id](DynamicDataArray_ddt_ndarray_id.md)  <sub>1..1</sub>
     * Description: Brick identifier (e.g., "Brick0000010")
     * Range: [String](types/String.md)
 * [brick_table_name](brick_table_name.md)  <sub>0..1</sub>
     * Description: Name of brick table (e.g., "ddt_brick0000010")
     * Range: [String](types/String.md)
 * [n_dimensions](n_dimensions.md)  <sub>0..1</sub>
     * Description: Number of dimensions in array
     * Range: [Integer](types/Integer.md)
 * [dimension_sizes](dimension_sizes.md)  <sub>0..1</sub>
     * Description: Comma-separated dimension sizes (e.g., "209,52,3,3")
     * Range: [String](types/String.md)
 * [n_variables](n_variables.md)  <sub>0..1</sub>
     * Description: Number of measured variables
     * Range: [Integer](types/Integer.md)
 * [total_rows](total_rows.md)  <sub>0..1</sub>
     * Description: Total number of data rows in brick table
     * Range: [Integer](types/Integer.md)
 * [associated_entity_type](associated_entity_type.md)  <sub>0..1</sub>
     * Description: Type of entities measured (e.g., "Sample", "Community")
     * Range: [String](types/String.md)
 * [associated_entity_names](associated_entity_names.md)  <sub>0..\*</sub>
     * Description: Names of entities associated with this brick
     * Range: [EntityName](types/EntityName.md)
 * [measurement_type_sys_oterm_id](measurement_type_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Type of measurement ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [measurement_type_sys_oterm_name](measurement_type_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Type of measurement ontology term name
     * Range: [String](types/String.md)
 * [creation_date](creation_date.md)  <sub>0..1</sub>
     * Description: Date brick was created
     * Range: [Date](types/Date.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: Free text description
     * Range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | kbase_cdm:DynamicDataArray |
