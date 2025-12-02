#!/usr/bin/env python3
"""
OBO file parser for extracting microtypes and ontology terms.

This parser reads OBO-format ontology files and extracts microtype definitions
for use in LinkML schema generation.
"""

from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field


@dataclass
class OBOTerm:
    """Represents a single term from an OBO ontology file."""

    id: str
    name: str
    namespace: Optional[str] = None
    definition: Optional[str] = None
    is_a: List[str] = field(default_factory=list)
    property_values: Dict[str, str] = field(default_factory=dict)
    xrefs: List[str] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)

    @property
    def data_type(self) -> Optional[str]:
        """Get the data_type property value."""
        return self.property_values.get('data_type')

    @property
    def is_microtype(self) -> bool:
        """Check if this term is marked as a microtype."""
        return self.property_values.get('is_microtype', '').lower() == 'true'

    @property
    def is_hidden(self) -> bool:
        """Check if this term is hidden."""
        return self.property_values.get('is_hidden', '').lower() == 'true'

    @property
    def valid_units_parent(self) -> Optional[str]:
        """Get the valid_units_parent property value."""
        return self.property_values.get('valid_units_parent')

    @property
    def valid_units(self) -> Optional[str]:
        """Get the valid_units property value."""
        return self.property_values.get('valid_units')

    def get_children(self, all_terms: Dict[str, 'OBOTerm']) -> List['OBOTerm']:
        """Get all direct children of this term."""
        children = []
        for term in all_terms.values():
            if self.id in term.is_a:
                children.append(term)
        return children


