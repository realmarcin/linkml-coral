
# Class: Sample

Environmental sample collected from a location.

CDM changes from CORAL:
- 2 ontology term fields split: material, env_package
- FK reference: location → location_ref

URI: [kbase_cdm:Sample](https://w3id.org/enigma/kbase-cdm/Sample)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Sample&#124;sdt_sample_id:string;sdt_sample_name:EntityName;location_ref:EntityName%20%3F;depth:Depth%20%3F;elevation:Elevation%20%3F;date:Date%20%3F;time:Time%20%3F;timezone:string%20%3F;material_sys_oterm_id:OntologyTermID%20%3F;material_sys_oterm_name:string%20%3F;env_package_sys_oterm_id:OntologyTermID%20%3F;env_package_sys_oterm_name:string%20%3F;description:string%20%3F]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Sample&#124;sdt_sample_id:string;sdt_sample_name:EntityName;location_ref:EntityName%20%3F;depth:Depth%20%3F;elevation:Elevation%20%3F;date:Date%20%3F;time:Time%20%3F;timezone:string%20%3F;material_sys_oterm_id:OntologyTermID%20%3F;material_sys_oterm_name:string%20%3F;env_package_sys_oterm_id:OntologyTermID%20%3F;env_package_sys_oterm_name:string%20%3F;description:string%20%3F]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_sample_id](sdt_sample_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Sample
     * Range: [String](types/String.md)
 * [sdt_sample_name](sdt_sample_name.md)  <sub>1..1</sub>
     * Description: Name of sample
     * Range: [EntityName](types/EntityName.md)
 * [location_ref](location_ref.md)  <sub>0..1</sub>
     * Description: Reference to location name (FK to Location.sdt_location_name)
     * Range: [EntityName](types/EntityName.md)
 * [depth](depth.md)  <sub>0..1</sub>
     * Description: Depth in meters
     * Range: [Depth](types/Depth.md)
 * [elevation](elevation.md)  <sub>0..1</sub>
     * Description: Elevation in meters
     * Range: [Elevation](types/Elevation.md)
 * [date](date.md)  <sub>0..1</sub>
     * Description: Collection date
     * Range: [Date](types/Date.md)
 * [time](time.md)  <sub>0..1</sub>
     * Description: Collection time
     * Range: [Time](types/Time.md)
 * [timezone](timezone.md)  <sub>0..1</sub>
     * Description: Timezone
     * Range: [String](types/String.md)
 * [material_sys_oterm_id](material_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Material type ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [material_sys_oterm_name](material_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Material type ontology term name
     * Range: [String](types/String.md)
 * [env_package_sys_oterm_id](env_package_sys_oterm_id.md)  <sub>0..1</sub>
     * Description: Environment package ontology term ID
     * Range: [OntologyTermID](types/OntologyTermID.md)
 * [env_package_sys_oterm_name](env_package_sys_oterm_name.md)  <sub>0..1</sub>
     * Description: Environment package ontology term name
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: Free text description
     * Range: [String](types/String.md)
