
# Class: SystemDDTTypedef

Type definitions for dynamic data tables (bricks).

Defines schema for N-dimensional measurement arrays including:
- Dimension semantics (Environmental Sample, Molecule, State, Statistic)
- Variable semantics (Concentration, Molecular Weight, etc.)
- Data types and units
- Brick structure metadata

Each brick can have different dimensionality and variable sets,
enabling flexible storage of heterogeneous measurement data.

URI: [kbase_cdm:SystemDDTTypedef](https://w3id.org/enigma/kbase-cdm/SystemDDTTypedef)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemEntity],[SystemDDTTypedef&#124;ddt_ndarray_id:string;cdm_column_name:string;cdm_column_data_type:string%20%3F;scalar_type:string%20%3F;dimension_number:integer%20%3F;variable_number:integer%20%3F;dimension_oterm_id:OntologyTermID%20%3F;dimension_oterm_name:string%20%3F;variable_oterm_id:OntologyTermID%20%3F;variable_oterm_name:string%20%3F;unit_sys_oterm_id:OntologyTermID%20%3F;unit_sys_oterm_name:string%20%3F]uses%20-.->[SystemEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemEntity],[SystemDDTTypedef&#124;ddt_ndarray_id:string;cdm_column_name:string;cdm_column_data_type:string%20%3F;scalar_type:string%20%3F;dimension_number:integer%20%3F;variable_number:integer%20%3F;dimension_oterm_id:OntologyTermID%20%3F;dimension_oterm_name:string%20%3F;variable_oterm_id:OntologyTermID%20%3F;variable_oterm_name:string%20%3F;unit_sys_oterm_id:OntologyTermID%20%3F;unit_sys_oterm_name:string%20%3F]uses%20-.->[SystemEntity])

## Uses Mixin

 *  mixin: [SystemEntity](SystemEntity.md) - Base mixin for CDM system tables (sys_*).

## Attributes


### Own

 * [ddt_ndarray_id](ddt_ndarray_id.md)  <sub>1..1</sub>
     * Description: Brick identifier (e.g., "Brick0000010")
     * Range: [String](types/String.md)
 * [cdm_column_name](cdm_column_name.md)  <sub>1..1</sub>
     * Description: Mapped CDM column name (snake_case with prefixes)
     * Range: [String](types/String.md)
 * [cdm_column_data_type](cdm_column_data_type.md)  <sub>0..1</sub>
     * Description: Column type (variable, dimension_variable, or dimension_index)
     * Range: [String](types/String.md)
 * [scalar_type](scalar_type.md)  <sub>0..1</sub>
     * Description: Data type (text, int, float, [text] for arrays)
     * Range: [String](types/String.md)
 * [dimension_number](dimension_number.md)  <sub>0..1</sub>
     * Description: Position in N-dimensional array (0-indexed)
     * Range: [Integer](types/Integer.md)
 * [variable_number](variable_number.md)  <sub>0..1</sub>
     * Description: Variable index in brick
     * Range: [Integer](types/Integer.md)
 * [dimension_oterm_id](dimension_oterm_id.md)  <sub>0..1</sub>
     * Description: Dimension semantic ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [dimension_oterm_name](dimension_oterm_name.md)  <sub>0..1</sub>
     * Description: Dimension semantic ontology term name
     * Range: [String](types/String.md)
 * [variable_oterm_id](variable_oterm_id.md)  <sub>0..1</sub>
     * Description: Variable semantic ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [variable_oterm_name](variable_oterm_name.md)  <sub>0..1</sub>
     * Description: Variable semantic ontology term name
     * Range: [String](types/String.md)
 * [unit_sys_oterm_id](unit_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Measurement unit ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [unit_sys_oterm_name](unit_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Measurement unit ontology term name
     * Range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | kbase_cdm:SystemDDTTypedef |
