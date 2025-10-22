#!/usr/bin/env python3
"""
Visualize relationships in the CORAL LinkML schema.

This script focuses specifically on entity relationships:
- Foreign key relationships between entities
- Multivalued (many-to-many) relationships
- Self-referential relationships
- Provenance workflow relationships from process_inputs annotations
"""

import argparse
from pathlib import Path
from collections import defaultdict
from linkml_runtime.utils.schemaview import SchemaView
from typing import Dict, List, Set, Tuple


def extract_relationships(schema_path: Path) -> Dict:
    """Extract all relationship information from the schema."""
    sv = SchemaView(str(schema_path))

    relationships = {
        'foreign_keys': [],
        'multivalued_refs': [],
        'self_refs': [],
        'provenance_flows': [],
        'entity_graph': defaultdict(list)
    }

    # Track which entities are used for provenance
    provenance_entities = set()

    # First pass: identify provenance entities and workflow relationships
    for class_name in sv.all_classes():
        class_def = sv.get_class(class_name)
        if not class_def:
            continue

        annotations = {}
        if hasattr(class_def, 'annotations'):
            for ann_name, ann_value in class_def.annotations.items():
                annotations[str(ann_name)] = str(ann_value.value) if hasattr(ann_value, 'value') else str(ann_value)

        # Check if used for provenance
        if annotations.get('used_for_provenance') == 'true':
            provenance_entities.add(class_name)

        # Extract workflow relationships from process_inputs
        if 'process_inputs' in annotations:
            # process_inputs is a list of lists in the schema
            # e.g., [['Sample'], ['Community']]
            process_inputs_str = annotations['process_inputs']
            if process_inputs_str:
                relationships['provenance_flows'].append({
                    'entity': class_name,
                    'inputs': process_inputs_str,
                    'process_types': annotations.get('process_types', '')
                })

    # Second pass: analyze slots for foreign key relationships
    for slot_name in sv.all_slots():
        slot_def = sv.get_slot(slot_name)
        if not slot_def:
            continue

        annotations = {}
        if hasattr(slot_def, 'annotations'):
            for ann_name, ann_value in slot_def.annotations.items():
                annotations[str(ann_name)] = str(ann_value.value) if hasattr(ann_value, 'value') else str(ann_value)

        # Check for foreign key annotation
        if 'foreign_key' not in annotations:
            continue

        fk_target = annotations['foreign_key']

        # Find which class owns this slot
        source_class = None
        for cls_name in sv.all_classes():
            class_slots = list(sv.class_slots(cls_name))
            if str(slot_name) in class_slots:
                source_class = cls_name
                break

        if not source_class or '.' not in fk_target:
            continue

        target_class, target_field = fk_target.split('.', 1)

        rel = {
            'from': source_class,
            'to': target_class,
            'via_slot': str(slot_name),
            'to_field': target_field,
            'multivalued': slot_def.multivalued or False,
            'required': slot_def.required or False
        }

        # Categorize relationship
        if source_class == target_class:
            relationships['self_refs'].append(rel)
        elif rel['multivalued']:
            relationships['multivalued_refs'].append(rel)
        else:
            relationships['foreign_keys'].append(rel)

        # Add to entity graph
        relationships['entity_graph'][source_class].append({
            'target': target_class,
            'slot': str(slot_name),
            'type': 'self-ref' if source_class == target_class else 'many' if rel['multivalued'] else 'one'
        })

    relationships['provenance_entities'] = list(provenance_entities)
    return relationships


def generate_mermaid_relationship_diagram(relationships: Dict, output_path: Path):
    """Generate a Mermaid ER diagram focusing on relationships."""

    mermaid = "erDiagram\n"

    # Add all entities
    all_entities = set()
    for rel in relationships['foreign_keys'] + relationships['multivalued_refs'] + relationships['self_refs']:
        all_entities.add(rel['from'])
        all_entities.add(rel['to'])

    # Generate relationship lines
    for rel in sorted(relationships['foreign_keys'], key=lambda x: (x['from'], x['to'])):
        cardinality = "||" if rel['required'] else "|o"
        mermaid += f"    {rel['from']} {cardinality}--|| {rel['to']} : \"{rel['via_slot']}\"\n"

    for rel in sorted(relationships['multivalued_refs'], key=lambda x: (x['from'], x['to'])):
        cardinality = "||" if rel['required'] else "|o"
        mermaid += f"    {rel['from']} {cardinality}--o{{ {rel['to']} : \"{rel['via_slot']}\"\n"

    for rel in sorted(relationships['self_refs'], key=lambda x: x['via_slot']):
        cardinality = "||" if rel['required'] else "|o"
        mermaid += f"    {rel['from']} {cardinality}--o{{ {rel['from']} : \"{rel['via_slot']}\"\n"

    output_path.write_text(mermaid)
    print(f"✅ Generated Mermaid relationship diagram: {output_path}")


