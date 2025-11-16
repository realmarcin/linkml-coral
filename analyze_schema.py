#!/usr/bin/env python3
"""
Analyze the CORAL LinkML schema using the LinkML Python API.

This script demonstrates programmatic schema analysis:
- Schema statistics
- Entity relationships
- Foreign key analysis
- Ontology term usage
"""

import argparse
from pathlib import Path
from collections import defaultdict
from linkml_runtime.utils.schemaview import SchemaView
from typing import Dict, List, Set, Tuple


def analyze_schema(schema_path: Path) -> Dict:
    """Analyze a LinkML schema and return statistics."""
    sv = SchemaView(str(schema_path))
    
    stats = {
        'classes': {},
        'slots': {},
        'relationships': [],
        'ontology_terms': defaultdict(set),
        'foreign_keys': [],
        'multivalued_slots': [],
        'required_slots': [],
        'provenance_entities': []
    }
    
    # Analyze classes
    for class_name in sv.all_classes():
        class_def = sv.get_class(class_name)
        if class_def:
            class_slots = list(sv.class_slots(class_name))
            
            # Get annotations
            annotations = {}
            if hasattr(class_def, 'annotations'):
                for ann_name, ann_value in class_def.annotations.items():
                    annotations[str(ann_name)] = str(ann_value.value) if hasattr(ann_value, 'value') else str(ann_value)
            
            stats['classes'][class_name] = {
                'description': class_def.description,
                'slots': class_slots,
                'slot_count': len(class_slots),
                'annotations': annotations
            }
            
            # Check if used for provenance
            if annotations.get('used_for_provenance') == 'true':
                stats['provenance_entities'].append(class_name)
            
            # Extract ontology terms
            if 'term' in annotations:
                stats['ontology_terms']['class_terms'].add(annotations['term'])
    
    # Analyze slots
    for slot_name in sv.all_slots():
        slot_def = sv.get_slot(slot_name)
        if slot_def:
            # Get annotations
            annotations = {}
            if hasattr(slot_def, 'annotations'):
                for ann_name, ann_value in slot_def.annotations.items():
                    annotations[str(ann_name)] = str(ann_value.value) if hasattr(ann_value, 'value') else str(ann_value)
            
            stats['slots'][str(slot_name)] = {
                'range': slot_def.range,
                'required': slot_def.required,
                'multivalued': slot_def.multivalued,
                'pattern': slot_def.pattern,
                'annotations': annotations
            }
            
            # Track foreign keys
            if 'foreign_key' in annotations:
                fk_target = annotations['foreign_key']
                stats['foreign_keys'].append({
                    'slot': str(slot_name),
                    'target': fk_target
                })
                
                # Extract relationship
                source_class = None
                for cls_name, cls_info in stats['classes'].items():
                    if str(slot_name) in cls_info['slots']:
                        source_class = cls_name
                        break
                
                if source_class and '.' in fk_target:
                    target_class = fk_target.split('.')[0]
                    stats['relationships'].append({
                        'from': source_class,
                        'to': target_class,
                        'via': str(slot_name),
                        'type': 'foreign_key'
                    })
            
            # Track multivalued slots
            if slot_def.multivalued:
                stats['multivalued_slots'].append(str(slot_name))
            
            # Track required slots
            if slot_def.required:
                stats['required_slots'].append(str(slot_name))
            
            # Extract ontology terms
            if 'type_term' in annotations:
                stats['ontology_terms']['slot_terms'].add(annotations['type_term'])
            if 'constraint' in annotations:
                stats['ontology_terms']['constraints'].add(annotations['constraint'])
    
    return stats


