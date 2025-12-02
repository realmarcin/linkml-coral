#!/usr/bin/env python3
"""
Update LinkML schema with microtypes, semantic types, and generated enums.

This script updates the CORAL LinkML schema to integrate:
1. Semantic type definitions based on common microtype patterns
2. Auto-generated enums from OBO file
3. Updated slot definitions with proper ranges and microtype annotations
4. Converted foreign keys to use proper object references
"""

import yaml
from pathlib import Path
from typing import Dict, Any
from src.linkml_coral.utils.obo_parser import OBOParser


# Semantic types to add (based on common microtype patterns)
SEMANTIC_TYPES = {
    'Date': {
        'typeof': 'string',
        'pattern': r'\d\d\d\d(-\d\d(-\d\d)?)?',
        'description': 'Date in YYYY-MM-DD format',
        'annotations': {
            'microtype': {'tag': 'microtype', 'value': 'ME:0000009'},
            'microtype_data_type': {'tag': 'microtype_data_type', 'value': 'string'}
        }
    },
    'Time': {
        'typeof': 'string',
        'pattern': r'\d(\d)?(:\d\d(:\d\d)?)?\s*([apAP][mM])?',
        'description': 'Time in HH:MM:SS format',
        'annotations': {
            'microtype': {'tag': 'microtype', 'value': 'ME:0000010'},
            'microtype_data_type': {'tag': 'microtype_data_type', 'value': 'string'}
        }
    },
    'Link': {
        'typeof': 'string',
        'pattern': r'http.*',
        'description': 'HTTP/HTTPS URL',
        'annotations': {
            'microtype': {'tag': 'microtype', 'value': 'ME:0000203'},
            'microtype_data_type': {'tag': 'microtype_data_type', 'value': 'string'}
        }
    },
    'Latitude': {
        'typeof': 'float',
        'minimum_value': -90,
        'maximum_value': 90,
        'description': 'Geographic latitude in decimal degrees',
        'annotations': {
            'microtype': {'tag': 'microtype', 'value': 'ME:0000211'},
            'microtype_data_type': {'tag': 'microtype_data_type', 'value': 'float'},
            'units_term': {'tag': 'units_term', 'value': 'UO:0000185'}
        }
    },
    'Longitude': {
        'typeof': 'float',
        'minimum_value': -180,
        'maximum_value': 180,
        'description': 'Geographic longitude in decimal degrees',
        'annotations': {
            'microtype': {'tag': 'microtype', 'value': 'ME:0000212'},
            'microtype_data_type': {'tag': 'microtype_data_type', 'value': 'float'},
            'units_term': {'tag': 'units_term', 'value': 'UO:0000185'}
        }
    },
    'Count': {
        'typeof': 'integer',
        'minimum_value': 0,
        'description': 'Non-negative integer count',
        'annotations': {
            'microtype': {'tag': 'microtype', 'value': 'ME:0000126'},
            'microtype_data_type': {'tag': 'microtype_data_type', 'value': 'int'},
            'units_term': {'tag': 'units_term', 'value': 'UO:0000189'}
        }
    },
    'Size': {
        'typeof': 'float',
        'minimum_value': 0,
        'description': 'Size measurement (non-negative)',
        'annotations': {
            'microtype': {'tag': 'microtype', 'value': 'ME:0000128'},
            'microtype_data_type': {'tag': 'microtype_data_type', 'value': 'float'}
        }
    },
    'Depth': {
        'typeof': 'float',
        'description': 'Depth measurement',
        'annotations': {
            'microtype': {'tag': 'microtype', 'value': 'ME:0000219'},
            'microtype_data_type': {'tag': 'microtype_data_type', 'value': 'float'},
            'units_term': {'tag': 'units_term', 'value': 'UO:0000008'}
        }
    },
    'Elevation': {
        'typeof': 'float',
        'description': 'Elevation measurement',
        'annotations': {
            'microtype': {'tag': 'microtype', 'value': 'ME:0000220'},
            'microtype_data_type': {'tag': 'microtype_data_type', 'value': 'float'},
            'units_term': {'tag': 'units_term', 'value': 'UO:0000008'}
        }
    },
    'Rate': {
        'typeof': 'float',
        'minimum_value': 0,
        'maximum_value': 1,
        'description': 'Rate as a fraction between 0 and 1',
        'annotations': {
            'microtype': {'tag': 'microtype', 'value': 'ME:0000264'},
            'microtype_data_type': {'tag': 'microtype_data_type', 'value': 'float'}
        }
    }
}

