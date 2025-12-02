#!/usr/bin/env python3
"""
Debug script to investigate linkml-validate Python object serialization errors.

This script creates detailed debug output to identify where LinkML runtime objects
(like SlotDefinitionName) might be getting into the YAML serialization process.
"""

import argparse
import csv
import json
import subprocess
import sys
import tempfile
import traceback
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict

from linkml_runtime.utils.schemaview import SchemaView


def debug_schema_view_objects(schema_view: SchemaView, class_name: str):
    """Debug function to inspect SchemaView objects and their types."""
    print(f"\n🔍 DEBUG: Inspecting SchemaView objects for class '{class_name}'")
    
    try:
        # Get class definition
        class_def = schema_view.get_class(class_name)
        print(f"  Class definition type: {type(class_def)}")
        if class_def:
            print(f"  Class name: {class_def.name}")
        
        # Get slot definitions
        slots = schema_view.class_slots(class_name)
        print(f"  Slots type: {type(slots)}")
        print(f"  Number of slots: {len(slots) if slots else 0}")
        
        if slots:
            print(f"  First few slot details:")
            for i, slot in enumerate(slots[:5]):
                print(f"    [{i}] Slot type: {type(slot)} | Value: {repr(slot)}")
                
                # Check if this is a SlotDefinitionName object
                if hasattr(slot, '__class__') and 'SlotDefinitionName' in str(type(slot)):
                    print(f"    ⚠️  FOUND SlotDefinitionName object: {slot}")
                    print(f"    ⚠️  String representation: {str(slot)}")
                
                # Try to get slot definition
                try:
                    slot_def = schema_view.get_slot(slot)
                    if slot_def:
                        print(f"    [{i}] Slot definition range: {slot_def.range}")
                except Exception as e:
                    print(f"    [{i}] Error getting slot definition: {e}")
    
    except Exception as e:
        print(f"  ❌ Error during schema inspection: {e}")
        traceback.print_exc()


def debug_slot_mapping(slots, class_name: str):
    """Debug the slot mapping process to find object contamination."""
    print(f"\n🔍 DEBUG: Creating slot mapping for class '{class_name}'")
    
    slot_mapping = {}
    problematic_slots = []
    
    for i, slot_name in enumerate(slots):
        print(f"  Processing slot [{i}]: {repr(slot_name)} (type: {type(slot_name)})")
        
        # Check if slot_name is actually a string
        if isinstance(slot_name, str):
            slot_mapping[slot_name] = slot_name
            
            # Also map without class prefix
            if slot_name.startswith(class_name.lower() + '_'):
                tsv_field = slot_name.replace(class_name.lower() + '_', '', 1)
                slot_mapping[tsv_field] = slot_name
                print(f"    ✅ Added mapping: {tsv_field} -> {slot_name}")
        else:
            # This is the problematic case!
            problematic_slots.append((i, slot_name, type(slot_name)))
            print(f"    ⚠️  NON-STRING SLOT FOUND: {repr(slot_name)}")
            
            # Try to convert to string safely
            try:
                slot_str = str(slot_name)
                slot_mapping[slot_str] = slot_str
                print(f"    🔧 Converted to string: {slot_str}")
            except Exception as e:
                print(f"    ❌ Failed to convert to string: {e}")
    
    if problematic_slots:
        print(f"\n⚠️  FOUND {len(problematic_slots)} non-string slots:")
        for i, slot, slot_type in problematic_slots:
            print(f"    [{i}] {repr(slot)} (type: {slot_type})")
    
    return slot_mapping, problematic_slots


