#!/usr/bin/env python3
"""
Schema-Aware Query Tool for CDM DuckDB Database

This tool uses the LinkML schema to provide intelligent, schema-aware querying
of the CDM DuckDB database. It understands the data model, relationships,
and semantics defined in the LinkML schema.

Usage:
    # Query with schema awareness
    python schema_aware_query.py --db cdm_store.db "Find samples from Location0000001"

    # Show schema information
    python schema_aware_query.py --db cdm_store.db --show-schema

    # Explore relationships
    python schema_aware_query.py --db cdm_store.db --explore-class Sample

    # Generate query suggestions
    python schema_aware_query.py --db cdm_store.db --suggest-queries
"""

import argparse
import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import duckdb

try:
    from linkml_runtime.utils.schemaview import SchemaView
except ImportError:
    print("Error: linkml-runtime package not installed.", file=sys.stderr)
    print("Install it with: uv sync", file=sys.stderr)
    sys.exit(1)

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed.", file=sys.stderr)
    print("Install it with: uv sync", file=sys.stderr)
    sys.exit(1)


class SchemaAwareQuery:
    """Schema-aware query interface using LinkML schema."""

    def __init__(
        self,
        db_path: str,
        schema_path: str,
        api_key: Optional[str] = None,
        verbose: bool = False
    ):
        """
        Initialize schema-aware query tool.

        Args:
            db_path: Path to DuckDB database
            schema_path: Path to LinkML schema YAML file
            api_key: Anthropic API key
            verbose: Enable verbose output
        """
        self.db_path = db_path
        self.schema_path = schema_path
        self.verbose = verbose
        self.conn = duckdb.connect(db_path, read_only=True)

        # Load LinkML schema
        if self.verbose:
            print(f"Loading LinkML schema from {schema_path}...", file=sys.stderr)
        self.schema_view = SchemaView(schema_path)

        # Initialize Anthropic client
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass --api-key parameter."
            )
        self.client = Anthropic(api_key=api_key)

    def get_schema_context(self) -> Dict[str, Any]:
        """Extract comprehensive schema context from LinkML schema."""
        context = {
            'classes': {},
            'relationships': [],
            'enums': {}
        }

        # Get all classes
        for class_name in self.schema_view.all_classes():
            cls = self.schema_view.get_class(class_name)

            class_info = {
                'name': class_name,
                'description': cls.description or '',
                'slots': {},
                'relationships': []
            }

            # Get slots (attributes)
            for slot_name in self.schema_view.class_slots(class_name):
                slot = self.schema_view.induced_slot(slot_name, class_name)

                slot_info = {
                    'name': slot_name,
                    'description': slot.description or '',
                    'range': slot.range,
                    'required': slot.required or False,
                    'multivalued': slot.multivalued or False,
                }

                # Check if it's a foreign key (range is another class)
                if slot.range in self.schema_view.all_classes():
                    slot_info['is_foreign_key'] = True
                    slot_info['target_class'] = slot.range
                    class_info['relationships'].append({
                        'from': class_name,
                        'to': slot.range,
                        'via': slot_name,
                        'required': slot.required or False
                    })

                class_info['slots'][slot_name] = slot_info

            context['classes'][class_name] = class_info

        # Get enums
        for enum_name in self.schema_view.all_enums():
            enum = self.schema_view.get_enum(enum_name)
            context['enums'][enum_name] = {
                'name': enum_name,
                'description': enum.description or '',
                'values': list(enum.permissible_values.keys()) if enum.permissible_values else []
            }

        return context

    def format_schema_for_prompt(self, context: Dict[str, Any]) -> str:
        """Format schema context for Claude prompt."""
        lines = ["LinkML Schema Information:\n"]

        lines.append("## Classes (Entities):\n")
        for class_name, class_info in sorted(context['classes'].items()):
            lines.append(f"\n### {class_name}")
            if class_info['description']:
                lines.append(f"Description: {class_info['description']}")

            lines.append("\nAttributes:")
            for slot_name, slot_info in class_info['slots'].items():
                required = " (REQUIRED)" if slot_info['required'] else ""
                fk = f" → FK to {slot_info['target_class']}" if slot_info.get('is_foreign_key') else ""
                lines.append(f"  - {slot_name}: {slot_info['range']}{required}{fk}")
                if slot_info['description']:
                    lines.append(f"    {slot_info['description']}")

        lines.append("\n## Relationships:\n")
        for class_name, class_info in sorted(context['classes'].items()):
            if class_info['relationships']:
                for rel in class_info['relationships']:
                    lines.append(f"  {rel['from']}.{rel['via']} → {rel['to']}")

        return "\n".join(lines)

    def get_database_schema(self) -> Dict[str, Any]:
        """Get actual database schema (tables and columns)."""
        db_schema = {'tables': {}}

        # Get all tables
        tables_result = self.conn.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'main'
            ORDER BY table_name
        """).fetchall()

        for (table_name,) in tables_result:
            # Get column information
            columns_result = self.conn.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """).fetchall()

            db_schema['tables'][table_name] = {
                'columns': [col for col, dtype in columns_result]
            }

        return db_schema

    def translate_to_sql(self, natural_query: str) -> str:
        """
        Translate natural language query to SQL using schema context.

        Args:
            natural_query: User's natural language question

        Returns:
            SQL query string
        """
        schema_context = self.get_schema_context()
        schema_text = self.format_schema_for_prompt(schema_context)
        db_schema = self.get_database_schema()

        # Format database tables
        db_tables = "\n".join([
            f"  - {table}: {', '.join(info['columns'])}"
            for table, info in sorted(db_schema['tables'].items())
        ])

        prompt = f"""You are a SQL expert with deep knowledge of the LinkML ENIGMA CDM schema.

{schema_text}

## Database Tables:
{db_tables}

## Table Naming Convention:
- Static entities: sdt_<class_name> (e.g., Sample → sdt_sample)
- System tables: sys_<table_name>
- Dynamic tables: ddt_<table_name>

## Important Guidelines:
1. Use the LinkML schema to understand relationships and data semantics
2. Generate proper JOINs based on foreign key relationships defined in schema
3. Use descriptive column aliases based on schema descriptions
4. Include LIMIT 100 unless user asks for more
5. Consider required fields and multivalued attributes
6. Use CDM table naming (sdt_*, sys_*, ddt_*)

Natural language query: {natural_query}

Generate ONLY the SQL query (no explanations):"""

        if self.verbose:
            print(f"Sending schema-aware prompt to Claude API...", file=sys.stderr)

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            sql_query = response.content[0].text.strip()

            # Remove markdown code blocks if present
            if sql_query.startswith("```"):
                lines = sql_query.split("\n")
                sql_query = "\n".join(lines[1:-1]) if len(lines) > 2 else sql_query
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            return sql_query

        except Exception as e:
            raise RuntimeError(f"Failed to translate query: {e}")

    def execute_sql(self, sql_query: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results."""
        try:
            result = self.conn.execute(sql_query).fetchall()
            columns = [desc[0] for desc in self.conn.description]

            return [
                dict(zip(columns, row))
                for row in result
            ]
        except Exception as e:
            raise RuntimeError(f"SQL execution failed: {e}\nQuery: {sql_query}")

    def query(self, natural_query: str) -> Dict[str, Any]:
        """Execute schema-aware natural language query."""
        if self.verbose:
            print(f"\n🔍 Schema-aware query: {natural_query}", file=sys.stderr)

        # Translate to SQL
        sql_query = self.translate_to_sql(natural_query)

        if self.verbose:
            print(f"\n📝 Generated SQL:\n{sql_query}\n", file=sys.stderr)

        # Execute SQL
        results = self.execute_sql(sql_query)

        if self.verbose:
            print(f"✅ Query returned {len(results)} rows\n", file=sys.stderr)

        return {
            'natural_query': natural_query,
            'sql_query': sql_query,
            'result_count': len(results),
            'results': results
        }

    def show_schema_info(self) -> str:
        """Display schema information."""
        context = self.get_schema_context()

        lines = ["# ENIGMA CDM LinkML Schema\n"]

        lines.append(f"Total Classes: {len(context['classes'])}")
        lines.append(f"Total Enums: {len(context['enums'])}\n")

        lines.append("## Classes:\n")
        for class_name, class_info in sorted(context['classes'].items()):
            lines.append(f"\n### {class_name}")
            if class_info['description']:
                lines.append(f"{class_info['description']}")
            lines.append(f"  Attributes: {len(class_info['slots'])}")
            lines.append(f"  Relationships: {len(class_info['relationships'])}")

        return "\n".join(lines)

    def explore_class(self, class_name: str) -> str:
        """Explore a specific class in detail."""
        context = self.get_schema_context()

        if class_name not in context['classes']:
            return f"Error: Class '{class_name}' not found in schema"

        class_info = context['classes'][class_name]
        lines = [f"# {class_name}\n"]

        if class_info['description']:
            lines.append(f"{class_info['description']}\n")

        lines.append("## Attributes:\n")
        for slot_name, slot_info in sorted(class_info['slots'].items()):
            required = " (REQUIRED)" if slot_info['required'] else ""
            multi = " (MULTIVALUED)" if slot_info['multivalued'] else ""
            lines.append(f"- **{slot_name}**: {slot_info['range']}{required}{multi}")
            if slot_info['description']:
                lines.append(f"  {slot_info['description']}")

        if class_info['relationships']:
            lines.append("\n## Relationships:\n")
            for rel in class_info['relationships']:
                lines.append(f"- {rel['via']} → {rel['to']}")

        return "\n".join(lines)

    def suggest_queries(self) -> str:
        """Generate query suggestions based on schema."""
        context = self.get_schema_context()

        lines = ["# Query Suggestions\n"]
        lines.append("Based on the LinkML schema, here are useful queries:\n")

        # Basic counts
        lines.append("## Basic Statistics:\n")
        for class_name in sorted(context['classes'].keys()):
            lines.append(f"- Count {class_name} records")

        # Relationship queries
        lines.append("\n## Relationship Queries:\n")
        for class_name, class_info in sorted(context['classes'].items()):
            for rel in class_info['relationships']:
                lines.append(f"- Find {class_name} records with their {rel['to']} information")

        return "\n".join(lines)

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


def format_results_text(query_result: Dict[str, Any]) -> str:
    """Format query results as human-readable text."""
    lines = []

    lines.append(f"Query: {query_result['natural_query']}")
    lines.append(f"\nGenerated SQL:\n{query_result['sql_query']}")
    lines.append(f"\nResults ({query_result['result_count']} rows):")

    if not query_result['results']:
        lines.append("  (no results)")
        return "\n".join(lines)

    # Get column widths
    results = query_result['results']
    columns = list(results[0].keys())
    col_widths = {
        col: max(len(col), max(len(str(row.get(col, ''))) for row in results[:20]))
        for col in columns
    }

    # Header
    header = " | ".join(f"{col:{col_widths[col]}}" for col in columns)
    lines.append(f"\n{header}")
    lines.append("-" * len(header))

    # Rows (limit to first 50 for display)
    for row in results[:50]:
        row_str = " | ".join(f"{str(row.get(col, '')):{col_widths[col]}}" for col in columns)
        lines.append(row_str)

    if len(results) > 50:
        lines.append(f"\n... and {len(results) - 50} more rows")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Schema-Aware Query Tool for CDM DuckDB Database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Schema-aware query
  python schema_aware_query.py --db cdm_store.db "Find samples from Location0000001"

  # Show schema information
  python schema_aware_query.py --db cdm_store.db --show-schema

  # Explore a specific class
  python schema_aware_query.py --db cdm_store.db --explore-class Sample

  # Get query suggestions
  python schema_aware_query.py --db cdm_store.db --suggest-queries
        """
    )

    parser.add_argument(
        'query',
        type=str,
        nargs='?',
        help='Natural language query (if not using --show-schema or --explore-class)'
    )

    parser.add_argument(
        '--db',
        type=str,
        default='cdm_store.db',
        help='Path to DuckDB database file (default: cdm_store.db)'
    )

    parser.add_argument(
        '--schema',
        type=str,
        default='src/linkml_coral/schema/linkml_coral.yaml',
        help='Path to LinkML schema file'
    )

    parser.add_argument(
        '--api-key',
        type=str,
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )

    parser.add_argument(
        '--show-schema',
        action='store_true',
        help='Display schema information'
    )

    parser.add_argument(
        '--explore-class',
        type=str,
        metavar='CLASS',
        help='Explore a specific class in detail'
    )

    parser.add_argument(
        '--suggest-queries',
        action='store_true',
        help='Generate query suggestions'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Check database and schema exist
    if not Path(args.db).exists():
        print(f"Error: Database not found: {args.db}", file=sys.stderr)
        print(f"Create it with: just load-cdm-store-bricks-64gb", file=sys.stderr)
        sys.exit(1)

    if not Path(args.schema).exists():
        print(f"Error: Schema not found: {args.schema}", file=sys.stderr)
        sys.exit(1)

    try:
        # Initialize tool
        tool = SchemaAwareQuery(
            db_path=args.db,
            schema_path=args.schema,
            api_key=args.api_key,
            verbose=args.verbose
        )

        # Handle different operations
        if args.show_schema:
            print(tool.show_schema_info())
        elif args.explore_class:
            print(tool.explore_class(args.explore_class))
        elif args.suggest_queries:
            print(tool.suggest_queries())
        elif args.query:
            result = tool.query(args.query)
            if args.json:
                print(json.dumps(result, indent=2, default=str))
            else:
                print(format_results_text(result))
        else:
            parser.print_help()
            sys.exit(1)

        tool.close()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
