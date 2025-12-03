"""
Unit tests for CDM parquet loader.

Tests the load_cdm_parquet_to_store.py script functionality including:
- Parquet reading (Delta Lake format)
- NaN handling
- Computed field generation
- Provenance parsing
- Collection creation
"""

import pytest
import tempfile
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "cdm_analysis"))

from load_cdm_parquet_to_store import (
    parse_array_field,
    extract_provenance_info,
    add_computed_fields,
    get_parquet_row_count,
    read_parquet_data,
    TABLE_TO_CLASS,
)


class TestTableMapping:
    """Test table name to class name mapping."""

    def test_static_entity_mappings(self):
        """Test static entity table mappings."""
        assert TABLE_TO_CLASS["sdt_location"] == "Location"
        assert TABLE_TO_CLASS["sdt_sample"] == "Sample"
        assert TABLE_TO_CLASS["sdt_reads"] == "Reads"
        assert TABLE_TO_CLASS["sdt_assembly"] == "Assembly"
        assert TABLE_TO_CLASS["sdt_genome"] == "Genome"
        assert TABLE_TO_CLASS["sdt_asv"] == "ASV"

    def test_system_table_mappings(self):
        """Test system table mappings."""
        assert TABLE_TO_CLASS["sys_typedef"] == "SystemTypedef"
        assert TABLE_TO_CLASS["sys_oterm"] == "SystemOntologyTerm"
        assert TABLE_TO_CLASS["sys_process"] == "SystemProcess"

    def test_dynamic_table_mappings(self):
        """Test dynamic table mappings."""
        assert TABLE_TO_CLASS["ddt_ndarray"] == "DynamicDataArray"

    def test_all_mappings_have_values(self):
        """Ensure all mappings have non-empty class names."""
        for table_name, class_name in TABLE_TO_CLASS.items():
            assert class_name, f"Empty class name for table {table_name}"
            assert isinstance(class_name, str)
            assert len(class_name) > 0


class TestArrayParsing:
    """Test array field parsing."""

    def test_parse_empty_array(self):
        """Test parsing empty/null values."""
        assert parse_array_field(None) == []
        assert parse_array_field("") == []
        assert parse_array_field([]) == []

    def test_parse_list_array(self):
        """Test parsing when input is already a list."""
        input_list = ["Reads:Reads0000001", "Sample:Sample0000001"]
        result = parse_array_field(input_list)
        assert result == ["Reads:Reads0000001", "Sample:Sample0000001"]

    def test_parse_string_array(self):
        """Test parsing string representation of array."""
        input_str = "['Reads:Reads0000001', 'Sample:Sample0000001']"
        result = parse_array_field(input_str)
        assert len(result) == 2
        assert "Reads:Reads0000001" in result
        assert "Sample:Sample0000001" in result

    def test_parse_numeric_list(self):
        """Test parsing list with numeric values."""
        input_list = [1, 2, 3]
        result = parse_array_field(input_list)
        assert result == ["1", "2", "3"]

    def test_parse_malformed_string(self):
        """Test parsing malformed string returns empty."""
        result = parse_array_field("not an array")
        assert result == []


class TestProvenanceParsing:
    """Test provenance information extraction."""

    def test_extract_input_objects(self):
        """Test extraction of input objects."""
        record = {
            "sys_process_input_objects": ["Reads:Reads0000001", "Sample:Sample0000001"]
        }
        result = extract_provenance_info(record)

        assert "input_objects_parsed" in result
        assert result["input_objects_parsed"] == [
            "Reads:Reads0000001",
            "Sample:Sample0000001",
        ]
        assert "input_entity_types" in result
        assert set(result["input_entity_types"]) == {"Reads", "Sample"}
        assert "input_entity_ids" in result
        assert "Reads0000001" in result["input_entity_ids"]
        assert "Sample0000001" in result["input_entity_ids"]

    def test_extract_output_objects(self):
        """Test extraction of output objects."""
        record = {"sys_process_output_objects": ["Assembly:Assembly0000001"]}
        result = extract_provenance_info(record)

        assert "output_objects_parsed" in result
        assert result["output_objects_parsed"] == ["Assembly:Assembly0000001"]
        assert "output_entity_types" in result
        assert result["output_entity_types"] == ["Assembly"]
        assert "output_entity_ids" in result
        assert result["output_entity_ids"] == ["Assembly0000001"]

    def test_extract_both_input_and_output(self):
        """Test extraction of both input and output."""
        record = {
            "sys_process_input_objects": ["Reads:Reads0000001"],
            "sys_process_output_objects": ["Assembly:Assembly0000001"],
        }
        result = extract_provenance_info(record)

        assert "input_objects_parsed" in result
        assert "output_objects_parsed" in result
        assert result["input_entity_types"] == ["Reads"]
        assert result["output_entity_types"] == ["Assembly"]

    def test_extract_empty_provenance(self):
        """Test extraction with no provenance fields."""
        record = {"some_other_field": "value"}
        result = extract_provenance_info(record)

        # Should still return original record
        assert "some_other_field" in result
        assert result["some_other_field"] == "value"

    def test_extract_with_multiple_same_type(self):
        """Test extraction with multiple entities of same type."""
        record = {
            "sys_process_input_objects": [
                "Reads:Reads0000001",
                "Reads:Reads0000002",
                "Sample:Sample0000001",
            ]
        }
        result = extract_provenance_info(record)

        # Entity types should be unique
        assert set(result["input_entity_types"]) == {"Reads", "Sample"}
        # Entity IDs should include all
        assert len(result["input_entity_ids"]) == 3


