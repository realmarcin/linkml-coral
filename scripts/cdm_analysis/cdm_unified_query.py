#!/usr/bin/env python3
"""
Unified CDM Query Tool - Intelligent Query Interface

Automatically chooses between fast SQL translation and schema-aware queries
based on query complexity.

Usage:
    python cdm_unified_query.py --db cdm_store.db "How many samples?"
    python cdm_unified_query.py --db cdm_store.db "Find samples with their locations"
    python cdm_unified_query.py --db cdm_store.db --explore Sample
"""

import argparse
import sys
import re
from pathlib import Path
from typing import Optional

# Import both query tools
try:
    from nl_sql_query import NaturalLanguageSQLQuery, format_results_text as format_nl
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from nl_sql_query import NaturalLanguageSQLQuery, format_results_text as format_nl

try:
    from schema_aware_query import SchemaAwareQuery, format_results_text as format_schema
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from schema_aware_query import SchemaAwareQuery, format_results_text as format_schema


class UnifiedCDMQuery:
    """Unified query interface with automatic strategy selection."""

    # Keywords that indicate complex queries
    COMPLEX_INDICATORS = [
        r'\bwith their\b',
        r'\band their\b',
        r'\brelated to\b',
        r'\btrace\b',
        r'\blineage\b',
        r'\bpipeline\b',
        r'\bprovenance\b',
        r'\bjoin\b',
        r'\bwhat is\b',
        r'\bexplain\b',
        r'\bshow.*relationship\b',
        r'\bhow.*related\b',
    ]

    # Keywords for schema exploration
    SCHEMA_INDICATORS = [
        r'\bwhat (is|are) (the )?(class|entity|table)\b',
        r'\bexplain (the )?(class|entity|schema)\b',
        r'\bshow (me )?(the )?(schema|classes|entities|tables)\b',
        r'\bwhat fields\b',
        r'\bwhat columns\b',
        r'\bwhat attributes\b',
        r'\brelationships?\b',
    ]

    def __init__(
        self,
        db_path: str,
        schema_path: str = "src/linkml_coral/schema/linkml_coral.yaml",
        api_key: Optional[str] = None,
        verbose: bool = False
    ):
        """
        Initialize unified query interface.

        Args:
            db_path: Path to DuckDB database
            schema_path: Path to LinkML schema
            api_key: Anthropic API key
            verbose: Enable verbose output
        """
        self.db_path = db_path
        self.schema_path = schema_path
        self.api_key = api_key
        self.verbose = verbose

        # Lazy initialization of query tools
        self._nl_query = None
        self._schema_query = None

    def get_nl_query(self):
        """Lazy initialize NL query tool."""
        if self._nl_query is None:
            self._nl_query = NaturalLanguageSQLQuery(
                self.db_path,
                self.api_key,
                self.verbose
            )
        return self._nl_query

    def get_schema_query(self):
        """Lazy initialize schema-aware query tool."""
        if self._schema_query is None:
            self._schema_query = SchemaAwareQuery(
                self.db_path,
                self.schema_path,
                self.api_key,
                self.verbose
            )
        return self._schema_query

    def detect_query_type(self, query: str) -> str:
        """
        Detect whether query is simple, complex, or schema-related.

        Args:
            query: User's natural language query

        Returns:
            'simple', 'complex', or 'schema'
        """
        query_lower = query.lower()

        # Check for schema exploration
        for pattern in self.SCHEMA_INDICATORS:
            if re.search(pattern, query_lower):
                return 'schema'

        # Check for complex query indicators
        for pattern in self.COMPLEX_INDICATORS:
            if re.search(pattern, query_lower):
                return 'complex'

        # Count entity mentions (rough heuristic)
        entities = ['sample', 'location', 'reads', 'assembly', 'genome', 'gene', 'community', 'taxon']
        entity_count = sum(1 for entity in entities if entity in query_lower)

        if entity_count > 1:
            return 'complex'

        # Default to simple
        return 'simple'

    def query(self, natural_query: str, force_strategy: Optional[str] = None):
        """
        Execute query with automatic or forced strategy selection.

        Args:
            natural_query: User's question
            force_strategy: Force 'fast' or 'schema' strategy

        Returns:
            Query results dictionary
        """
        if force_strategy:
            strategy = 'complex' if force_strategy == 'schema' else 'simple'
        else:
            strategy = self.detect_query_type(natural_query)

        if self.verbose:
            strategy_name = {
                'simple': 'Fast SQL Translation',
                'complex': 'Schema-Aware Query',
                'schema': 'Schema Exploration'
            }[strategy]
            print(f"\n🎯 Strategy: {strategy_name}", file=sys.stderr)

        try:
            if strategy == 'simple':
                result = self.get_nl_query().query(natural_query)
                result['strategy'] = 'fast'
                return result
            else:
                result = self.get_schema_query().query(natural_query)
                result['strategy'] = 'schema-aware'
                return result
        except Exception as e:
            # If fast path fails, try schema-aware
            if strategy == 'simple' and self.verbose:
                print(f"\n⚠️  Fast path failed, trying schema-aware: {e}", file=sys.stderr)
                result = self.get_schema_query().query(natural_query)
                result['strategy'] = 'schema-aware (fallback)'
                return result
            raise

    def explore_schema(self, class_name: Optional[str] = None):
        """Explore schema information."""
        schema_query = self.get_schema_query()
        if class_name:
            return schema_query.explore_class(class_name)
        else:
            return schema_query.show_schema_info()

    def suggest_queries(self):
        """Get query suggestions."""
        return self.get_schema_query().suggest_queries()

    def close(self):
        """Close database connections."""
        if self._nl_query:
            self._nl_query.close()
        if self._schema_query:
            self._schema_query.close()


