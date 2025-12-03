
# Class: CDMEntity

Base mixin for all CDM static data tables (sdt_*).

Enforces CDM naming conventions:
- Primary key: sdt_{entity}_id with pattern EntityName\d{7}
- Name field: sdt_{entity}_name (unique, used for FK references)
- All columns use snake_case with entity prefix

Example:
- Location: sdt_location_id, sdt_location_name
- Sample: sdt_sample_id, sdt_sample_name

Note: Each entity class must define its own id and name slots
with entity-specific names (e.g., sdt_location_id, sdt_location_name).

URI: [kbase_cdm:CDMEntity](https://w3id.org/enigma/kbase-cdm/CDMEntity)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TnSeqLibrary]uses%20-.->[CDMEntity],[Taxon]uses%20-.->[CDMEntity],[Strain]uses%20-.->[CDMEntity],[Sample]uses%20-.->[CDMEntity],[Reads]uses%20-.->[CDMEntity],[Protocol]uses%20-.->[CDMEntity],[Location]uses%20-.->[CDMEntity],[Image]uses%20-.->[CDMEntity],[Genome]uses%20-.->[CDMEntity],[Gene]uses%20-.->[CDMEntity],[ENIGMA]uses%20-.->[CDMEntity],[DubSeqLibrary]uses%20-.->[CDMEntity],[Condition]uses%20-.->[CDMEntity],[Community]uses%20-.->[CDMEntity],[Bin]uses%20-.->[CDMEntity],[Assembly]uses%20-.->[CDMEntity],[ASV]uses%20-.->[CDMEntity],[TnSeqLibrary],[Taxon],[Strain],[Sample],[Reads],[Protocol],[Location],[Image],[Genome],[Gene],[ENIGMA],[DubSeqLibrary],[Condition],[Community],[Bin],[Assembly],[ASV])](https://yuml.me/diagram/nofunky;dir:TB/class/[TnSeqLibrary]uses%20-.->[CDMEntity],[Taxon]uses%20-.->[CDMEntity],[Strain]uses%20-.->[CDMEntity],[Sample]uses%20-.->[CDMEntity],[Reads]uses%20-.->[CDMEntity],[Protocol]uses%20-.->[CDMEntity],[Location]uses%20-.->[CDMEntity],[Image]uses%20-.->[CDMEntity],[Genome]uses%20-.->[CDMEntity],[Gene]uses%20-.->[CDMEntity],[ENIGMA]uses%20-.->[CDMEntity],[DubSeqLibrary]uses%20-.->[CDMEntity],[Condition]uses%20-.->[CDMEntity],[Community]uses%20-.->[CDMEntity],[Bin]uses%20-.->[CDMEntity],[Assembly]uses%20-.->[CDMEntity],[ASV]uses%20-.->[CDMEntity],[TnSeqLibrary],[Taxon],[Strain],[Sample],[Reads],[Protocol],[Location],[Image],[Genome],[Gene],[ENIGMA],[DubSeqLibrary],[Condition],[Community],[Bin],[Assembly],[ASV])

## Mixin for

 * [ASV](ASV.md) (mixin)  - Amplicon Sequence Variant (formerly OTU).
 * [Assembly](Assembly.md) (mixin)  - Genome assembly from sequencing reads.
 * [Bin](Bin.md) (mixin)  - Genome bin extracted from metagenomic assembly.
 * [Community](Community.md) (mixin)  - Microbial community (isolate, enrichment, assemblage, or environmental).
 * [Condition](Condition.md) (mixin)  - Growth or experimental condition.
 * [DubSeqLibrary](DubSeqLibrary.md) (mixin)  - Dual Barcoded Sequencing (DubSeq) library.
 * [ENIGMA](ENIGMA.md) (mixin)  - Root entity (database singleton).
 * [Gene](Gene.md) (mixin)  - Annotated gene within a genome.
 * [Genome](Genome.md) (mixin)  - Assembled and annotated genome.
 * [Image](Image.md) (mixin)  - Microscopy or other image data.
 * [Location](Location.md) (mixin)  - Sampling location with geographic coordinates and environmental context.
 * [Protocol](Protocol.md) (mixin)  - Experimental protocol.
 * [Reads](Reads.md) (mixin)  - Sequencing reads dataset.
 * [Sample](Sample.md) (mixin)  - Environmental sample collected from a location.
 * [Strain](Strain.md) (mixin)  - Microbial strain (isolated or derived).
 * [Taxon](Taxon.md) (mixin)  - Taxonomic classification.
 * [TnSeqLibrary](TnSeqLibrary.md) (mixin)  - Transposon Sequencing (TnSeq) library.

## Referenced by Class


## Attributes


## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | This mixin does not define slots - each entity defines its own |
|  | | Used for grouping and documentation purposes |
