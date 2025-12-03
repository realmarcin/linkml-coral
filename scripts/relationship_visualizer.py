#!/usr/bin/env python3
"""
Visualize LinkML schema relationships using foreign key annotations.

This script generates Mermaid ER diagrams that show both entity structures
and the relationships (foreign keys) between entities.
"""

import argparse
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
from linkml_runtime.utils.schemaview import SchemaView


@dataclass
class Relationship:
    """Represents a foreign key relationship between entities."""
    from_class: str
    from_slot: str
    to_class: str
    to_slot: str
    is_multivalued: bool = False
    description: str = ""


@dataclass
class EntityInfo:
    """Information about an entity/class."""
    name: str
    slots: List[str]
    relationships: List[Relationship]


class RelationshipExtractor:
    """Extract relationship information from LinkML schema."""
    
    def __init__(self, schema_view: SchemaView):
        self.schema_view = schema_view
        self.relationships: List[Relationship] = []
        self.entities: Dict[str, EntityInfo] = {}
    
    def extract_relationships(self) -> Dict[str, List[Relationship]]:
        """Extract all foreign key relationships from the schema."""
        relationships_by_class = {}
        
        for class_name in self.schema_view.all_classes():
            class_def = self.schema_view.get_class(class_name)
            class_relationships = []
            
            # Get all slots for this class
            slots = self.schema_view.class_slots(class_name)
            slot_names = []
            
            for slot_name in slots:
                slot_def = self.schema_view.get_slot(slot_name)
                slot_names.append(str(slot_name))
                
                # Check for foreign key annotation
                if slot_def.annotations:
                    for annotation in slot_def.annotations:
                        if annotation.tag == 'foreign_key':
                            fk_value = annotation.value
                            
                            # Parse foreign key format: "TargetClass.target_field"
                            if '.' in fk_value:
                                target_class, target_field = fk_value.split('.', 1)
                                
                                relationship = Relationship(
                                    from_class=class_name,
                                    from_slot=str(slot_name),
                                    to_class=target_class,
                                    to_slot=target_field,
                                    is_multivalued=slot_def.multivalued or False,
                                    description=slot_def.description or ""
                                )
                                
                                class_relationships.append(relationship)
                                self.relationships.append(relationship)
            
            # Store entity info
            self.entities[class_name] = EntityInfo(
                name=class_name,
                slots=slot_names,
                relationships=class_relationships
            )
            
            relationships_by_class[class_name] = class_relationships
        
        return relationships_by_class
    
    def get_relationship_summary(self) -> str:
        """Generate a text summary of all relationships."""
        summary = "# Schema Relationship Summary\n\n"
        
        summary += f"Total entities: {len(self.entities)}\n"
        summary += f"Total relationships: {len(self.relationships)}\n\n"
        
        # Group by source class
        by_source = {}
        for rel in self.relationships:
            if rel.from_class not in by_source:
                by_source[rel.from_class] = []
            by_source[rel.from_class].append(rel)
        
        summary += "## Relationships by Entity\n\n"
        for class_name in sorted(by_source.keys()):
            rels = by_source[class_name]
            summary += f"### {class_name}\n"
            for rel in rels:
                cardinality = "many" if rel.is_multivalued else "one"
                summary += f"- `{rel.from_slot}` → {rel.to_class}.{rel.to_slot} ({cardinality})\n"
            summary += "\n"
        
        return summary


class MermaidRelationshipGenerator:
    """Generate Mermaid ER diagrams with relationships."""
    
    def __init__(self, extractor: RelationshipExtractor):
        self.extractor = extractor
    
    def generate_er_diagram(self, include_attributes: bool = True, 
                          filter_classes: Optional[List[str]] = None) -> str:
        """Generate a Mermaid ER diagram with relationships."""
        
        # Filter entities if specified
        entities = self.extractor.entities
        if filter_classes:
            entities = {k: v for k, v in entities.items() if k in filter_classes}
        
        # Start Mermaid diagram
        mermaid = "erDiagram\n"
        
        # Add entities with their attributes
        for entity_name, entity_info in entities.items():
            mermaid += f"    {entity_name} {{\n"
            
            if include_attributes:
                # Add key slots (identifiers first)
                for slot_name in entity_info.slots:
                    slot_def = self.extractor.schema_view.get_slot(slot_name)
                    
                    # Determine field type
                    field_type = "string"
                    if slot_def.range:
                        field_type = str(slot_def.range)
                    
                    # Add identifier marker
                    if slot_def.identifier:
                        field_type += " PK"
                    elif any(rel.from_slot == slot_name for rel in entity_info.relationships):
                        field_type += " FK"
                    
                    # Clean slot name for display
                    display_name = str(slot_name).replace(f"{entity_name.lower()}_", "")
                    mermaid += f"        {field_type} {display_name}\n"
            
            mermaid += "    }\n"
        
        # Add relationships
        mermaid += "\n"
        relationships_added = set()
        
        for entity_name, entity_info in entities.items():
            for rel in entity_info.relationships:
                # Only add if target entity is in our filtered set
                if filter_classes and rel.to_class not in filter_classes:
                    continue
                
                # Avoid duplicate relationships
                rel_key = f"{rel.from_class}-{rel.to_class}-{rel.from_slot}"
                if rel_key in relationships_added:
                    continue
                relationships_added.add(rel_key)
                
                # Determine relationship type
                if rel.is_multivalued:
                    # One-to-many relationship
                    mermaid += f"    {rel.to_class} ||--o{{ {rel.from_class} : \"{rel.from_slot}\"\n"
                else:
                    # One-to-one or many-to-one relationship
                    mermaid += f"    {rel.to_class} ||--|| {rel.from_class} : \"{rel.from_slot}\"\n"
        
        return mermaid
    
    def generate_network_diagram(self) -> str:
        """Generate a simplified network diagram showing just relationships."""
        mermaid = "graph TD\n"
        
        # Add nodes
        for entity_name in self.extractor.entities.keys():
            mermaid += f"    {entity_name}[{entity_name}]\n"
        
        # Add edges
        for rel in self.extractor.relationships:
            arrow = "-->|many|" if rel.is_multivalued else "-->|one|"
            mermaid += f"    {rel.from_class} {arrow} {rel.to_class}\n"
        
        return mermaid


