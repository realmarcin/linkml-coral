
# Class: TnSeqLibrary

Transposon Sequencing (TnSeq) library.

CDM changes from CORAL:
- FK reference: genome → genome_ref

URI: [kbase_cdm:TnSeqLibrary](https://w3id.org/enigma/kbase-cdm/TnSeqLibrary)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TnSeqLibrary&#124;sdt_tnseq_library_id:string;sdt_tnseq_library_name:EntityName;genome_ref:EntityName%20%3F;primers_model:string%20%3F;n_mapped_reads:Count%20%3F;n_good_reads:Count%20%3F;n_genes_hit:Count%20%3F]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[TnSeqLibrary&#124;sdt_tnseq_library_id:string;sdt_tnseq_library_name:EntityName;genome_ref:EntityName%20%3F;primers_model:string%20%3F;n_mapped_reads:Count%20%3F;n_good_reads:Count%20%3F;n_genes_hit:Count%20%3F]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_tnseq_library_id](sdt_tnseq_library_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for TnSeqLibrary
     * Range: [String](types/String.md)
 * [sdt_tnseq_library_name](sdt_tnseq_library_name.md)  <sub>1..1</sub>
     * Description: Name of TnSeq library
     * Range: [EntityName](types/EntityName.md)
 * [genome_ref](genome_ref.md)  <sub>0..1</sub>
     * Description: Reference to genome name (FK to Genome.sdt_genome_name)
     * Range: [EntityName](types/EntityName.md)
 * [primers_model](primers_model.md)  <sub>0..1</sub>
     * Description: Primers model used
     * Range: [String](types/String.md)
 * [n_mapped_reads](n_mapped_reads.md)  <sub>0..1</sub>
     * Description: Number of mapped reads
     * Range: [Count](types/Count.md)
 * [n_good_reads](n_good_reads.md)  <sub>0..1</sub>
     * Description: Number of good quality reads
     * Range: [Count](types/Count.md)
 * [n_genes_hit](n_genes_hit.md)  <sub>0..1</sub>
     * Description: Number of genes with transposon insertions
     * Range: [Count](types/Count.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | kbase_cdm:TnSeqLibrary |
