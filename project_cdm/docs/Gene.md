
# Class: Gene

Annotated gene within a genome.

CDM changes from CORAL:
- FK reference: genome → genome_ref
- Gene ID convention: GeneName{genome_name}_{contig}_{start}_{stop}

URI: [kbase_cdm:Gene](https://w3id.org/enigma/kbase-cdm/Gene)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Gene&#124;sdt_gene_id:string;sdt_gene_name:EntityName;genome_ref:EntityName%20%3F;contig_number:integer%20%3F;strand:string%20%3F;start:integer%20%3F;stop:integer%20%3F;function:string%20%3F]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Gene&#124;sdt_gene_id:string;sdt_gene_name:EntityName;genome_ref:EntityName%20%3F;contig_number:integer%20%3F;strand:string%20%3F;start:integer%20%3F;stop:integer%20%3F;function:string%20%3F]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_gene_id](sdt_gene_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Gene
     * Range: [String](types/String.md)
 * [sdt_gene_name](sdt_gene_name.md)  <sub>1..1</sub>
     * Description: Name of gene
     * Range: [EntityName](types/EntityName.md)
 * [genome_ref](genome_ref.md)  <sub>0..1</sub>
     * Description: Reference to genome name (FK to Genome.sdt_genome_name)
     * Range: [EntityName](types/EntityName.md)
 * [contig_number](contig_number.md)  <sub>0..1</sub>
     * Description: Contig number where gene is located
     * Range: [Integer](types/Integer.md)
 * [strand](strand.md)  <sub>0..1</sub>
     * Description: DNA strand (+ or -)
     * Range: [String](types/String.md)
 * [start](start.md)  <sub>0..1</sub>
     * Description: Start position on contig
     * Range: [Integer](types/Integer.md)
 * [stop](stop.md)  <sub>0..1</sub>
     * Description: Stop position on contig
     * Range: [Integer](types/Integer.md)
 * [function](function.md)  <sub>0..1</sub>
     * Description: Predicted gene function
     * Range: [String](types/String.md)
