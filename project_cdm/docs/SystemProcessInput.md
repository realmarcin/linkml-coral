
# Class: SystemProcessInput

Normalized process input relationships.

Denormalizes the input_objects array from sys_process for efficient
querying. Each row represents one input entity to one process.

Enables queries like:
- "Find all processes that used this sample"
- "What samples were used in sequencing processes?"

URI: [kbase_cdm:SystemProcessInput](https://w3id.org/enigma/kbase-cdm/SystemProcessInput)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemProcessInput&#124;sys_process_id:string;input_object_type:string%20%3F;input_object_name:EntityName%20%3F;input_index:integer%20%3F]uses%20-.->[SystemEntity],[SystemEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemProcessInput&#124;sys_process_id:string;input_object_type:string%20%3F;input_object_name:EntityName%20%3F;input_index:integer%20%3F]uses%20-.->[SystemEntity],[SystemEntity])

## Uses Mixin

 *  mixin: [SystemEntity](SystemEntity.md) - Base mixin for CDM system tables (sys_*).

## Attributes


### Own

 * [sys_process_id](sys_process_id.md)  <sub>1..1</sub>
     * Description: Unique process identifier
     * Range: [String](types/String.md)
 * [input_object_type](input_object_type.md)  <sub>0..1</sub>
     * Description: Type of input entity (e.g., "Sample", "Reads")
     * Range: [String](types/String.md)
 * [input_object_name](input_object_name.md)  <sub>0..1</sub>
     * Description: Name of input entity
     * Range: [EntityName](types/EntityName.md)
 * [input_index](input_index.md)  <sub>0..1</sub>
     * Description: Index in input_objects array
     * Range: [Integer](types/Integer.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | kbase_cdm:SystemProcessInput |
