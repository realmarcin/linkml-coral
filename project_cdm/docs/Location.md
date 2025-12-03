
# Class: Location

Sampling location with geographic coordinates and environmental context.

CDM changes from CORAL:
- 4 ontology term fields split into ID+name pairs:
  continent, country, biome, feature

URI: [kbase_cdm:Location](https://w3id.org/enigma/kbase-cdm/Location)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Location&#124;sdt_location_id:string;sdt_location_name:EntityName;latitude:Latitude%20%3F;longitude:Longitude%20%3F;continent_sys_oterm_id:OntologyTermID%20%3F;continent_sys_oterm_name:string%20%3F;country_sys_oterm_id:OntologyTermID%20%3F;country_sys_oterm_name:string%20%3F;region:string%20%3F;biome_sys_oterm_id:OntologyTermID%20%3F;biome_sys_oterm_name:string%20%3F;feature_sys_oterm_id:OntologyTermID%20%3F;feature_sys_oterm_name:string%20%3F]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Location&#124;sdt_location_id:string;sdt_location_name:EntityName;latitude:Latitude%20%3F;longitude:Longitude%20%3F;continent_sys_oterm_id:OntologyTermID%20%3F;continent_sys_oterm_name:string%20%3F;country_sys_oterm_id:OntologyTermID%20%3F;country_sys_oterm_name:string%20%3F;region:string%20%3F;biome_sys_oterm_id:OntologyTermID%20%3F;biome_sys_oterm_name:string%20%3F;feature_sys_oterm_id:OntologyTermID%20%3F;feature_sys_oterm_name:string%20%3F]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_location_id](sdt_location_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Location
     * Range: [String](types/String.md)
 * [sdt_location_name](sdt_location_name.md)  <sub>1..1</sub>
     * Description: Name of location
     * Range: [EntityName](types/EntityName.md)
 * [latitude](latitude.md)  <sub>0..1</sub>
     * Description: Latitude in decimal degrees
     * Range: [Latitude](types/Latitude.md)
 * [longitude](longitude.md)  <sub>0..1</sub>
     * Description: Longitude in decimal degrees
     * Range: [Longitude](types/Longitude.md)
 * [continent_sys_oterm_id](continent_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Continent ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [continent_sys_oterm_name](continent_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Continent ontology term name
     * Range: [String](types/String.md)
 * [country_sys_oterm_id](country_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Country ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [country_sys_oterm_name](country_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Country ontology term name
     * Range: [String](types/String.md)
 * [region](region.md)  <sub>0..1</sub>
     * Description: Geographic region
     * Range: [String](types/String.md)
 * [biome_sys_oterm_id](biome_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Biome ontology term ID (ENVO)
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [biome_sys_oterm_name](biome_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Biome ontology term name
     * Range: [String](types/String.md)
 * [feature_sys_oterm_id](feature_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Environmental feature ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [feature_sys_oterm_name](feature_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Environmental feature ontology term name
     * Range: [String](types/String.md)
