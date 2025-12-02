
# Class: Bin

Genome bin extracted from metagenomic assembly.

CDM changes from CORAL:
- FK reference: assembly → assembly_ref
- contigs field contains comma-separated contig names

URI: [kbase_cdm:Bin](https://w3id.org/enigma/kbase-cdm/Bin)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[CDMEntity],[Bin&#124;sdt_bin_id:string;sdt_bin_name:EntityName;assembly_ref:EntityName%20%3F;contigs:string%20%3F]uses%20-.->[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[CDMEntity],[Bin&#124;sdt_bin_id:string;sdt_bin_name:EntityName;assembly_ref:EntityName%20%3F;contigs:string%20%3F]uses%20-.->[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_bin_id](sdt_bin_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Bin
     * Range: [String](types/String.md)
 * [sdt_bin_name](sdt_bin_name.md)  <sub>1..1</sub>
     * Description: Name of bin
     * Range: [EntityName](types/EntityName.md)
 * [assembly_ref](assembly_ref.md)  <sub>0..1</sub>
     * Description: Reference to assembly name (FK to Assembly.sdt_assembly_name)
     * Range: [EntityName](types/EntityName.md)
 * [contigs](contigs.md)  <sub>0..1</sub>
     * Description: Comma-separated list of contig names
     * Range: [String](types/String.md)
