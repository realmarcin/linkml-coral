
# Slot: genome_ref

Reference to genome name (FK to Genome.sdt_genome_name)

URI: [kbase_cdm:genome_ref](https://w3id.org/enigma/kbase-cdm/genome_ref)


## Domain and Range

None &#8594;  <sub>0..1</sub> [EntityName](types/EntityName.md)

## Parents


## Children


## Used by

 * [DubSeqLibrary](DubSeqLibrary.md)
 * [Gene](Gene.md)
 * [Strain](Strain.md)
 * [TnSeqLibrary](TnSeqLibrary.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | {'CDM convention': 'FK references use entity name, not ID'} |
|  | | References Genome.sdt_genome_name |
|  | | {'Used by': 'Gene, Strain, DubSeqLibrary, TnSeqLibrary'} |