class TestComputedFields:
    """Test computed field generation."""

    def test_reads_very_high_category(self):
        """Test very_high read count category."""
        record = {"sdt_reads_read_count": 150000}
        result = add_computed_fields(record, "Reads")
        assert result["read_count_category"] == "very_high"

    def test_reads_high_category(self):
        """Test high read count category."""
        record = {"sdt_reads_read_count": 75000}
        result = add_computed_fields(record, "Reads")
        assert result["read_count_category"] == "high"

    def test_reads_medium_category(self):
        """Test medium read count category."""
        record = {"sdt_reads_read_count": 25000}
        result = add_computed_fields(record, "Reads")
        assert result["read_count_category"] == "medium"

    def test_reads_low_category(self):
        """Test low read count category."""
        record = {"sdt_reads_read_count": 5000}
        result = add_computed_fields(record, "Reads")
        assert result["read_count_category"] == "low"

    def test_reads_boundary_values(self):
        """Test boundary values for read count categories."""
        # Exactly at boundary
        record1 = {"sdt_reads_read_count": 100000}
        assert add_computed_fields(record1, "Reads")["read_count_category"] == "very_high"

        record2 = {"sdt_reads_read_count": 50000}
        assert add_computed_fields(record2, "Reads")["read_count_category"] == "high"

        record3 = {"sdt_reads_read_count": 10000}
        assert add_computed_fields(record3, "Reads")["read_count_category"] == "medium"

    def test_assembly_high_contigs(self):
        """Test high contig count category."""
        record = {"sdt_assembly_n_contigs": 1500}
        result = add_computed_fields(record, "Assembly")
        assert result["contig_count_category"] == "high"

    def test_assembly_medium_contigs(self):
        """Test medium contig count category."""
        record = {"sdt_assembly_n_contigs": 150}
        result = add_computed_fields(record, "Assembly")
        assert result["contig_count_category"] == "medium"

    def test_assembly_low_contigs(self):
        """Test low contig count category."""
        record = {"sdt_assembly_n_contigs": 50}
        result = add_computed_fields(record, "Assembly")
        assert result["contig_count_category"] == "low"

    def test_no_computed_field_for_other_classes(self):
        """Test that no computed fields added for other classes."""
        record = {"sdt_sample_id": "Sample0000001"}
        result = add_computed_fields(record, "Sample")
        assert "read_count_category" not in result
        assert "contig_count_category" not in result

    def test_nan_handling_in_computed_fields(self):
        """Test that NaN values don't cause computed fields."""
        record = {"sdt_reads_read_count": float("nan")}
        result = add_computed_fields(record, "Reads")
        # Should not add category for NaN
        assert "read_count_category" not in result

    def test_none_handling_in_computed_fields(self):
        """Test that None values don't cause computed fields."""
        record = {"sdt_reads_read_count": None}
        result = add_computed_fields(record, "Reads")
        # Should not add category for None
        assert "read_count_category" not in result