class OBOParser:
    """Parser for OBO format ontology files."""

    def __init__(self, obo_file: str):
        """
        Initialize the OBO parser.

        Args:
            obo_file: Path to the OBO file to parse
        """
        self.obo_file = Path(obo_file)
        self.terms: Dict[str, OBOTerm] = {}
        self.ontology_id: Optional[str] = None
        self.format_version: Optional[str] = None

    def parse(self) -> Dict[str, OBOTerm]:
        """
        Parse the OBO file and return all terms.

        Returns:
            Dictionary mapping term IDs to OBOTerm objects
        """
        with open(self.obo_file, 'r') as f:
            lines = f.readlines()

        current_term = None
        in_header = True

        for line in lines:
            line = line.rstrip()

            # Skip empty lines
            if not line:
                continue

            # Parse header section
            if in_header:
                if line.startswith('[Term]'):
                    in_header = False
                    current_term = OBOTerm(id='', name='')
                elif line.startswith('format-version:'):
                    self.format_version = line.split(':', 1)[1].strip()
                elif line.startswith('ontology:'):
                    self.ontology_id = line.split(':', 1)[1].strip()
                continue

            # Start new term
            if line.startswith('[Term]'):
                if current_term and current_term.id:
                    self.terms[current_term.id] = current_term
                current_term = OBOTerm(id='', name='')
                continue

            # Skip other stanzas
            if line.startswith('['):
                current_term = None
                continue

            if current_term is None:
                continue

            # Parse term fields
            if ':' not in line:
                continue

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            if key == 'id':
                current_term.id = value
            elif key == 'name':
                current_term.name = value
            elif key == 'namespace':
                current_term.namespace = value
            elif key == 'def':
                # Remove quotes and trailing metadata
                if value.startswith('"'):
                    end_quote = value.find('"', 1)
                    if end_quote > 0:
                        current_term.definition = value[1:end_quote]
                    else:
                        current_term.definition = value[1:]
                else:
                    current_term.definition = value
            elif key == 'is_a':
                # Extract just the term ID, ignore comment
                parent = value.split('!')[0].strip()
                current_term.is_a.append(parent)
            elif key == 'property_value':
                # Parse property_value: name "value" xsd:type
                parts = value.split('"')
                if len(parts) >= 3:
                    prop_name = parts[0].strip()
                    prop_value = parts[1]
                    current_term.property_values[prop_name] = prop_value
            elif key == 'xref':
                current_term.xrefs.append(value)
            elif key == 'comment':
                current_term.comments.append(value)

        # Add last term
        if current_term and current_term.id:
            self.terms[current_term.id] = current_term

        return self.terms

    def get_microtypes(self) -> Dict[str, OBOTerm]:
        """
        Get all terms marked as microtypes.

        Returns:
            Dictionary mapping term IDs to microtype OBOTerm objects
        """
        return {
            term_id: term
            for term_id, term in self.terms.items()
            if term.is_microtype
        }

    def get_microtypes_by_data_type(self, data_type: str) -> Dict[str, OBOTerm]:
        """
        Get all microtypes with a specific data_type.

        Args:
            data_type: The data type to filter by (e.g., 'oterm_ref', 'string', 'int')

        Returns:
            Dictionary mapping term IDs to matching microtype OBOTerm objects
        """
        microtypes = self.get_microtypes()
        return {
            term_id: term
            for term_id, term in microtypes.items()
            if term.data_type == data_type
        }

    def get_enum_microtypes(self) -> Dict[str, OBOTerm]:
        """
        Get all microtypes that should be represented as enums (data_type='oterm_ref').

        Returns:
            Dictionary mapping term IDs to enum microtype OBOTerm objects
        """
        return self.get_microtypes_by_data_type('oterm_ref')

    def get_term_hierarchy(self, term_id: str) -> List[str]:
        """
        Get the full hierarchy path from root to the specified term.

        Args:
            term_id: The term ID to get hierarchy for

        Returns:
            List of term IDs from root to term
        """
        if term_id not in self.terms:
            return []

        path = [term_id]
        current = self.terms[term_id]

        while current.is_a:
            # Take first parent (assuming single inheritance for simplicity)
            parent_id = current.is_a[0]
            if parent_id in path:  # Avoid cycles
                break
            path.insert(0, parent_id)
            if parent_id not in self.terms:
                break
            current = self.terms[parent_id]

        return path

    def get_all_descendants(self, term_id: str) -> Set[str]:
        """
        Get all descendant term IDs (recursive).

        Args:
            term_id: The parent term ID

        Returns:
            Set of descendant term IDs
        """
        if term_id not in self.terms:
            return set()

        descendants = set()
        term = self.terms[term_id]
        children = term.get_children(self.terms)

        for child in children:
            descendants.add(child.id)
            descendants.update(self.get_all_descendants(child.id))

        return descendants

    def find_terms_by_name(self, name: str, case_sensitive: bool = False) -> List[OBOTerm]:
        """
        Find terms by name (exact match or substring).

        Args:
            name: Name to search for
            case_sensitive: Whether to perform case-sensitive search

        Returns:
            List of matching OBOTerm objects
        """
        if not case_sensitive:
            name = name.lower()

        results = []
        for term in self.terms.values():
            term_name = term.name if case_sensitive else term.name.lower()
            if name in term_name:
                results.append(term)

        return results


def main():
    """Example usage of the OBO parser."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python obo_parser.py <obo_file>")
        sys.exit(1)

    parser = OBOParser(sys.argv[1])
    terms = parser.parse()

    print(f"Parsed {len(terms)} terms from {parser.obo_file}")
    print(f"Ontology ID: {parser.ontology_id}")
    print(f"Format version: {parser.format_version}")

    microtypes = parser.get_microtypes()
    print(f"\nFound {len(microtypes)} microtypes")

    enum_types = parser.get_enum_microtypes()
    print(f"Found {len(enum_types)} enum microtypes (oterm_ref)")

    # Show a few examples
    print("\nExample microtypes:")
    for i, (term_id, term) in enumerate(microtypes.items()):
        if i >= 5:
            break
        print(f"  {term_id}: {term.name} (data_type={term.data_type})")

    print("\nExample enum microtypes:")
    for i, (term_id, term) in enumerate(enum_types.items()):
        if i >= 5:
            break
        children = term.get_children(terms)
        print(f"  {term_id}: {term.name} ({len(children)} children)")


if __name__ == '__main__':
    main()
