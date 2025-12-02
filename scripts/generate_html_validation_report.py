#!/usr/bin/env python3
"""
Generate HTML validation report from JSON validation results.

This script converts JSON validation output into an interactive HTML report
with filtering, sorting, and quality metrics visualization.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ENIGMA TSV Validation Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
        }

        h2 {
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }

        h3 {
            color: #7f8c8d;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .summary-card.success {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }

        .summary-card.warning {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }

        .summary-card.error {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }

        .summary-card h3 {
            color: white;
            font-size: 14px;
            margin-bottom: 8px;
            opacity: 0.9;
        }

        .summary-card .value {
            font-size: 36px;
            font-weight: bold;
        }

        .file-section {
            margin-bottom: 40px;
            border: 1px solid #ecf0f1;
            border-radius: 6px;
            overflow: hidden;
        }

        .file-header {
            background: #34495e;
            color: white;
            padding: 15px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .file-header:hover {
            background: #2c3e50;
        }

        .file-header h3 {
            color: white;
            margin: 0;
        }

        .file-stats {
            display: flex;
            gap: 20px;
            font-size: 14px;
        }

        .stat-badge {
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 12px;
        }

        .stat-badge.pass { background: #27ae60; }
        .stat-badge.warning { background: #f39c12; }
        .stat-badge.error { background: #e74c3c; }

        .file-content {
            padding: 20px;
            background: #fafafa;
        }

        .file-content.collapsed {
            display: none;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background: white;
            border-radius: 6px;
            overflow: hidden;
        }

        th {
            background: #3498db;
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

        .status-pass { color: #27ae60; font-weight: bold; }
        .status-warning { color: #f39c12; font-weight: bold; }
        .status-error { color: #e74c3c; font-weight: bold; }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .metric-card {
            background: white;
            border: 1px solid #ecf0f1;
            border-radius: 6px;
            padding: 15px;
        }

        .metric-card h4 {
            color: #34495e;
            margin-bottom: 10px;
            font-size: 14px;
        }

        .metric-row {
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            font-size: 13px;
        }

        .metric-label {
            color: #7f8c8d;
        }

        .metric-value {
            font-weight: 600;
            color: #2c3e50;
        }

        .progress-bar {
            height: 6px;
            background: #ecf0f1;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 8px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
            transition: width 0.3s ease;
        }

        .filters {
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
        }

        .filter-group {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        label {
            font-weight: 600;
            margin-right: 8px;
        }

        select, input {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }

        .timestamp {
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 20px;
            text-align: center;
        }

        .no-issues {
            color: #27ae60;
            font-size: 18px;
            padding: 30px;
            text-align: center;
            background: #d5f4e6;
            border-radius: 6px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 ENIGMA TSV Validation Report</h1>

        <!-- Summary Section -->
        <div class="summary">
            <div class="summary-card">
                <h3>Files Validated</h3>
                <div class="value">{{total_files}}</div>
            </div>
            <div class="summary-card success">
                <h3>Records Passed</h3>
                <div class="value">{{total_pass}}</div>
            </div>
            <div class="summary-card warning">
                <h3>Warnings</h3>
                <div class="value">{{total_warnings}}</div>
            </div>
            <div class="summary-card error">
                <h3>Errors</h3>
                <div class="value">{{total_errors}}</div>
            </div>
        </div>

        <!-- File Details -->
        <h2>📁 Validation Details by File</h2>
        {{file_sections}}

        <!-- Timestamp -->
        <div class="timestamp">
            Report generated: {{generation_time}}
        </div>
    </div>

    <script>
        // Toggle file sections
        document.querySelectorAll('.file-header').forEach(header => {
            header.addEventListener('click', () => {
                const content = header.nextElementSibling;
                content.classList.toggle('collapsed');
            });
        });

        // Expand all files with errors
        document.querySelectorAll('.file-section').forEach(section => {
            const errorBadge = section.querySelector('.stat-badge.error');
            if (errorBadge && parseInt(errorBadge.textContent.match(/\\d+/)[0]) > 0) {
                section.querySelector('.file-content').classList.remove('collapsed');
            }
        });
    </script>
</body>
</html>
"""


