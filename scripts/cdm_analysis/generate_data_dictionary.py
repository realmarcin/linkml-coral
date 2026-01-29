#!/usr/bin/env python3
"""
Generate comprehensive data dictionary from CDM metadata catalogs.

Outputs:
- HTML data dictionary (interactive, searchable)
- Markdown data dictionary
- CSV data dictionary
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def load_catalogs(metadata_dir: Path) -> Dict[str, List[Dict[str, Any]]]:
    """Load all metadata catalogs."""
    combined_file = metadata_dir / 'all_catalogs.json'

    if not combined_file.exists():
        print(f"Error: Catalog file not found: {combined_file}", file=sys.stderr)
        print("Run: uv run python scripts/cdm_analysis/create_metadata_catalog.py", file=sys.stderr)
        sys.exit(1)

    with open(combined_file) as f:
        return json.load(f)


def generate_markdown_dictionary(catalogs: Dict[str, List[Dict[str, Any]]]) -> str:
    """Generate Markdown data dictionary."""
    lines = []

    lines.append("# ENIGMA CDM Data Dictionary")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Table of Contents
    lines.append("## Table of Contents")
    lines.append("")
    lines.append("- [Overview](#overview)")
    lines.append("- [Static Tables (sdt_*)](#static-tables)")
    lines.append("- [System Tables (sys_*)](#system-tables)")
    lines.append("- [Dynamic Tables (ddt_*)](#dynamic-tables)")
    lines.append("- [Microtype Reference](#microtype-reference)")
    lines.append("- [Relationship Catalog](#relationship-catalog)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Overview
    lines.append("## Overview")
    lines.append("")

    table_catalog = {t['table_name']: t for t in catalogs['table_catalog']}
    column_catalog_by_table = {}
    for col in catalogs['column_catalog']:
        table_name = col['table_name']
        if table_name not in column_catalog_by_table:
            column_catalog_by_table[table_name] = []
        column_catalog_by_table[table_name].append(col)

    total_tables = len(table_catalog)
    total_columns = len(catalogs['column_catalog'])
    total_rows = sum(t.get('total_rows', 0) for t in catalogs['table_catalog'])

    lines.append(f"- **Total Tables:** {total_tables}")
    lines.append(f"- **Total Columns:** {total_columns}")
    lines.append(f"- **Total Rows:** {total_rows:,}")
    lines.append(f"- **Microtypes Used:** {len(catalogs['microtype_catalog'])}")
    lines.append(f"- **FK Relationships:** {len(catalogs['relationship_catalog'])}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group tables by category
    tables_by_category = {'static': [], 'system': [], 'dynamic': []}
    for table_name, table_info in table_catalog.items():
        category = table_info['table_category']
        tables_by_category[category].append((table_name, table_info))

    # Static Tables
    lines.append("## Static Tables")
    lines.append("")
    lines.append("Static entity tables (sdt_*) store core domain entities.")
    lines.append("")

    for table_name, table_info in sorted(tables_by_category['static']):
        lines.extend(format_table_section(
            table_name,
            table_info,
            column_catalog_by_table.get(table_name, [])
        ))

    # System Tables
    lines.append("## System Tables")
    lines.append("")
    lines.append("System tables (sys_*) store metadata and provenance information.")
    lines.append("")

    for table_name, table_info in sorted(tables_by_category['system']):
        lines.extend(format_table_section(
            table_name,
            table_info,
            column_catalog_by_table.get(table_name, [])
        ))

    # Dynamic Tables
    lines.append("## Dynamic Tables")
    lines.append("")
    lines.append("Dynamic data tables (ddt_*) store measurement arrays in brick format.")
    lines.append("")

    for table_name, table_info in sorted(tables_by_category['dynamic']):
        lines.extend(format_table_section(
            table_name,
            table_info,
            column_catalog_by_table.get(table_name, [])
        ))

    # Microtype Reference
    lines.append("## Microtype Reference")
    lines.append("")
    lines.append("Semantic type annotations used across the CDM schema.")
    lines.append("")
    lines.append("| Microtype | Usage Count | Example Description |")
    lines.append("|-----------|-------------|---------------------|")

    for microtype in sorted(catalogs['microtype_catalog'], key=lambda x: -x['usage_count'])[:20]:
        usage = microtype['usage_count']
        desc = microtype['example_description'][:80]
        lines.append(f"| {microtype['microtype']} | {usage} | {desc} |")

    lines.append("")
    lines.append(f"*Showing top 20 of {len(catalogs['microtype_catalog'])} microtypes*")
    lines.append("")

    # Relationship Catalog
    lines.append("## Relationship Catalog")
    lines.append("")
    lines.append("Foreign key relationships between tables.")
    lines.append("")
    lines.append("| Source Table | Source Column | Target Table | Target Column | Required |")
    lines.append("|--------------|---------------|--------------|---------------|----------|")

    for rel in sorted(catalogs['relationship_catalog'], key=lambda x: x['source_table'])[:50]:
        req = "✓" if rel['is_required'] else ""
        target_col = rel['target_column'] or "(any)"
        lines.append(
            f"| {rel['source_table']} | {rel['source_column']} | "
            f"{rel['target_table']} | {target_col} | {req} |"
        )

    lines.append("")
    lines.append(f"*Showing 50 of {len(catalogs['relationship_catalog'])} relationships*")
    lines.append("")

    return '\n'.join(lines)


def format_table_section(
    table_name: str,
    table_info: Dict[str, Any],
    columns: List[Dict[str, Any]]
) -> List[str]:
    """Format a table section for the data dictionary."""
    lines = []

    lines.append(f"### {table_name}")
    lines.append("")
    lines.append(f"**Rows:** {table_info.get('total_rows', 0):,} | **Columns:** {table_info.get('num_columns', 0)}")
    lines.append("")

    if table_info.get('description'):
        lines.append(f"_{table_info['description']}_")
        lines.append("")

    # Column table
    lines.append("| Column | Type | Description | Constraints |")
    lines.append("|--------|------|-------------|-------------|")

    for col in sorted(columns, key=lambda x: x['column_name']):
        col_name = col['column_name']
        col_type = col['column_type']
        desc = (col.get('description') or '')[:100]

        # Build constraints
        constraints = []
        if col.get('is_primary_key'):
            constraints.append('PK')
        if col.get('is_unique_key'):
            constraints.append('UNIQUE')
        if col.get('is_foreign_key'):
            fk_ref = col.get('fk_references', '')
            constraints.append(f"FK→{fk_ref}")
        if col.get('is_required'):
            constraints.append('REQUIRED')

        constraint_str = ', '.join(constraints) if constraints else ''

        lines.append(f"| {col_name} | {col_type} | {desc} | {constraint_str} |")

    lines.append("")

    return lines


def generate_html_dictionary(catalogs: Dict[str, List[Dict[str, Any]]]) -> str:
    """Generate HTML data dictionary with search and filtering."""
    html = []

    html.append("<!DOCTYPE html>")
    html.append("<html lang='en'>")
    html.append("<head>")
    html.append("  <meta charset='UTF-8'>")
    html.append("  <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
    html.append("  <title>ENIGMA CDM Data Dictionary</title>")
    html.append("  <style>")
    html.append(get_html_styles())
    html.append("  </style>")
    html.append("</head>")
    html.append("<body>")
    html.append("  <div class='container'>")
    html.append("    <h1>ENIGMA CDM Data Dictionary</h1>")
    html.append(f"    <p class='subtitle'>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")

    # Overview stats
    html.append("    <div class='stats'>")
    html.append(f"      <div class='stat'><strong>{len(catalogs['table_catalog'])}</strong><br>Tables</div>")
    html.append(f"      <div class='stat'><strong>{len(catalogs['column_catalog'])}</strong><br>Columns</div>")
    html.append(f"      <div class='stat'><strong>{len(catalogs['microtype_catalog'])}</strong><br>Microtypes</div>")
    html.append(f"      <div class='stat'><strong>{len(catalogs['relationship_catalog'])}</strong><br>Relationships</div>")
    html.append("    </div>")

    # Search box
    html.append("    <div class='search-box'>")
    html.append("      <input type='text' id='searchInput' placeholder='Search tables, columns, descriptions...' onkeyup='filterTables()'>")
    html.append("    </div>")

    # Tables
    table_catalog = {t['table_name']: t for t in catalogs['table_catalog']}
    column_catalog_by_table = {}
    for col in catalogs['column_catalog']:
        table_name = col['table_name']
        if table_name not in column_catalog_by_table:
            column_catalog_by_table[table_name] = []
        column_catalog_by_table[table_name].append(col)

    for table_name in sorted(table_catalog.keys()):
        table_info = table_catalog[table_name]
        columns = column_catalog_by_table.get(table_name, [])

        html.append(f"    <div class='table-section' data-table='{table_name}'>")
        html.append(f"      <h2>{table_name}</h2>")
        html.append(f"      <p class='table-info'>")
        html.append(f"        <span class='badge'>{table_info['table_category']}</span> ")
        html.append(f"        {table_info.get('total_rows', 0):,} rows • {table_info.get('num_columns', 0)} columns")
        html.append(f"      </p>")

        html.append("      <table>")
        html.append("        <thead>")
        html.append("          <tr><th>Column</th><th>Type</th><th>Description</th><th>Constraints</th></tr>")
        html.append("        </thead>")
        html.append("        <tbody>")

        for col in sorted(columns, key=lambda x: x['column_name']):
            constraints = []
            if col.get('is_primary_key'):
                constraints.append('<span class="badge badge-pk">PK</span>')
            if col.get('is_unique_key'):
                constraints.append('<span class="badge badge-unique">UNIQUE</span>')
            if col.get('is_foreign_key'):
                fk_ref = col.get('fk_references', '')
                constraints.append(f'<span class="badge badge-fk">FK→{fk_ref}</span>')
            if col.get('is_required'):
                constraints.append('<span class="badge badge-req">REQ</span>')

            html.append("          <tr>")
            html.append(f"            <td><code>{col['column_name']}</code></td>")
            html.append(f"            <td><code>{col['column_type']}</code></td>")
            html.append(f"            <td>{col.get('description', '')}</td>")
            html.append(f"            <td>{' '.join(constraints)}</td>")
            html.append("          </tr>")

        html.append("        </tbody>")
        html.append("      </table>")
        html.append("    </div>")

    html.append("  </div>")

    # JavaScript for search
    html.append("  <script>")
    html.append("""
    function filterTables() {
      const input = document.getElementById('searchInput');
      const filter = input.value.toLowerCase();
      const sections = document.getElementsByClassName('table-section');

      for (let section of sections) {
        const text = section.textContent || section.innerText;
        if (text.toLowerCase().indexOf(filter) > -1) {
          section.style.display = '';
        } else {
          section.style.display = 'none';
        }
      }
    }
    """)
    html.append("  </script>")
    html.append("</body>")
    html.append("</html>")

    return '\n'.join(html)


def get_html_styles() -> str:
    """Get CSS styles for HTML dictionary."""
    return """
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
      background: #f5f5f5;
    }
    .container {
      background: white;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    h1 {
      color: #2c3e50;
      border-bottom: 3px solid #3498db;
      padding-bottom: 10px;
    }
    h2 {
      color: #34495e;
      margin-top: 30px;
      border-bottom: 1px solid #ecf0f1;
      padding-bottom: 8px;
    }
    .subtitle {
      color: #7f8c8d;
      font-size: 14px;
    }
    .stats {
      display: flex;
      gap: 20px;
      margin: 30px 0;
    }
    .stat {
      flex: 1;
      text-align: center;
      padding: 20px;
      background: #ecf0f1;
      border-radius: 8px;
    }
    .stat strong {
      display: block;
      font-size: 32px;
      color: #3498db;
    }
    .search-box {
      margin: 30px 0;
    }
    #searchInput {
      width: 100%;
      padding: 12px 20px;
      font-size: 16px;
      border: 2px solid #ecf0f1;
      border-radius: 8px;
      box-sizing: border-box;
    }
    #searchInput:focus {
      outline: none;
      border-color: #3498db;
    }
    .table-section {
      margin: 40px 0;
      padding: 20px;
      background: #fafafa;
      border-radius: 8px;
    }
    .table-info {
      color: #7f8c8d;
      margin: 10px 0;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      background: white;
      margin-top: 15px;
    }
    th {
      background: #34495e;
      color: white;
      padding: 12px;
      text-align: left;
      font-weight: 600;
    }
    td {
      padding: 10px 12px;
      border-bottom: 1px solid #ecf0f1;
    }
    tr:hover {
      background: #f8f9fa;
    }
    code {
      background: #ecf0f1;
      padding: 2px 6px;
      border-radius: 3px;
      font-family: 'Courier New', monospace;
      font-size: 13px;
    }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      margin-right: 4px;
    }
    .badge-pk {
      background: #e74c3c;
      color: white;
    }
    .badge-unique {
      background: #f39c12;
      color: white;
    }
    .badge-fk {
      background: #9b59b6;
      color: white;
    }
    .badge-req {
      background: #27ae60;
      color: white;
    }
    """


def main():
    parser = argparse.ArgumentParser(
        description='Generate comprehensive data dictionary from CDM metadata'
    )

    parser.add_argument(
        '--metadata-dir',
        type=Path,
        default=Path('data/cdm_metadata'),
        help='Directory containing metadata catalog files'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('docs'),
        help='Output directory for data dictionary files'
    )

    parser.add_argument(
        '--format',
        choices=['html', 'markdown', 'all'],
        default='all',
        help='Output format (default: all)'
    )

    args = parser.parse_args()

    print("📚 Generating CDM Data Dictionary")
    print("="*70)
    print()

    # Load catalogs
    print("📥 Loading metadata catalogs...")
    catalogs = load_catalogs(args.metadata_dir)
    print(f"   ✅ Loaded {len(catalogs)} catalogs")
    print()

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Generate markdown
    if args.format in ['markdown', 'all']:
        print("📝 Generating Markdown dictionary...")
        markdown = generate_markdown_dictionary(catalogs)
        md_file = args.output_dir / 'CDM_DATA_DICTIONARY.md'
        with open(md_file, 'w') as f:
            f.write(markdown)
        print(f"   ✅ {md_file}")
        print()

    # Generate HTML
    if args.format in ['html', 'all']:
        print("🌐 Generating HTML dictionary...")
        html = generate_html_dictionary(catalogs)
        html_file = args.output_dir / 'cdm_data_dictionary.html'
        with open(html_file, 'w') as f:
            f.write(html)
        print(f"   ✅ {html_file}")
        print()

    print("="*70)
    print("✅ Data dictionary generated successfully!")
    print()
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
