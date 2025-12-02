
# Class: Image

Microscopy or other image data.

CDM changes from CORAL:
- Added 'link' field for image files

URI: [kbase_cdm:Image](https://w3id.org/enigma/kbase-cdm/Image)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Image&#124;sdt_image_id:string;sdt_image_name:EntityName;mime_type:string%20%3F;size:Size%20%3F;dimensions:string%20%3F;link:Link%20%3F]uses%20-.->[CDMEntity],[CDMEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Image&#124;sdt_image_id:string;sdt_image_name:EntityName;mime_type:string%20%3F;size:Size%20%3F;dimensions:string%20%3F;link:Link%20%3F]uses%20-.->[CDMEntity],[CDMEntity])

## Uses Mixin

 *  mixin: [CDMEntity](CDMEntity.md) - Base mixin for all CDM static data tables (sdt_*).

## Attributes


### Own

 * [sdt_image_id](sdt_image_id.md)  <sub>1..1</sub>
     * Description: Unique identifier for Image
     * Range: [String](types/String.md)
 * [sdt_image_name](sdt_image_name.md)  <sub>1..1</sub>
     * Description: Name of image
     * Range: [EntityName](types/EntityName.md)
 * [mime_type](mime_type.md)  <sub>0..1</sub>
     * Description: MIME type of image
     * Range: [String](types/String.md)
 * [size](size.md)  <sub>0..1</sub>
     * Description: File size in bytes
     * Range: [Size](types/Size.md)
 * [dimensions](dimensions.md)  <sub>0..1</sub>
     * Description: Image dimensions (e.g., "1024x768")
     * Range: [String](types/String.md)
 * [link](link.md)  <sub>0..1</sub>
     * Description: External reference URL or file path
     * Range: [Link](types/Link.md)
