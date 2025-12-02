
# Class: SystemProcess

Provenance tracking for all data transformations.

Records experimental processes with:
- Process type (Assay Growth, Sequencing, etc.)
- People, protocols, campaigns
- Temporal metadata (start/end dates)
- Input/output relationships (denormalized arrays)

Enables complete lineage tracing from raw samples to final analyses.

URI: [kbase_cdm:SystemProcess](https://w3id.org/enigma/kbase-cdm/SystemProcess)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemProcess&#124;sys_process_id:string;process_type_sys_oterm_id:OntologyTermID%20%3F;process_type_sys_oterm_name:string%20%3F;person_sys_oterm_id:OntologyTermID%20%3F;person_sys_oterm_name:string%20%3F;campaign_sys_oterm_id:OntologyTermID%20%3F;campaign_sys_oterm_name:string%20%3F;sdt_protocol_name:EntityName;date_start:Date%20%3F;date_end:Date%20%3F;input_objects:string%20*;output_objects:string%20*]uses%20-.->[SystemEntity],[SystemEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemProcess&#124;sys_process_id:string;process_type_sys_oterm_id:OntologyTermID%20%3F;process_type_sys_oterm_name:string%20%3F;person_sys_oterm_id:OntologyTermID%20%3F;person_sys_oterm_name:string%20%3F;campaign_sys_oterm_id:OntologyTermID%20%3F;campaign_sys_oterm_name:string%20%3F;sdt_protocol_name:EntityName;date_start:Date%20%3F;date_end:Date%20%3F;input_objects:string%20*;output_objects:string%20*]uses%20-.->[SystemEntity],[SystemEntity])

## Uses Mixin

 *  mixin: [SystemEntity](SystemEntity.md) - Base mixin for CDM system tables (sys_*).

## Referenced by Class


## Attributes


### Own

 * [SystemProcess➞sys_process_id](SystemProcess_sys_process_id.md)  <sub>1..1</sub>
     * Description: Unique process identifier
     * Range: [String](types/String.md)
 * [process_type_sys_oterm_id](process_type_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Process type ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [process_type_sys_oterm_name](process_type_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Process type ontology term name
     * Range: [String](types/String.md)
 * [person_sys_oterm_id](person_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Person who performed process (ontology term ID)
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [person_sys_oterm_name](person_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Person who performed process (ontology term name)
     * Range: [String](types/String.md)
 * [campaign_sys_oterm_id](campaign_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Research campaign ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [campaign_sys_oterm_name](campaign_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Research campaign ontology term name
     * Range: [String](types/String.md)
 * [sdt_protocol_name](sdt_protocol_name.md)  <sub>1..1</sub>
     * Description: Name of protocol
     * Range: [EntityName](types/EntityName.md)
 * [date_start](date_start.md)  <sub>0..1</sub>
     * Description: Process start date
     * Range: [Date](types/Date.md)
 * [date_end](date_end.md)  <sub>0..1</sub>
     * Description: Process end date
     * Range: [Date](types/Date.md)
 * [input_objects](input_objects.md)  <sub>0..\*</sub>
     * Description: Array of input entity references (type:name format)
     * Range: [String](types/String.md)
 * [output_objects](output_objects.md)  <sub>0..\*</sub>
     * Description: Array of output entity references (type:name format)
     * Range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | kbase_cdm:SystemProcess |
