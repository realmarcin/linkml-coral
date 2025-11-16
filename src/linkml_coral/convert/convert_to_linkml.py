#!/usr/bin/env python3
"""
Convert ENIGMA typedef.json to LinkML schema format.

This script converts the ENIGMA data type definitions to a LinkML schema
that can be used for data validation, documentation, and code generation.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional


class TypedefToLinkMLConverter:
    """Converts ENIGMA typedef.json to LinkML schema."""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.schema = self._initialize_schema()
        
    def _initialize_schema(self) -> Dict[str, Any]:
        """Initialize the base LinkML schema structure."""
        return {
            "id": "https://w3id.org/enigma/enigma-cdm",
            "name": "enigma-cdm", 
            "title": "ENIGMA Common Data Model",
            "description": "LinkML schema for ENIGMA (Environmental Molecular Sciences Laboratory Integrated Genomics Initiative) Common Data Model",
            "version": "1.0.0",
            "license": "MIT",
            "prefixes": {
                "linkml": "https://w3id.org/linkml/",
                "enigma": "https://w3id.org/enigma/",
                "DA": "http://purl.obolibrary.org/obo/DA_",
                "ME": "http://purl.obolibrary.org/obo/ME_",
                "ENVO": "http://purl.obolibrary.org/obo/ENVO_",
                "UO": "http://purl.obolibrary.org/obo/UO_",
                "PROCESS": "http://purl.obolibrary.org/obo/PROCESS_",
                "ENIGMA_TERM": "http://purl.obolibrary.org/obo/ENIGMA_",
                "CONTINENT": "http://purl.obolibrary.org/obo/CONTINENT_",
                "COUNTRY": "http://purl.obolibrary.org/obo/COUNTRY_",
                "MIxS": "http://purl.obolibrary.org/obo/MIxS_"
            },
            "default_prefix": "enigma",
            "imports": ["linkml:types"],
            "classes": {},
            "slots": {},
            "types": {},
            "enums": {}
        }
    
    def _scalar_type_to_linkml_type(self, scalar_type: str) -> str:
        """Convert scalar type to LinkML type."""
        type_mapping = {
            "text": "string",
            "int": "integer", 
            "float": "float",
            "term": "string",  # Terms will be validated with enums
            "[text]": "string",  # Array types handled with multivalued
            "[ref]": "string"   # References handled with ranges
        }
        return type_mapping.get(scalar_type, "string")
    
    def _create_slot_from_field(self, field: Dict[str, Any], class_name: str) -> Dict[str, Any]:
        """Create a LinkML slot definition from a field."""
        slot = {
            "description": f"{field['name']} field for {class_name}"
        }
        
        # Add type information
        scalar_type = field.get("scalar_type", "text")
        slot["range"] = self._scalar_type_to_linkml_type(scalar_type)
        
        # Handle required fields
        if field.get("required", False):
            slot["required"] = True
            
        # Handle primary keys
        if field.get("PK", False):
            slot["identifier"] = True
            
        # Handle unique keys
        if field.get("UPK", False):
            slot["key"] = True
            
        # Handle foreign keys
        if "FK" in field:
            fk_ref = field["FK"]
            if fk_ref.startswith("[") and fk_ref.endswith("]"):
                # Array of references
                slot["multivalued"] = True
                slot["range"] = fk_ref[1:-1].split(".")[0]  # Extract class name
            else:
                slot["range"] = fk_ref.split(".")[0]  # Extract class name
                
        # Handle array types
        if scalar_type.startswith("[") and scalar_type.endswith("]"):
            slot["multivalued"] = True
            
        # Add constraints as patterns for text fields
        if "constraint" in field and scalar_type == "text":
            constraint = field["constraint"]
            if constraint.startswith("\\") or "(" in constraint:
                slot["pattern"] = constraint
                
        # Add units
        if "units_term" in field:
            slot["annotations"] = {
                "units": {
                    "tag": "units",
                    "value": field["units_term"]
                }
            }
            
        # Add comments
        if "comment" in field:
            slot["comments"] = [field["comment"]]
            
        # Add type term annotation
        if "type_term" in field:
            if "annotations" not in slot:
                slot["annotations"] = {}
            slot["annotations"]["type_term"] = {
                "tag": "type_term",
                "value": field["type_term"]
            }
            
        return slot
    
    def _create_class_from_type(self, type_def: Dict[str, Any]) -> Dict[str, Any]:
        """Create a LinkML class definition from a type definition."""
        class_def = {
            "description": f"{type_def['name']} entity in the ENIGMA data model"
        }
        
        # Add term annotation if present
        if "term" in type_def:
            class_def["annotations"] = {
                "term": {
                    "tag": "term",
                    "value": type_def["term"]
                }
            }
            
        # Add provenance flag
        if type_def.get("used_for_provenance", False):
            if "annotations" not in class_def:
                class_def["annotations"] = {}
            class_def["annotations"]["used_for_provenance"] = {
                "tag": "used_for_provenance", 
                "value": True
            }
            
        # Process fields as slots
        slots = []
        for field in type_def.get("fields", []):
            slot_name = f"{type_def['name'].lower()}_{field['name']}"
            self.schema["slots"][slot_name] = self._create_slot_from_field(field, type_def['name'])
            slots.append(slot_name)
            
        if slots:
            class_def["slots"] = slots
            
        # Add process type information as annotations
        if "process_types" in type_def:
            if "annotations" not in class_def:
                class_def["annotations"] = {}
            class_def["annotations"]["process_types"] = {
                "tag": "process_types",
                "value": type_def["process_types"]
            }
            
        if "process_inputs" in type_def:
            if "annotations" not in class_def:
                class_def["annotations"] = {}
            class_def["annotations"]["process_inputs"] = {
                "tag": "process_inputs", 
                "value": type_def["process_inputs"]
            }
            
        return class_def
    
    def convert(self) -> None:
        """Convert the typedef.json file to LinkML schema."""
        # Load input JSON
        with open(self.input_file, 'r') as f:
            typedef_data = json.load(f)
            
        # Process system types
        for system_type in typedef_data.get("system_types", []):
            class_name = system_type["name"]
            self.schema["classes"][class_name] = self._create_class_from_type(system_type)
            
        # Process static types
        for static_type in typedef_data.get("static_types", []):
            class_name = static_type["name"]
            if class_name != "ENIGMA":  # Skip empty ENIGMA type
                self.schema["classes"][class_name] = self._create_class_from_type(static_type)
                
        # Write output YAML
        with open(self.output_file, 'w') as f:
            yaml.dump(self.schema, f, default_flow_style=False, sort_keys=False, width=120)
            
        print(f"Successfully converted {self.input_file} to {self.output_file}")
        print(f"Generated {len(self.schema['classes'])} classes and {len(self.schema['slots'])} slots")


def main():
    """Main conversion function."""
    converter = TypedefToLinkMLConverter(
        input_file="CORAL/back_end/python/var/typedef.json",
        output_file="data/coral_enigma_schema.yaml"
    )
    converter.convert()


if __name__ == "__main__":
    main()