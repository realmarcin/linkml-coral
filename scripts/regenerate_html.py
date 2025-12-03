#!/usr/bin/env python3
"""Regenerate the HTML viewer with fixed content."""

from pathlib import Path

def create_html_viewer(diagrams, output_path: Path):
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
    </style>
    <script>
        mermaid.initialize({ startOnLoad: true });
    </script>
</head>
<body>
    <h1>CORAL LinkML Schema Visualization</h1>
    <p>Entity-Relationship diagrams for the ENIGMA Common Data Model</p>
"""
    
    for title, diagram_path in diagrams:
        content = diagram_path.read_text()
        
        # Clean up mermaid code for HTML rendering
        lines = content.split('\n')
        mermaid_lines = []
        for line in lines:
            line = line.strip()
            # Skip empty lines and comment lines that start with %%
            if line and not line.startswith('%%'):
                mermaid_lines.append(line)
        
        # Join with proper spacing
        mermaid_code = '\n'.join(mermaid_lines)
        
        html_content += f"""
    <div class="diagram-container">
        <h2>{title}</h2>
        <div class="mermaid">
{mermaid_code}
        </div>
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    output_path.write_text(html_content)
    print(f"✅ Created HTML viewer: {output_path}")

# Regenerate the HTML viewer
schema_dir = Path("schema_diagrams")
if schema_dir.exists():
    diagrams = [
        ("CORAL Complete Schema", schema_dir / "full_schema.mmd"),
        ("CORAL Schema Overview (No Attributes)", schema_dir / "schema_overview.mmd")
    ]
    
    # Filter to only existing files
    existing_diagrams = [(title, path) for title, path in diagrams if path.exists()]
    
    if existing_diagrams:
        html_path = schema_dir / "schema_visualization.html"
        create_html_viewer(existing_diagrams, html_path)
        print(f"\n🎉 Regenerated HTML viewer with {len(existing_diagrams)} diagrams")
    else:
        print("❌ No diagram files found")
else:
    print("❌ Schema diagrams directory not found")