# Mapping of slot names to semantic types (based on common patterns)
SLOT_TO_SEMANTIC_TYPE = {
    # Date/Time fields
    'date': 'Date',
    'date_start': 'Date',
    'date_end': 'Date',
    'time': 'Time',
    'timezone': 'string',  # Keep as string (complex format)

    # Geographic coordinates
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'depth': 'Depth',
    'elevation': 'Elevation',

    # Links/URLs
    'link': 'Link',

    # Counts
    'read_count': 'Count',
    'n_contigs': 'Count',
    'n_features': 'Count',
    'n_fragments': 'Count',

    # Size
    'size': 'Size',

    # Rates
    'hit_rate': 'Rate',
}

# Mapping of slot names to enums (based on microtype analysis)
SLOT_TO_ENUM = {
    'read_type': 'ReadTypeEnum',
    'sequencing_technology': 'SequencingTechnologyEnum',
    'strand': 'StrandEnum',
    'community_type': 'CommunityTypeEnum',
}

# Foreign key mappings (field name -> target class)
FOREIGN_KEY_MAPPINGS = {
    'location': 'Location',
    'taxon': 'Taxon',
    'strain': 'Strain',
    'genome': 'Genome',
    'assembly': 'Assembly',
    'protocol': 'Protocol',
    'condition': 'Condition',
    'parent_community': 'Community',
    'sample': 'Sample',
}


def load_schema(schema_file: str) -> Dict[str, Any]:
    """Load the current LinkML schema."""
    with open(schema_file, 'r') as f:
        return yaml.safe_load(f)


def load_generated_enums(enums_file: str) -> Dict[str, Any]:
    """Load the generated enums from file."""
    with open(enums_file, 'r') as f:
        data = yaml.safe_load(f)
        return data.get('enums', {})


def update_slot_with_semantic_type(slot_name: str, slot_def: Dict[str, Any]) -> Dict[str, Any]:
    """Update a slot definition to use semantic types where appropriate."""
    # Extract the base field name (without class prefix)
    if '_' in slot_name:
        field_name = '_'.join(slot_name.split('_')[1:])
    else:
        field_name = slot_name

    # Check if this field should use a semantic type
    for pattern, sem_type in SLOT_TO_SEMANTIC_TYPE.items():
        if pattern in field_name:
            slot_def['range'] = sem_type
            # Remove pattern if it exists (now in the type definition)
            if 'pattern' in slot_def:
                del slot_def['pattern']
            break

    return slot_def


def update_slot_with_enum(slot_name: str, slot_def: Dict[str, Any]) -> Dict[str, Any]:
    """Update a slot definition to use enums where appropriate."""
    # Extract the base field name
    if '_' in slot_name:
        field_name = '_'.join(slot_name.split('_')[1:])
    else:
        field_name = slot_name

    # Check if this field should use an enum
    for pattern, enum_name in SLOT_TO_ENUM.items():
        if pattern in field_name:
            slot_def['range'] = enum_name
            # Remove constraint annotation (now in enum definition)
            if 'annotations' in slot_def and 'constraint' in slot_def['annotations']:
                del slot_def['annotations']['constraint']
            break

    return slot_def


def update_slot_with_fk_range(slot_name: str, slot_def: Dict[str, Any]) -> Dict[str, Any]:
    """Update a slot definition to use proper object references for foreign keys."""
    # Check if slot has foreign_key annotation
    if 'annotations' not in slot_def:
        return slot_def

    annotations = slot_def['annotations']
    if 'foreign_key' not in annotations:
        return slot_def

    # Extract FK info
    fk_value = annotations['foreign_key'].get('value', '')
    if '.' in fk_value:
        target_class = fk_value.split('.')[0]

        # Update range to target class
        slot_def['range'] = target_class

        # Keep FK annotation for documentation but also use proper range
        # Don't delete the annotation - it provides useful context

    return slot_def