class TestParquetReading:
    """Test parquet file reading functionality."""

    def test_read_parquet_data_creates_dataframe(self):
        """Test that reading parquet creates proper DataFrame."""
        # Create temporary parquet file
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = Path(tmpdir) / "test.parquet"
            df = pd.DataFrame(
                {
                    "sdt_sample_id": ["Sample0000001", "Sample0000002"],
                    "sdt_sample_name": ["Sample_A", "Sample_B"],
                    "depth": [10.5, 20.3],
                }
            )
            df.to_parquet(tmpfile)

            # Read it back
            result = read_parquet_data(tmpfile)

            assert isinstance(result, pd.DataFrame)
            assert len(result) == 2
            assert "sdt_sample_id" in result.columns
            assert "depth" in result.columns

    def test_read_parquet_with_max_rows(self):
        """Test reading with row limit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = Path(tmpdir) / "test.parquet"
            df = pd.DataFrame({"id": list(range(100)), "value": list(range(100))})
            df.to_parquet(tmpfile)

            # Read only 10 rows
            result = read_parquet_data(tmpfile, max_rows=10)

            assert len(result) == 10

    def test_read_parquet_with_offset(self):
        """Test reading with offset."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = Path(tmpdir) / "test.parquet"
            df = pd.DataFrame({"id": list(range(100)), "value": list(range(100))})
            df.to_parquet(tmpfile)

            # Read from offset 50
            result = read_parquet_data(tmpfile, offset=50)

            assert len(result) == 50
            assert result.iloc[0]["id"] == 50

    def test_read_parquet_with_offset_and_limit(self):
        """Test reading with both offset and limit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = Path(tmpdir) / "test.parquet"
            df = pd.DataFrame({"id": list(range(100)), "value": list(range(100))})
            df.to_parquet(tmpfile)

            # Read 10 rows starting from offset 50
            result = read_parquet_data(tmpfile, max_rows=10, offset=50)

            assert len(result) == 10
            assert result.iloc[0]["id"] == 50
            assert result.iloc[9]["id"] == 59

    def test_get_parquet_row_count(self):
        """Test getting row count without loading file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = Path(tmpdir) / "test.parquet"
            df = pd.DataFrame({"id": list(range(100)), "value": list(range(100))})
            df.to_parquet(tmpfile)

            count = get_parquet_row_count(tmpfile)

            assert count == 100

    @pytest.mark.skipif(
        not Path("/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db").exists(),
        reason="CDM database not available",
    )
    def test_read_real_cdm_table(self):
        """Integration test: Read a small real CDM table."""
        cdm_db = Path(
            "/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db"
        )
        protocol_table = cdm_db / "sdt_protocol"

        if protocol_table.exists():
            df = read_parquet_data(protocol_table, max_rows=10)
            assert isinstance(df, pd.DataFrame)
            assert len(df) <= 10


class TestNaNHandling:
    """Test NaN value handling."""

    def test_nan_conversion_in_dataframe(self):
        """Test that NaN values are properly identified."""
        df = pd.DataFrame({"a": [1, float("nan"), 3], "b": ["x", None, "z"]})

        records = df.to_dict("records")

        # Check NaN detection
        assert pd.isna(records[1]["a"])

    def test_none_vs_nan(self):
        """Test distinction between None and NaN."""
        df = pd.DataFrame({"a": [None, float("nan"), "value"]})

        # Both None and NaN become NaN in pandas
        assert pd.isna(df.iloc[0]["a"])
        assert pd.isna(df.iloc[1]["a"])
        assert not pd.isna(df.iloc[2]["a"])


class TestDeltaLakeFormat:
    """Test Delta Lake directory format handling."""

    def test_read_delta_lake_directory(self):
        """Test reading parquet from Delta Lake directory structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create Delta Lake structure
            table_dir = Path(tmpdir) / "sdt_sample"
            table_dir.mkdir()

            # Create parquet file in directory
            df = pd.DataFrame(
                {
                    "sdt_sample_id": ["Sample0000001", "Sample0000002"],
                    "sdt_sample_name": ["Sample_A", "Sample_B"],
                }
            )
            parquet_file = table_dir / "part-00000.parquet"
            df.to_parquet(parquet_file)

            # Create _delta_log directory (metadata)
            delta_log = table_dir / "_delta_log"
            delta_log.mkdir()

            # Read from directory
            result = read_parquet_data(table_dir)

            assert isinstance(result, pd.DataFrame)
            assert len(result) == 2

    def test_get_row_count_delta_lake(self):
        """Test getting row count from Delta Lake directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            table_dir = Path(tmpdir) / "sdt_sample"
            table_dir.mkdir()

            # Create multiple parquet files
            df1 = pd.DataFrame({"id": list(range(50))})
            df2 = pd.DataFrame({"id": list(range(50, 100))})

            (table_dir / "part-00000.parquet").write_bytes(
                df1.to_parquet(None, engine="pyarrow")
            )
            (table_dir / "part-00001.parquet").write_bytes(
                df2.to_parquet(None, engine="pyarrow")
            )

            count = get_parquet_row_count(table_dir)

            # Should sum both files
            assert count == 100


class TestFieldPreservation:
    """Test that all fields are preserved during loading."""

    def test_ontology_term_fields_preserved(self):
        """Test that ontology term ID and name fields are preserved."""
        record = {
            "material_sys_oterm_id": "ENVO:00001234",
            "material_sys_oterm_name": "soil",
            "sdt_sample_id": "Sample0000001",
        }

        result = add_computed_fields(record, "Sample")

        # All original fields should be preserved
        assert result["material_sys_oterm_id"] == "ENVO:00001234"
        assert result["material_sys_oterm_name"] == "soil"
        assert result["sdt_sample_id"] == "Sample0000001"

    def test_foreign_key_fields_preserved(self):
        """Test that foreign key reference fields are preserved."""
        record = {
            "sdt_sample_id": "Sample0000001",
            "location_ref": "Location0000001",  # FK using name
            "depth": 10.5,
        }

        result = add_computed_fields(record, "Sample")

        assert result["location_ref"] == "Location0000001"
        assert result["depth"] == 10.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
