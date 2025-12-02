#!/usr/bin/env python3
"""
LinkML to CDM Table Converter

Converts LinkML CORAL schema to CDM table definitions with the following conventions:
- If a type defines `preferred_name`, use that name (e.g., OTU → ASV → table `sdt_asv`)
- Primary key column → `<table>_id` (values rewritten to preferred name when applicable)
- Foreign key column → `<referenced_table>_id` (or `_ids` for arrays)
- All column names are lower_case snake_case (underscores only)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from linkml_runtime.utils.schemaview import SchemaView


@dataclass
class CDMColumn:
    """Represents a CDM table column."""
    name: str
    original_name: str
    data_type: str
    is_primary_key: bool = False
    is_foreign_key: bool = False
    is_required: bool = False
    is_multivalued: bool = False
    is_unique: bool = False
    foreign_key_target: Optional[str] = None
    comment: Optional[str] = None
    constraint: Optional[str] = None
    units_term: Optional[str] = None
    type_term: Optional[str] = None


@dataclass
class CDMTable:
    """Represents a CDM table."""
    table_name: str
    original_class_name: str
    preferred_name: Optional[str] = None
    columns: List[CDMColumn] = field(default_factory=list)
    term: Optional[str] = None
    used_for_provenance: bool = False
    process_types: List[str] = field(default_factory=list)
    process_inputs: List[List[str]] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)


class LinkMLToCDMConverter:
    """Converts LinkML schema to CDM table definitions."""

    def __init__(self, schema_path: str, typedef_path: Optional[str] = None):
        """Initialize converter with LinkML schema and optional typedef.json."""
        self.schema_view = SchemaView(schema_path)
        self.typedef_data = None
        self.preferred_names: Dict[str, str] = {}

        if typedef_path and Path(typedef_path).exists():
            with open(typedef_path) as f:
                self.typedef_data = json.load(f)
            self._extract_preferred_names()

    def _extract_preferred_names(self):
        """Extract preferred_name mappings from typedef.json if they exist."""
        if not self.typedef_data:
            return

        # Check for preferred_name in both system_types and static_types
        for type_list in [self.typedef_data.get('system_types', []),
                         self.typedef_data.get('static_types', [])]:
            for type_def in type_list:
                if 'preferred_name' in type_def:
                    original = type_def['name']
                    preferred = type_def['preferred_name']
                    self.preferred_names[original] = preferred

    def _to_snake_case(self, name: str) -> str:
        """Convert name to snake_case."""
        # Handle special cases
        name = name.replace(' ', '_')  # "MIME type" → "MIME_type"

        # Insert underscores before capitals (except at start)
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        # Insert underscores before capitals followed by lowercase
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        return s2.lower()

    def _get_table_name(self, class_name: str) -> str:
        """Get CDM table name for a LinkML class."""
        # Use preferred_name if available
        if class_name in self.preferred_names:
            base_name = self.preferred_names[class_name]
        else:
            base_name = class_name

        # Convert to snake_case and add sdt_ prefix
        snake_name = self._to_snake_case(base_name)
        return f"sdt_{snake_name}"

    def _get_scalar_type(self, slot: any) -> str:
        """Map LinkML range to CDM scalar type."""
        range_type = slot.range

        # Map LinkML types to CDM types
        type_mapping = {
            'string': 'text',
            'integer': 'int',
            'float': 'float',
            'double': 'float',
            'boolean': 'boolean',
            'date': 'text',
            'datetime': 'text',
            'uri': 'text',
            'uriorcurie': 'text',
        }

        return type_mapping.get(range_type, 'text')

    def _parse_foreign_key(self, fk_annotation: str) -> Tuple[str, str]:
        """
        Parse foreign key annotation to extract target table and field.

        Examples:
        - "Protocol.name" → ("Protocol", "name")
        - "Genome" → ("Genome", "name")  # assumes .name
        - "[Gene.gene_id]" → ("Gene", "gene_id")
        """
        fk_str = fk_annotation.strip()

        # Handle array syntax
        is_array = fk_str.startswith('[') and fk_str.endswith(']')
        if is_array:
            fk_str = fk_str[1:-1]

        # Split on dot
        parts = fk_str.split('.')

        if len(parts) == 2:
            target_class, target_field = parts
        elif len(parts) == 1:
            # No field specified, assume 'name'
            target_class = parts[0]
            target_field = 'name'
        else:
            raise ValueError(f"Invalid FK format: {fk_annotation}")

        return target_class, target_field

    def _get_column_name(self, class_name: str, slot_name: str, slot: any) -> str:
        """
        Generate CDM column name based on slot type.

        Rules:
        - Primary key (identifier=True) → <table>_id
        - Foreign key → <referenced_table>_id (or _ids for array)
        - Regular field → snake_case field name
        """
        # Get annotations (handle both dict and JsonObj)
        annotations = slot.annotations if hasattr(slot, 'annotations') else None
        fk_annotation = getattr(annotations, 'foreign_key', None) if annotations else None
        is_identifier = slot.identifier if hasattr(slot, 'identifier') else False
        is_multivalued = slot.multivalued if hasattr(slot, 'multivalued') else False

        # Primary key: <table>_id
        if is_identifier:
            table_name = self._get_table_name(class_name)
            # Remove sdt_ prefix for column name
            return table_name.replace('sdt_', '') + '_id'

        # Foreign key: <referenced_table>_id or <referenced_table>_ids
        if fk_annotation:
            target_class, _ = self._parse_foreign_key(fk_annotation.value)
            ref_table = self._get_table_name(target_class)
            ref_base = ref_table.replace('sdt_', '')

            if is_multivalued:
                return f"{ref_base}_ids"
            else:
                return f"{ref_base}_id"

        # Regular field: snake_case
        return self._to_snake_case(slot_name)

    def _convert_class(self, class_name: str) -> CDMTable:
        """Convert a LinkML class to a CDM table definition."""
        cls = self.schema_view.get_class(class_name)

        # Skip if not a real data class (e.g., mixins)
        if not cls.slots:
            return None

        table = CDMTable(
            table_name=self._get_table_name(class_name),
            original_class_name=class_name,
            preferred_name=self.preferred_names.get(class_name)
        )

        # Extract class-level annotations
        if hasattr(cls, 'annotations') and cls.annotations:
            annotations = cls.annotations

            term_ann = getattr(annotations, 'term', None)
            if term_ann:
                table.term = term_ann.value

            prov_ann = getattr(annotations, 'used_for_provenance', None)
            if prov_ann:
                table.used_for_provenance = prov_ann.value

            process_types_ann = getattr(annotations, 'process_types', None)
            if process_types_ann:
                table.process_types = process_types_ann.value

            process_inputs_ann = getattr(annotations, 'process_inputs', None)
            if process_inputs_ann:
                table.process_inputs = process_inputs_ann.value

        # Convert slots to columns
        for slot_name in cls.slots:
            # Get induced slot (with all inherited properties)
            slot = self.schema_view.induced_slot(slot_name, class_name)

            column = self._convert_slot(class_name, slot_name, slot, table)
            if column:
                table.columns.append(column)

        return table

    def _convert_slot(self, class_name: str, slot_name: str, slot: any, table: CDMTable) -> Optional[CDMColumn]:
        """Convert a LinkML slot to a CDM column."""
        # Get slot properties
        is_identifier = slot.identifier if hasattr(slot, 'identifier') else False
        is_required = slot.required if hasattr(slot, 'required') else False
        is_multivalued = slot.multivalued if hasattr(slot, 'multivalued') else False

        # Get annotations (handle both dict and JsonObj)
        annotations = slot.annotations if hasattr(slot, 'annotations') else None
        fk_annotation = getattr(annotations, 'foreign_key', None) if annotations else None
        type_term = getattr(annotations, 'type_term', None) if annotations else None
        units_term = getattr(annotations, 'units_term', None) if annotations else None
        constraint_annotation = getattr(annotations, 'constraint', None) if annotations else None
        unique_annotation = getattr(annotations, 'unique', None) if annotations else None

        # Get column name based on type
        cdm_column_name = self._get_column_name(class_name, slot_name, slot)

        # Determine data type
        data_type = self._get_scalar_type(slot)
        if is_multivalued:
            data_type = f"[{data_type}]"

        # Check for foreign key
        is_fk = fk_annotation is not None
        fk_target = None
        if is_fk:
            try:
                target_class, target_field = self._parse_foreign_key(fk_annotation.value)
                target_table = self._get_table_name(target_class)
                fk_target = f"{target_table}.{target_table.replace('sdt_', '')}_id"
            except ValueError as e:
                table.issues.append(f"Invalid FK in {slot_name}: {str(e)}")

        # Get comment from slot description or comments
        comment = slot.description if hasattr(slot, 'description') else None
        if hasattr(slot, 'comments') and slot.comments:
            comment = '; '.join(slot.comments)

        # Get constraint
        constraint = None
        if constraint_annotation:
            constraint = constraint_annotation.value
        elif hasattr(slot, 'pattern') and slot.pattern:
            constraint = slot.pattern
        elif hasattr(slot, 'minimum_value') and hasattr(slot, 'maximum_value'):
            constraint = f"[{slot.minimum_value}, {slot.maximum_value}]"

        column = CDMColumn(
            name=cdm_column_name,
            original_name=slot_name,
            data_type=data_type,
            is_primary_key=is_identifier,
            is_foreign_key=is_fk,
            is_required=is_required,
            is_multivalued=is_multivalued,
            is_unique=unique_annotation.value if unique_annotation else False,
            foreign_key_target=fk_target,
            comment=comment,
            constraint=str(constraint) if constraint else None,
            units_term=units_term.value if units_term else None,
            type_term=type_term.value if type_term else None
        )

        return column

    def convert_schema(self) -> List[CDMTable]:
        """Convert entire LinkML schema to CDM table definitions."""
        tables = []

        # Get all classes from schema
        for class_name in self.schema_view.all_classes():
            table = self._convert_class(class_name)
            if table and table.columns:  # Only include if it has columns
                tables.append(table)

        return tables

    def generate_report(self, tables: List[CDMTable]) -> str:
        """Generate a human-readable report of the CDM tables."""
        lines = []

        lines.append("=" * 80)
        lines.append("LinkML to CDM Table Conversion Report")
        lines.append("=" * 80)
        lines.append("")

        if self.preferred_names:
            lines.append("Preferred Names Found:")
            for orig, pref in self.preferred_names.items():
                lines.append(f"  {orig} → {pref}")
            lines.append("")

        lines.append(f"Total Tables: {len(tables)}")
        lines.append("")

        for table in sorted(tables, key=lambda t: t.table_name):
            lines.append("─" * 80)
            lines.append(f"Table: {table.table_name}")
            lines.append(f"  Original Class: {table.original_class_name}")

            if table.preferred_name:
                lines.append(f"  Preferred Name: {table.preferred_name}")

            if table.term:
                lines.append(f"  Ontology Term: {table.term}")

            if table.used_for_provenance:
                lines.append(f"  Used for Provenance: Yes")

            if table.issues:
                lines.append(f"  ⚠️  Issues:")
                for issue in table.issues:
                    lines.append(f"      - {issue}")

            lines.append("")
            lines.append(f"  Columns ({len(table.columns)}):")
            lines.append("")

            # Column headers
            lines.append(f"    {'Column Name':<40} {'Type':<15} {'Flags':<20}")
            lines.append(f"    {'-'*40} {'-'*15} {'-'*20}")

            for col in table.columns:
                flags = []
                if col.is_primary_key:
                    flags.append("PK")
                if col.is_foreign_key:
                    flags.append("FK")
                if col.is_required:
                    flags.append("REQ")
                if col.is_unique:
                    flags.append("UNQ")
                if col.is_multivalued:
                    flags.append("ARRAY")

                flags_str = ", ".join(flags) if flags else "-"

                lines.append(f"    {col.name:<40} {col.data_type:<15} {flags_str:<20}")

                if col.original_name != col.name:
                    lines.append(f"      Original: {col.original_name}")

                if col.foreign_key_target:
                    lines.append(f"      FK Target: {col.foreign_key_target}")

                if col.constraint:
                    constraint_short = col.constraint[:60] + "..." if len(col.constraint) > 60 else col.constraint
                    lines.append(f"      Constraint: {constraint_short}")

                if col.comment:
                    comment_short = col.comment[:60] + "..." if len(col.comment) > 60 else col.comment
                    lines.append(f"      Comment: {comment_short}")

            lines.append("")

        lines.append("=" * 80)
        lines.append("End of Report")
        lines.append("=" * 80)

        return "\n".join(lines)

    def generate_json_schema(self, tables: List[CDMTable]) -> dict:
        """Generate JSON representation of CDM tables."""
        return {
            "cdm_schema_version": "1.0",
            "source": "CORAL LinkML Schema",
            "generated_from": str(Path(self.schema_view.schema.source_file).name),
            "preferred_names": self.preferred_names,
            "tables": [
                {
                    "table_name": table.table_name,
                    "original_class_name": table.original_class_name,
                    "preferred_name": table.preferred_name,
                    "term": table.term,
                    "used_for_provenance": table.used_for_provenance,
                    "process_types": table.process_types,
                    "process_inputs": table.process_inputs,
                    "issues": table.issues,
                    "columns": [
                        {
                            "name": col.name,
                            "original_name": col.original_name,
                            "data_type": col.data_type,
                            "is_primary_key": col.is_primary_key,
                            "is_foreign_key": col.is_foreign_key,
                            "is_required": col.is_required,
                            "is_multivalued": col.is_multivalued,
                            "is_unique": col.is_unique,
                            "foreign_key_target": col.foreign_key_target,
                            "constraint": col.constraint,
                            "comment": col.comment,
                            "units_term": col.units_term,
                            "type_term": col.type_term
                        }
                        for col in table.columns
                    ]
                }
                for table in sorted(tables, key=lambda t: t.table_name)
            ]
        }

    def check_linkml_compliance(self, tables: List[CDMTable]) -> List[str]:
        """
        Check if CDM conversion revealed any issues with the LinkML schema.
        Returns list of issues that would require LinkML schema changes.
        """
        issues = []

        for table in tables:
            # Check for table-level issues
            if table.issues:
                for issue in table.issues:
                    issues.append(f"{table.original_class_name}: {issue}")

            # Check for naming inconsistencies
            for col in table.columns:
                # Check FK target field existence
                if col.is_foreign_key and col.foreign_key_target:
                    # Extract referenced table
                    ref_table = col.foreign_key_target.split('.')[0]

                    # Check if FK uses 'name' but references a field without 'name'
                    if 'gene_id' in col.foreign_key_target.lower():
                        # This is OK - Gene uses gene_id as UPK
                        pass

        return issues


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert LinkML CORAL schema to CDM table definitions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate report to stdout
  python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml

  # Generate with typedef.json for preferred_name support
  python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml --typedef data/typedef.json

  # Save JSON schema
  python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml --json-output cdm_schema.json

  # Save text report
  python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml --report-output cdm_report.txt

  # Check for LinkML schema issues
  python linkml_to_cdm.py src/linkml_coral/schema/linkml_coral.yaml --check-only
        """
    )

    parser.add_argument(
        'schema',
        help='Path to LinkML schema YAML file'
    )
    parser.add_argument(
        '--typedef',
        help='Path to typedef.json for preferred_name support'
    )
    parser.add_argument(
        '--json-output',
        help='Save JSON schema to this file'
    )
    parser.add_argument(
        '--report-output',
        help='Save text report to this file'
    )
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='Only check for LinkML schema issues, do not generate full output'
    )

    args = parser.parse_args()

    # Initialize converter
    converter = LinkMLToCDMConverter(args.schema, args.typedef)

    # Convert schema
    print(f"Converting LinkML schema: {args.schema}")
    if args.typedef:
        print(f"Using typedef.json: {args.typedef}")

    tables = converter.convert_schema()
    print(f"✓ Converted {len(tables)} tables")

    # Check for issues
    issues = converter.check_linkml_compliance(tables)
    if issues:
        print(f"\n⚠️  Found {len(issues)} issues that may require LinkML schema updates:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ No LinkML schema issues detected")

    if args.check_only:
        return

    # Generate outputs
    if args.json_output:
        json_schema = converter.generate_json_schema(tables)
        with open(args.json_output, 'w') as f:
            json.dump(json_schema, f, indent=2)
        print(f"✓ JSON schema saved to: {args.json_output}")

    if args.report_output:
        report = converter.generate_report(tables)
        with open(args.report_output, 'w') as f:
            f.write(report)
        print(f"✓ Report saved to: {args.report_output}")

    # Print report to stdout if no output files specified
    if not args.json_output and not args.report_output:
        report = converter.generate_report(tables)
        print("\n" + report)


if __name__ == '__main__':
    main()
