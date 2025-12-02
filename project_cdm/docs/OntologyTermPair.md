
# Class: OntologyTermPair

Mixin for ontology-constrained fields in KBase CDM.

The CDM splits each ontology-controlled field into two columns:
- {field}_sys_oterm_id: CURIE identifier (FK to sys_oterm)
- {field}_sys_oterm_name: Human-readable term name

This pattern enables:
- Ontology validation via FK constraint
- Human-readable labels without joins
- Ontology evolution without data migration

Examples:
- material → material_sys_oterm_id + material_sys_oterm_name
- biome → biome_sys_oterm_id + biome_sys_oterm_name
- read_type → read_type_sys_oterm_id + read_type_sys_oterm_name

URI: [kbase_cdm:OntologyTermPair](https://w3id.org/enigma/kbase-cdm/OntologyTermPair)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OntologyTermPair])](https://yuml.me/diagram/nofunky;dir:TB/class/[OntologyTermPair])

## Attributes


## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | Use this mixin when defining ontology-constrained slot pairs |
|  | | Ensures consistent naming and typing across all entities |
