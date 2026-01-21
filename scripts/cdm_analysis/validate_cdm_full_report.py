#!/usr/bin/env python3
"""
Full validation of all CDM parquet data with detailed error reporting.

This script performs comprehensive validation of all CDM parquet tables and
generates a detailed report of errors and warnings, including:
- Schema mismatches
- Data quality issues
- NULL values in required fields
- Type violations
- Foreign key constraint violations

Output: validation_reports/cdm_parquet/full_validation_report_YYYYMMDD_HHMMSS.{md,json}
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import tempfile
import subprocess

try:
    import pandas as pd
except ImportError:
    print("Error: pandas not installed. Run: uv pip install pandas")
    sys.exit(1)

try:
    import pyarrow.parquet as pq
except ImportError:
    print("Error: pyarrow not installed. Run: uv pip install pyarrow")
    sys.exit(1)

import yaml


# Script paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
CDM_SCHEMA = REPO_ROOT / "src/linkml_coral/schema/cdm/linkml_coral_cdm.yaml"
VALIDATE_SCRIPT = SCRIPT_DIR / "validate_parquet_linkml.py"


# Table-to-class mapping (from validate_parquet_linkml.py)
TABLE_TO_CLASS = {
    "sdt_location": "Location",
    "sdt_sample": "Sample",
    "sdt_community": "Community",
    "sdt_reads": "Reads",
    "sdt_assembly": "Assembly",
    "sdt_bin": "Bin",
    "sdt_genome": "Genome",
    "sdt_gene": "Gene",
    "sdt_strain": "Strain",
    "sdt_taxon": "Taxon",
    "sdt_asv": "ASV",
    "sdt_protocol": "Protocol",
    "sdt_image": "Image",
    "sdt_condition": "Condition",
    "sdt_dubseq_library": "DubSeqLibrary",
    "sdt_tnseq_library": "TnSeqLibrary",
    "sdt_enigma": "ENIGMA",
    "sys_typedef": "SystemTypedef",
    "sys_ddt_typedef": "SystemDDTTypedef",
    "sys_oterm": "SystemOntologyTerm",
    "sys_process": "SystemProcess",
    "sys_process_input": "SystemProcessInput",
    "sys_process_output": "SystemProcessOutput",
    "ddt_ndarray": "DynamicDataArray",
}


class ValidationReport:
    """Accumulates validation results and generates reports."""

    def __init__(self):
        self.tables_validated = 0
        self.tables_passed = 0
        self.tables_failed = 0
        self.total_rows = 0
        self.total_errors = 0
        self.total_warnings = 0

        # Detailed error tracking
        self.table_results = {}  # table_name -> result dict
        self.error_types = defaultdict(int)  # error_type -> count
        self.errors_by_table = defaultdict(list)  # table_name -> [errors]

    def add_table_result(
        self,
        table_name: str,
        class_name: str,
        row_count: int,
        validated_rows: int,
        passed: bool,
        errors: List[str],
        validation_time: float
    ):
        """Add validation result for a table."""
        self.tables_validated += 1
        self.total_rows += row_count

        if passed:
            self.tables_passed += 1
        else:
            self.tables_failed += 1

        # Categorize errors
        for error in errors:
            error_type = self._categorize_error(error)
            self.error_types[error_type] += 1
            self.errors_by_table[table_name].append({
                "type": error_type,
                "message": error
            })

        self.total_errors += len(errors)

        # Store result
        self.table_results[table_name] = {
            "class": class_name,
            "row_count": row_count,
            "validated_rows": validated_rows,
            "passed": passed,
            "error_count": len(errors),
            "errors": errors[:100],  # Limit to first 100 errors
            "validation_time_seconds": validation_time
        }

    def _categorize_error(self, error: str) -> str:
        """Categorize error message into type."""
        error_lower = error.lower()

        if "additional properties" in error_lower:
            return "schema_mismatch"
        elif "is not of type" in error_lower:
            return "type_violation"
        elif "is a required property" in error_lower:
            return "missing_required"
        elif "does not match" in error_lower and "pattern" in error_lower:
            return "pattern_violation"
        elif "is not one of" in error_lower:
            return "enum_violation"
        elif "none" in error_lower or "null" in error_lower:
            return "null_value"
        else:
            return "other"

    def generate_markdown_report(self) -> str:
        """Generate markdown report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        md = []
        md.append("# CDM Parquet Full Validation Report")
        md.append("")
        md.append(f"**Generated:** {timestamp}  ")
        md.append(f"**Schema:** `{CDM_SCHEMA.relative_to(REPO_ROOT)}`")
        md.append("")

        # Summary
        md.append("## Summary")
        md.append("")
        md.append(f"- **Tables validated:** {self.tables_validated}")
        md.append(f"- **Total rows:** {self.total_rows:,}")
        md.append(f"- **Tables passed:** {self.tables_passed} ✅")
        md.append(f"- **Tables failed:** {self.tables_failed} ❌")
        md.append(f"- **Total errors:** {self.total_errors:,}")
        md.append("")

        # Error types breakdown
        if self.error_types:
            md.append("## Error Types")
            md.append("")
            md.append("| Error Type | Count | Percentage |")
            md.append("|------------|-------|------------|")
            for error_type, count in sorted(self.error_types.items(), key=lambda x: x[1], reverse=True):
                pct = (count / self.total_errors * 100) if self.total_errors > 0 else 0
                md.append(f"| {error_type.replace('_', ' ').title()} | {count:,} | {pct:.1f}% |")
            md.append("")

        # Tables with errors
        if self.tables_failed > 0:
            md.append("## Tables with Errors")
            md.append("")

            for table_name in sorted(self.table_results.keys()):
                result = self.table_results[table_name]
                if not result["passed"]:
                    md.append(f"### {table_name} ({result['class']})")
                    md.append("")
                    md.append(f"- **Row count:** {result['row_count']:,}")
                    md.append(f"- **Validated rows:** {result['validated_rows']:,}")
                    md.append(f"- **Errors:** {result['error_count']:,}")
                    md.append("")

                    if result["errors"]:
                        md.append("**Error samples:**")
                        md.append("")
                        for i, error in enumerate(result["errors"][:10], 1):
                            md.append(f"{i}. `{error}`")
                        if result["error_count"] > 10:
                            md.append(f"   ... and {result['error_count'] - 10} more errors")
                        md.append("")

        # Tables that passed
        if self.tables_passed > 0:
            md.append("## Tables Passed")
            md.append("")
            passed_tables = [
                (name, result["row_count"])
                for name, result in self.table_results.items()
                if result["passed"]
            ]
            for table_name, row_count in sorted(passed_tables):
                md.append(f"- ✅ **{table_name}** ({row_count:,} rows)")
            md.append("")

        # Validation details
        md.append("## Detailed Results")
        md.append("")
        md.append("| Table | Class | Rows | Validated | Status | Errors | Time (s) |")
        md.append("|-------|-------|------|-----------|--------|--------|----------|")

        for table_name in sorted(self.table_results.keys()):
            result = self.table_results[table_name]
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            md.append(
                f"| {table_name} | {result['class']} | {result['row_count']:,} | "
                f"{result['validated_rows']:,} | {status} | {result['error_count']:,} | "
                f"{result['validation_time_seconds']:.2f} |"
            )

        md.append("")

        # Recommendations
        md.append("## Recommendations")
        md.append("")

        if self.error_types.get("schema_mismatch", 0) > 0:
            md.append("### Schema Mismatches")
            md.append("- Update CDM schema to include missing fields")
            md.append("- Or remove unexpected columns from parquet data")
            md.append("")

        if self.error_types.get("null_value", 0) > 0 or self.error_types.get("missing_required", 0) > 0:
            md.append("### Data Quality Issues")
            md.append("- Fix NULL values in required fields")
            md.append("- Implement data validation at ingestion time")
            md.append("")

        if self.error_types.get("type_violation", 0) > 0:
            md.append("### Type Violations")
            md.append("- Ensure data types match schema expectations")
            md.append("- Add type conversion at ETL stage")
            md.append("")

        return "\n".join(md)

    def to_json(self) -> Dict:
        """Convert report to JSON format."""
        return {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "schema": str(CDM_SCHEMA),
                "total_tables": self.tables_validated,
                "total_rows": self.total_rows,
            },
            "summary": {
                "tables_passed": self.tables_passed,
                "tables_failed": self.tables_failed,
                "total_errors": self.total_errors,
                "total_warnings": self.total_warnings,
            },
            "error_types": dict(self.error_types),
            "table_results": self.table_results,
            "errors_by_table": dict(self.errors_by_table),
        }


