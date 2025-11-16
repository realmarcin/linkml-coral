#!/usr/bin/env python3
"""
Generate LinkML enum definitions from OBO microtype ontology.

This script parses the context_measurement_ontology.obo file and generates
LinkML enum definitions for all oterm_ref type microtypes that have child terms.
"""

import yaml
from pathlib import Path
from typing import Dict, List
from src.linkml_coral.utils.obo_parser import OBOParser, OBOTerm


def sanitize_enum_name(name: str) -> str:
    """
    Convert a term name to a valid LinkML enum name.

    Args:
        name: The original term name

    Returns:
        Sanitized enum name (PascalCase + Enum suffix)
    """
    # Remove special characters and convert to PascalCase
    words = name.replace('-', ' ').replace('/', ' ').split()
    pascal = ''.join(word.capitalize() for word in words)

    # Add Enum suffix if not already present
    if not pascal.endswith('Enum'):
        pascal += 'Enum'

    return pascal


def sanitize_permissible_value(name: str) -> str:
    """
    Convert a term name to a valid permissible value key.

    Args:
        name: The original term name

    Returns:
        Sanitized value key (snake_case)
    """
    # Convert to lowercase and replace spaces/special chars with underscores
    key = name.lower()
    key = key.replace(' ', '_').replace('-', '_').replace('/', '_')
    key = key.replace('(', '').replace(')', '')
    key = key.replace('__', '_').strip('_')

    # Handle special cases for symbols
    if key == '+':
        return 'forward'
    elif key == '-':
        return 'reverse_complement'

    return key


def should_generate_enum(term: OBOTerm, all_terms: Dict[str, OBOTerm]) -> bool:
    """
    Determine if a term should have an enum generated.

    Args:
        term: The microtype term to check
        all_terms: All terms in the ontology

    Returns:
        True if enum should be generated
    """
    # Must be oterm_ref type
    if term.data_type != 'oterm_ref':
        return False

    # Must not be hidden
    if term.is_hidden:
        return False

    # Must have at least one child term
    children = term.get_children(all_terms)
    if not children:
        return False

    return True


def generate_enum_definition(
    term: OBOTerm,
    all_terms: Dict[str, OBOTerm],
    include_hierarchy: bool = False
) -> Dict:
    """
    Generate a LinkML enum definition for a microtype term.

    Args:
        term: The parent term defining the enum
        all_terms: All terms in the ontology
        include_hierarchy: Whether to include full hierarchy or just direct children

    Returns:
        LinkML enum definition as a dictionary
    """
    enum_name = sanitize_enum_name(term.name)
    children = term.get_children(all_terms)

    # Sort children by ID for consistent ordering
    children.sort(key=lambda t: t.id)

    enum_def = {
        'description': term.definition or f"{term.name} enumeration",
        'annotations': {
            'microtype': {
                'tag': 'microtype',
                'value': term.id
            },
            'microtype_data_type': {
                'tag': 'microtype_data_type',
                'value': 'oterm_ref'
            }
        }
    }

    # Generate permissible values from children
    permissible_values = {}
    for child in children:
        key = sanitize_permissible_value(child.name)
        value_def = {}

        # Use original name as title if it differs from key
        if key != child.name:
            value_def['title'] = child.name

        # Add description if available
        if child.definition:
            value_def['description'] = child.definition

        # Add term annotation
        value_def['annotations'] = {
            'term': {
                'tag': 'term',
                'value': child.id
            }
        }

        permissible_values[key] = value_def

    enum_def['permissible_values'] = permissible_values

    return {enum_name: enum_def}


def generate_all_enums(obo_file: str, output_file: str = None, verbose: bool = False):
    """
    Generate all enum definitions from OBO file.

    Args:
        obo_file: Path to the OBO file
        output_file: Optional path to write YAML output
        verbose: Whether to print verbose output
    """
    print(f"Parsing OBO file: {obo_file}")
    parser = OBOParser(obo_file)
    terms = parser.parse()

    print(f"Found {len(terms)} terms")

    # Get all enum microtypes
    enum_microtypes = parser.get_enum_microtypes()
    print(f"Found {len(enum_microtypes)} oterm_ref microtypes")

    # Filter to those that should have enums generated
    enums_to_generate = {
        term_id: term
        for term_id, term in enum_microtypes.items()
        if should_generate_enum(term, terms)
    }

    print(f"Generating enums for {len(enums_to_generate)} microtypes")

    # Generate all enums
    all_enums = {}
    for term_id, term in enums_to_generate.items():
        if verbose:
            children = term.get_children(terms)
            print(f"  Generating {sanitize_enum_name(term.name)} ({len(children)} values)")

        enum_def = generate_enum_definition(term, terms)
        all_enums.update(enum_def)

    # Create the enums section
    enums_section = {'enums': all_enums}

    # Print or write output
    yaml_output = yaml.dump(
        enums_section,
        default_flow_style=False,
        sort_keys=False,
        width=120,
        allow_unicode=True
    )

    if output_file:
        output_path = Path(output_file)
        output_path.write_text(yaml_output)
        print(f"\nWrote {len(all_enums)} enum definitions to {output_file}")
    else:
        print("\n" + "="*80)
        print(yaml_output)
        print("="*80)

    # Print summary
    print(f"\nSummary:")
    print(f"  Total enums generated: {len(all_enums)}")

    if verbose:
        print("\nGenerated enums:")
        for enum_name in sorted(all_enums.keys()):
            num_values = len(all_enums[enum_name]['permissible_values'])
            print(f"  - {enum_name} ({num_values} values)")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate LinkML enums from OBO microtype ontology"
    )
    parser.add_argument(
        '--obo',
        default='CORAL/example/enigma/ontologies/context_measurement_ontology.obo',
        help='Path to OBO file (default: CORAL submodule)'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output YAML file (default: print to stdout)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    generate_all_enums(args.obo, args.output, args.verbose)


if __name__ == '__main__':
    main()
