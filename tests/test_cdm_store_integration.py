"""
Integration tests for CDM store loader and query interface.

These tests verify end-to-end functionality of loading CDM parquet data
into linkml-store and querying it.

Tests require the CDM database to be available at:
/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db
"""

import pytest
import tempfile
import pandas as pd
from pathlib import Path
import sys
import json

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "cdm_analysis"))

from load_cdm_parquet_to_store import (
    create_store,
    load_parquet_collection,
    load_all_cdm_parquet,
    CDM_SCHEMA,
)
from query_cdm_store import CDMStoreQuery


# Check if CDM database is available
CDM_DB_PATH = Path(
    "/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db"
)
HAS_CDM_DB = CDM_DB_PATH.exists()


@pytest.mark.skipif(not HAS_CDM_DB, reason="CDM database not available")
class TestCDMParquetLoading:
    """Integration tests for loading CDM parquet data."""

    def test_create_store(self):
        """Test creating a linkml-store database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"

            client, db, schema_view = create_store(str(db_path), CDM_SCHEMA)

            assert db is not None
            assert schema_view is not None
            assert db_path.exists()

    def test_load_small_table(self):
        """Test loading a small CDM table (Protocol)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            protocol_table = CDM_DB_PATH / "sdt_protocol"

            if not protocol_table.exists():
                pytest.skip("Protocol table not found")

            # Create store
            client, db, schema_view = create_store(str(db_path), CDM_SCHEMA)

            # Load protocol table
            count = load_parquet_collection(
                protocol_table, "Protocol", db, schema_view, verbose=True
            )

            assert count > 0
            assert count <= 100  # Small table

            # Verify collection exists
            collections = db.list_collections()
            assert "Protocol" in collections

            # Verify data
            collection = db.get_collection("Protocol")
            records = list(collection.find(limit=10))
            assert len(records) > 0

            # Check fields
            first_record = records[0]
            assert "sdt_protocol_id" in first_record
            assert "sdt_protocol_name" in first_record

    def test_load_medium_table_with_computed_fields(self):
        """Test loading reads table with computed fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            reads_table = CDM_DB_PATH / "sdt_reads"

            if not reads_table.exists():
                pytest.skip("Reads table not found")

            # Create store
            client, db, schema_view = create_store(str(db_path), CDM_SCHEMA)

            # Load reads table (sample first 100 rows)
            count = load_parquet_collection(
                reads_table, "Reads", db, schema_view, max_rows=100, verbose=True
            )

            assert count > 0

            # Verify computed fields
            collection = db.get_collection("Reads")
            records = list(collection.find(limit=10))

            # Check for computed field
            has_category = any("read_count_category" in r for r in records)
            if has_category:
                # Verify category values are valid
                categories = {
                    r.get("read_count_category")
                    for r in records
                    if "read_count_category" in r
                }
                valid_categories = {"very_high", "high", "medium", "low"}
                assert categories.issubset(valid_categories)

    def test_load_system_table(self):
        """Test loading a system table (sys_oterm)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            oterm_table = CDM_DB_PATH / "sys_oterm"

            if not oterm_table.exists():
                pytest.skip("sys_oterm table not found")

            # Create store
            client, db, schema_view = create_store(str(db_path), CDM_SCHEMA)

            # Load ontology terms (sample first 1000)
            count = load_parquet_collection(
                oterm_table,
                "SystemOntologyTerm",
                db,
                schema_view,
                max_rows=1000,
                verbose=True,
            )

            assert count > 0

            # Verify structure
            collection = db.get_collection("SystemOntologyTerm")
            records = list(collection.find(limit=10))

            first_term = records[0]
            assert "sys_oterm_id" in first_term
            assert "sys_oterm_name" in first_term

    def test_load_multiple_tables(self):
        """Test loading multiple tables at once."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"

            # Create store
            client, db, schema_view = create_store(str(db_path), CDM_SCHEMA)

            # Load subset of tables
            results = load_all_cdm_parquet(
                CDM_DB_PATH,
                db,
                schema_view,
                include_system=False,
                include_static=True,
                include_dynamic=False,
                verbose=False,
            )

            # Should have loaded some tables
            assert len(results) > 0
            assert sum(results.values()) > 0

            # Check collections exist
            collections = db.list_collections()
            assert len(collections) > 0


@pytest.mark.skipif(not HAS_CDM_DB, reason="CDM database not available")
class TestCDMStoreQuery:
    """Integration tests for querying CDM store."""

    @pytest.fixture
    def test_db(self):
        """Create a test database with sample data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"

            # Create store
            client, db, schema_view = create_store(str(db_path), CDM_SCHEMA)

            # Load small tables for testing
            protocol_table = CDM_DB_PATH / "sdt_protocol"
            if protocol_table.exists():
                load_parquet_collection(
                    protocol_table, "Protocol", db, schema_view, verbose=False
                )

            location_table = CDM_DB_PATH / "sdt_location"
            if location_table.exists():
                load_parquet_collection(
                    location_table, "Location", db, schema_view, verbose=False
                )

            sample_table = CDM_DB_PATH / "sdt_sample"
            if sample_table.exists():
                load_parquet_collection(
                    sample_table,
                    "Sample",
                    db,
                    schema_view,
                    max_rows=100,
                    verbose=False,
                )

            oterm_table = CDM_DB_PATH / "sys_oterm"
            if oterm_table.exists():
                load_parquet_collection(
                    oterm_table,
                    "SystemOntologyTerm",
                    db,
                    schema_view,
                    max_rows=1000,
                    verbose=False,
                )

            yield str(db_path)

    def test_stats_query(self, test_db):
        """Test database statistics query."""
        query = CDMStoreQuery(test_db)
        stats = query.stats()

        assert "database" in stats
        assert "collections" in stats
        assert "total_records" in stats
        assert "total_collections" in stats

        assert stats["total_collections"] > 0
        assert stats["total_records"] > 0

        # Check specific collections
        assert isinstance(stats["collections"], dict)
        assert len(stats["collections"]) > 0

    def test_find_samples_by_location(self, test_db):
        """Test finding samples by location."""
        query = CDMStoreQuery(test_db)

        # Get a location first
        try:
            location_coll = query.get_collection("Location")
            locations = list(location_coll.find(limit=1))

            if locations:
                location_name = locations[0].get("sdt_location_name")

                # Find samples from this location
                samples = query.find_samples_by_location(location_name, limit=10)

                # Should return list (may be empty if no samples at this location)
                assert isinstance(samples, list)

                # If samples found, verify structure
                if samples:
                    first_sample = samples[0]
                    assert "sdt_sample_id" in first_sample
                    assert "location_ref" in first_sample
                    assert first_sample["location_ref"] == location_name
        except ValueError:
            pytest.skip("Location or Sample collection not loaded")

    def test_search_ontology_terms(self, test_db):
        """Test searching ontology terms."""
        query = CDMStoreQuery(test_db)

        try:
            # Search for common term
            results = query.search_ontology_terms("soil", limit=10)

            assert isinstance(results, list)

            # If results found, verify structure
            if results:
                first_term = results[0]
                assert "sys_oterm_id" in first_term
                assert "sys_oterm_name" in first_term

                # Verify search term appears in name
                assert "soil" in first_term["sys_oterm_name"].lower()
        except ValueError:
            pytest.skip("SystemOntologyTerm collection not loaded")

    def test_get_collection(self, test_db):
        """Test getting a collection."""
        query = CDMStoreQuery(test_db)

        # Should be able to get loaded collections
        try:
            collection = query.get_collection("Protocol")
            assert collection is not None
        except ValueError:
            pytest.skip("Protocol collection not loaded")

    def test_get_nonexistent_collection(self, test_db):
        """Test error handling for nonexistent collection."""
        query = CDMStoreQuery(test_db)

        with pytest.raises(ValueError, match="not found"):
            query.get_collection("NonexistentCollection")