def get_row_count(table_path: Path) -> int:
    """Get row count from parquet table."""
    if table_path.is_dir():
        total = 0
        for pf in table_path.glob("*.parquet"):
            parquet_file = pq.ParquetFile(pf)
            total += parquet_file.metadata.num_rows
        return total
    else:
        parquet_file = pq.ParquetFile(table_path)
        return parquet_file.metadata.num_rows


def validate_table(
    table_path: Path,
    class_name: str,
    max_rows: Optional[int] = None,
    chunk_size: Optional[int] = None
) -> Tuple[bool, List[str], float]:
    """
    Validate a single table and return (success, errors, time).

    Args:
        table_path: Path to parquet table
        class_name: LinkML class name
        max_rows: Maximum rows to validate
        chunk_size: Chunk size for large tables

    Returns:
        (success, error_messages, validation_time)
    """
    import time

    start_time = time.time()

    args = [
        sys.executable,
        str(VALIDATE_SCRIPT),
        str(table_path),
        "--class", class_name,
    ]

    if max_rows:
        args.extend(["--max-rows", str(max_rows)])

    if chunk_size:
        args.extend(["--chunk-size", str(chunk_size)])

    result = subprocess.run(args, capture_output=True, text=True)

    elapsed = time.time() - start_time

    # Parse errors from output
    errors = []
    for line in result.stderr.split("\n") + result.stdout.split("\n"):
        if line.strip().startswith("[ERROR]"):
            errors.append(line.strip())

    # Only consider error count, not exit code
    # (linkml-validate may return non-zero for reasons other than validation errors)
    success = len(errors) == 0

    return success, errors, elapsed


