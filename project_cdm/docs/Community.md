
# Class: Community

Microbial community (isolate, enrichment, assemblage, or environmental).

CDM changes from CORAL:
- 1 ontology term field split: community_type
- FK references: sample → sample_ref, parent_community → parent_community_ref
- Multivalued FK: defined_strains → defined_strains_ref

URI: [kbase_cdm:Community](https://w3id.org/enigma/kbase-cdm/Community)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Community&#124;sdt_community_id:string;sdt_community_name:EntityName;community_type_sys_oterm_id:OntologyTermID%20%3F;community_type_sys_oterm_name:string%20%3F;sample_ref:EntityName%20%3F;parent_community_ref:EntityName%20%3F;defined_strains_ref:EntityName%20*]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Community&#124;sdt_community_id:string;sdt_community_name:EntityName;community_type_sys_oterm_id:OntologyTermID%20%3F;community_type_sys_oterm_name:string%20%3F;sample_ref:EntityName%20%3F;parent_community_ref:EntityName%20%3F;defined_strains_ref:EntityName%20*]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_community_id](sdt_community_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Community
     * Range: [String](types/String.md)
 * [sdt_community_name](sdt_community_name.md)  <sub>1..1</sub>
     * Description: Name of community
     * Range: [EntityName](types/EntityName.md)
 * [community_type_sys_oterm_id](community_type_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Community type ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [community_type_sys_oterm_name](community_type_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Community type ontology term name
     * Range: [String](types/String.md)
 * [sample_ref](sample_ref.md)  <sub>0..1</sub>
     * Description: Reference to sample name (FK to Sample.sdt_sample_name)
     * Range: [EntityName](types/EntityName.md)
 * [parent_community_ref](parent_community_ref.md)  <sub>0..1</sub>
     * Description: Reference to parent community name (FK, self-referential to Community.sdt_community_name)
     * Range: [EntityName](types/EntityName.md)
 * [defined_strains_ref](defined_strains_ref.md)  <sub>0..\*</sub>
     * Description: References to defined strain names (multivalued FK to Strain.sdt_strain_name)
     * Range: [EntityName](types/EntityName.md)