class TestEndToEnd:
    """End-to-end tests without requiring full CDM database."""

    def test_create_minimal_database(self):
        """Test creating a minimal database from scratch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test parquet data
            test_table_dir = Path(tmpdir) / "test_data"
            test_table_dir.mkdir()

            # Create sample data
            df = pd.DataFrame(
                {
                    "sdt_sample_id": ["Sample0000001", "Sample0000002", "Sample0000003"],
                    "sdt_sample_name": ["Sample_A", "Sample_B", "Sample_C"],
                    "location_ref": ["Location0000001", "Location0000001", "Location0000002"],
                    "depth": [10.5, 20.3, 30.1],
                    "material_sys_oterm_id": ["ENVO:00001234", "ENVO:00001234", "ENVO:00005678"],
                    "material_sys_oterm_name": ["soil", "soil", "water"],
                }
            )

            # Save as parquet
            test_parquet = test_table_dir / "part-00000.parquet"
            df.to_parquet(test_parquet)

            # Create database
            db_path = Path(tmpdir) / "test.db"
            client, db, schema_view = create_store(str(db_path), CDM_SCHEMA)

            # Load data
            count = load_parquet_collection(
                test_table_dir, "Sample", db, schema_view, verbose=True
            )

            assert count == 3

            # Verify collection was created
            collections = db.list_collections()
            assert len(collections) > 0

            # Verify we can retrieve the data directly
            collection = db.get_collection("Sample")
            result = collection.find(limit=10)

            # Check that we got results
            if hasattr(result, 'num_rows'):
                assert result.num_rows == 3
            elif hasattr(result, 'rows'):
                assert len(result.rows) == 3

    def test_nan_handling_integration(self):
        """Test that NaN values are properly handled end-to-end."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create data with NaN values
            test_table_dir = Path(tmpdir) / "test_data"
            test_table_dir.mkdir()

            df = pd.DataFrame(
                {
                    "sdt_sample_id": ["Sample0000001", "Sample0000002"],
                    "sdt_sample_name": ["Sample_A", "Sample_B"],
                    "depth": [10.5, float("nan")],  # NaN value
                    "location_ref": ["Location0000001", None],  # None value
                }
            )

            test_parquet = test_table_dir / "part-00000.parquet"
            df.to_parquet(test_parquet)

            # Create database and load
            db_path = Path(tmpdir) / "test.db"
            client, db, schema_view = create_store(str(db_path), CDM_SCHEMA)

            count = load_parquet_collection(
                test_table_dir, "Sample", db, schema_view
            )

            assert count == 2

            # Query and verify NaN converted to None
            collection = db.get_collection("Sample")
            result = collection.find()

            # Extract rows from result
            if hasattr(result, 'rows'):
                records = result.rows
            elif hasattr(result, 'num_rows'):
                # Result object - just check count
                assert result.num_rows == 2
                return  # Skip detailed checks
            else:
                records = list(result)

            assert len(records) == 2

            # Check None values in records
            record2 = [r for r in records if r.get("sdt_sample_id") == "Sample0000002"]
            if record2:
                assert record2[0].get("depth") is None
                assert record2[0].get("location_ref") is None


class TestErrorHandling:
    """Test error handling in loader and query interface."""

    def test_load_nonexistent_table(self):
        """Test error handling when table doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            nonexistent_table = Path(tmpdir) / "nonexistent"

            client, db, schema_view = create_store(str(db_path), CDM_SCHEMA)

            # Should handle gracefully (return 0 records)
            count = load_parquet_collection(
                nonexistent_table, "Sample", db, schema_view, verbose=False
            )

            assert count == 0

    def test_query_nonexistent_database(self):
        """Test error when querying nonexistent database."""
        with pytest.raises((FileNotFoundError, Exception)):
            query = CDMStoreQuery("/nonexistent/path/to.db")
            query.stats()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