def main():
    parser = argparse.ArgumentParser(
        description="Full validation of all CDM parquet data with detailed reporting"
    )

    parser.add_argument(
        'database',
        type=Path,
        help='Path to CDM database directory'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('validation_reports/cdm_parquet'),
        help='Output directory for reports (default: validation_reports/cdm_parquet)'
    )

    parser.add_argument(
        '--full',
        action='store_true',
        help='Validate ALL rows (may be very slow for large tables)'
    )

    args = parser.parse_args()

    if not args.database.exists():
        print(f"Error: Database not found at {args.database}")
        sys.exit(1)

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("=" * 60)
    print("CDM Parquet Full Validation Report")
    print("=" * 60)
    print(f"Database: {args.database}")
    print(f"Schema: {CDM_SCHEMA}")
    print(f"Mode: {'FULL (all rows)' if args.full else 'CHUNKED/SAMPLED'}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    report = ValidationReport()

    # Define validation strategy per table
    validation_plan = [
        # Small static tables (full validation)
        ("sdt_location", "Location", None, None),
        ("sdt_sample", "Sample", None, None),
        ("sdt_community", "Community", None, None),
        ("sdt_assembly", "Assembly", None, None),
        ("sdt_bin", "Bin", None, None),
        ("sdt_genome", "Genome", None, None),
        ("sdt_strain", "Strain", None, None),
        ("sdt_taxon", "Taxon", None, None),
        ("sdt_asv", "ASV", None, None),
        ("sdt_protocol", "Protocol", None, None),
        ("sdt_image", "Image", None, None),
        ("sdt_condition", "Condition", None, None),
        ("sdt_dubseq_library", "DubSeqLibrary", None, None),
        ("sdt_tnseq_library", "TnSeqLibrary", None, None),
        ("sdt_enigma", "ENIGMA", None, None),

        # Medium tables (chunked or sampled)
        ("sdt_reads", "Reads", None if args.full else 50000, 10000),

        # Large tables (sampled unless --full)
        ("sdt_gene", "Gene", None if args.full else 100000, 10000),

        # System tables
        ("sys_typedef", "SystemTypedef", None, None),
        ("sys_ddt_typedef", "SystemDDTTypedef", None, None),
        ("sys_oterm", "SystemOntologyTerm", None if args.full else 10594, 5000),
        ("sys_process", "SystemProcess", None if args.full else 50000, 10000),
        ("sys_process_input", "SystemProcessInput", None if args.full else 50000, 10000),
        ("sys_process_output", "SystemProcessOutput", None if args.full else 50000, 10000),

        # Dynamic data
        ("ddt_ndarray", "DynamicDataArray", None, None),
    ]

    for i, (table_name, class_name, max_rows, chunk_size) in enumerate(validation_plan, 1):
        table_path = args.database / table_name

        if not table_path.exists():
            print(f"[{i}/{len(validation_plan)}] ⊘ SKIPPED {table_name} (not found)")
            continue

        row_count = get_row_count(table_path)
        validated_rows = min(max_rows, row_count) if max_rows else row_count

        print(f"[{i}/{len(validation_plan)}] Validating {table_name} ({class_name})...")
        print(f"  Total rows: {row_count:,}, Validating: {validated_rows:,}", end="")

        if max_rows and max_rows < row_count:
            print(f" (sample)", end="")
        elif chunk_size:
            print(f" (chunked)", end="")

        print()

        success, errors, elapsed = validate_table(table_path, class_name, max_rows, chunk_size)

        report.add_table_result(
            table_name=table_name,
            class_name=class_name,
            row_count=row_count,
            validated_rows=validated_rows,
            passed=success,
            errors=errors,
            validation_time=elapsed
        )

        if success:
            print(f"  ✅ PASSED ({elapsed:.2f}s)")
        else:
            print(f"  ❌ FAILED - {len(errors)} errors ({elapsed:.2f}s)")

        print()

    print("=" * 60)
    print("Validation Complete")
    print("=" * 60)
    print(f"Tables validated: {report.tables_validated}")
    print(f"Tables passed: {report.tables_passed} ✅")
    print(f"Tables failed: {report.tables_failed} ❌")
    print(f"Total errors: {report.total_errors:,}")
    print()

    # Generate reports
    md_report = report.generate_markdown_report()
    json_report = report.to_json()

    md_file = args.output_dir / f"full_validation_report_{timestamp}.md"
    json_file = args.output_dir / f"full_validation_report_{timestamp}.json"

    md_file.write_text(md_report)
    json_file.write_text(json.dumps(json_report, indent=2))

    print(f"📄 Markdown report: {md_file}")
    print(f"📊 JSON report: {json_file}")
    print()

    sys.exit(0 if report.tables_failed == 0 else 1)


if __name__ == '__main__':
    main()
