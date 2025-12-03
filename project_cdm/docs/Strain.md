
# Class: Strain

Microbial strain (isolated or derived).

CDM changes from CORAL:
- FK references: genome → genome_ref, derived_from → derived_from_strain_ref
- Self-referential for strain derivation lineage

URI: [kbase_cdm:Strain](https://w3id.org/enigma/kbase-cdm/Strain)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Strain&#124;sdt_strain_id:string;sdt_strain_name:EntityName;genome_ref:EntityName%20%3F;derived_from_strain_ref:EntityName%20%3F;gene_names_changed:EntityName%20*]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Strain&#124;sdt_strain_id:string;sdt_strain_name:EntityName;genome_ref:EntityName%20%3F;derived_from_strain_ref:EntityName%20%3F;gene_names_changed:EntityName%20*]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_strain_id](sdt_strain_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Strain
     * Range: [String](types/String.md)
 * [sdt_strain_name](sdt_strain_name.md)  <sub>1..1</sub>
     * Description: Name of strain
     * Range: [EntityName](types/EntityName.md)
 * [genome_ref](genome_ref.md)  <sub>0..1</sub>
     * Description: Reference to genome name (FK to Genome.sdt_genome_name)
     * Range: [EntityName](types/EntityName.md)
 * [derived_from_strain_ref](derived_from_strain_ref.md)  <sub>0..1</sub>
     * Description: Reference to parent strain name (FK, self-referential to Strain.sdt_strain_name)
     * Range: [EntityName](types/EntityName.md)
 * [gene_names_changed](gene_names_changed.md)  <sub>0..\*</sub>
     * Description: Names of genes that were changed
     * Range: [EntityName](types/EntityName.md)
