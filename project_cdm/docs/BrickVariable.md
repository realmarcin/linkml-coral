
# Class: BrickVariable

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

URI: [kbase_cdm:BrickVariable](https://w3id.org/enigma/kbase-cdm/BrickVariable)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[BrickVariable&#124;variable_number:integer%20%3F;variable_oterm_id:OntologyTermID%20%3F;variable_oterm_name:string%20%3F;variable_data_type:string%20%3F;unit_sys_oterm_id:OntologyTermID%20%3F;unit_sys_oterm_name:string%20%3F;min_value:float%20%3F;max_value:float%20%3F])](https://yuml.me/diagram/nofunky;dir:TB/class/[BrickVariable&#124;variable_number:integer%20%3F;variable_oterm_id:OntologyTermID%20%3F;variable_oterm_name:string%20%3F;variable_data_type:string%20%3F;unit_sys_oterm_id:OntologyTermID%20%3F;unit_sys_oterm_name:string%20%3F;min_value:float%20%3F;max_value:float%20%3F])

## Attributes


### Own

 * [variable_number](variable_number.md)  <sub>0..1</sub>
     * Description: Variable index in brick
     * Range: [Integer](types/Integer.md)
 * [variable_oterm_id](variable_oterm_id.md)  <sub>0..1</sub>
     * Description: Variable semantic ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [variable_oterm_name](variable_oterm_name.md)  <sub>0..1</sub>
     * Description: Variable semantic ontology term name
     * Range: [String](types/String.md)
 * [variable_data_type](variable_data_type.md)  <sub>0..1</sub>
     * Description: Data type of variable (float, int, bool, oterm_ref, object_ref)
     * Range: [String](types/String.md)
 * [unit_sys_oterm_id](unit_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Measurement unit ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [unit_sys_oterm_name](unit_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Measurement unit ontology term name
     * Range: [String](types/String.md)
 * [min_value](min_value.md)  <sub>0..1</sub>
     * Description: Minimum allowed value (for numeric variables)
     * Range: [Float](types/Float.md)
 * [max_value](max_value.md)  <sub>0..1</sub>
     * Description: Maximum allowed value (for numeric variables)
     * Range: [Float](types/Float.md)