def generate_graphviz_relationship_diagram(relationships: Dict, output_path: Path):
    """Generate a Graphviz DOT diagram focusing on relationships."""

    dot = "digraph Relationships {\n"
    dot += "    rankdir=LR;\n"
    dot += "    node [shape=box, style=rounded];\n"
    dot += "    edge [fontsize=10];\n\n"

    # Highlight provenance entities
    if relationships['provenance_entities']:
        dot += "    // Provenance-tracked entities\n"
        dot += "    node [style=\"rounded,filled\", fillcolor=lightblue];\n"
        for entity in sorted(relationships['provenance_entities']):
            dot += f"    {entity};\n"
        dot += "\n"
        dot += "    // Other entities\n"
        dot += "    node [style=rounded, fillcolor=white];\n"
        all_entities = set()
        for rel in relationships['foreign_keys'] + relationships['multivalued_refs'] + relationships['self_refs']:
            all_entities.add(rel['from'])
            all_entities.add(rel['to'])
        other_entities = all_entities - set(relationships['provenance_entities'])
        for entity in sorted(other_entities):
            dot += f"    {entity};\n"
        dot += "\n"

    # Add relationships
    dot += "    // One-to-one and many-to-one relationships\n"
    for rel in sorted(relationships['foreign_keys'], key=lambda x: (x['from'], x['to'])):
        style = "solid" if rel['required'] else "dashed"
        label = rel['via_slot'].replace(rel['from'].lower() + '_', '')
        dot += f"    {rel['from']} -> {rel['to']} [label=\"{label}\", style={style}];\n"

    dot += "\n    // Many-to-many relationships\n"
    for rel in sorted(relationships['multivalued_refs'], key=lambda x: (x['from'], x['to'])):
        style = "solid" if rel['required'] else "dashed"
        label = rel['via_slot'].replace(rel['from'].lower() + '_', '')
        dot += f"    {rel['from']} -> {rel['to']} [label=\"{label}\", style={style}, color=blue, arrowhead=crow];\n"

    dot += "\n    // Self-referential relationships\n"
    for rel in sorted(relationships['self_refs'], key=lambda x: x['via_slot']):
        label = rel['via_slot'].replace(rel['from'].lower() + '_', '')
        dot += f"    {rel['from']} -> {rel['from']} [label=\"{label}\", style=dashed, color=green];\n"

    dot += "}\n"

    output_path.write_text(dot)
    print(f"✅ Generated Graphviz relationship diagram: {output_path}")

    # Try to generate PNG if graphviz is available
    try:
        import subprocess
        result = subprocess.run(['which', 'dot'], capture_output=True)
        if result.returncode == 0:
            png_path = output_path.with_suffix('.png')
            subprocess.run(['dot', '-Tpng', str(output_path), '-o', str(png_path)])
            print(f"✅ Generated PNG: {png_path}")
            svg_path = output_path.with_suffix('.svg')
            subprocess.run(['dot', '-Tsvg', str(output_path), '-o', str(svg_path)])
            print(f"✅ Generated SVG: {svg_path}")
    except Exception as e:
        print(f"ℹ️  Graphviz not available for image generation: {e}")


