
# Class: Genome

Assembled and annotated genome.

CDM changes from CORAL:
- FK reference: strain → strain_ref
- Added 'link' field

URI: [kbase_cdm:Genome](https://w3id.org/enigma/kbase-cdm/Genome)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Genome&#124;sdt_genome_id:string;sdt_genome_name:EntityName;strain_ref:EntityName%20%3F;n_contigs:Count%20%3F;n_features:Count%20%3F;total_size:Size%20%3F;link:Link%20%3F]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Genome&#124;sdt_genome_id:string;sdt_genome_name:EntityName;strain_ref:EntityName%20%3F;n_contigs:Count%20%3F;n_features:Count%20%3F;total_size:Size%20%3F;link:Link%20%3F]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_genome_id](sdt_genome_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Genome
     * Range: [String](types/String.md)
 * [sdt_genome_name](sdt_genome_name.md)  <sub>1..1</sub>
     * Description: Name of genome
     * Range: [EntityName](types/EntityName.md)
 * [strain_ref](strain_ref.md)  <sub>0..1</sub>
     * Description: Reference to strain name (FK to Strain.sdt_strain_name)
     * Range: [EntityName](types/EntityName.md)
 * [n_contigs](n_contigs.md)  <sub>0..1</sub>
     * Description: Number of contigs
     * Range: [Count](types/Count.md)
 * [n_features](n_features.md)  <sub>0..1</sub>
     * Description: Number of annotated features
     * Range: [Count](types/Count.md)
 * [total_size](total_size.md)  <sub>0..1</sub>
     * Description: Total assembly size in base pairs
     * Range: [Size](types/Size.md)
 * [link](link.md)  <sub>0..1</sub>
     * Description: External reference URL or file path
     * Range: [Link](types/Link.md)
