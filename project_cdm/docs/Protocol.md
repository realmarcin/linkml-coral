
# Class: Protocol

Experimental protocol.

CDM changes from CORAL:
- Added 'link' field for protocol documents

URI: [kbase_cdm:Protocol](https://w3id.org/enigma/kbase-cdm/Protocol)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Protocol&#124;sdt_protocol_id:string;sdt_protocol_name:EntityName;description:string%20%3F;link:Link%20%3F]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Protocol&#124;sdt_protocol_id:string;sdt_protocol_name:EntityName;description:string%20%3F;link:Link%20%3F]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_protocol_id](sdt_protocol_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Protocol
     * Range: [String](types/String.md)
 * [sdt_protocol_name](sdt_protocol_name.md)  <sub>1..1</sub>
     * Description: Name of protocol
     * Range: [EntityName](types/EntityName.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: Free text description
     * Range: [String](types/String.md)
 * [link](link.md)  <sub>0..1</sub>
     * Description: External reference URL or file path
     * Range: [Link](types/Link.md)
