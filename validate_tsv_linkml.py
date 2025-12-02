#!/usr/bin/env python3
"""
Validate TSV files against the CORAL LinkML schema using linkml-validate.

This script converts TSV data to LinkML-compatible format and uses the official
linkml-validate command for comprehensive validation including controlled
vocabularies, foreign keys, and all schema constraints.

Enhanced with:
- Pre-validation enum checking with detailed error reporting
- Foreign key validation across TSV files
- Data quality metrics collection
- Multi-format reporting (JSON, CSV, HTML)
"""

import argparse
import csv
import json
import subprocess
import sys
import tempfile
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict
from datetime import datetime

from linkml_runtime.utils.schemaview import SchemaView

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Import validation utilities
try:
    from linkml_coral.utils.validation_utils import (
        ValidationStatus,
        ValidationResult,
        RecordValidationResult,
        FileValidationResult,
        EnumValidator,
        ForeignKeyValidator,
        DataQualityAnalyzer,
        build_fk_index_from_tsvs
    )
except ImportError:
    # Fallback for when running from different directory
    from src.linkml_coral.utils.validation_utils import (
        ValidationStatus,
        ValidationResult,
        RecordValidationResult,
        FileValidationResult,
        EnumValidator,
        ForeignKeyValidator,
        DataQualityAnalyzer,
        build_fk_index_from_tsvs
    )


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
    
    # Get the identifier slot for this class to avoid mapping conflicts
    identifier_slot = None
    for slot_name in slots:
        slot_def = schema_view.get_slot(str(slot_name))
        if slot_def and slot_def.identifier:
            identifier_slot = str(slot_name)
            break

    # 1. Direct mappings (TSV column matches schema slot exactly)
    for slot_name in slots:
        # Convert SlotDefinitionName objects to strings
        # SlotDefinitionName objects have string representation but aren't isinstance(str)
        slot_name_str = str(slot_name)

        # Ensure we have a valid string slot name
        if slot_name_str and isinstance(slot_name_str, str):
            # SKIP direct mapping for identifier slots - these should come from 'id' column via special mappings
            # For example, don't map TSV's 'community_id' column directly if it's the identifier
            if slot_name_str != identifier_slot:
                slot_mapping[slot_name_str] = slot_name_str

            # Also map without class prefix
            if slot_name_str.startswith(class_name.lower() + '_'):
                tsv_field = slot_name_str.replace(class_name.lower() + '_', '', 1)

                # SKIP direct mapping for TSV columns that will be handled by special mappings
                # For example, TSV has both 'id' and 'community_id' columns,
                # but only 'id' should map to the schema's 'community_id' field
                if tsv_field not in ['id', 'name', 'description', 'link'] and slot_name_str != identifier_slot:
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

        # Gene-specific mappings (special case: name → gene_id, genome_id → genome)
        **({'name': 'gene_gene_id', 'genome_id': 'gene_genome'} if class_name == 'Gene' else {}),
        
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

        # Bin mappings
        'assembly_id': 'bin_assembly',
        'contigs': 'bin_contigs',

        # Sample mappings
        'location_id': 'sample_location',
    }

    # Library-specific mappings (DubSeq, TnSeq) - only add if class is a Library
    if 'Library' in class_name:
        special_mappings['genome_id'] = f'{class_name.lower()}_genome'

    # Strain-specific mapping for genome_id
    if class_name == 'Strain':
        special_mappings['genome_id'] = 'strain_genome'

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
            
            # Get slot definition early to check if multivalued
            slot = schema_view.get_slot(mapped_field)

            # Handle multivalued fields (convert string lists to actual lists)
            if value and isinstance(value, str):
                # Check if field is multivalued in schema
                if slot and slot.multivalued:
                    # Handle bracket notation: [item1, item2]
                    if value.startswith('[') and value.endswith(']'):
                        try:
                            import ast
                            value = ast.literal_eval(value)
                        except (ValueError, SyntaxError):
                            # If parsing fails, treat as single item list
                            value = [value.strip('[]')]
                    # Handle comma-separated values: item1, item2, item3
                    elif ', ' in value:
                        value = [item.strip() for item in value.split(', ')]
                    # Single value for multivalued field - wrap in list
                    else:
                        value = [value]

            # Convert numeric values and enum ontology terms for proper LinkML validation
            # Check slot definition to determine expected type
            if slot and value is not None and isinstance(value, str):
                # Check if range is a numeric type (or subtype)
                range_type = schema_view.get_type(slot.range) if slot.range else None

                if slot.range == 'float' or (range_type and range_type.typeof == 'float'):
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        pass  # Keep as string for validation error
                elif slot.range == 'integer' or (range_type and range_type.typeof == 'integer'):
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        pass  # Keep as string for validation error
                # Check if this is an enum field with ontology term format
                elif schema_view.get_enum(slot.range):
                    # Try to map ontology term format to enum key
                    import re
                    match = re.match(r'^(.+?)\s+<([A-Z_]+):(\d+)>$', value.strip())
                    if match:
                        label, prefix, term_id = match.groups()
                        full_term = f"{prefix}:{term_id}"

                        # Find permissible value with matching meaning/term annotation
                        enum_def = schema_view.get_enum(slot.range)
                        if enum_def and enum_def.permissible_values:
                            for pv_key, pv_def in enum_def.permissible_values.items():
                                # Check meaning field
                                if pv_def.meaning and pv_def.meaning == full_term:
                                    value = pv_key
                                    break
                                # Check annotations dict for 'term' key
                                if pv_def.annotations and 'term' in pv_def.annotations:
                                    ann = pv_def.annotations['term']
                                    if ann.value == full_term:
                                        value = pv_key
                                        break

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