def generate_file_section(file_data: Dict[str, Any]) -> str:
    """Generate HTML for a single file section."""
    filename = file_data['filename']
    total_records = file_data['total_records']
    pass_count = file_data['pass_count']
    warning_count = file_data['warning_count']
    error_count = file_data['error_count']
    pass_rate = file_data['pass_rate']

    # File header
    html = f"""
    <div class="file-section">
        <div class="file-header">
            <h3>{filename}</h3>
            <div class="file-stats">
                <span class="stat-badge">{total_records} records</span>
                <span class="stat-badge pass">{pass_count} pass</span>
                <span class="stat-badge warning">{warning_count} warnings</span>
                <span class="stat-badge error">{error_count} errors</span>
                <span class="stat-badge">{pass_rate:.1%} pass rate</span>
            </div>
        </div>
        <div class="file-content collapsed">
    """

    # Show validation issues if any
    record_results = file_data.get('record_results', [])
    has_issues = any(r['results'] for r in record_results)

    if has_issues:
        html += """
            <h3>Validation Issues</h3>
            <table>
                <thead>
                    <tr>
                        <th>Line</th>
                        <th>Entity ID</th>
                        <th>Status</th>
                        <th>Field</th>
                        <th>Value</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
        """

        for record in record_results:
            for result in record['results']:
                status_class = f"status-{result['status'].lower()}"
                html += f"""
                    <tr>
                        <td>{record['record_line']}</td>
                        <td>{record.get('entity_id', 'N/A')}</td>
                        <td class="{status_class}">{result['status']}</td>
                        <td>{result.get('field', '')}</td>
                        <td>{result.get('value', '')[:50]}</td>
                        <td>{result['message']}</td>
                    </tr>
                """

        html += """
                </tbody>
            </table>
        """
    else:
        html += '<div class="no-issues">✅ No validation issues found - all records passed!</div>'

    # Quality metrics if available
    quality_metrics = file_data.get('quality_metrics', {})
    if quality_metrics:
        html += '<h3>Data Quality Metrics</h3><div class="metrics-grid">'

        for field_name, metrics in sorted(quality_metrics.items()):
            completeness = metrics.get('completeness', 0)
            html += f"""
            <div class="metric-card">
                <h4>{field_name}</h4>
                <div class="metric-row">
                    <span class="metric-label">Completeness:</span>
                    <span class="metric-value">{completeness:.1f}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {completeness}%"></div>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Non-empty:</span>
                    <span class="metric-value">{metrics.get('non_empty_count', 0)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Unique values:</span>
                    <span class="metric-value">{metrics.get('unique_count', 0)}</span>
                </div>
            </div>
            """

        html += '</div>'

    html += """
        </div>
    </div>
    """

    return html


def generate_html_report(json_data: Dict[str, Any]) -> str:
    """Generate complete HTML report from JSON data."""
    files = json_data.get('files', [])

    # Calculate totals
    total_files = len(files)
    total_pass = sum(f['pass_count'] for f in files)
    total_warnings = sum(f['warning_count'] for f in files)
    total_errors = sum(f['error_count'] for f in files)

    # Generate file sections
    file_sections = '\n'.join(generate_file_section(f) for f in files)

    # Fill template
    html = HTML_TEMPLATE
    html = html.replace('{{total_files}}', str(total_files))
    html = html.replace('{{total_pass}}', str(total_pass))
    html = html.replace('{{total_warnings}}', str(total_warnings))
    html = html.replace('{{total_errors}}', str(total_errors))
    html = html.replace('{{file_sections}}', file_sections)
    html = html.replace('{{generation_time}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    return html


def main():
    parser = argparse.ArgumentParser(
        description='Generate HTML report from JSON validation results'
    )
    parser.add_argument('json_file', help='JSON validation results file')
    parser.add_argument('--output', '-o',
                       help='Output HTML file (default: <json_file>.html)')

    args = parser.parse_args()

    # Load JSON data
    json_path = Path(args.json_file)
    if not json_path.exists():
        print(f"Error: JSON file not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(json_path, 'r') as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate HTML
    html_content = generate_html_report(json_data)

    # Save HTML
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = json_path.with_suffix('.html')

    try:
        with open(output_path, 'w') as f:
            f.write(html_content)
        print(f"✅ HTML report generated: {output_path}")
        print(f"📊 Open in browser: file://{output_path.absolute()}")
    except Exception as e:
        print(f"Error writing HTML: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
