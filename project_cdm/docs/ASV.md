
# Class: ASV

Amplicon Sequence Variant (formerly OTU).

CDM changes from CORAL:
- Entity renamed from OTU to ASV (Amplicon Sequence Variant)
- Table name: sdt_asv

URI: [kbase_cdm:ASV](https://w3id.org/enigma/kbase-cdm/ASV)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[CDMEntity],[ASV&#124;sdt_asv_id:string;sdt_asv_name:EntityName;sequence:string%20%3F]uses%20-.->[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[CDMEntity],[ASV&#124;sdt_asv_id:string;sdt_asv_name:EntityName;sequence:string%20%3F]uses%20-.->[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_asv_id](sdt_asv_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for ASV
     * Range: [String](types/String.md)
 * [sdt_asv_name](sdt_asv_name.md)  <sub>1..1</sub>
     * Description: Name of ASV
     * Range: [EntityName](types/EntityName.md)
 * [sequence](sequence.md)  <sub>0..1</sub>
     * Description: DNA sequence
     * Range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | kbase_cdm:ASV |
