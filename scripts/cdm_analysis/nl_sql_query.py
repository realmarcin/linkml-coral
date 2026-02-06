#!/usr/bin/env python3
"""
Natural Language SQL Query Tool for CDM DuckDB Database

This tool takes natural language queries, translates them to SQL using Claude API,
and executes them against the CDM DuckDB database.

Usage:
    # Basic query
    python nl_sql_query.py --db cdm_store.db "How many samples are there?"

    # Query with table schema inspection
    python nl_sql_query.py --db cdm_store.db "Show me samples from Location0000001"

    # With verbose output
    python nl_sql_query.py --db cdm_store.db "Find reads with high read counts" --verbose

    # Output as JSON
    python nl_sql_query.py --db cdm_store.db "List all locations" --json
"""

import argparse
import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import duckdb

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed.", file=sys.stderr)
    print("Install it with: uv add anthropic", file=sys.stderr)
    sys.exit(1)


class NaturalLanguageSQLQuery:
    """Natural language to SQL query translator and executor."""

    def __init__(self, db_path: str, api_key: Optional[str] = None, verbose: bool = False):
        """
        Initialize the NL SQL query tool.

        Args:
            db_path: Path to DuckDB database
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
            verbose: Enable verbose output
        """
        self.db_path = db_path
        self.verbose = verbose
        self.conn = duckdb.connect(db_path, read_only=True)

        # Initialize Anthropic client
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass --api-key parameter."
            )
        self.client = Anthropic(api_key=api_key)

        # Cache schema information
        self._schema_cache = None

    def get_database_schema(self) -> Dict[str, Any]:
        """Get database schema information (tables, columns, types)."""
        if self._schema_cache:
            return self._schema_cache

        schema = {
            'tables': {},
            'table_counts': {}
        }

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

            schema['tables'][table_name] = {
                'columns': [
                    {'name': col, 'type': dtype}
                    for col, dtype in columns_result
                ]
            }

            # Get row count
            try:
                count = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
                schema['table_counts'][table_name] = count
            except:
                schema['table_counts'][table_name] = 0

        self._schema_cache = schema
        return schema

    def format_schema_for_prompt(self, schema: Dict[str, Any]) -> str:
        """Format schema information for the Claude prompt."""
        lines = ["Available tables and their structure:\n"]

        for table_name, table_info in sorted(schema['tables'].items()):
            count = schema['table_counts'].get(table_name, 0)
            lines.append(f"\n{table_name} ({count:,} rows):")

            for col in table_info['columns']:
                lines.append(f"  - {col['name']}: {col['type']}")

        return "\n".join(lines)

    def translate_to_sql(self, natural_query: str) -> str:
        """
        Translate natural language query to SQL using Claude API.

        Args:
            natural_query: User's natural language question

        Returns:
            SQL query string
        """
        schema = self.get_database_schema()
        schema_text = self.format_schema_for_prompt(schema)

        prompt = f"""You are a SQL expert. Convert the following natural language query into a valid DuckDB SQL query.

Database Schema:
{schema_text}

Important notes:
- Use proper DuckDB SQL syntax
- Return ONLY the SQL query, no explanations or markdown
- Use appropriate JOINs when querying related tables
- Limit results to 100 rows unless the user asks for more
- For CDM tables: sdt_* = static data tables, sys_* = system tables, ddt_* = dynamic brick tables
- Common foreign key patterns: sample_id, location_id, reads_id, assembly_id, etc.

Natural language query: {natural_query}

SQL query:"""

        if self.verbose:
            print(f"Sending prompt to Claude API...", file=sys.stderr)

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
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
        """
        Execute SQL query and return results.

        Args:
            sql_query: SQL query string

        Returns:
            List of result rows as dictionaries
        """
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
        """
        Complete natural language query pipeline.

        Args:
            natural_query: User's natural language question

        Returns:
            Dictionary with sql, results, and metadata
        """
        if self.verbose:
            print(f"\n🤔 Natural language query: {natural_query}", file=sys.stderr)

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

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


def format_results_text(query_result: Dict[str, Any]) -> str:
    """Format query results as human-readable text."""
    lines = []

    lines.append(f"Natural Query: {query_result['natural_query']}")
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
        description="Natural Language SQL Query Tool for CDM DuckDB Database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic queries
  python nl_sql_query.py --db cdm_store.db "How many samples are there?"
  python nl_sql_query.py --db cdm_store.db "Show me the top 10 locations by sample count"

  # Complex queries
  python nl_sql_query.py --db cdm_store.db "Find samples with depth greater than 100"
  python nl_sql_query.py --db cdm_store.db "List all reads with read_count over 50000"

  # JSON output
  python nl_sql_query.py --db cdm_store.db "Count assemblies by type" --json
        """
    )

    parser.add_argument(
        'query',
        type=str,
        help='Natural language query'
    )

    parser.add_argument(
        '--db',
        type=str,
        default='cdm_store.db',
        help='Path to DuckDB database file (default: cdm_store.db)'
    )

    parser.add_argument(
        '--api-key',
        type=str,
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
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

    # Check database exists
    if not Path(args.db).exists():
        print(f"Error: Database not found: {args.db}", file=sys.stderr)
        print(f"Create it with: just load-cdm-store-bricks-64gb", file=sys.stderr)
        sys.exit(1)

    try:
        # Initialize query tool
        nl_sql = NaturalLanguageSQLQuery(
            db_path=args.db,
            api_key=args.api_key,
            verbose=args.verbose
        )

        # Execute query
        result = nl_sql.query(args.query)

        # Output results
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(format_results_text(result))

        nl_sql.close()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