def validate_enums_in_data(
    mapped_data: List[Dict[str, Any]],
    class_name: str,
    schema_view: SchemaView,
    enum_validator: EnumValidator
) -> List[RecordValidationResult]:
    """
    Pre-validate enum fields in the data.

    Args:
        mapped_data: List of records with mapped field names
        class_name: Schema class name
        schema_view: SchemaView instance
        enum_validator: EnumValidator instance

    Returns:
        List of RecordValidationResult for records with issues only
    """
    record_results = []

    # Get all slots for the class
    class_slots = schema_view.class_slots(class_name)
    enum_slots = {}

    # Identify which slots have enum ranges
    for slot_name in class_slots:
        slot_name_str = str(slot_name)
        slot = schema_view.induced_slot(slot_name_str, class_name)
        if slot and slot.range:
            enum_def = schema_view.get_enum(slot.range)
            if enum_def:
                enum_slots[slot_name_str] = slot.range

    # Early exit if no enum fields
    if not enum_slots:
        return record_results

    # Validate each record
    for line_num, record in enumerate(mapped_data, start=2):  # Line 2 is first data row (after header)
        validation_results = []
        entity_id = record.get(f'{class_name.lower()}_id', f'record_{line_num}')

        # Check each enum field
        for slot_name, enum_name in enum_slots.items():
            if slot_name in record:
                value = record[slot_name]
                result = enum_validator.validate(slot_name, value, enum_name)

                # Only add warnings and errors to results
                if result.status != ValidationStatus.PASS:
                    validation_results.append(result)

        # Only create record result if there are issues
        if validation_results:
            record_results.append(RecordValidationResult(
                record_line=line_num,
                entity_id=str(entity_id) if entity_id else None,
                results=validation_results
            ))

    return record_results


def validate_foreign_keys_in_data(
    mapped_data: List[Dict[str, Any]],
    class_name: str,
    schema_view: SchemaView,
    fk_validator: ForeignKeyValidator
) -> Dict[int, RecordValidationResult]:
    """
    Validate foreign key references in the data.

    Args:
        mapped_data: List of records with mapped field names
        class_name: Schema class name
        schema_view: SchemaView instance
        fk_validator: ForeignKeyValidator instance

    Returns:
        Dictionary mapping line number to RecordValidationResult (only for records with issues)
    """
    record_results = {}

    # Get all slots for the class
    class_slots = schema_view.class_slots(class_name)
    fk_slots = {}

    # Identify which slots are foreign keys (have class ranges)
    for slot_name in class_slots:
        slot_name_str = str(slot_name)
        slot = schema_view.induced_slot(slot_name_str, class_name)
        if slot and slot.range:
            # Check if range is a class (not a type or enum)
            range_class = schema_view.get_class(slot.range)
            if range_class:
                fk_slots[slot_name_str] = slot.range

    # Early exit if no FK fields
    if not fk_slots:
        return record_results

    # Validate each record
    for line_num, record in enumerate(mapped_data, start=2):  # Line 2 is first data row (after header)
        validation_results = []
        entity_id = record.get(f'{class_name.lower()}_id', f'record_{line_num}')

        # Check each FK field
        for slot_name, target_class in fk_slots.items():
            if slot_name in record:
                value = record[slot_name]
                result = fk_validator.validate(slot_name, target_class, value)

                # Only add warnings and errors to results
                if result.status != ValidationStatus.PASS:
                    validation_results.append(result)

        # Only store record result if there are issues
        if validation_results:
            record_results[line_num] = RecordValidationResult(
                record_line=line_num,
                entity_id=str(entity_id) if entity_id else None,
                results=validation_results
            )

    return record_results


