
# Class: SystemOntologyTerm

Centralized ontology term catalog.

Stores all ontology terms used across the CDM with:
- CURIE identifiers (ME:, ENVO:, UO:, etc.)
- Human-readable names
- Hierarchical relationships (parent terms)
- Definitions, synonyms, and external links

Benefits:
- Single source of truth for ontology terms
- Supports ontology evolution without data migration
- Enables semantic queries and reasoning
- Foreign key target for all *_sys_oterm_id columns

URI: [kbase_cdm:SystemOntologyTerm](https://w3id.org/enigma/kbase-cdm/SystemOntologyTerm)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemOntologyTerm&#124;sys_oterm_id:OntologyTermID;sys_oterm_name:string%20%3F;sys_oterm_ontology:string%20%3F;parent_sys_oterm_id:OntologyTermID%20%3F;sys_oterm_definition:string%20%3F;sys_oterm_synonyms:string%20%3F;sys_oterm_links:string%20%3F;sys_oterm_properties:string%20%3F]uses%20-.->[SystemEntity],[SystemEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[SystemOntologyTerm&#124;sys_oterm_id:OntologyTermID;sys_oterm_name:string%20%3F;sys_oterm_ontology:string%20%3F;parent_sys_oterm_id:OntologyTermID%20%3F;sys_oterm_definition:string%20%3F;sys_oterm_synonyms:string%20%3F;sys_oterm_links:string%20%3F;sys_oterm_properties:string%20%3F]uses%20-.->[SystemEntity],[SystemEntity])

## Uses Mixin

 *  mixin: [SystemEntity](SystemEntity.md) - Base mixin for CDM system tables (sys_*).

## Referenced by Class


## Attributes


### Own

 * [SystemOntologyTerm➞sys_oterm_id](SystemOntologyTerm_sys_oterm_id.md)  <sub>1..1</sub>
     * Description: Ontology term identifier (CURIE format)
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [sys_oterm_name](sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Human-readable ontology term name
     * Range: [String](types/String.md)
 * [sys_oterm_ontology](sys_oterm_ontology.md)  <sub>0..1</sub>
     * Description: Source ontology name
     * Range: [String](types/String.md)
 * [parent_sys_oterm_id](parent_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Parent term in ontology hierarchy (FK to sys_oterm)
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [sys_oterm_definition](sys_oterm_definition.md)  <sub>0..1</sub>
     * Description: Formal term definition
     * Range: [String](types/String.md)
 * [sys_oterm_synonyms](sys_oterm_synonyms.md)  <sub>0..1</sub>
     * Description: Alternative term names (pipe-separated)
     * Range: [String](types/String.md)
 * [sys_oterm_links](sys_oterm_links.md)  <sub>0..1</sub>
     * Description: External links (URLs, pipe-separated)
     * Range: [String](types/String.md)
 * [sys_oterm_properties](sys_oterm_properties.md)  <sub>0..1</sub>
     * Description: Additional term properties (JSON or key=value pairs)
     * Range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | kbase_cdm:SystemOntologyTerm |
