#!/usr/bin/env python3
"""
Validate TSV files against the CORAL LinkML schema.

This script reads TSV files and validates them against the ENIGMA Common Data Model
schema using linkml-validate. It converts TSV data to the expected format and
validates each entity type.
"""

import argparse
import csv
import json
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Any

import yaml
from linkml_runtime.utils.schemaview import SchemaView


def load_schema(schema_path: Path) -> SchemaView:
    """Load the LinkML schema from file."""
    return SchemaView(str(schema_path))


def read_tsv_file(tsv_path: Path) -> List[Dict[str, Any]]:
    """Read TSV file and return list of dictionaries."""
    data = []
    with open(tsv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            # Convert empty strings to None
            cleaned_row = {k: (v if v.strip() else None) for k, v in row.items()}
            data.append(cleaned_row)
    return data


def map_tsv_to_schema_fields(data: List[Dict[str, Any]], class_name: str, schema_view: SchemaView) -> List[Dict[str, Any]]:
    """Map TSV column names to schema field names."""
    if not data:
        return data
    
    # Get class definition from schema
    class_def = schema_view.get_class(class_name)
    if not class_def:
        raise ValueError(f"Class {class_name} not found in schema")
    
    # Get slot definitions for the class
    slots = schema_view.class_slots(class_name)
    slot_mapping = {}
    
    # Create mapping from TSV columns to schema slots
    for slot_name in slots:
        slot_def = schema_view.get_slot(slot_name)
        if slot_def:
            # Try direct mapping first
            slot_mapping[slot_name] = slot_name
            
            # Try mapping without class prefix
            if slot_name.startswith(class_name.lower() + '_'):
                tsv_field = slot_name.replace(class_name.lower() + '_', '', 1)
                slot_mapping[tsv_field] = slot_name
    
    # Special mappings for ENIGMA data format
    special_mappings = {
        'id': f'{class_name.lower()}_id',
        'name': f'{class_name.lower()}_name', 
        'location': f'{class_name.lower()}_location',
        'depth': f'{class_name.lower()}_depth',
        'elevation': f'{class_name.lower()}_elevation',
        'date': f'{class_name.lower()}_date',
        'time': f'{class_name.lower()}_time',
        'timezone': f'{class_name.lower()}_timezone',
        'description': f'{class_name.lower()}_description',
        # Map material term to material field
        'material_term_id': f'{class_name.lower()}_material',
        # Map env_package term to env_package field  
        'env_package_term_id': f'{class_name.lower()}_env_package',
        # Process-specific mappings
        'process_term_id': 'process_process',
        'person_term_id': 'process_person',
        'campaign_term_id': 'process_campaign',
        'input_objects': 'process_input_objects',
        'output_objects': 'process_output_objects',
        'protocol': 'process_protocol',
        # Location-specific mappings
        'latitude': 'location_latitude',
        'longitude': 'location_longitude',
        'continent_term_id': 'location_continent',
        'country_term_id': 'location_country',
        'region': 'location_region',
        'biome_term_id': 'location_biome',
        'feature_term_id': 'location_feature',
        # OTU/ASV mappings
        'ASV_id': 'otu_id',
        'OTU_name': 'otu_name',
        # Reads mappings
        'read_count': 'reads_read_count',
        'read_type': 'reads_read_type',
        'read_type_term_id': 'reads_read_type',
        'sequencing_technology': 'reads_sequencing_technology',
        'sequencing_technology_term_id': 'reads_sequencing_technology',
        # Community mappings
        'community_type': 'community_community_type',
        'community_type_term_id': 'community_community_type',
        'sample': 'community_sample',
        'parent_community': 'community_parent_community',
        'condition': 'community_condition',
        'defined_strains': 'community_defined_strains',
    }
    
    # Add special mappings
    slot_mapping.update(special_mappings)
    
    # Map the data
    mapped_data = []
    for row in data:
        mapped_row = {}
        for tsv_col, value in row.items():
            # Find matching slot
            mapped_field = slot_mapping.get(tsv_col, tsv_col)
            
            # Special handling for generic fields that need class prefix
            if tsv_col in ['link', 'name', 'id', 'strain', 'n_contigs'] and tsv_col not in slot_mapping:
                # Add class prefix for these common fields
                mapped_field = f'{class_name.lower()}_{tsv_col}'
            
            # Handle multivalued fields (convert string lists)
            if value and isinstance(value, str) and value.startswith('[') and value.endswith(']'):
                try:
                    # Parse as Python list literal
                    import ast
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    # If parsing fails, treat as single string
                    pass
            
            # Convert numeric strings to appropriate types
            if value and isinstance(value, str):
                # Try integer conversion
                try:
                    if '.' not in value and value.isdigit():
                        value = int(value)
                except (ValueError, TypeError):
                    # Try float conversion
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        pass
            
            mapped_row[mapped_field] = value
        
        mapped_data.append(mapped_row)
    
    return mapped_data


def validate_data(data: List[Dict[str, Any]], class_name: str, schema_view: SchemaView) -> List[str]:
    """Validate data against the schema and return list of errors."""
    errors = []
    
    try:
        # Get class definition
        class_def = schema_view.get_class(class_name)
        if not class_def:
            return [f"Class {class_name} not found in schema"]
        
        # Get slots for this class
        class_slots = schema_view.class_slots(class_name)
        
        # Validate each record
        for i, record in enumerate(data):
            try:
                # Check required fields
                for slot_name in class_slots:
                    slot_def = schema_view.get_slot(slot_name)
                    if slot_def and slot_def.required:
                        if slot_name not in record or record[slot_name] is None or record[slot_name] == '':
                            errors.append(f"Record {i+1}: Missing required field '{slot_name}'")
                
                # Check field constraints
                for field_name, value in record.items():
                    if field_name in class_slots and value is not None:
                        slot_def = schema_view.get_slot(field_name)
                        if slot_def:
                            # Check range/type
                            if slot_def.range:
                                if slot_def.range == 'integer' and not isinstance(value, int):
                                    try:
                                        int(value)
                                    except (ValueError, TypeError):
                                        errors.append(f"Record {i+1}: Field '{field_name}' should be integer, got: {value}")
                                elif slot_def.range == 'float' and not isinstance(value, (int, float)):
                                    try:
                                        float(value)
                                    except (ValueError, TypeError):
                                        errors.append(f"Record {i+1}: Field '{field_name}' should be float, got: {value}")
                            
                            # Check patterns
                            if slot_def.pattern and isinstance(value, str):
                                import re
                                if not re.match(slot_def.pattern, value):
                                    errors.append(f"Record {i+1}: Field '{field_name}' does not match pattern {slot_def.pattern}: {value}")
                            
                            # Check min/max values
                            if slot_def.minimum_value is not None:
                                try:
                                    if float(value) < slot_def.minimum_value:
                                        errors.append(f"Record {i+1}: Field '{field_name}' below minimum {slot_def.minimum_value}: {value}")
                                except (ValueError, TypeError):
                                    pass
                                    
                            if slot_def.maximum_value is not None:
                                try:
                                    if float(value) > slot_def.maximum_value:
                                        errors.append(f"Record {i+1}: Field '{field_name}' above maximum {slot_def.maximum_value}: {value}")
                                except (ValueError, TypeError):
                                    pass
                
            except Exception as e:
                errors.append(f"Record {i+1}: Validation error: {str(e)}")
                
    except Exception as e:
        errors.append(f"Schema validation setup error: {str(e)}")
    
    return errors


def infer_class_name_from_filename(filename: str) -> str:
    """Infer the class name from the TSV filename."""
    # Remove .tsv extension and use as class name
    base_name = Path(filename).stem
    
    # Map filenames to schema class names
    filename_to_class = {
        'ASV': 'OTU',  # ASV data maps to OTU class
        'ASV_count': None,  # ASV count data is a measurement table, no direct class mapping
        'DubSeq_Library': 'DubSeq_Library',
        'TnSeq_Library': 'TnSeq_Library',
    }
    
    return filename_to_class.get(base_name, base_name)


def main():
    parser = argparse.ArgumentParser(description='Validate TSV files against CORAL LinkML schema')
    parser.add_argument('tsv_files', nargs='+', help='TSV files to validate')
    parser.add_argument('--schema', 
                       default='src/linkml_coral/schema/linkml_coral.yaml',
                       help='Path to LinkML schema file')
    parser.add_argument('--class', dest='class_name',
                       help='Override class name (inferred from filename if not provided)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed validation information')
    
    args = parser.parse_args()
    
    # Load schema
    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        schema_view = load_schema(schema_path)
        print(f"Loaded schema: {schema_view.schema.name}")
    except Exception as e:
        print(f"Error loading schema: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Validate each TSV file
    total_errors = 0
    
    for tsv_file in args.tsv_files:
        tsv_path = Path(tsv_file)
        if not tsv_path.exists():
            print(f"Error: TSV file not found: {tsv_path}", file=sys.stderr)
            continue
        
        # Determine class name
        class_name = args.class_name or infer_class_name_from_filename(tsv_path.name)
        
        if class_name is None:
            print(f"\nSkipping {tsv_path.name} - No corresponding class in schema (measurement/count table)")
            continue
            
        print(f"\nValidating {tsv_path.name} as {class_name} entities...")
        
        try:
            # Read and process TSV data
            raw_data = read_tsv_file(tsv_path)
            if not raw_data:
                print(f"  No data found in {tsv_path.name}")
                continue
            
            print(f"  Read {len(raw_data)} records")
            
            # Map TSV fields to schema fields
            mapped_data = map_tsv_to_schema_fields(raw_data, class_name, schema_view)
            
            if args.verbose:
                print(f"  Sample mapped record: {json.dumps(mapped_data[0], indent=2)}")
            
            # Validate data
            errors = validate_data(mapped_data, class_name, schema_view)
            
            if errors:
                print(f"  ❌ Found {len(errors)} validation errors:")
                # Show first 10 errors
                for i, error in enumerate(errors[:10]):
                    print(f"    - {error}")
                if len(errors) > 10:
                    print(f"    ... and {len(errors) - 10} more errors")
                total_errors += len(errors)
            else:
                print(f"  ✅ All {len(mapped_data)} records are valid")
        
        except Exception as e:
            print(f"  ❌ Error processing {tsv_path.name}: {e}")
            total_errors += 1
    
    # Summary
    print(f"\nValidation complete. Total errors: {total_errors}")
    
    if total_errors > 0:
        sys.exit(1)
    else:
        print("🎉 All files validated successfully!")


if __name__ == "__main__":
    main()