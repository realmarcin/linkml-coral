
# Class: Condition

Growth or experimental condition.

URI: [kbase_cdm:Condition](https://w3id.org/enigma/kbase-cdm/Condition)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Condition&#124;sdt_condition_id:string;sdt_condition_name:EntityName]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Condition&#124;sdt_condition_id:string;sdt_condition_name:EntityName]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_condition_id](sdt_condition_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Condition
     * Range: [String](types/String.md)
 * [sdt_condition_name](sdt_condition_name.md)  <sub>1..1</sub>
     * Description: Name of condition
     * Range: [EntityName](types/EntityName.md)