def generate_text_report(relationships: Dict, output_path: Path):
    """Generate a detailed text report of relationships."""

    report = []
    report.append("=" * 80)
    report.append("CORAL LinkML Schema - Relationship Analysis")
    report.append("=" * 80)
    report.append("")

    # Summary statistics
    report.append("## Summary")
    report.append("")
    report.append(f"Total relationships: {len(relationships['foreign_keys']) + len(relationships['multivalued_refs']) + len(relationships['self_refs'])}")
    report.append(f"  - One-to-one/Many-to-one: {len(relationships['foreign_keys'])}")
    report.append(f"  - Many-to-many: {len(relationships['multivalued_refs'])}")
    report.append(f"  - Self-referential: {len(relationships['self_refs'])}")
    report.append(f"  - Provenance-tracked entities: {len(relationships['provenance_entities'])}")
    report.append("")

    # Provenance entities
    if relationships['provenance_entities']:
        report.append("## Provenance-Tracked Entities")
        report.append("")
        report.append("These entities are tracked through the provenance workflow:")
        for entity in sorted(relationships['provenance_entities']):
            report.append(f"  - {entity}")
        report.append("")

    # One-to-one and many-to-one relationships
    report.append("## One-to-One and Many-to-One Relationships")
    report.append("")
    for rel in sorted(relationships['foreign_keys'], key=lambda x: (x['from'], x['to'])):
        req = " [REQUIRED]" if rel['required'] else " [OPTIONAL]"
        report.append(f"  {rel['from']}.{rel['via_slot']} → {rel['to']}.{rel['to_field']}{req}")
    report.append("")

    # Many-to-many relationships
    if relationships['multivalued_refs']:
        report.append("## Many-to-Many Relationships")
        report.append("")
        for rel in sorted(relationships['multivalued_refs'], key=lambda x: (x['from'], x['to'])):
            req = " [REQUIRED]" if rel['required'] else " [OPTIONAL]"
            report.append(f"  {rel['from']}.{rel['via_slot']} → {rel['to']}.{rel['to_field']}{req}")
        report.append("")

    # Self-referential relationships
    if relationships['self_refs']:
        report.append("## Self-Referential Relationships")
        report.append("")
        report.append("Entities that reference themselves (hierarchies):")
        for rel in sorted(relationships['self_refs'], key=lambda x: x['via_slot']):
            req = " [REQUIRED]" if rel['required'] else " [OPTIONAL]"
            report.append(f"  {rel['from']}.{rel['via_slot']} → {rel['to']}.{rel['to_field']}{req}")
        report.append("")

    # Entity connectivity
    report.append("## Entity Relationship Graph")
    report.append("")
    report.append("Outgoing relationships from each entity:")
    for entity in sorted(relationships['entity_graph'].keys()):
        rels = relationships['entity_graph'][entity]
        report.append(f"\n{entity}:")
        for rel in rels:
            rel_type = rel['type']
            arrow = "⟹" if rel_type == "many" else "→"
            indicator = " (self)" if rel_type == "self-ref" else ""
            report.append(f"  {arrow} {rel['target']} via {rel['slot']}{indicator}")
    report.append("")

    # Provenance workflows
    if relationships['provenance_flows']:
        report.append("## Provenance Workflow Relationships")
        report.append("")
        report.append("Derived from process_inputs annotations:")
        for flow in relationships['provenance_flows']:
            report.append(f"\n{flow['entity']}:")
            report.append(f"  Inputs: {flow['inputs']}")
            report.append(f"  Process types: {flow['process_types']}")
        report.append("")

    report.append("=" * 80)
    report.append("Legend:")
    report.append("  → : one-to-one or many-to-one relationship")
    report.append("  ⟹ : many-to-many relationship (multivalued)")
    report.append("  [REQUIRED] : relationship is required")
    report.append("  [OPTIONAL] : relationship is optional")
    report.append("=" * 80)

    output_path.write_text("\n".join(report))
    print(f"✅ Generated text report: {output_path}")


