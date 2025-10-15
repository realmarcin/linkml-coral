#!/usr/bin/env python3
"""
Query Provenance Tracker - Deep provenance tracking for ENIGMA database queries.

Records complete execution metadata for reproducibility and auditing:
- Who executed the query (user, system)
- When it was executed (timestamp)
- What query was run (command, parameters)
- What data was queried (database version, record counts)
- What results were obtained (summary statistics)
- System environment (Python version, dependencies, hardware)
"""

import json
import hashlib
import platform
import socket
import getpass
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import sys


class QueryProvenanceTracker:
    """Track and record query execution provenance."""

    def __init__(self, db_path: str, provenance_dir: str = "query_provenance"):
        """
        Initialize provenance tracker.

        Args:
            db_path: Path to the database being queried
            provenance_dir: Directory to store provenance records
        """
        self.db_path = Path(db_path)
        self.provenance_dir = Path(provenance_dir)
        self.provenance_dir.mkdir(exist_ok=True)

        self.execution_id = None
        self.start_time = None
        self.metadata = {}

    def start_query(
        self,
        query_type: str,
        parameters: Dict[str, Any],
        description: Optional[str] = None
    ) -> str:
        """
        Start tracking a query execution.

        Args:
            query_type: Type of query (e.g., 'unused_reads', 'lineage')
            parameters: Query parameters
            description: Human-readable description

        Returns:
            Execution ID for this query run
        """
        self.start_time = datetime.now()

        # Generate unique execution ID
        execution_data = f"{query_type}_{self.start_time.isoformat()}_{getpass.getuser()}"
        self.execution_id = hashlib.sha256(execution_data.encode()).hexdigest()[:16]

        # Gather system metadata
        self.metadata = {
            "execution": {
                "execution_id": self.execution_id,
                "start_time": self.start_time.isoformat(),
                "query_type": query_type,
                "description": description or f"{query_type} query",
                "parameters": parameters
            },
            "user": {
                "username": getpass.getuser(),
                "hostname": socket.gethostname(),
                "platform": platform.platform(),
                "python_version": sys.version
            },
            "database": {
                "path": str(self.db_path),
                "size_bytes": self.db_path.stat().st_size if self.db_path.exists() else None,
                "size_mb": round(self.db_path.stat().st_size / 1024 / 1024, 2) if self.db_path.exists() else None,
                "last_modified": datetime.fromtimestamp(
                    self.db_path.stat().st_mtime
                ).isoformat() if self.db_path.exists() else None,
                "checksum": self._compute_db_checksum() if self.db_path.exists() else None
            },
            "environment": self._get_environment_info()
        }

        return self.execution_id

    def record_database_stats(self, stats: Dict[str, Any]):
        """
        Record database statistics at query execution time.

        Args:
            stats: Database statistics (record counts, etc.)
        """
        self.metadata["database_stats"] = stats

    def end_query(
        self,
        results_summary: Dict[str, Any],
        output_files: Optional[Dict[str, str]] = None,
        error: Optional[str] = None
    ):
        """
        Complete query tracking and save provenance record.

        Args:
            results_summary: Summary of query results
            output_files: Paths to any output files created
            error: Error message if query failed
        """
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        self.metadata["execution"]["end_time"] = end_time.isoformat()
        self.metadata["execution"]["duration_seconds"] = duration
        self.metadata["execution"]["status"] = "error" if error else "success"

        if error:
            self.metadata["execution"]["error"] = error

        self.metadata["results"] = results_summary

        if output_files:
            self.metadata["outputs"] = output_files

        # Save provenance record
        self._save_provenance_record()

        return self.execution_id

    def _compute_db_checksum(self) -> str:
        """Compute SHA256 checksum of database file."""
        sha256_hash = hashlib.sha256()

        # Read in chunks to handle large files
        with open(self.db_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    def _get_environment_info(self) -> Dict[str, Any]:
        """Gather environment information."""
        try:
            import pkg_resources
            packages = {
                pkg.key: pkg.version
                for pkg in pkg_resources.working_set
                if pkg.key in ['linkml-store', 'linkml-runtime', 'duckdb', 'pandas', 'numpy']
            }
        except Exception:
            packages = {}

        return {
            "python_executable": sys.executable,
            "python_path": sys.path[:3],  # First 3 entries
            "platform_info": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "processor": platform.processor()
            },
            "key_packages": packages
        }

    def _save_provenance_record(self):
        """Save provenance record to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_type = self.metadata["execution"]["query_type"]
        filename = f"{timestamp}_{query_type}_{self.execution_id}.json"

        filepath = self.provenance_dir / filename

        with open(filepath, 'w') as f:
            json.dump(self.metadata, f, indent=2, default=str)

        # Also create a latest symlink/copy for easy access
        latest_file = self.provenance_dir / f"latest_{query_type}.json"
        with open(latest_file, 'w') as f:
            json.dump(self.metadata, f, indent=2, default=str)

        print(f"\n📋 Provenance record saved: {filepath}")
        print(f"   Execution ID: {self.execution_id}")

    @classmethod
    def load_provenance(cls, execution_id: str, provenance_dir: str = "query_provenance") -> Dict[str, Any]:
        """
        Load a provenance record by execution ID.

        Args:
            execution_id: Execution ID to load
            provenance_dir: Directory containing provenance records

        Returns:
            Provenance metadata dictionary
        """
        prov_dir = Path(provenance_dir)

        # Search for file with this execution ID
        for filepath in prov_dir.glob(f"*_{execution_id}.json"):
            with open(filepath) as f:
                return json.load(f)

        raise FileNotFoundError(f"No provenance record found for execution ID: {execution_id}")

    @classmethod
    def list_executions(cls, provenance_dir: str = "query_provenance") -> list:
        """
        List all tracked query executions.

        Args:
            provenance_dir: Directory containing provenance records

        Returns:
            List of provenance summaries
        """
        prov_dir = Path(provenance_dir)
        executions = []

        for filepath in sorted(prov_dir.glob("*.json"), reverse=True):
            if filepath.name.startswith("latest_"):
                continue

            try:
                with open(filepath) as f:
                    metadata = json.load(f)
                    executions.append({
                        "file": filepath.name,
                        "execution_id": metadata["execution"]["execution_id"],
                        "query_type": metadata["execution"]["query_type"],
                        "start_time": metadata["execution"]["start_time"],
                        "duration": metadata["execution"].get("duration_seconds"),
                        "status": metadata["execution"].get("status", "unknown"),
                        "user": metadata["user"]["username"]
                    })
            except Exception:
                continue

        return executions

    @classmethod
    def generate_provenance_report(cls, execution_id: str, provenance_dir: str = "query_provenance") -> str:
        """
        Generate human-readable provenance report.

        Args:
            execution_id: Execution ID to report on
            provenance_dir: Directory containing provenance records

        Returns:
            Formatted report string
        """
        metadata = cls.load_provenance(execution_id, provenance_dir)

        report = []
        report.append("="*70)
        report.append("QUERY EXECUTION PROVENANCE REPORT")
        report.append("="*70)
        report.append("")

        # Execution Info
        exec_info = metadata["execution"]
        report.append("EXECUTION INFORMATION")
        report.append("-" * 40)
        report.append(f"Execution ID:    {exec_info['execution_id']}")
        report.append(f"Query Type:      {exec_info['query_type']}")
        report.append(f"Description:     {exec_info.get('description', 'N/A')}")
        report.append(f"Start Time:      {exec_info['start_time']}")
        report.append(f"End Time:        {exec_info.get('end_time', 'N/A')}")
        report.append(f"Duration:        {exec_info.get('duration_seconds', 'N/A')} seconds")
        report.append(f"Status:          {exec_info.get('status', 'unknown').upper()}")
        report.append("")

        # Parameters
        report.append("QUERY PARAMETERS")
        report.append("-" * 40)
        for key, value in exec_info.get('parameters', {}).items():
            report.append(f"  {key}: {value}")
        report.append("")

        # User Info
        user_info = metadata["user"]
        report.append("USER & SYSTEM")
        report.append("-" * 40)
        report.append(f"User:            {user_info['username']}")
        report.append(f"Hostname:        {user_info['hostname']}")
        report.append(f"Platform:        {user_info['platform']}")
        report.append(f"Python:          {user_info['python_version'].split()[0]}")
        report.append("")

        # Database Info
        db_info = metadata["database"]
        report.append("DATABASE")
        report.append("-" * 40)
        report.append(f"Path:            {db_info['path']}")
        report.append(f"Size:            {db_info.get('size_mb', 'N/A')} MB")
        report.append(f"Last Modified:   {db_info.get('last_modified', 'N/A')}")
        report.append(f"Checksum:        {db_info.get('checksum', 'N/A')[:16]}...")
        report.append("")

        # Database Stats
        if "database_stats" in metadata:
            report.append("DATABASE STATISTICS AT EXECUTION")
            report.append("-" * 40)
            for key, value in metadata["database_stats"].items():
                report.append(f"  {key}: {value}")
            report.append("")

        # Results
        if "results" in metadata:
            report.append("RESULTS SUMMARY")
            report.append("-" * 40)
            for key, value in metadata["results"].items():
                if isinstance(value, dict):
                    report.append(f"  {key}:")
                    for k, v in value.items():
                        report.append(f"    {k}: {v}")
                else:
                    report.append(f"  {key}: {value}")
            report.append("")

        # Output Files
        if "outputs" in metadata:
            report.append("OUTPUT FILES")
            report.append("-" * 40)
            for key, path in metadata["outputs"].items():
                report.append(f"  {key}: {path}")
            report.append("")

        report.append("="*70)

        return "\n".join(report)


def main():
    """Demo/test the provenance tracker."""
    import argparse

    parser = argparse.ArgumentParser(description='Query Provenance Tracker')
    parser.add_argument('--list', action='store_true', help='List all tracked executions')
    parser.add_argument('--report', metavar='EXEC_ID', help='Generate report for execution ID')
    parser.add_argument('--provenance-dir', default='query_provenance',
                       help='Provenance directory (default: query_provenance)')

    args = parser.parse_args()

    if args.list:
        executions = QueryProvenanceTracker.list_executions(args.provenance_dir)
        print(f"\n📋 Query Execution History ({len(executions)} executions)\n")
        print(f"{'Date/Time':<20} {'Query Type':<20} {'Duration':<10} {'Status':<10} {'User':<15} {'ID':<16}")
        print("-" * 100)
        for exec in executions:
            start = exec['start_time'][:19].replace('T', ' ')
            duration = f"{exec.get('duration', 'N/A'):.1f}s" if exec.get('duration') else 'N/A'
            status = exec.get('status', 'unknown')
            print(f"{start:<20} {exec['query_type']:<20} {duration:<10} {status:<10} {exec['user']:<15} {exec['execution_id']:<16}")

    elif args.report:
        report = QueryProvenanceTracker.generate_provenance_report(args.report, args.provenance_dir)
        print(report)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
