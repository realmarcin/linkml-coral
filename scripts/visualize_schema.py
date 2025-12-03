#!/usr/bin/env python3
"""
Visualize the CORAL LinkML schema using LinkML's built-in diagram generators.

This script demonstrates various visualization capabilities:
- Full schema ER diagrams
- Focused entity group diagrams
- Workflow visualizations
- Output in multiple formats (Mermaid, PNG, SVG, HTML)
"""

import argparse
import subprocess
import sys
import re
from pathlib import Path
from typing import List, Optional
import tempfile
import shutil


def run_command(cmd: List[str], capture=True) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    result = subprocess.run(
        cmd,
        capture_output=capture,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def generate_erdiagram(
    schema_path: Path,
    output_path: Path,
    classes: Optional[List[str]] = None,
    exclude_attributes: bool = False,
    title: Optional[str] = None
) -> bool:
    """Generate an ER diagram using LinkML's gen-erdiagram."""
    
    # For now, ignore class filtering since it's problematic
    # Generate full schema with or without attributes
    cmd = ['uv', 'run', 'gen-erdiagram', str(schema_path)]
    
    if exclude_attributes:
        cmd.append('--exclude-attributes')
    
    # Run the command
    exit_code, stdout, stderr = run_command(cmd)
    
    if exit_code != 0:
        print(f"Error generating ER diagram: {stderr}")
        return False
    
    # Clean up the output - remove markdown code blocks for .mmd files
    content = stdout
    
    # Comprehensive cleanup using regex to handle all markdown artifacts
    
    # Remove markdown code block markers
    content = re.sub(r'^```mermaid\s*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n```\s*$', '', content, flags=re.MULTILINE)
    
    # Remove any standalone ``` lines
    lines = content.split('\n')
    clean_lines = []
    
    for line in lines:
        stripped = line.strip()
        # Skip empty lines or lines that are just backticks
        if stripped and not re.match(r'^`{3,}', stripped):
            clean_lines.append(line)
    
    # Join and clean up whitespace
    content = '\n'.join(clean_lines).strip()
    
    # Final check - remove any trailing backticks that might remain
    content = re.sub(r'```+\s*$', '', content, flags=re.MULTILINE).strip()
    
    # For .mmd files, add title as a comment for GitHub
    # For HTML processing, we'll create clean versions without comments
    final_content = content
    
    if title:
        # Store both versions - one with comments for GitHub, one clean for HTML
        github_content = f"%% {title}\n{final_content}"
        output_path.write_text(github_content)
        
        # Also create a clean version for HTML processing
        clean_path = output_path.with_suffix('.clean.mmd')
        clean_path.write_text(final_content)
    else:
        output_path.write_text(final_content)
    print(f"✅ Generated: {output_path}")
    return True


def convert_mermaid_to_image(mermaid_path: Path, output_format: str) -> Optional[Path]:
    """Convert Mermaid diagram to PNG/SVG using mermaid-cli if available."""
    output_path = mermaid_path.with_suffix(f'.{output_format}')
    
    # Check if mmdc (mermaid-cli) is available
    exit_code, _, _ = run_command(['which', 'mmdc'], capture=True)
    if exit_code != 0:
        print(f"⚠️  mermaid-cli not found. Install with: npm install -g @mermaid-js/mermaid-cli")
        return None
    
    # Convert using mermaid-cli
    cmd = ['mmdc', '-i', str(mermaid_path), '-o', str(output_path), '-t', 'dark']
    exit_code, _, stderr = run_command(cmd)
    
    if exit_code == 0:
        print(f"✅ Converted to {output_format.upper()}: {output_path}")
        return output_path
    else:
        print(f"❌ Failed to convert: {stderr}")
        return None


def create_html_viewer(diagrams: List[tuple[str, Path]], output_path: Path):
    """Create an HTML file to view all diagrams."""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>CORAL LinkML Schema Diagrams</title>
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
        }
        .mermaid {
            text-align: center;
        }
        .nav {
            background-color: #333;
            padding: 10px;
            margin: -20px -20px 20px -20px;
            border-radius: 8px 8px 0 0;
        }
        .nav a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
            font-weight: bold;
        }
        .nav a:hover {
            text-decoration: underline;
        }
        .image-diagram {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
    <script>
        mermaid.initialize({ startOnLoad: true });
    </script>
</head>
<body>
    <h1>CORAL LinkML Schema Visualization</h1>
    <p>Entity-Relationship diagrams for the ENIGMA Common Data Model</p>

    <div class="nav">
        <a href="#schema">Schema Structure</a>
        <a href="#relationships">Entity Relationships</a>
    </div>
"""
    
    # Add schema structure diagrams
    html_content += """
    <h2 id="schema">Schema Structure</h2>
"""

    for title, diagram_path in diagrams:
        # Check if there's a clean version for HTML processing
        clean_path = diagram_path.with_suffix('.clean.mmd')
        if clean_path.exists():
            mermaid_code = clean_path.read_text().strip()
        else:
            # Fall back to cleaning the regular file
            content = diagram_path.read_text()

            # Clean up mermaid code for HTML rendering
            lines = content.split('\n')
            mermaid_lines = []
            for line in lines:
                line = line.strip()
                # Skip empty lines, comment lines that start with %%, and markdown markers
                if (line and
                    not line.startswith('%%') and
                    not line.startswith('```') and
                    line != '```mermaid'):
                    mermaid_lines.append(line)

            # Join with proper spacing and ensure clean output
            mermaid_code = '\n'.join(mermaid_lines)

            # Remove any remaining markdown artifacts
            mermaid_code = mermaid_code.replace('```mermaid', '').replace('```', '')

        html_content += f"""
    <div class="diagram-container">
        <h3>{title}</h3>
        <div class="mermaid">
{mermaid_code}
        </div>
    </div>
"""

    # Add relationship diagrams
    relationship_mermaid = output_path.parent.parent / 'relationship_diagrams' / 'relationships.mmd'
    relationship_png = output_path.parent.parent / 'relationship_diagrams' / 'relationships.png'

    html_content += """
    <h2 id="relationships">Entity Relationships</h2>
"""

    if relationship_mermaid.exists():
        rel_content = relationship_mermaid.read_text().strip()
        html_content += f"""
    <div class="diagram-container">
        <h3>Entity Relationship Diagram</h3>
        <p>Shows foreign key relationships, hierarchies, and cardinality between entities.</p>
        <div class="mermaid">
{rel_content}
        </div>
    </div>
"""

    if relationship_png.exists():
        # Use relative path
        rel_path = '../relationship_diagrams/relationships.png'
        html_content += f"""
    <div class="diagram-container">
        <h3>Entity Relationship Graph (Graphviz)</h3>
        <p>Alternative view showing relationship types. Solid lines = required, dashed = optional, blue = many-to-many, green = self-referential.</p>
        <img src="{rel_path}" alt="Entity Relationship Graph" class="image-diagram">
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    output_path.write_text(html_content)
    print(f"✅ Created HTML viewer: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Visualize CORAL LinkML schema')
    parser.add_argument(
        '--schema',
        default='src/linkml_coral/schema/linkml_coral.yaml',
        help='Path to LinkML schema file'
    )
    parser.add_argument(
        '--output-dir',
        default='schema_diagrams',
        help='Output directory for diagrams'
    )
    parser.add_argument(
        '--format',
        choices=['mermaid', 'png', 'svg', 'all'],
        default='mermaid',
        help='Output format'
    )
    parser.add_argument(
        '--no-attributes',
        action='store_true',
        help='Exclude attributes for cleaner diagrams'
    )
    
    args = parser.parse_args()
    
    # Setup paths
    schema_path = Path(args.schema)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}")
        sys.exit(1)
    
    print(f"🔍 Visualizing schema: {schema_path}")
    print(f"📁 Output directory: {output_dir}")
    
    # Define diagram configurations (simplified - class filtering is problematic)
    diagrams = [
        # Full schema
        {
            'name': 'full_schema',
            'title': 'CORAL Complete Schema',
            'classes': None,
            'description': 'Complete ENIGMA Common Data Model'
        },
        
        # Full schema without attributes (overview)
        {
            'name': 'schema_overview',
            'title': 'CORAL Schema Overview (No Attributes)',
            'classes': None,
            'description': 'High-level view of all entities without field details',
            'exclude_attributes': True
        }
    ]
    
    # Generate diagrams
    generated_diagrams = []
    for config in diagrams:
        output_path = output_dir / f"{config['name']}.mmd"
        
        success = generate_erdiagram(
            schema_path,
            output_path,
            classes=config.get('classes'),
            exclude_attributes=config.get('exclude_attributes', args.no_attributes),
            title=config['title']
        )
        
        if success:
            generated_diagrams.append((config['title'], output_path))
            
            # Convert to image formats if requested
            if args.format in ['png', 'all']:
                convert_mermaid_to_image(output_path, 'png')
            if args.format in ['svg', 'all']:
                convert_mermaid_to_image(output_path, 'svg')
    
    # Create HTML viewer
    if generated_diagrams:
        html_path = output_dir / 'schema_visualization.html'
        create_html_viewer(generated_diagrams, html_path)
        
        print(f"\n📊 Generated {len(generated_diagrams)} diagrams")
        print(f"📄 View all diagrams: {html_path}")
        
        # Create a README
        readme_path = output_dir / 'README.md'
        readme_content = "# CORAL LinkML Schema Diagrams\n\n"
        readme_content += "Entity-Relationship diagrams for the ENIGMA Common Data Model.\n\n"
        readme_content += "## Available Diagrams\n\n"
        
        for config in diagrams:
            if (output_dir / f"{config['name']}.mmd").exists():
                readme_content += f"- **{config['title']}** - {config['description']}\n"
                readme_content += f"  - [Mermaid](./{config['name']}.mmd)\n"
                if (output_dir / f"{config['name']}.png").exists():
                    readme_content += f"  - [PNG](./{config['name']}.png)\n"
                if (output_dir / f"{config['name']}.svg").exists():
                    readme_content += f"  - [SVG](./{config['name']}.svg)\n"
                readme_content += "\n"
        
        readme_content += "## Viewing Options\n\n"
        readme_content += "1. **HTML Viewer**: Open `schema_visualization.html` in a web browser\n"
        readme_content += "2. **GitHub**: Mermaid diagrams (.mmd files) render automatically in GitHub\n"
        readme_content += "3. **VS Code**: Install the Mermaid extension to view diagrams\n"
        readme_content += "4. **Online**: Copy .mmd content to [mermaid.live](https://mermaid.live)\n"
        
        readme_path.write_text(readme_content)
        print(f"📝 Created README: {readme_path}")
    
    print("\n✨ Schema visualization complete!")


if __name__ == "__main__":
    main()