def generate_markdown_report(relationships: Dict, output_path: Path):
    """Generate a Markdown report suitable for documentation."""

    report = []
    report.append("# CORAL LinkML Schema - Relationship Documentation")
    report.append("")
    report.append("## Overview")
    report.append("")
    report.append(f"This document describes the relationships between entities in the ENIGMA Common Data Model.")
    report.append("")
    report.append(f"- **Total relationships**: {len(relationships['foreign_keys']) + len(relationships['multivalued_refs']) + len(relationships['self_refs'])}")
    report.append(f"- **One-to-one/Many-to-one**: {len(relationships['foreign_keys'])}")
    report.append(f"- **Many-to-many**: {len(relationships['multivalued_refs'])}")
    report.append(f"- **Self-referential**: {len(relationships['self_refs'])}")
    report.append(f"- **Provenance-tracked entities**: {len(relationships['provenance_entities'])}")
    report.append("")

    # Provenance entities
    if relationships['provenance_entities']:
        report.append("## Provenance-Tracked Entities")
        report.append("")
        report.append("The following entities are tracked through the provenance workflow system:")
        report.append("")
        for entity in sorted(relationships['provenance_entities']):
            report.append(f"- `{entity}`")
        report.append("")

    # Relationship table
    report.append("## Relationship Reference")
    report.append("")
    report.append("### One-to-One and Many-to-One Relationships")
    report.append("")
    report.append("| Source Entity | Slot | Target Entity | Target Field | Required |")
    report.append("|---------------|------|---------------|--------------|----------|")
    for rel in sorted(relationships['foreign_keys'], key=lambda x: (x['from'], x['to'])):
        req = "✓" if rel['required'] else ""
        report.append(f"| `{rel['from']}` | `{rel['via_slot']}` | `{rel['to']}` | `{rel['to_field']}` | {req} |")
    report.append("")

    if relationships['multivalued_refs']:
        report.append("### Many-to-Many Relationships")
        report.append("")
        report.append("| Source Entity | Slot | Target Entity | Target Field | Required |")
        report.append("|---------------|------|---------------|--------------|----------|")
        for rel in sorted(relationships['multivalued_refs'], key=lambda x: (x['from'], x['to'])):
            req = "✓" if rel['required'] else ""
            report.append(f"| `{rel['from']}` | `{rel['via_slot']}` | `{rel['to']}` | `{rel['to_field']}` | {req} |")
        report.append("")

    if relationships['self_refs']:
        report.append("### Self-Referential Relationships")
        report.append("")
        report.append("These relationships create hierarchies within a single entity type:")
        report.append("")
        report.append("| Entity | Slot | Target Field | Description |")
        report.append("|--------|------|--------------|-------------|")
        for rel in sorted(relationships['self_refs'], key=lambda x: x['via_slot']):
            desc = "Hierarchical relationship" if "parent" in rel['via_slot'] else "Derived relationship" if "derived" in rel['via_slot'] else ""
            report.append(f"| `{rel['from']}` | `{rel['via_slot']}` | `{rel['to_field']}` | {desc} |")
        report.append("")

    # Entity connectivity diagram
    report.append("## Entity Relationship Graph")
    report.append("")
    report.append("```")
    for entity in sorted(relationships['entity_graph'].keys()):
        rels = relationships['entity_graph'][entity]
        if rels:
            report.append(f"{entity}")
            for rel in rels:
                arrow = "==>" if rel['type'] == "many" else "-->"
                indicator = " (self-reference)" if rel['type'] == "self-ref" else ""
                report.append(f"  {arrow} {rel['target']} [{rel['slot']}]{indicator}")
    report.append("```")
    report.append("")

    output_path.write_text("\n".join(report))
    print(f"✅ Generated markdown report: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Visualize relationships in CORAL LinkML schema'
    )
    parser.add_argument(
        '--schema',
        default='src/linkml_coral/schema/linkml_coral.yaml',
        help='Path to LinkML schema file'
    )
    parser.add_argument(
        '--output-dir',
        default='relationship_diagrams',
        help='Output directory for diagrams and reports'
    )
    parser.add_argument(
        '--format',
        choices=['all', 'mermaid', 'graphviz', 'text', 'markdown'],
        default='all',
        help='Output format'
    )

    args = parser.parse_args()

    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}")
        return 1

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    print(f"🔍 Analyzing relationships in: {schema_path}")
    print(f"📁 Output directory: {output_dir}")
    print("")

    # Extract relationships
    relationships = extract_relationships(schema_path)

    # Generate outputs
    if args.format in ['all', 'mermaid']:
        generate_mermaid_relationship_diagram(
            relationships,
            output_dir / 'relationships.mmd'
        )

    if args.format in ['all', 'graphviz']:
        generate_graphviz_relationship_diagram(
            relationships,
            output_dir / 'relationships.dot'
        )

    if args.format in ['all', 'text']:
        generate_text_report(
            relationships,
            output_dir / 'relationships.txt'
        )

    if args.format in ['all', 'markdown']:
        generate_markdown_report(
            relationships,
            output_dir / 'RELATIONSHIPS.md'
        )

    print("")
    print("✨ Relationship visualization complete!")
    return 0


if __name__ == "__main__":
    exit(main())