def collect_quality_metrics(
    mapped_data: List[Dict[str, Any]],
    class_name: str
) -> Dict[str, Any]:
    """
    Collect data quality metrics for all fields.

    Args:
        mapped_data: List of records with mapped field names
        class_name: Schema class name

    Returns:
        Dictionary of field metrics
    """
    if not mapped_data:
        return {}

    analyzer = DataQualityAnalyzer()
    metrics = {}

    # Get all field names
    all_fields = set()
    for record in mapped_data:
        all_fields.update(record.keys())

    # Analyze each field
    for field_name in sorted(all_fields):
        # Collect all values for this field
        values = [record.get(field_name) for record in mapped_data]

        # Analyze field
        field_metrics = analyzer.analyze_field(field_name, values)
        metrics[field_name] = field_metrics.to_dict()

    return metrics


def export_results_json(
    file_results: List[FileValidationResult],
    output_path: Path
):
    """Export validation results to JSON."""
    results_dict = {
        'validation_date': datetime.now().isoformat(),
        'files': [fr.to_dict() for fr in file_results]
    }

    with open(output_path, 'w') as f:
        json.dump(results_dict, f, indent=2)

    print(f"📄 Exported JSON report to {output_path}")


def export_results_csv(
    file_results: List[FileValidationResult],
    output_path: Path
):
    """Export validation results to CSV."""
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow([
            'Filename', 'Total Records', 'Pass Count', 'Warning Count',
            'Error Count', 'Pass Rate', 'Entity ID', 'Record Line',
            'Issue Type', 'Field', 'Value', 'Message'
        ])

        # Write data
        for file_result in file_results:
            for record_result in file_result.record_results:
                if record_result.results:
                    # Record has issues
                    for validation_result in record_result.results:
                        writer.writerow([
                            file_result.filename,
                            file_result.total_records,
                            file_result.pass_count,
                            file_result.warning_count,
                            file_result.error_count,
                            f"{file_result.pass_rate:.2%}",
                            record_result.entity_id,
                            record_result.record_line,
                            validation_result.status.value,
                            validation_result.field_name,
                            validation_result.value,
                            validation_result.message
                        ])
                else:
                    # Record passed
                    writer.writerow([
                        file_result.filename,
                        file_result.total_records,
                        file_result.pass_count,
                        file_result.warning_count,
                        file_result.error_count,
                        f"{file_result.pass_rate:.2%}",
                        record_result.entity_id,
                        record_result.record_line,
                        'PASS',
                        '',
                        '',
                        ''
                    ])

    print(f"📊 Exported CSV report to {output_path}")


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

    # Enhanced validation options
    parser.add_argument('--enum-validate', action='store_true',
                       help='Enable enum value pre-validation')
    parser.add_argument('--fk-validate', action='store_true',
                       help='Enable foreign key validation (requires --tsv-dir)')
    parser.add_argument('--quality-metrics', action='store_true',
                       help='Collect data quality metrics')
    parser.add_argument('--tsv-dir',
                       help='Directory containing all TSV files (for FK index building)')

    # Reporting options
    parser.add_argument('--report-format', choices=['console', 'json', 'csv', 'all'],
                       default='console',
                       help='Output format for validation report')
    parser.add_argument('--output-dir',
                       help='Directory for output reports (default: validation_reports/)')

    args = parser.parse_args()
    
    # Setup output directory
    output_dir = Path(args.output_dir) if args.output_dir else Path('validation_reports')
    if args.report_format in ['json', 'csv', 'all']:
        output_dir.mkdir(exist_ok=True)

    # Load schema
    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)

    try:
        schema_view = load_schema(schema_path)
        print(f"Loaded schema: {schema_view.schema.name}")

        # Initialize validators if requested
        enum_validator = None
        fk_validator = None

        if args.enum_validate:
            enum_validator = EnumValidator(schema_view)
            print(f"✓ Enum validation enabled")

        if args.fk_validate:
            if not args.tsv_dir:
                print(f"Error: --fk-validate requires --tsv-dir", file=sys.stderr)
                sys.exit(1)

            tsv_dir = Path(args.tsv_dir)
            if not tsv_dir.exists():
                print(f"Error: TSV directory not found: {tsv_dir}", file=sys.stderr)
                sys.exit(1)

            print(f"Building FK index from {tsv_dir}...")
            fk_index = build_fk_index_from_tsvs(tsv_dir)
            fk_validator = ForeignKeyValidator(fk_index)
            print(f"✓ FK validation enabled ({len(fk_index)} entity types indexed)")

        print(f"Using linkml-validate for comprehensive validation")
    except Exception as e:
        print(f"Error loading schema: {e}", file=sys.stderr)
        sys.exit(1)

    # Track validation results
    total_errors = 0
    files_with_errors = []
    files_validated = 0
    all_file_results = []
    
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

            # Initialize file validation result
            file_result = FileValidationResult(
                filename=tsv_path.name,
                total_records=len(mapped_data)
            )

            # Enhanced validations
            # Use a dict to merge results by line number
            record_results_dict = {}

            # 1. Enum validation
            if enum_validator:
                print(f"  🔍 Validating enums...")
                enum_results = validate_enums_in_data(mapped_data, class_name, schema_view, enum_validator)

                # Add to dict
                for result in enum_results:
                    record_results_dict[result.record_line] = result

                # Count enum issues
                enum_errors = sum(1 for r in enum_results if r.error_count > 0)
                enum_warnings = sum(1 for r in enum_results if r.warning_count > 0)
                if enum_errors > 0:
                    print(f"    ⚠️  Found {enum_errors} records with enum errors")
                if enum_warnings > 0:
                    print(f"    ⚠️  Found {enum_warnings} records with enum warnings")

            # 2. FK validation
            if fk_validator:
                print(f"  🔗 Validating foreign keys...")
                fk_results = validate_foreign_keys_in_data(mapped_data, class_name, schema_view, fk_validator)

                # Merge FK results with existing results
                for line_num, fk_result in fk_results.items():
                    if line_num in record_results_dict:
                        # Extend existing result
                        record_results_dict[line_num].results.extend(fk_result.results)
                    else:
                        # Add new result
                        record_results_dict[line_num] = fk_result

                # Count FK issues
                fk_errors = sum(1 for r in fk_results.values() if r.error_count > 0)
                fk_warnings = sum(1 for r in fk_results.values() if r.warning_count > 0)
                if fk_errors > 0:
                    print(f"    ⚠️  Found {fk_errors} records with FK errors")
                if fk_warnings > 0:
                    print(f"    ⚠️  Found {fk_warnings} records with FK warnings")

            # Convert dict to sorted list
            all_record_results = [record_results_dict[line] for line in sorted(record_results_dict.keys())]

            # 3. Quality metrics
            if args.quality_metrics:
                print(f"  📊 Collecting quality metrics...")
                metrics = collect_quality_metrics(mapped_data, class_name)
                file_result.quality_metrics = metrics

            # Store record results
            file_result.record_results = all_record_results

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

            # Add to results collection
            all_file_results.append(file_result)

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

    # Enhanced summary for enum/FK/quality
    if enum_validator or fk_validator or args.quality_metrics:
        print(f"\n📋 Enhanced Validation Results:")
        total_enum_errors = sum(sum(1 for r in fr.record_results if r.error_count > 0) for fr in all_file_results)
        total_enum_warnings = sum(sum(1 for r in fr.record_results if r.warning_count > 0) for fr in all_file_results)

        if enum_validator:
            print(f"  Enum validation:")
            print(f"    - Records with errors: {total_enum_errors}")
            print(f"    - Records with warnings: {total_enum_warnings}")

        if fk_validator:
            print(f"  Foreign key validation: enabled")

        if args.quality_metrics:
            print(f"  Quality metrics: collected for {len(all_file_results)} files")

    if files_with_errors:
        print(f"\n❌ Files with validation errors:")
        for filename in files_with_errors:
            print(f"  - {filename}")

    # Export results in requested formats
    if all_file_results and args.report_format != 'console':
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if args.report_format in ['json', 'all']:
            json_path = output_dir / f'validation_report_{timestamp}.json'
            export_results_json(all_file_results, json_path)

        if args.report_format in ['csv', 'all']:
            csv_path = output_dir / f'validation_report_{timestamp}.csv'
            export_results_csv(all_file_results, csv_path)

    if total_errors == 0:
        print("\n🎉 All files validated successfully with linkml-validate!")
        sys.exit(0)
    else:
        print(f"\n⚠️  Validation completed with {total_errors} errors")
        sys.exit(1)


if __name__ == "__main__":
    main()