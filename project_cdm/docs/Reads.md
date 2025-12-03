
# Class: Reads

Sequencing reads dataset.

CDM changes from CORAL:
- 2 ontology term fields split: read_type, sequencing_technology
- Added 'link' field for external data references

URI: [kbase_cdm:Reads](https://w3id.org/enigma/kbase-cdm/Reads)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Reads&#124;sdt_reads_id:string;sdt_reads_name:EntityName;read_count:Count%20%3F;base_count:Count%20%3F;read_type_sys_oterm_id:OntologyTermID%20%3F;read_type_sys_oterm_name:string%20%3F;sequencing_technology_sys_oterm_id:OntologyTermID%20%3F;sequencing_technology_sys_oterm_name:string%20%3F;link:Link%20%3F]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Reads&#124;sdt_reads_id:string;sdt_reads_name:EntityName;read_count:Count%20%3F;base_count:Count%20%3F;read_type_sys_oterm_id:OntologyTermID%20%3F;read_type_sys_oterm_name:string%20%3F;sequencing_technology_sys_oterm_id:OntologyTermID%20%3F;sequencing_technology_sys_oterm_name:string%20%3F;link:Link%20%3F]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_reads_id](sdt_reads_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Reads
     * Range: [String](types/String.md)
 * [sdt_reads_name](sdt_reads_name.md)  <sub>1..1</sub>
     * Description: Name of reads dataset
     * Range: [EntityName](types/EntityName.md)
 * [read_count](read_count.md)  <sub>0..1</sub>
     * Description: Number of reads
     * Range: [Count](types/Count.md)
 * [base_count](base_count.md)  <sub>0..1</sub>
     * Description: Total number of bases
     * Range: [Count](types/Count.md)
 * [read_type_sys_oterm_id](read_type_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Read type ontology term ID (e.g., paired-end, single-end)
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [read_type_sys_oterm_name](read_type_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Read type ontology term name
     * Range: [String](types/String.md)
 * [sequencing_technology_sys_oterm_id](sequencing_technology_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Sequencing technology ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [sequencing_technology_sys_oterm_name](sequencing_technology_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Sequencing technology ontology term name
     * Range: [String](types/String.md)
 * [link](link.md)  <sub>0..1</sub>
     * Description: External reference URL or file path
     * Range: [Link](types/Link.md)
