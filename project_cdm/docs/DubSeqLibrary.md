
# Class: DubSeqLibrary

Dual Barcoded Sequencing (DubSeq) library.

CDM changes from CORAL:
- FK reference: genome → genome_ref

URI: [kbase_cdm:DubSeqLibrary](https://w3id.org/enigma/kbase-cdm/DubSeqLibrary)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[DubSeqLibrary&#124;sdt_dubseq_library_id:string;sdt_dubseq_library_name:EntityName;genome_ref:EntityName%20%3F;n_fragments:Count%20%3F]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[DubSeqLibrary&#124;sdt_dubseq_library_id:string;sdt_dubseq_library_name:EntityName;genome_ref:EntityName%20%3F;n_fragments:Count%20%3F]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_dubseq_library_id](sdt_dubseq_library_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for DubSeqLibrary
     * Range: [String](types/String.md)
 * [sdt_dubseq_library_name](sdt_dubseq_library_name.md)  <sub>1..1</sub>
     * Description: Name of DubSeq library
     * Range: [EntityName](types/EntityName.md)
 * [genome_ref](genome_ref.md)  <sub>0..1</sub>
     * Description: Reference to genome name (FK to Genome.sdt_genome_name)
     * Range: [EntityName](types/EntityName.md)
 * [n_fragments](n_fragments.md)  <sub>0..1</sub>
     * Description: Number of fragments
     * Range: [Count](types/Count.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | kbase_cdm:DubSeqLibrary |
