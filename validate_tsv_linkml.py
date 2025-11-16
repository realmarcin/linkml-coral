#!/usr/bin/env python3
"""
Validate TSV files against the CORAL LinkML schema using linkml-validate.

This script converts TSV data to LinkML-compatible format and uses the official
linkml-validate command for comprehensive validation including controlled
vocabularies, foreign keys, and all schema constraints.
"""

import argparse
import ast
import csv
import json
import subprocess
import sys
import tempfile
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict

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
            # Convert empty strings to None, but keep them as strings for now
            # Let LinkML handle type conversion
            cleaned_row = {k: (v if v.strip() else None) for k, v in row.items()}
            data.append(cleaned_row)
    return data


def map_tsv_to_schema_fields(data: List[Dict[str, Any]], class_name: str, schema_view: SchemaView) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Map TSV column names to schema field names."""
    if not data:
        return data, {"status": "no_data"}
    
    mapping_report = {
        "class_name": class_name,
        "tsv_columns": sorted(data[0].keys()) if data else [],
        "schema_slots": [],
        "mappings_applied": {},
        "unmapped_columns": [],
        "mapping_summary": ""
    }
    
    # Get class definition from schema
    class_def = schema_view.get_class(class_name)
    if not class_def:
        mapping_report["status"] = "class_not_found"
        return data, mapping_report
    
    # Get slot definitions for the class
    slots = schema_view.class_slots(class_name)
    mapping_report["schema_slots"] = sorted(slots)
    
    # Create comprehensive mapping strategy
    slot_mapping = {}
    
    # 1. Direct mappings (TSV column matches schema slot exactly)
    for slot_name in slots:
        # Convert SlotDefinitionName objects to strings
        # SlotDefinitionName objects have string representation but aren't isinstance(str)
        slot_name_str = str(slot_name)
        
        # Ensure we have a valid string slot name
        if slot_name_str and isinstance(slot_name_str, str):
            slot_mapping[slot_name_str] = slot_name_str
            
            # Also map without class prefix
            if slot_name_str.startswith(class_name.lower() + '_'):
                tsv_field = slot_name_str.replace(class_name.lower() + '_', '', 1)
                slot_mapping[tsv_field] = slot_name_str
    
    # 2. Special mappings for ENIGMA data format
    special_mappings = {
        # Generic fields that need class prefix
        'id': f'{class_name.lower()}_id',
        'name': f'{class_name.lower()}_name',
        'link': f'{class_name.lower()}_link',
        'description': f'{class_name.lower()}_description',
        'strain': f'{class_name.lower()}_strain',
        'n_contigs': f'{class_name.lower()}_n_contigs',
        'n_features': f'{class_name.lower()}_n_features',
        
        # Sample-specific mappings
        'location': 'sample_location',
        'depth': 'sample_depth',
        'elevation': 'sample_elevation',
        'date': 'sample_date',
        'time': 'sample_time',
        'timezone': 'sample_timezone',
        'material_term_id': 'sample_material',
        'env_package_term_id': 'sample_env_package',
        
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
        'read_type_term_id': 'reads_read_type',
        'sequencing_technology_term_id': 'reads_sequencing_technology',
        
        # Community mappings
        'community_type_term_id': 'community_community_type',
        'sample': 'community_sample',
        'parent_community': 'community_parent_community',
        'condition': 'community_condition',
        'defined_strains': 'community_defined_strains',
    }
    
    # Update slot mapping with special mappings
    slot_mapping.update(special_mappings)
    
    # Map the data
    mapped_data = []
    tsv_columns = set()
    mappings_used = {}
    
    for row in data:
        mapped_row = {}
        for tsv_col, value in row.items():
            tsv_columns.add(tsv_col)
            
            # Find mapping
            if tsv_col in slot_mapping:
                mapped_field = slot_mapping[tsv_col]
                mappings_used[tsv_col] = mapped_field
            else:
                # No mapping found - skip unmapped columns to avoid validation errors
                continue
            
            # Skip if mapped_field is not a string (could be a schema object)
            if not isinstance(mapped_field, str):
                continue
            
            # Handle multivalued fields (convert string lists to actual lists)
            if value and isinstance(value, str) and value.startswith('[') and value.endswith(']'):
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    # If parsing fails, treat as single item list
                    value = [value.strip('[]')]
            
            # Convert numeric values for proper LinkML validation
            # Check slot definition to determine expected type
            slot = schema_view.get_slot(mapped_field)
            if slot and value is not None and isinstance(value, str):
                if slot.range == 'float':
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        pass  # Keep as string for validation error
                elif slot.range == 'integer':
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        pass  # Keep as string for validation error
            
            mapped_row[mapped_field] = value
        
        mapped_data.append(mapped_row)
    
    # Report mapping results
    mapping_report["mappings_applied"] = mappings_used
    mapping_report["unmapped_columns"] = sorted(tsv_columns - set(mappings_used.keys()))
    
    if mappings_used:
        mapping_report["mapping_summary"] = f"Applied {len(mappings_used)} field mappings"
    else:
        mapping_report["mapping_summary"] = "No field mappings required"
    
    mapping_report["status"] = "success"
    return mapped_data, mapping_report


def convert_to_linkml_format(data: List[Dict[str, Any]], class_name: str) -> str:
    """Convert mapped data to LinkML-compatible YAML format."""
    # Create a collection format for validation
    collection_data = []
    
    for record in data:
        # Create a clean record with only basic Python types
        linkml_record = {}
        for key, value in record.items():
            # Convert keys to strings and check for LinkML runtime objects
            key_str = str(key)
            
            # Double-check key is a clean string
            if not isinstance(key_str, str):
                print(f"WARNING: Non-string key found after conversion: {type(key_str)} = {key_str}")
                continue
            
            # Check for LinkML runtime objects in key
            if hasattr(key, '__class__') and 'linkml_runtime' in str(type(key)):
                print(f"WARNING: LinkML runtime object found as key, converted to string: {type(key)} -> {key_str}")
                
            if value is not None:
                # Ensure all values are basic Python types that YAML can handle
                if isinstance(value, (str, int, float, bool)):
                    linkml_record[key_str] = value
                elif isinstance(value, list):
                    # Handle lists by ensuring all items are basic types
                    clean_list = []
                    for item in value:
                        if isinstance(item, (str, int, float, bool)):
                            clean_list.append(item)
                        else:
                            clean_list.append(str(item))
                    linkml_record[key_str] = clean_list
                else:
                    # Convert complex objects to string representation
                    print(f"WARNING: Complex object found in {key_str}: {type(value)}")
                    linkml_record[key_str] = str(value)
        
        collection_data.append(linkml_record)
    
    # Use safe YAML dump with explicit Dumper to avoid Python object references
    return yaml.dump(collection_data, 
                     Dumper=yaml.SafeDumper,
                     default_flow_style=False, 
                     allow_unicode=True)


def validate_with_linkml(yaml_data: str, class_name: str, schema_path: Path) -> Tuple[bool, List[str], str]:
    """Use linkml-validate to validate the data."""
    
    validation_errors = []
    validation_output = ""
    
    # Create temporary files for validation
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
        temp_file.write(yaml_data)
        temp_file_path = temp_file.name
    
    try:
        # Run linkml-validate command
        cmd = [
            'linkml-validate',
            '-s', str(schema_path),
            '-C', class_name,
            temp_file_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        validation_output = result.stderr + result.stdout
        
        if result.returncode == 0:
            return True, [], validation_output
        else:
            # Parse validation errors from output
            for line in validation_output.split('\n'):
                if '[ERROR]' in line:
                    # Clean up the error message
                    error_msg = line.replace('[ERROR]', '').strip()
                    validation_errors.append(error_msg)
            
            return False, validation_errors, validation_output
            
    except subprocess.TimeoutExpired:
        return False, ["Validation timed out after 5 minutes"], ""
    except Exception as e:
        return False, [f"Validation failed: {str(e)}"], ""
    finally:
        # Clean up temporary file
        Path(temp_file_path).unlink(missing_ok=True)


def infer_class_name_from_filename(filename: str) -> str:
    """Infer the class name from the TSV filename."""
    base_name = Path(filename).stem
    
    # Map filenames to schema class names
    filename_to_class = {
        'ASV': 'OTU',  # ASV data maps to OTU class
        'ASV_count': None,  # ASV count data is a measurement table, no direct class mapping
        'DubSeq_Library': 'DubSeq_Library',
        'TnSeq_Library': 'TnSeq_Library',
    }
    
    return filename_to_class.get(base_name, base_name)


def print_mapping_report(mapping_report: Dict[str, Any], filename: str):
    """Print a concise mapping report."""
    print(f"  📊 {mapping_report.get('mapping_summary', 'No mappings')}")
    
    if mapping_report.get('mappings_applied'):
        print(f"  🔄 {len(mapping_report['mappings_applied'])} field mappings applied")
        
    if mapping_report.get('unmapped_columns'):
        print(f"  ⚠️  {len(mapping_report['unmapped_columns'])} unmapped columns: {', '.join(mapping_report['unmapped_columns'][:3])}")
        if len(mapping_report['unmapped_columns']) > 3:
            print(f"      (and {len(mapping_report['unmapped_columns']) - 3} more)")


def print_validation_errors(errors: List[str], max_errors: int = 10, temp_file_path: str = None):
    """Print validation errors in a readable format."""
    print(f"  ❌ Found {len(errors)} validation errors:")
    
    for i, error in enumerate(errors[:max_errors]):
        # Clean up error message for better readability
        clean_error = error.replace(temp_file_path, 'record') if temp_file_path else error
        print(f"    • {clean_error}")
    
    if len(errors) > max_errors:
        print(f"    ... and {len(errors) - max_errors} more errors")


def main():
    parser = argparse.ArgumentParser(description='Validate TSV files against CORAL LinkML schema using linkml-validate')
    parser.add_argument('tsv_files', nargs='+', help='TSV files to validate')
    parser.add_argument('--schema', 
                       default='src/linkml_coral/schema/linkml_coral.yaml',
                       help='Path to LinkML schema file')
    parser.add_argument('--class', dest='class_name',
                       help='Override class name (inferred from filename if not provided)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed validation information')
    parser.add_argument('--max-errors', type=int, default=10,
                       help='Maximum number of errors to display per file')
    parser.add_argument('--save-yaml', 
                       help='Save converted YAML data to specified directory')
    parser.add_argument('--timeout', type=int, default=300,
                       help='Validation timeout in seconds (default: 300)')
    
    args = parser.parse_args()
    
    # Load schema
    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        schema_view = load_schema(schema_path)
        print(f"Loaded schema: {schema_view.schema.name}")
        print(f"Using linkml-validate for comprehensive validation")
    except Exception as e:
        print(f"Error loading schema: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Validate each TSV file
    total_errors = 0
    files_with_errors = []
    files_validated = 0
    
    for tsv_file in args.tsv_files:
        tsv_path = Path(tsv_file)
        if not tsv_path.exists():
            print(f"Error: TSV file not found: {tsv_path}", file=sys.stderr)
            continue
        
        # Determine class name
        class_name = args.class_name or infer_class_name_from_filename(tsv_path.name)
        
        if class_name is None:
            print(f"\n❌ {tsv_path.name}: No corresponding class in schema")
            print(f"  - This appears to be a measurement/count table")
            continue
            
        print(f"\n🔍 Validating {tsv_path.name} as {class_name} entities...")
        
        try:
            # Read and map TSV data
            raw_data = read_tsv_file(tsv_path)
            if not raw_data:
                print(f"  📋 No data found in {tsv_path.name}")
                continue
            
            print(f"  📋 Read {len(raw_data)} records")
            
            # Map TSV fields to schema fields
            mapped_data, mapping_report = map_tsv_to_schema_fields(raw_data, class_name, schema_view)
            
            if mapping_report.get("status") == "class_not_found":
                print(f"  ❌ Class '{class_name}' not found in schema")
                total_errors += 1
                continue
            
            # Print mapping report
            print_mapping_report(mapping_report, tsv_path.name)
            
            # Convert to LinkML format
            yaml_data = convert_to_linkml_format(mapped_data, class_name)
            
            # Save YAML if requested
            if args.save_yaml:
                yaml_dir = Path(args.save_yaml)
                yaml_dir.mkdir(exist_ok=True)
                yaml_file = yaml_dir / f"{tsv_path.stem}_{class_name}.yaml"
                with open(yaml_file, 'w') as f:
                    f.write(yaml_data)
                print(f"  💾 Saved converted data to {yaml_file}")
            
            if args.verbose:
                print(f"  🔄 Converting to LinkML format...")
            
            # Validate with linkml-validate
            is_valid, errors, output = validate_with_linkml(yaml_data, class_name, schema_path)
            
            if is_valid:
                print(f"  ✅ All {len(mapped_data)} records are valid")
                files_validated += 1
            else:
                print_validation_errors(errors, args.max_errors)
                total_errors += len(errors)
                files_with_errors.append(tsv_path.name)
                
                if args.verbose and output:
                    print(f"  🔍 Raw validation output:")
                    print(f"    {output}")
        
        except Exception as e:
            print(f"  ❌ Error processing {tsv_path.name}: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            total_errors += 1
            files_with_errors.append(tsv_path.name)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Validation Summary")
    print(f"Files processed: {len(args.tsv_files)}")
    print(f"Files validated: {files_validated}")
    print(f"Files with errors: {len(files_with_errors)}")
    print(f"Total validation errors: {total_errors}")
    
    if files_with_errors:
        print(f"\n❌ Files with validation errors:")
        for filename in files_with_errors:
            print(f"  - {filename}")
    
    if total_errors == 0:
        print("\n🎉 All files validated successfully with linkml-validate!")
        sys.exit(0)
    else:
        print(f"\n⚠️  Validation completed with {total_errors} errors")
        sys.exit(1)


if __name__ == "__main__":
    main()