def add_microtype_annotation(slot_name: str, slot_def: Dict[str, Any], obo_parser: OBOParser) -> Dict[str, Any]:
    """Add microtype annotation to a slot if type_term is present."""
    if 'annotations' not in slot_def:
        return slot_def

    annotations = slot_def['annotations']
    if 'type_term' not in annotations:
        return slot_def

    # Get the ME: term
    type_term = annotations['type_term'].get('value', '')
    if not type_term.startswith('ME:'):
        return slot_def

    # Look up the term in OBO
    if type_term in obo_parser.terms:
        term = obo_parser.terms[type_term]

        # Add microtype annotation
        if 'microtype' not in annotations:
            annotations['microtype'] = {
                'tag': 'microtype',
                'value': type_term
            }

        # Add microtype_data_type if available
        if term.data_type and 'microtype_data_type' not in annotations:
            annotations['microtype_data_type'] = {
                'tag': 'microtype_data_type',
                'value': term.data_type
            }

    return slot_def


def update_schema(
    schema_file: str,
    enums_file: str,
    obo_file: str,
    output_file: str = None
):
    """
    Update the schema with semantic types, enums, and microtype annotations.

    Args:
        schema_file: Path to current LinkML schema
        enums_file: Path to generated enums YAML
        obo_file: Path to OBO ontology file
        output_file: Optional output file (defaults to updating schema_file)
    """
    print(f"Loading schema from {schema_file}")
    schema = load_schema(schema_file)

    print(f"Loading generated enums from {enums_file}")
    enums = load_generated_enums(enums_file)

    print(f"Parsing OBO file {obo_file}")
    obo_parser = OBOParser(obo_file)
    obo_parser.parse()

    # Add semantic types
    print(f"\nAdding {len(SEMANTIC_TYPES)} semantic types...")
    schema['types'] = SEMANTIC_TYPES

    # Add enums
    print(f"Adding {len(enums)} enum definitions...")
    schema['enums'] = enums

    # Update slots
    if 'slots' in schema:
        print(f"\nUpdating {len(schema['slots'])} slot definitions...")
        updated_count = 0

        for slot_name, slot_def in schema['slots'].items():
            original = str(slot_def)

            # Apply updates
            slot_def = update_slot_with_semantic_type(slot_name, slot_def)
            slot_def = update_slot_with_enum(slot_name, slot_def)
            slot_def = update_slot_with_fk_range(slot_name, slot_def)
            slot_def = add_microtype_annotation(slot_name, slot_def, obo_parser)

            if str(slot_def) != original:
                updated_count += 1

        print(f"  Updated {updated_count} slots")

    # Write output
    output_path = output_file or schema_file
    print(f"\nWriting updated schema to {output_path}")

    with open(output_path, 'w') as f:
        yaml.dump(schema, f, default_flow_style=False, sort_keys=False, width=120, allow_unicode=True)

    print("\nSchema update complete!")
    print(f"  Semantic types added: {len(SEMANTIC_TYPES)}")
    print(f"  Enums added: {len(enums)}")
    print(f"  Slots updated: {updated_count}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Update LinkML schema with microtypes and enums"
    )
    parser.add_argument(
        '--schema',
        default='src/linkml_coral/schema/linkml_coral.yaml',
        help='Path to LinkML schema file'
    )
    parser.add_argument(
        '--enums',
        default='generated_enums.yaml',
        help='Path to generated enums file'
    )
    parser.add_argument(
        '--obo',
        default='CORAL/example/enigma/ontologies/context_measurement_ontology.obo',
        help='Path to OBO file'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output file (default: update schema in place)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform dry run without writing changes'
    )

    args = parser.parse_args()

    if args.dry_run:
        args.output = 'schema_updated_dry_run.yaml'
        print("DRY RUN MODE - Changes will be written to", args.output)

    update_schema(
        schema_file=args.schema,
        enums_file=args.enums,
        obo_file=args.obo,
        output_file=args.output
    )


if __name__ == '__main__':
    main()