def safe_yaml_serialization_check(data: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Check if data can be safely serialized to YAML without Python objects."""
    print(f"\n🔍 DEBUG: Checking YAML serialization safety for {len(data)} records")
    
    issues = []
    
    for record_idx, record in enumerate(data[:5]):  # Check first 5 records
        print(f"  Checking record {record_idx}:")
        
        for key, value in record.items():
            key_type = type(key)
            value_type = type(value)
            
            # Check for problematic key types
            if not isinstance(key, str):
                issue = f"Record {record_idx}: Non-string key {repr(key)} (type: {key_type})"
                issues.append(issue)
                print(f"    ❌ {issue}")
            
            # Check for problematic value types
            if value is not None:
                if hasattr(value, '__class__') and ('linkml_runtime' in str(value_type) or 'SlotDefinitionName' in str(value_type)):
                    issue = f"Record {record_idx}: LinkML runtime object in value for key '{key}': {repr(value)} (type: {value_type})"
                    issues.append(issue)
                    print(f"    ❌ {issue}")
                elif not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                    issue = f"Record {record_idx}: Non-basic type in value for key '{key}': {repr(value)} (type: {value_type})"
                    issues.append(issue)
                    print(f"    ⚠️  {issue}")
    
    return len(issues) == 0, issues


def create_debug_yaml_with_temp_file(data: List[Dict[str, Any]], class_name: str, debug_dir: Path) -> Tuple[str, Path]:
    """Create YAML with debug information and save temporary file."""
    print(f"\n🔍 DEBUG: Creating YAML for {len(data)} records")
    
    # Create debug directory
    debug_dir.mkdir(exist_ok=True)
    
    # Check for serialization safety first
    is_safe, issues = safe_yaml_serialization_check(data)
    
    if not is_safe:
        print(f"  ⚠️  Serialization issues found: {len(issues)}")
        for issue in issues:
            print(f"    - {issue}")
    
    # Create a clean collection format for validation
    collection_data = []
    
    for record_idx, record in enumerate(data):
        # Create a clean record with only basic Python types
        linkml_record = {}
        
        for key, value in record.items():
            # Double-check key is a string and not a LinkML object
            if not isinstance(key, str):
                print(f"  ⚠️  Skipping non-string key in record {record_idx}: {repr(key)} (type: {type(key)})")
                continue
            
            # Check for LinkML runtime objects in the key name itself
            if hasattr(key, '__class__') and 'linkml_runtime' in str(type(key)):
                print(f"  ⚠️  LinkML runtime object found as key in record {record_idx}: {repr(key)}")
                continue
                
            if value is not None:
                # Ensure all values are basic Python types that YAML can handle
                if isinstance(value, (str, int, float, bool)):
                    linkml_record[key] = value
                elif isinstance(value, list):
                    # Handle lists by ensuring all items are basic types
                    clean_list = []
                    for item in value:
                        if isinstance(item, (str, int, float, bool)):
                            clean_list.append(item)
                        elif hasattr(item, '__class__') and 'linkml_runtime' in str(type(item)):
                            print(f"  ⚠️  LinkML runtime object in list for key '{key}': {repr(item)}")
                            clean_list.append(str(item))
                        else:
                            clean_list.append(str(item))
                    linkml_record[key] = clean_list
                elif hasattr(value, '__class__') and 'linkml_runtime' in str(type(value)):
                    print(f"  ⚠️  LinkML runtime object found for key '{key}': {repr(value)} (type: {type(value)})")
                    linkml_record[key] = str(value)
                else:
                    # Convert complex objects to string representation
                    linkml_record[key] = str(value)
        
        collection_data.append(linkml_record)
    
    # Save debug information
    debug_info = {
        'class_name': class_name,
        'total_records': len(data),
        'collection_records': len(collection_data),
        'serialization_safe': is_safe,
        'serialization_issues': issues,
        'sample_record': collection_data[0] if collection_data else None
    }
    
    debug_info_file = debug_dir / f"{class_name}_debug_info.json"
    with open(debug_info_file, 'w') as f:
        json.dump(debug_info, f, indent=2, default=str)
    print(f"  💾 Saved debug info to {debug_info_file}")
    
    # Use safe YAML dump with explicit Dumper to avoid Python object references
    try:
        yaml_content = yaml.dump(collection_data, 
                                Dumper=yaml.SafeDumper,
                                default_flow_style=False, 
                                allow_unicode=True)
        
        # Save the YAML content to a file in debug directory
        yaml_file = debug_dir / f"{class_name}_converted.yaml"
        with open(yaml_file, 'w') as f:
            f.write(yaml_content)
        print(f"  💾 Saved YAML to {yaml_file}")
        
        return yaml_content, yaml_file
        
    except yaml.representer.RepresenterError as e:
        print(f"  ❌ YAML RepresenterError: {e}")
        raise
    except Exception as e:
        print(f"  ❌ YAML serialization error: {e}")
        raise


def validate_with_debug_output(yaml_data: str, yaml_file: Path, class_name: str, schema_path: Path, debug_dir: Path) -> Tuple[bool, List[str], str]:
    """Use linkml-validate with debug output capture."""
    print(f"\n🔍 DEBUG: Running linkml-validate on {yaml_file}")
    
    validation_errors = []
    validation_output = ""
    
    # Create a copy of the YAML file that won't be deleted (for debugging)
    debug_yaml_file = debug_dir / f"{class_name}_for_validation.yaml"
    debug_yaml_file.write_text(yaml_data)
    
    try:
        # Run linkml-validate command with maximum verbosity
        cmd = [
            'linkml-validate',
            '-s', str(schema_path),
            '-C', class_name,
            '--verbose',
            str(debug_yaml_file)
        ]
        
        print(f"  Running command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        validation_output = result.stderr + result.stdout
        
        # Save raw validation output
        output_file = debug_dir / f"{class_name}_validation_output.txt"
        with open(output_file, 'w') as f:
            f.write(f"Command: {' '.join(cmd)}\n")
            f.write(f"Return code: {result.returncode}\n")
            f.write(f"STDOUT:\n{result.stdout}\n")
            f.write(f"STDERR:\n{result.stderr}\n")
        print(f"  💾 Saved validation output to {output_file}")
        
        if result.returncode == 0:
            print(f"  ✅ Validation successful")
            return True, [], validation_output
        else:
            print(f"  ❌ Validation failed with return code {result.returncode}")
            
            # Parse validation errors from output
            for line in validation_output.split('\n'):
                if '[ERROR]' in line or 'ConstructorError' in line or 'could not determine a constructor' in line:
                    # Clean up the error message
                    error_msg = line.replace('[ERROR]', '').strip()
                    validation_errors.append(error_msg)
                    print(f"    Error: {error_msg}")
            
            return False, validation_errors, validation_output
            
    except subprocess.TimeoutExpired:
        error_msg = "Validation timed out after 5 minutes"
        print(f"  ❌ {error_msg}")
        return False, [error_msg], ""
    except Exception as e:
        error_msg = f"Validation failed: {str(e)}"
        print(f"  ❌ {error_msg}")
        return False, [error_msg], ""


def main():
    parser = argparse.ArgumentParser(description='Debug linkml-validate Python object serialization errors')
    parser.add_argument('tsv_file', help='TSV file to debug')
    parser.add_argument('--schema', 
                       default='src/linkml_coral/schema/linkml_coral.yaml',
                       help='Path to LinkML schema file')
    parser.add_argument('--class', dest='class_name',
                       help='Override class name (inferred from filename if not provided)')
    parser.add_argument('--debug-dir', default='debug_linkml_validate',
                       help='Directory to save debug files')
    
    args = parser.parse_args()
    
    # Setup debug directory
    debug_dir = Path(args.debug_dir)
    debug_dir.mkdir(exist_ok=True)
    print(f"🔍 Debug files will be saved to: {debug_dir.absolute()}")
    
    # Load schema
    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        schema_view = SchemaView(str(schema_path))
        print(f"✅ Loaded schema: {schema_view.schema.name}")
    except Exception as e:
        print(f"❌ Error loading schema: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Load TSV file
    tsv_path = Path(args.tsv_file)
    if not tsv_path.exists():
        print(f"Error: TSV file not found: {tsv_path}", file=sys.stderr)
        sys.exit(1)
    
    # Determine class name
    class_name = args.class_name or tsv_path.stem
    print(f"🔍 Processing {tsv_path.name} as {class_name} entities")
    
    try:
        # Debug schema view objects
        debug_schema_view_objects(schema_view, class_name)
        
        # Get class definition and slots with debugging
        class_def = schema_view.get_class(class_name)
        if not class_def:
            print(f"❌ Class '{class_name}' not found in schema")
            sys.exit(1)
        
        slots = schema_view.class_slots(class_name)
        print(f"✅ Found {len(slots)} slots for class {class_name}")
        
        # Debug slot mapping
        slot_mapping, problematic_slots = debug_slot_mapping(slots, class_name)
        
        # Read TSV data
        print(f"\n🔍 Reading TSV file: {tsv_path}")
        data = []
        with open(tsv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                # Convert empty strings to None
                cleaned_row = {k: (v if v.strip() else None) for k, v in row.items()}
                data.append(cleaned_row)
        
        print(f"✅ Read {len(data)} records from TSV")
        
        # Map TSV fields to schema fields with debugging
        print(f"\n🔍 Mapping TSV fields to schema fields")
        mapped_data = []
        
        for row_idx, row in enumerate(data[:5]):  # Debug first 5 rows
            mapped_row = {}
            print(f"  Processing row {row_idx}:")
            
            for tsv_col, value in row.items():
                if tsv_col in slot_mapping:
                    mapped_field = slot_mapping[tsv_col]
                    print(f"    {tsv_col} -> {mapped_field} = {repr(value)}")
                    
                    # Check types again
                    if not isinstance(mapped_field, str):
                        print(f"    ⚠️  Mapped field is not a string: {repr(mapped_field)} (type: {type(mapped_field)})")
                        continue
                    
                    mapped_row[mapped_field] = value
                else:
                    print(f"    {tsv_col} (unmapped)")
            
            mapped_data.append(mapped_row)
        
        # Process all remaining rows without debug output
        for row in data[5:]:
            mapped_row = {}
            for tsv_col, value in row.items():
                if tsv_col in slot_mapping:
                    mapped_field = slot_mapping[tsv_col]
                    if isinstance(mapped_field, str):
                        mapped_row[mapped_field] = value
            mapped_data.append(mapped_row)
        
        print(f"✅ Mapped {len(mapped_data)} records")
        
        # Create YAML with debugging
        yaml_content, yaml_file = create_debug_yaml_with_temp_file(mapped_data, class_name, debug_dir)
        
        # Validate with debugging
        is_valid, errors, output = validate_with_debug_output(yaml_content, yaml_file, class_name, schema_path, debug_dir)
        
        if is_valid:
            print(f"\n✅ Validation successful!")
        else:
            print(f"\n❌ Validation failed with {len(errors)} errors:")
            for error in errors:
                print(f"  - {error}")
        
        print(f"\n📁 All debug files saved to: {debug_dir.absolute()}")
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()