def main():
    parser = argparse.ArgumentParser(description='Visualize LinkML schema relationships')
    parser.add_argument(
        '--schema',
        default='src/linkml_coral/schema/linkml_coral.yaml',
        help='Path to LinkML schema file'
    )
    parser.add_argument(
        '--output-dir',
        default='relationship_diagrams',
        help='Output directory for diagrams'
    )
    parser.add_argument(
        '--format',
        choices=['er', 'network', 'both'],
        default='both',
        help='Diagram format to generate'
    )
    parser.add_argument(
        '--no-attributes',
        action='store_true',
        help='Exclude attributes for cleaner diagrams'
    )
    parser.add_argument(
        '--classes',
        nargs='*',
        help='Filter to specific classes'
    )
    
    args = parser.parse_args()
    
    # Setup paths
    schema_path = Path(args.schema)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}")
        sys.exit(1)
    
    print(f"🔍 Analyzing relationships in: {schema_path}")
    print(f"📁 Output directory: {output_dir}")
    
    # Load schema and extract relationships
    schema_view = SchemaView(str(schema_path))
    extractor = RelationshipExtractor(schema_view)
    relationships_by_class = extractor.extract_relationships()
    
    # Generate summary report
    summary = extractor.get_relationship_summary()
    summary_path = output_dir / 'relationship_summary.md'
    summary_path.write_text(summary)
    print(f"📊 Relationship summary: {summary_path}")
    
    # Generate diagrams
    generator = MermaidRelationshipGenerator(extractor)
    
    if args.format in ['er', 'both']:
        # Full ER diagram with relationships
        er_diagram = generator.generate_er_diagram(
            include_attributes=not args.no_attributes,
            filter_classes=args.classes
        )
        
        er_path = output_dir / 'schema_relationships.mmd'
        er_path.write_text(er_diagram)
        print(f"🔗 ER diagram with relationships: {er_path}")
    
    if args.format in ['network', 'both']:
        # Network diagram showing just relationships
        network_diagram = generator.generate_network_diagram()
        
        network_path = output_dir / 'relationship_network.mmd'
        network_path.write_text(network_diagram)
        print(f"🕸️  Relationship network: {network_path}")
    
    # Create HTML viewer
    create_relationship_html_viewer(output_dir, args.format)
    
    print(f"\n✨ Relationship analysis complete!")
    print(f"📄 View diagrams: {output_dir}/relationship_viewer.html")


def create_relationship_html_viewer(output_dir: Path, format_type: str):
    """Create an HTML viewer for relationship diagrams."""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>CORAL Schema Relationships</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1, h2 {
            color: #333;
        }
        .diagram-container {
            background-color: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow-x: auto;
        }
        .mermaid {
            text-align: center;
        }
        .summary {
            background-color: #e8f4f8;
            padding: 15px;
            border-left: 4px solid #0066cc;
            margin: 20px 0;
        }
    </style>
    <script>
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            er: {
                layoutDirection: 'TB'
            }
        });
    </script>
</head>
<body>
    <h1>CORAL LinkML Schema Relationships</h1>
    <div class="summary">
        <p><strong>This visualization shows the foreign key relationships between entities in the ENIGMA Common Data Model.</strong></p>
        <p>Relationships are extracted from <code>foreign_key</code> annotations in the LinkML schema.</p>
    </div>
"""
    
    # Add ER diagram
    if format_type in ['er', 'both']:
        er_file = output_dir / 'schema_relationships.mmd'
        if er_file.exists():
            er_content = er_file.read_text().strip()
            html_content += f"""
    <div class="diagram-container">
        <h2>Entity Relationship Diagram</h2>
        <p>Complete schema showing entities, attributes, and foreign key relationships.</p>
        <div class="mermaid">
{er_content}
        </div>
    </div>
"""
    
    # Add network diagram
    if format_type in ['network', 'both']:
        network_file = output_dir / 'relationship_network.mmd'
        if network_file.exists():
            network_content = network_file.read_text().strip()
            html_content += f"""
    <div class="diagram-container">
        <h2>Relationship Network</h2>
        <p>Simplified view showing only the relationships between entities.</p>
        <div class="mermaid">
{network_content}
        </div>
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    html_path = output_dir / 'relationship_viewer.html'
    html_path.write_text(html_content)


if __name__ == "__main__":
    main()