def main():
    parser = argparse.ArgumentParser(
        description="Unified CDM Query Tool - Intelligent Query Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detection (recommended)
  python cdm_unified_query.py --db cdm_store.db "How many samples?"
  python cdm_unified_query.py --db cdm_store.db "Find samples with their locations"

  # Force strategy
  python cdm_unified_query.py --db cdm_store.db "Count samples" --fast
  python cdm_unified_query.py --db cdm_store.db "Simple query" --schema-aware

  # Schema exploration
  python cdm_unified_query.py --db cdm_store.db --explore Sample
  python cdm_unified_query.py --db cdm_store.db --info
        """
    )

    parser.add_argument(
        'query',
        type=str,
        nargs='?',
        help='Natural language query'
    )

    parser.add_argument(
        '--db',
        type=str,
        default='cdm_store.db',
        help='Path to DuckDB database file'
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
        help='Anthropic API key'
    )

    parser.add_argument(
        '--fast',
        action='store_true',
        help='Force fast SQL translation strategy'
    )

    parser.add_argument(
        '--schema-aware',
        action='store_true',
        help='Force schema-aware strategy'
    )

    parser.add_argument(
        '--explore',
        type=str,
        metavar='CLASS',
        help='Explore a specific class'
    )

    parser.add_argument(
        '--info',
        action='store_true',
        help='Show schema information'
    )

    parser.add_argument(
        '--suggest',
        action='store_true',
        help='Get query suggestions'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Check database exists
    if not Path(args.db).exists():
        print(f"Error: Database not found: {args.db}", file=sys.stderr)
        sys.exit(1)

    # Check schema exists for schema operations
    if (args.schema_aware or args.explore or args.info or args.suggest) and not Path(args.schema).exists():
        print(f"Error: Schema not found: {args.schema}", file=sys.stderr)
        sys.exit(1)

    try:
        tool = UnifiedCDMQuery(
            db_path=args.db,
            schema_path=args.schema,
            api_key=args.api_key,
            verbose=args.verbose
        )

        # Handle different operations
        if args.info:
            print(tool.explore_schema())
        elif args.explore:
            print(tool.explore_schema(args.explore))
        elif args.suggest:
            print(tool.suggest_queries())
        elif args.query:
            force_strategy = None
            if args.fast:
                force_strategy = 'fast'
            elif args.schema_aware:
                force_strategy = 'schema'

            result = tool.query(args.query, force_strategy)

            if args.json:
                import json
                print(json.dumps(result, indent=2, default=str))
            else:
                # Use appropriate formatter
                if result.get('strategy', '').startswith('fast'):
                    print(format_nl(result))
                else:
                    print(format_schema(result))

                if args.verbose:
                    print(f"\n📊 Strategy used: {result.get('strategy', 'unknown')}", file=sys.stderr)
        else:
            parser.print_help()

        tool.close()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
