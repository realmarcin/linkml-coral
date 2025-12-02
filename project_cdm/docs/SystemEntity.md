
# Class: SystemEntity

Base mixin for CDM system tables (sys_*).

System tables provide metadata, type definitions, provenance tracking,
and ontology catalogs. They support the static and dynamic data tables
but are not directly linked to experimental entities.

System tables: sys_typedef, sys_ddt_typedef, sys_oterm, sys_process,
sys_process_input, sys_process_output

URI: [kbase_cdm:SystemEntity](https://w3id.org/enigma/kbase-cdm/SystemEntity)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemTypedef]uses%20-.->[SystemEntity],[SystemProcessOutput]uses%20-.->[SystemEntity],[SystemProcessInput]uses%20-.->[SystemEntity],[SystemProcess]uses%20-.->[SystemEntity],[SystemOntologyTerm]uses%20-.->[SystemEntity],[SystemDDTTypedef]uses%20-.->[SystemEntity],[DynamicDataArray]uses%20-.->[SystemEntity],[SystemTypedef],[SystemProcessOutput],[SystemProcessInput],[SystemProcess],[SystemOntologyTerm],[SystemDDTTypedef],[DynamicDataArray])](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemTypedef]uses%20-.->[SystemEntity],[SystemProcessOutput]uses%20-.->[SystemEntity],[SystemProcessInput]uses%20-.->[SystemEntity],[SystemProcess]uses%20-.->[SystemEntity],[SystemOntologyTerm]uses%20-.->[SystemEntity],[SystemDDTTypedef]uses%20-.->[SystemEntity],[DynamicDataArray]uses%20-.->[SystemEntity],[SystemTypedef],[SystemProcessOutput],[SystemProcessInput],[SystemProcess],[SystemOntologyTerm],[SystemDDTTypedef],[DynamicDataArray])

## Mixin for

 * [DynamicDataArray](DynamicDataArray.md) (mixin)  - Brick index table (ddt_ndarray).
 * [SystemDDTTypedef](SystemDDTTypedef.md) (mixin)  - Type definitions for dynamic data tables (bricks).
 * [SystemOntologyTerm](SystemOntologyTerm.md) (mixin)  - Centralized ontology term catalog.
 * [SystemProcess](SystemProcess.md) (mixin)  - Provenance tracking for all data transformations.
 * [SystemProcessInput](SystemProcessInput.md) (mixin)  - Normalized process input relationships.
 * [SystemProcessOutput](SystemProcessOutput.md) (mixin)  - Normalized process output relationships.
 * [SystemTypedef](SystemTypedef.md) (mixin)  - Type definitions for static entity tables (equivalent to typedef.json).

## Referenced by Class


## Attributes


## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | System tables have their own identifier conventions |
|  | | No sdt_ prefix (use sys_ instead) |
|  | | May have composite keys or generated IDs |
