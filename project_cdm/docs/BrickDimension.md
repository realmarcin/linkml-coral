
# Class: BrickDimension

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

URI: [kbase_cdm:BrickDimension](https://w3id.org/enigma/kbase-cdm/BrickDimension)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[BrickDimension&#124;dimension_number:integer%20%3F;dimension_oterm_id:OntologyTermID%20%3F;dimension_oterm_name:string%20%3F;dimension_size:integer%20%3F;dimension_values:string%20%3F])](https://yuml.me/diagram/nofunky;dir:TB/class/[BrickDimension&#124;dimension_number:integer%20%3F;dimension_oterm_id:OntologyTermID%20%3F;dimension_oterm_name:string%20%3F;dimension_size:integer%20%3F;dimension_values:string%20%3F])

## Attributes


### Own

 * [dimension_number](dimension_number.md)  <sub>0..1</sub>
     * Description: Position in N-dimensional array (0-indexed)
     * Range: [Integer](types/Integer.md)
 * [dimension_oterm_id](dimension_oterm_id.md)  <sub>0..1</sub>
     * Description: Dimension semantic ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [dimension_oterm_name](dimension_oterm_name.md)  <sub>0..1</sub>
     * Description: Dimension semantic ontology term name
     * Range: [String](types/String.md)
 * [dimension_size](dimension_size.md)  <sub>0..1</sub>
     * Description: Number of values along this dimension
     * Range: [Integer](types/Integer.md)
 * [dimension_values](dimension_values.md)  <sub>0..1</sub>
     * Description: Comma-separated dimension value labels
     * Range: [String](types/String.md)