def print_analysis_report(stats: Dict):
    """Print a formatted analysis report."""
    print("=" * 60)
    print("CORAL LinkML Schema Analysis Report")
    print("=" * 60)
    
    # Basic statistics
    print(f"\n📊 Basic Statistics:")
    print(f"  - Classes: {len(stats['classes'])}")
    print(f"  - Slots: {len(stats['slots'])}")
    print(f"  - Foreign Keys: {len(stats['foreign_keys'])}")
    print(f"  - Relationships: {len(stats['relationships'])}")
    print(f"  - Multivalued Slots: {len(stats['multivalued_slots'])}")
    print(f"  - Required Slots: {len(stats['required_slots'])}")
    
    # Provenance entities
    print(f"\n🔍 Provenance-Tracked Entities ({len(stats['provenance_entities'])}):")
    for entity in sorted(stats['provenance_entities']):
        print(f"  - {entity}")
    
    # Class details
    print(f"\n📋 Classes Overview:")
    for class_name, info in sorted(stats['classes'].items()):
        print(f"\n  {class_name}:")
        print(f"    - Slots: {info['slot_count']}")
        if info.get('description'):
            print(f"    - Description: {info['description'][:60]}...")
        if 'term' in info.get('annotations', {}):
            print(f"    - Ontology Term: {info['annotations']['term']}")
    
    # Foreign key relationships
    print(f"\n🔗 Foreign Key Relationships:")
    for fk in sorted(stats['foreign_keys'], key=lambda x: x['slot']):
        print(f"  - {fk['slot']} → {fk['target']}")
    
    # Entity relationships graph
    print(f"\n📊 Entity Relationship Graph:")
    for rel in sorted(stats['relationships'], key=lambda x: (x['from'], x['to'])):
        print(f"  - {rel['from']} --[{rel['via']}]--> {rel['to']}")
    
    # Ontology usage
    print(f"\n🔬 Ontology Usage:")
    print(f"  - Unique class terms: {len(stats['ontology_terms']['class_terms'])}")
    print(f"  - Unique slot terms: {len(stats['ontology_terms']['slot_terms'])}")
    print(f"  - Unique constraints: {len(stats['ontology_terms']['constraints'])}")
    
    # Ontology prefixes used
    all_terms = set()
    for term_set in stats['ontology_terms'].values():
        all_terms.update(term_set)
    
    prefixes = defaultdict(int)
    for term in all_terms:
        if ':' in term:
            prefix = term.split(':')[0]
            prefixes[prefix] += 1
    
    print(f"\n  Ontology Prefixes Used:")
    for prefix, count in sorted(prefixes.items()):
        print(f"    - {prefix}: {count} terms")
    
    # Complex slots
    print(f"\n🔧 Complex Slot Types:")
    pattern_slots = [name for name, info in stats['slots'].items() if info.get('pattern')]
    print(f"  - Slots with regex patterns: {len(pattern_slots)}")
    if pattern_slots:
        for slot in pattern_slots[:5]:  # Show first 5
            print(f"    • {slot}: {stats['slots'][slot]['pattern']}")
        if len(pattern_slots) > 5:
            print(f"    ... and {len(pattern_slots) - 5} more")


def generate_relationship_matrix(stats: Dict) -> str:
    """Generate a relationship matrix in Markdown format."""
    classes = sorted(stats['classes'].keys())
    
    # Build adjacency matrix
    matrix = defaultdict(lambda: defaultdict(list))
    for rel in stats['relationships']:
        matrix[rel['from']][rel['to']].append(rel['via'])
    
    # Generate markdown table
    md = "## Entity Relationship Matrix\n\n"
    md += "| From \\ To |"
    for cls in classes:
        md += f" {cls} |"
    md += "\n"
    
    # Header separator
    md += "|------------|"
    for _ in classes:
        md += "----------|"
    md += "\n"
    
    # Matrix rows
    for from_cls in classes:
        md += f"| **{from_cls}** |"
        for to_cls in classes:
            if to_cls in matrix[from_cls]:
                slots = matrix[from_cls][to_cls]
                md += f" {', '.join(slots)} |"
            else:
                md += " - |"
        md += "\n"
    
    return md


def main():
    parser = argparse.ArgumentParser(description='Analyze CORAL LinkML schema')
    parser.add_argument(
        '--schema',
        default='src/linkml_coral/schema/linkml_coral.yaml',
        help='Path to LinkML schema file'
    )
    parser.add_argument(
        '--output-dir',
        help='Output directory for reports (optional)'
    )
    parser.add_argument(
        '--matrix',
        action='store_true',
        help='Generate relationship matrix'
    )
    
    args = parser.parse_args()
    
    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}")
        return 1
    
    print(f"🔍 Analyzing schema: {schema_path}")
    
    # Analyze schema
    stats = analyze_schema(schema_path)
    
    # Print report
    print_analysis_report(stats)
    
    # Generate additional outputs if requested
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Save detailed stats as JSON
        import json
        
        # Convert sets to lists for JSON serialization
        json_stats = stats.copy()
        json_stats['ontology_terms'] = {k: list(v) for k, v in stats['ontology_terms'].items()}
        
        stats_file = output_dir / 'schema_analysis.json'
        with open(stats_file, 'w') as f:
            json.dump(json_stats, f, indent=2)
        print(f"\n📄 Saved detailed statistics: {stats_file}")
    
    if args.matrix:
        matrix = generate_relationship_matrix(stats)
        print(f"\n{matrix}")
        
        if args.output_dir:
            matrix_file = output_dir / 'relationship_matrix.md'
            matrix_file.write_text(matrix)
            print(f"📄 Saved relationship matrix: {matrix_file}")
    
    return 0


if __name__ == "__main__":
    exit(main())