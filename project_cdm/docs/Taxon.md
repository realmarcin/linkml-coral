
# Class: Taxon

Taxonomic classification.

URI: [kbase_cdm:Taxon](https://w3id.org/enigma/kbase-cdm/Taxon)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Taxon&#124;sdt_taxon_id:string;sdt_taxon_name:EntityName;ncbi_taxid:integer%20%3F]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Taxon&#124;sdt_taxon_id:string;sdt_taxon_name:EntityName;ncbi_taxid:integer%20%3F]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_taxon_id](sdt_taxon_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Taxon
     * Range: [String](types/String.md)
 * [sdt_taxon_name](sdt_taxon_name.md)  <sub>1..1</sub>
     * Description: Taxonomic name
     * Range: [EntityName](types/EntityName.md)
 * [ncbi_taxid](ncbi_taxid.md)  <sub>0..1</sub>
     * Description: NCBI Taxonomy ID
     * Range: [Integer](types/Integer.md)
