
# Class: SystemProcessOutput

Normalized process output relationships.

Denormalizes the output_objects array from sys_process for efficient
querying. Each row represents one output entity from one process.

Enables queries like:
- "What process created this assembly?"
- "Find all assemblies from sequencing processes"

URI: [kbase_cdm:SystemProcessOutput](https://w3id.org/enigma/kbase-cdm/SystemProcessOutput)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemProcessOutput&#124;sys_process_id:string;output_object_type:string%20%3F;output_object_name:EntityName%20%3F;output_index:integer%20%3F]uses%20-.->[SystemEntity],[SystemEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemProcessOutput&#124;sys_process_id:string;output_object_type:string%20%3F;output_object_name:EntityName%20%3F;output_index:integer%20%3F]uses%20-.->[SystemEntity],[SystemEntity])

## Uses Mixin

 *  mixin: [SystemEntity](SystemEntity.md) - Base mixin for CDM system tables (sys_*).

## Attributes


### Own

 * [sys_process_id](sys_process_id.md)  <sub>1..1</sub>
     * Description: Unique process identifier
     * Range: [String](types/String.md)
 * [output_object_type](output_object_type.md)  <sub>0..1</sub>
     * Description: Type of output entity (e.g., "Assembly", "Genome")
     * Range: [String](types/String.md)
 * [output_object_name](output_object_name.md)  <sub>0..1</sub>
     * Description: Name of output entity
     * Range: [EntityName](types/EntityName.md)
 * [output_index](output_index.md)  <sub>0..1</sub>
     * Description: Index in output_objects array
     * Range: [Integer](types/Integer.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | kbase_cdm:SystemProcessOutput |
