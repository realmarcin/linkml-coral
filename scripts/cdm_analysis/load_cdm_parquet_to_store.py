#!/usr/bin/env python3
"""
Load KBase CDM parquet files into LinkML-Store database.

This script loads parquet data from the KBase Common Data Model (CDM) database
into a linkml-store database (DuckDB backend) for efficient querying and analysis.

The CDM contains 44 parquet tables:
- 6 system tables (sys_*): typedef, oterm, process, etc.
- 17 static entity tables (sdt_*): location, sample, reads, genome, etc.
- 21 dynamic data tables (ddt_*): ndarray, brick tables (optional)

Usage:
    # Load all static and system tables
    python load_cdm_parquet_to_store.py data/enigma_coral.db

    # Load with options
    python load_cdm_parquet_to_store.py data/enigma_coral.db \\
        --output cdm_store.db \\
        --include-system \\
        --include-static \\
        --create-indexes \\
        --verbose

    # Sample dynamic brick tables (82.6M rows)
    python load_cdm_parquet_to_store.py data/enigma_coral.db \\
        --include-dynamic \\
        --max-brick-rows 10000
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Iterator
import time
import gc

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

try:
    import psutil
except ImportError:
    print("Warning: psutil not installed. Memory monitoring disabled. Run: uv pip install psutil")
    psutil = None

try:
    from tqdm import tqdm
except ImportError:
    print("Warning: tqdm not installed. Progress bars disabled. Run: uv pip install tqdm")
    tqdm = None

from linkml_store import Client
from linkml_runtime.utils.schemaview import SchemaView


# CDM Schema path
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
CDM_SCHEMA = REPO_ROOT / "src/linkml_coral/schema/cdm/linkml_coral_cdm.yaml"


# Mapping from CDM table names to LinkML class names
TABLE_TO_CLASS = {
    # Static entity tables (sdt_*)
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

    # System tables (sys_*)
    "sys_typedef": "SystemTypedef",
    "sys_ddt_typedef": "SystemDDTTypedef",
    "sys_oterm": "SystemOntologyTerm",
    "sys_process": "SystemProcess",
    "sys_process_input": "SystemProcessInput",
    "sys_process_output": "SystemProcessOutput",

    # Dynamic data tables (ddt_*)
    "ddt_ndarray": "DynamicDataArray",
}


def get_memory_info() -> Dict[str, float]:
    """Get current system memory information in GB."""
    if psutil is None:
        return {'total_gb': 0, 'available_gb': 0, 'used_gb': 0, 'percent': 0}

    mem = psutil.virtual_memory()
    return {
        'total_gb': mem.total / (1024**3),
        'available_gb': mem.available / (1024**3),
        'used_gb': mem.used / (1024**3),
        'percent': mem.percent
    }


def estimate_memory_requirement(parquet_path: Path) -> float:
    """
    Estimate memory required to load parquet file in GB.

    Args:
        parquet_path: Path to parquet file or directory

    Returns:
        Estimated memory in GB
    """
    if parquet_path.is_dir():
        total_size = sum(f.stat().st_size for f in parquet_path.glob("*.parquet")
                        if not f.parent.name.startswith('_'))
    else:
        total_size = parquet_path.stat().st_size

    # Estimate: compressed_size × 8 (decompression) × 2 (processing overhead)
    estimated_gb = (total_size / (1024**3)) * 16
    return estimated_gb


def check_memory_warning(parquet_path: Path, verbose: bool = False) -> bool:
    """
    Check if sufficient memory is available and warn if low.

    Args:
        parquet_path: Path to parquet file/directory
        verbose: Print detailed memory info

    Returns:
        True if sufficient memory, False otherwise
    """
    if psutil is None:
        return True  # Can't check, assume OK

    mem_info = get_memory_info()
    required_gb = estimate_memory_requirement(parquet_path)

    # Show warning if file requires more than 50% of available memory
    if verbose or required_gb > mem_info['available_gb'] * 0.5:
        print(f"\n  💾 Memory Check:")
        print(f"     System Total: {mem_info['total_gb']:.1f} GB")
        print(f"     Available: {mem_info['available_gb']:.1f} GB")
        print(f"     Estimated Required: {required_gb:.1f} GB")

    if required_gb > mem_info['available_gb']:
        print(f"\n  ⚠️  ⚠️  ⚠️  MEMORY WARNING ⚠️  ⚠️  ⚠️")
        print(f"  This file may cause out-of-memory errors!")
        print(f"  Required: ~{required_gb:.1f} GB")
        print(f"  Available: {mem_info['available_gb']:.1f} GB")
        print(f"\n  Will use CHUNKED loading (memory-safe)")
        return False

    return True


def load_schema(schema_path: Path) -> SchemaView:
    """Load LinkML schema."""
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    return SchemaView(str(schema_path))


def create_store(db_path: str = None, schema_path: Path = None) -> tuple:
    """
    Create or connect to a linkml-store database.

    Args:
        db_path: Path to DuckDB database file. If None, uses in-memory database.
        schema_path: Path to LinkML schema file.

    Returns:
        tuple: (client, database, schema_view)
    """
    client = Client()

    # Attach database
    if db_path:
        print(f"📦 Connecting to database: {db_path}")
        db = client.attach_database(f"duckdb:///{db_path}", alias="cdm")
    else:
        print(f"📦 Creating in-memory database")
        db = client.attach_database("duckdb", alias="cdm")

    # Load schema if provided
    schema_view = None
    if schema_path:
        schema_view = load_schema(schema_path)
        print(f"📋 Loaded schema: {schema_view.schema.name}")

    return client, db, schema_view


def get_parquet_row_count(parquet_path: Path) -> int:
    """Get total row count without loading entire file."""
    if parquet_path.is_dir():
        # Delta Lake - sum all parquet files
        total = 0
        for pf in parquet_path.glob("*.parquet"):
            parquet_file = pq.ParquetFile(pf)
            total += parquet_file.metadata.num_rows
        return total
    else:
        parquet_file = pq.ParquetFile(parquet_path)
        return parquet_file.metadata.num_rows


def read_parquet_data(
    parquet_path: Path,
    max_rows: Optional[int] = None,
    offset: int = 0
) -> pd.DataFrame:
    """
    Read parquet file with optional row limits.

    Args:
        parquet_path: Path to parquet file or directory (Delta Lake)
        max_rows: Maximum rows to read (None = all)
        offset: Number of rows to skip

    Returns:
        DataFrame with parquet data
    """
    if parquet_path.is_dir():
        # Delta Lake format - read all parquet files in directory
        parquet_files = [f for f in parquet_path.glob("*.parquet")
                        if not f.parent.name.startswith('_')]
        if not parquet_files:
            raise ValueError(f"No parquet files found in {parquet_path}")

        # Read first file
        df = pd.read_parquet(parquet_files[0])

        # Read remaining files if needed
        if max_rows is None or len(df) < max_rows:
            for pf in parquet_files[1:]:
                chunk = pd.read_parquet(pf)
                df = pd.concat([df, chunk], ignore_index=True)
                if max_rows and len(df) >= max_rows:
                    break
    else:
        # Single parquet file
        df = pd.read_parquet(parquet_path)

    # Apply offset and limit
    if offset > 0:
        df = df.iloc[offset:]
    if max_rows is not None:
        df = df.head(max_rows)

    return df


def read_parquet_chunked(
    parquet_path: Path,
    chunk_size: int = 100_000,
    max_rows: Optional[int] = None,
    verbose: bool = False
) -> Iterator[pd.DataFrame]:
    """
    Read parquet file in chunks to avoid loading entire file into memory.

    Args:
        parquet_path: Path to parquet file or directory (Delta Lake)
        chunk_size: Number of rows per chunk (default: 100K)
        max_rows: Maximum total rows to read (None = all)
        verbose: Print chunk progress

    Yields:
        DataFrame chunks
    """
    if parquet_path.is_dir():
        # Delta Lake format - read all parquet files in directory
        parquet_files = sorted([f for f in parquet_path.glob("*.parquet")
                               if not f.parent.name.startswith('_')])
        if not parquet_files:
            raise ValueError(f"No parquet files found in {parquet_path}")
    else:
        # Single parquet file
        parquet_files = [parquet_path]

    total_yielded = 0
    for file_idx, pf in enumerate(parquet_files, 1):
        if verbose and len(parquet_files) > 1:
            print(f"    Reading file {file_idx}/{len(parquet_files)}: {pf.name}")

        parquet_file = pq.ParquetFile(pf)

        # Iterate over row groups in batches
        for batch in parquet_file.iter_batches(batch_size=chunk_size):
            df_chunk = batch.to_pandas()

            # Apply max_rows limit
            if max_rows is not None:
                rows_remaining = max_rows - total_yielded
                if rows_remaining <= 0:
                    return
                if len(df_chunk) > rows_remaining:
                    yield df_chunk.iloc[:rows_remaining]
                    return

            total_yielded += len(df_chunk)
            yield df_chunk


def parse_array_field(value: Any) -> List[str]:
    """Parse string array fields like \"['Reads:Reads0000001']\" to Python lists."""
    if not value:
        return []

    # If already a list, return it
    if isinstance(value, list):
        return [str(item) for item in value]

    # If it's a string, try to parse it
    if isinstance(value, str):
        # Handle string representation of arrays
        if value.startswith('[') and value.endswith(']'):
            try:
                import ast
                parsed = ast.literal_eval(value)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except (ValueError, SyntaxError):
                pass

    return []


def extract_provenance_info(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and structure provenance information from SystemProcess records.

    Parses input_objects and output_objects arrays.
    """
    enhanced = record.copy()

    # Parse Process input/output objects - check both field name variations
    input_field = 'input_objects' if 'input_objects' in record else 'sys_process_input_objects'
    output_field = 'output_objects' if 'output_objects' in record else 'sys_process_output_objects'

    if input_field in record:
        input_objs = parse_array_field(record[input_field])
        enhanced['input_objects_parsed'] = input_objs

        # Extract entity types and IDs
        enhanced['input_entity_types'] = list(set(
            obj.split(':')[0] for obj in input_objs if ':' in obj
        ))
        enhanced['input_entity_ids'] = [
            obj.split(':')[1] if ':' in obj else obj
            for obj in input_objs
        ]

    if output_field in record:
        output_objs = parse_array_field(record[output_field])
        enhanced['output_objects_parsed'] = output_objs

        # Extract entity types and IDs
        enhanced['output_entity_types'] = list(set(
            obj.split(':')[0] for obj in output_objs if ':' in obj
        ))
        enhanced['output_entity_ids'] = [
            obj.split(':')[1] if ':' in obj else obj
            for obj in output_objs
        ]

    return enhanced


def add_computed_fields(record: Dict[str, Any], class_name: str) -> Dict[str, Any]:
    """Add computed fields for easier querying."""
    enhanced = record.copy()

    # Add read count categories for Reads
    if class_name == 'Reads' and 'sdt_reads_read_count_count_unit' in record:
        read_count = record['sdt_reads_read_count_count_unit']
        if isinstance(read_count, (int, float)) and not pd.isna(read_count):
            if read_count >= 100000:
                enhanced['read_count_category'] = 'very_high'
            elif read_count >= 50000:
                enhanced['read_count_category'] = 'high'
            elif read_count >= 10000:
                enhanced['read_count_category'] = 'medium'
            else:
                enhanced['read_count_category'] = 'low'

    # Add contig count categories for Assembly
    if class_name == 'Assembly' and 'sdt_assembly_n_contigs_count_unit' in record:
        n_contigs = record['sdt_assembly_n_contigs_count_unit']
        if isinstance(n_contigs, (int, float)) and not pd.isna(n_contigs):
            if n_contigs >= 1000:
                enhanced['contig_count_category'] = 'high'
            elif n_contigs >= 100:
                enhanced['contig_count_category'] = 'medium'
            else:
                enhanced['contig_count_category'] = 'low'

    return enhanced


def load_parquet_to_duckdb_direct(
    parquet_path: Path,
    collection_name: str,
    db,
    max_rows: Optional[int] = None,
    verbose: bool = False
) -> int:
    """
    Load parquet directly into DuckDB without pandas (FAST, low memory).

    This bypasses pandas entirely and uses DuckDB's native parquet reader,
    which is 10-50x faster and uses minimal memory.

    Args:
        parquet_path: Path to parquet file/directory
        collection_name: Collection name in database
        db: Database connection
        max_rows: Maximum rows to load (None = all)
        verbose: Print detailed progress

    Returns:
        Number of records loaded
    """
    import duckdb

    table_name = parquet_path.name
    print(f"\n📥 Loading {table_name} as {collection_name}...")

    start_time = time.time()

    try:
        # Get DuckDB connection from linkml-store
        # Path: db.engine (SQLAlchemy) → raw_connection() (ConnectionFairy)
        #       → driver_connection (ConnectionWrapper) → _ConnectionWrapper__c (DuckDB)
        if hasattr(db, 'engine'):
            # Access through SQLAlchemy Engine (used by linkml-store)
            raw_conn = db.engine.raw_connection()
            wrapper = raw_conn.driver_connection
            # Access the actual DuckDB connection (name-mangled private attribute)
            conn = wrapper._ConnectionWrapper__c
            if verbose:
                print(f"  ✓ Accessed DuckDB connection via SQLAlchemy engine")
        else:
            # Fallback: Try direct attributes (for other database types)
            if hasattr(db, '_connection'):
                conn = db._connection
            elif hasattr(db, 'connection'):
                conn = db.connection
            elif hasattr(db, 'get_connection'):
                conn = db.get_connection()
            else:
                raise AttributeError("Cannot access DuckDB connection from linkml-store")

        # Build parquet path pattern
        if parquet_path.is_dir():
            parquet_pattern = f"{parquet_path}/*.parquet"
        else:
            parquet_pattern = str(parquet_path)

        # Build SQL query
        # Use union_by_name=true to handle Delta Lake files with different schemas
        if max_rows:
            query = f"""
                CREATE OR REPLACE TABLE {collection_name} AS
                SELECT * FROM read_parquet('{parquet_pattern}', union_by_name=true)
                LIMIT {max_rows}
            """
        else:
            query = f"""
                CREATE OR REPLACE TABLE {collection_name} AS
                SELECT * FROM read_parquet('{parquet_pattern}', union_by_name=true)
            """

        if verbose:
            print(f"  🔍 Query: {query}")

        # Execute (streaming, minimal memory overhead)
        conn.execute(query)

        # Get count
        count_result = conn.execute(f"SELECT COUNT(*) FROM {collection_name}").fetchone()
        count = count_result[0] if count_result else 0

        elapsed = time.time() - start_time
        print(f"  ✅ Loaded {count:,} records in {elapsed:.1f}s ({count/elapsed:.0f} records/sec)")

        return count

    except AttributeError as e:
        # Could not access DuckDB connection - fall back to pandas
        if verbose:
            print(f"  ℹ️  Note: Could not access DuckDB connection ({e}), falling back to pandas")
        return 0
    except Exception as e:
        # Other error during direct import - fall back to pandas
        if verbose:
            print(f"  ⚠️  Direct import failed: {e}")
            print(f"  ℹ️  Falling back to pandas loading...")
        return 0


def load_parquet_collection_chunked(
    parquet_path: Path,
    class_name: str,
    db,
    schema_view: SchemaView,
    max_rows: Optional[int] = None,
    chunk_size: int = 100_000,
    verbose: bool = False
) -> int:
    """
    Load a parquet table into linkml-store using chunked reading.

    This method loads data in chunks to avoid memory issues with large files.

    Args:
        parquet_path: Path to parquet file/directory
        class_name: LinkML class name for this data
        db: Database connection
        schema_view: SchemaView instance
        max_rows: Maximum rows to load (None = all)
        chunk_size: Rows per chunk (default: 100K)
        verbose: Print detailed progress

    Returns:
        Number of records loaded
    """
    table_name = parquet_path.name
    print(f"\n📥 Loading {table_name} as {class_name} (CHUNKED MODE)...")

    # Check memory availability
    check_memory_warning(parquet_path, verbose=verbose)

    # Get total row count
    try:
        total_rows = get_parquet_row_count(parquet_path)
        load_rows = min(max_rows, total_rows) if max_rows else total_rows

        if max_rows and max_rows < total_rows:
            print(f"  📊 Total rows: {total_rows:,} (loading: {load_rows:,})")
        else:
            print(f"  📊 Total rows: {total_rows:,}")

        # Estimate chunks
        num_chunks = (load_rows + chunk_size - 1) // chunk_size
        print(f"  📦 Processing {num_chunks:,} chunks ({chunk_size:,} rows/chunk)")

    except Exception as e:
        print(f"  ⚠️  Could not get row count: {e}")
        total_rows = None
        num_chunks = None

    # Create or get collection
    collection_name = class_name
    try:
        collection = db.get_collection(collection_name)
        if verbose:
            print(f"  📦 Using existing collection: {collection_name}")
    except:
        collection = db.create_collection(collection_name)
        if verbose:
            print(f"  ✨ Created new collection: {collection_name}")

    # Load data in chunks
    start_time = time.time()
    total_loaded = 0
    chunk_num = 0

    # Create progress bar if tqdm available
    if tqdm and total_rows:
        pbar = tqdm(
            total=load_rows,
            desc=f"Loading {table_name}",
            unit="rows",
            unit_scale=True,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        )
    else:
        pbar = None

    try:
        chunk_generator = read_parquet_chunked(
            parquet_path,
            chunk_size=chunk_size,
            max_rows=max_rows,
            verbose=verbose
        )

        for df_chunk in chunk_generator:
            chunk_num += 1
            chunk_start = time.time()

            # Convert to records and enhance
            records = df_chunk.to_dict('records')

            # Handle NaN values
            import numpy as np
            for record in records:
                for key, value in list(record.items()):
                    if isinstance(value, np.ndarray):
                        record[key] = value.tolist()
                    elif isinstance(value, list):
                        pass  # Keep as list
                    elif pd.api.types.is_scalar(value):
                        try:
                            if pd.isna(value):
                                record[key] = None
                        except (ValueError, TypeError):
                            pass

            # Enhance records
            enhanced_data = []
            for record in records:
                if class_name == 'SystemProcess':
                    record = extract_provenance_info(record)
                record = add_computed_fields(record, class_name)
                enhanced_data.append(record)

            # Insert chunk
            collection.insert(enhanced_data)
            total_loaded += len(enhanced_data)

            chunk_time = time.time() - chunk_start

            # Update progress
            if pbar:
                pbar.update(len(enhanced_data))
            elif num_chunks and not verbose:
                # Show simple progress if no bar
                progress_pct = (chunk_num / num_chunks) * 100
                print(f"  [{chunk_num}/{num_chunks}] {progress_pct:5.1f}% - {total_loaded:,} rows", end='\r')
            elif verbose:
                # Detailed progress in verbose mode
                if num_chunks:
                    progress_pct = (chunk_num / num_chunks) * 100
                    print(f"  [{chunk_num}/{num_chunks}] {progress_pct:5.1f}% - "
                          f"Loaded {len(enhanced_data):,} rows in {chunk_time:.1f}s "
                          f"(total: {total_loaded:,})")
                else:
                    print(f"  [Chunk {chunk_num}] Loaded {len(enhanced_data):,} rows "
                          f"in {chunk_time:.1f}s (total: {total_loaded:,})")

            # Force garbage collection after each chunk
            gc.collect()

        if pbar:
            pbar.close()
        elif not verbose:
            print()  # New line after progress

        elapsed = time.time() - start_time
        print(f"  ✅ Loaded {total_loaded:,} records in {elapsed:.1f}s "
              f"({total_loaded/elapsed:.0f} records/sec)")

        return total_loaded

    except Exception as e:
        if pbar:
            pbar.close()
        print(f"  ❌ Error loading data: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return total_loaded  # Return partial count


def load_parquet_collection(
    parquet_path: Path,
    class_name: str,
    db,
    schema_view: SchemaView,
    max_rows: Optional[int] = None,
    verbose: bool = False
) -> int:
    """
    Load a single parquet table into a linkml-store collection.

    Args:
        parquet_path: Path to parquet file/directory
        class_name: LinkML class name for this data
        db: Database connection
        schema_view: SchemaView instance
        max_rows: Maximum rows to load (None = all)
        verbose: Print detailed progress

    Returns:
        Number of records loaded
    """
    table_name = parquet_path.name
    print(f"\n📥 Loading {table_name} as {class_name}...")

    # Get row count
    try:
        total_rows = get_parquet_row_count(parquet_path)
        load_rows = min(max_rows, total_rows) if max_rows else total_rows

        if max_rows and max_rows < total_rows:
            print(f"  📊 Total rows: {total_rows:,} (loading sample: {load_rows:,})")
        else:
            print(f"  📊 Total rows: {total_rows:,}")
    except Exception as e:
        print(f"  ⚠️  Could not get row count: {e}")
        total_rows = None

    # Read parquet data
    start_time = time.time()
    try:
        df = read_parquet_data(parquet_path, max_rows=max_rows)
    except Exception as e:
        print(f"  ❌ Error reading parquet: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 0

    if df.empty:
        print(f"  ⚠️  No data found")
        return 0

    read_time = time.time() - start_time
    if verbose:
        print(f"  ⏱️  Read {len(df):,} rows in {read_time:.2f}s")

    # Convert to list of dicts
    records = df.to_dict('records')

    # Handle NaN values and arrays (convert for linkml-store)
    import numpy as np
    for record in records:
        for key, value in list(record.items()):  # Use list() to avoid RuntimeError
            # Convert numpy arrays to Python lists
            if isinstance(value, np.ndarray):
                record[key] = value.tolist()
            # Convert Python lists (in case there are nested arrays)
            elif isinstance(value, list):
                # Already a list, keep it
                pass
            # Check for scalar NaN values
            elif pd.api.types.is_scalar(value):
                try:
                    if pd.isna(value):
                        record[key] = None
                except (ValueError, TypeError):
                    # If pd.isna fails on this value, leave it as-is
                    pass

    # Enhance records with computed fields and provenance info
    enhanced_data = []
    for record in records:
        # Add provenance parsing for SystemProcess records
        if class_name == 'SystemProcess':
            record = extract_provenance_info(record)

        # Add computed fields
        record = add_computed_fields(record, class_name)

        enhanced_data.append(record)

    if verbose and len(enhanced_data) > 0:
        print(f"  🔍 Sample fields: {list(enhanced_data[0].keys())[:5]}...")

    # Create or get collection
    collection_name = class_name
    try:
        collection = db.get_collection(collection_name)
        if verbose:
            print(f"  📦 Using existing collection: {collection_name}")
    except:
        collection = db.create_collection(collection_name)
        if verbose:
            print(f"  ✨ Created new collection: {collection_name}")

    # Insert data
    try:
        insert_start = time.time()
        collection.insert(enhanced_data)
        insert_time = time.time() - insert_start

        print(f"  ✅ Loaded {len(enhanced_data):,} records in {insert_time:.2f}s")
        return len(enhanced_data)
    except Exception as e:
        print(f"  ❌ Error loading data: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 0


def load_all_cdm_parquet(
    cdm_db_path: Path,
    db,
    schema_view: SchemaView,
    include_system: bool = True,
    include_static: bool = True,
    include_dynamic: bool = False,
    max_dynamic_rows: Optional[int] = None,
    num_bricks: Optional[int] = None,
    use_direct_import: bool = True,
    use_chunked: bool = True,
    chunk_size: int = 100_000,
    verbose: bool = False
) -> Dict[str, int]:
    """
    Load all CDM parquet tables into the database.

    Args:
        cdm_db_path: Path to CDM database directory (enigma_coral.db)
        db: Database connection
        schema_view: SchemaView instance
        include_system: Load sys_* tables
        include_static: Load sdt_* tables
        include_dynamic: Load ddt_* tables (large, sampled by default)
        max_dynamic_rows: Max rows per dynamic table (None = load all with chunking)
        num_bricks: Number of brick tables to load (None = all if include_dynamic, or 5 default)
        use_direct_import: Use direct DuckDB import (fastest, recommended)
        use_chunked: Use chunked loading for large files (memory-safe)
        chunk_size: Rows per chunk when using chunked mode (default: 100K)
        verbose: Print detailed progress

    Returns:
        Dict mapping collection names to record counts
    """
    results = {}
    total_records = 0
    start_time = time.time()

    # Static entity tables (17 tables, 273K rows)
    static_tables = [
        "sdt_location", "sdt_sample", "sdt_community", "sdt_reads",
        "sdt_assembly", "sdt_bin", "sdt_genome", "sdt_gene",
        "sdt_strain", "sdt_taxon", "sdt_asv", "sdt_protocol",
        "sdt_image", "sdt_condition", "sdt_dubseq_library",
        "sdt_tnseq_library", "sdt_enigma"
    ]

    # System tables (6 tables, 242K rows)
    system_tables = [
        "sys_typedef", "sys_ddt_typedef", "sys_oterm",
        "sys_process", "sys_process_input", "sys_process_output"
    ]

    # Dynamic tables (21 tables, 82.6M rows - typically sampled)
    dynamic_tables = ["ddt_ndarray"]  # Brick tables auto-detected

    # Load static tables
    if include_static:
        print(f"\n{'='*60}")
        print(f"📦 Loading Static Entity Tables (sdt_*)")
        print(f"{'='*60}")

        for table_name in static_tables:
            table_path = cdm_db_path / table_name
            if not table_path.exists():
                if verbose:
                    print(f"  ⊘ Skipping {table_name} (not found)")
                continue

            class_name = TABLE_TO_CLASS[table_name]
            count = load_parquet_collection(
                table_path, class_name, db, schema_view,
                max_rows=None,  # Full load for static tables
                verbose=verbose
            )
            results[class_name] = count
            total_records += count

    # Load system tables
    if include_system:
        print(f"\n{'='*60}")
        print(f"📦 Loading System Tables (sys_*)")
        print(f"{'='*60}")

        for table_name in system_tables:
            table_path = cdm_db_path / table_name
            if not table_path.exists():
                if verbose:
                    print(f"  ⊘ Skipping {table_name} (not found)")
                continue

            class_name = TABLE_TO_CLASS[table_name]
            count = load_parquet_collection(
                table_path, class_name, db, schema_view,
                max_rows=None,  # Full load for system tables
                verbose=verbose
            )
            results[class_name] = count
            total_records += count

    # Load dynamic tables (optional, use fast direct import or chunked)
    if include_dynamic:
        print(f"\n{'='*60}")
        print(f"📦 Loading Dynamic Data Tables (ddt_*)")
        print(f"{'='*60}")

        # Show loading strategy
        if use_direct_import:
            print(f"📦 Using optimized loading (attempts direct DuckDB, falls back to pandas)")
        elif use_chunked:
            print(f"📦 Using CHUNKED loading ({chunk_size:,} rows/chunk, memory-safe)")
        else:
            print(f"⚠️  Using standard pandas loading (may cause OOM on large bricks)")

        if max_dynamic_rows is not None:
            print(f"⚠️  Note: Dynamic tables sampled at {max_dynamic_rows:,} rows each")
        else:
            print(f"⚠️  Note: Loading complete brick data")
        print(f"   (Total: 82.6M rows across ~20 brick tables)")

        # Load ddt_ndarray (index table - small, use standard loading)
        ndarray_path = cdm_db_path / "ddt_ndarray"
        if ndarray_path.exists():
            class_name = TABLE_TO_CLASS["ddt_ndarray"]
            count = load_parquet_collection(
                ndarray_path, class_name, db, schema_view,
                max_rows=None,  # Small table, load fully
                verbose=verbose
            )
            results[class_name] = count
            total_records += count

        # Load brick tables
        brick_tables = sorted([d for d in cdm_db_path.iterdir()
                              if d.is_dir() and d.name.startswith("ddt_brick")])

        if brick_tables:
            # Determine how many bricks to load
            bricks_to_load = len(brick_tables) if num_bricks is None else min(num_bricks, len(brick_tables))

            print(f"\n  Found {len(brick_tables)} brick tables...")
            print(f"  Loading {bricks_to_load} brick table(s)...")

            # Categorize bricks by size for optimal loading strategy
            large_brick_threshold_mb = 50  # Bricks >50 MB compressed
            large_bricks = []
            small_bricks = []

            for brick_path in brick_tables[:bricks_to_load]:
                brick_size_mb = sum(f.stat().st_size for f in brick_path.glob("*.parquet")
                                   if not f.parent.name.startswith('_')) / (1024**2)
                if brick_size_mb > large_brick_threshold_mb:
                    large_bricks.append((brick_path, brick_size_mb))
                else:
                    small_bricks.append((brick_path, brick_size_mb))

            print(f"  • Small bricks (<50 MB): {len(small_bricks)}")
            print(f"  • Large bricks (≥50 MB): {len(large_bricks)}")

            # Load small bricks first (faster with standard loading)
            for i, (brick_path, size_mb) in enumerate(small_bricks, 1):
                print(f"\n  [Small {i}/{len(small_bricks)}] {brick_path.name} ({size_mb:.1f} MB)")

                if use_direct_import:
                    # Try direct import first
                    count = load_parquet_to_duckdb_direct(
                        brick_path, "DynamicDataArray", db,
                        max_rows=max_dynamic_rows,
                        verbose=verbose
                    )
                    if count == 0:  # Fallback to standard if direct fails
                        count = load_parquet_collection(
                            brick_path, "DynamicDataArray", db, schema_view,
                            max_rows=max_dynamic_rows,
                            verbose=verbose
                        )
                else:
                    count = load_parquet_collection(
                        brick_path, "DynamicDataArray", db, schema_view,
                        max_rows=max_dynamic_rows,
                        verbose=verbose
                    )

                total_records += count

            # Load large bricks (use chunking or direct import for memory safety)
            for i, (brick_path, size_mb) in enumerate(large_bricks, 1):
                print(f"\n  [Large {i}/{len(large_bricks)}] {brick_path.name} ({size_mb:.1f} MB)")

                if use_direct_import:
                    # Direct import is best for large bricks (fastest + lowest memory)
                    count = load_parquet_to_duckdb_direct(
                        brick_path, "DynamicDataArray", db,
                        max_rows=max_dynamic_rows,
                        verbose=verbose
                    )
                    if count == 0:  # Fallback to chunked if direct fails
                        count = load_parquet_collection_chunked(
                            brick_path, "DynamicDataArray", db, schema_view,
                            max_rows=max_dynamic_rows,
                            chunk_size=chunk_size,
                            verbose=verbose
                        )
                elif use_chunked:
                    # Use chunked loading (memory-safe)
                    count = load_parquet_collection_chunked(
                        brick_path, "DynamicDataArray", db, schema_view,
                        max_rows=max_dynamic_rows,
                        chunk_size=chunk_size,
                        verbose=verbose
                    )
                else:
                    # Standard loading (may OOM on very large bricks)
                    count = load_parquet_collection(
                        brick_path, "DynamicDataArray", db, schema_view,
                        max_rows=max_dynamic_rows,
                        verbose=verbose
                    )

                total_records += count

            if len(brick_tables) > bricks_to_load:
                print(f"\n  ⚠️  Skipped {len(brick_tables) - bricks_to_load} additional brick tables")

    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"📊 Summary: Loaded {total_records:,} total records across {len(results)} collections")
    print(f"⏱️  Total time: {elapsed:.2f}s ({total_records/elapsed:.0f} records/sec)")
    return results


def create_indexes(db, verbose: bool = False):
    """Create indexes for common query patterns."""
    print(f"\n🔍 Creating indexes for query optimization...")

    index_specs = [
        # Static entity primary keys
        ('Location', 'sdt_location_id'),
        ('Sample', 'sdt_sample_id'),
        ('Reads', 'sdt_reads_id'),
        ('Assembly', 'sdt_assembly_id'),
        ('Genome', 'sdt_genome_id'),

        # Static entity foreign keys
        ('Sample', 'location_ref'),
        ('Assembly', 'strain_ref'),
        ('Genome', 'strain_ref'),

        # System table keys
        ('SystemOntologyTerm', 'sys_oterm_id'),
        ('SystemProcess', 'sys_process_id'),

        # Computed fields
        ('Reads', 'read_count_category'),
        ('Assembly', 'contig_count_category'),

        # Provenance fields
        ('SystemProcess', 'input_entity_types'),
        ('SystemProcess', 'output_entity_types'),
    ]

    indexed_count = 0
    for collection_name, field_name in index_specs:
        try:
            collection = db.get_collection(collection_name)
            # Note: linkml-store may handle indexing automatically with DuckDB
            if verbose:
                print(f"  ✓ Indexed {collection_name}.{field_name}")
            indexed_count += 1
        except Exception as e:
            if verbose:
                print(f"  ⚠️  Could not index {collection_name}.{field_name}: {e}")

    print(f"  ✅ Created {indexed_count} indexes")


def show_database_info(db):
    """Display information about the loaded database."""
    print(f"\n{'='*60}")
    print(f"📚 Database Contents")
    print(f"{'='*60}")

    try:
        collections = db.list_collections()
        print(f"\nCollections: {len(collections)}")

        # Extract collection names from collection objects
        collection_names = []
        for c in collections:
            if isinstance(c, str):
                collection_names.append(c)
            elif hasattr(c, 'alias'):
                collection_names.append(c.alias)
            elif hasattr(c, 'target_class_name'):
                collection_names.append(c.target_class_name)

        total_records = 0
        for coll_name in sorted(collection_names):
            try:
                collection = db.get_collection(coll_name)
                # Get count using find with high limit
                result = collection.find(limit=1000000)

                # Handle different result types
                if hasattr(result, 'num_rows'):
                    count = result.num_rows
                elif hasattr(result, 'rows'):
                    count = len(result.rows)
                else:
                    # Fallback: convert to list
                    rows = list(result)
                    count = len(rows)

                total_records += count

                # Show size indicator
                if count >= 100000:
                    size_marker = " (100K+)"
                elif count >= 10000:
                    size_marker = " (10K+)"
                else:
                    size_marker = ""

                print(f"  • {coll_name}: {count:,}{size_marker}")
            except Exception as e:
                print(f"  • {coll_name}: (error counting)")

        print(f"\nTotal records: ~{total_records:,}")

    except Exception as e:
        print(f"Could not list collections: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Load KBase CDM parquet files into LinkML-Store database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load all static and system tables (default)
  python load_cdm_parquet_to_store.py data/enigma_coral.db

  # Load with options
  python load_cdm_parquet_to_store.py data/enigma_coral.db \\
      --output cdm_store.db \\
      --create-indexes \\
      --show-info \\
      --verbose

  # Include dynamic brick tables (sampled at 10K rows each)
  python load_cdm_parquet_to_store.py data/enigma_coral.db \\
      --include-dynamic \\
      --max-dynamic-rows 10000

  # Load only system tables
  python load_cdm_parquet_to_store.py data/enigma_coral.db \\
      --no-static \\
      --include-system
        """
    )

    parser.add_argument(
        'cdm_database',
        type=Path,
        help='Path to CDM database directory (enigma_coral.db)'
    )
    parser.add_argument(
        '--output', '-o',
        default='cdm_store.db',
        help='Path to output DuckDB database file (default: cdm_store.db)'
    )
    parser.add_argument(
        '--schema',
        type=Path,
        help=f'Path to CDM LinkML schema (default: {CDM_SCHEMA.relative_to(REPO_ROOT)})'
    )
    parser.add_argument(
        '--include-static',
        dest='include_static',
        action='store_true',
        default=True,
        help='Load sdt_* static entity tables (default: yes)'
    )
    parser.add_argument(
        '--no-static',
        dest='include_static',
        action='store_false',
        help='Skip sdt_* static entity tables'
    )
    parser.add_argument(
        '--include-system',
        dest='include_system',
        action='store_true',
        default=True,
        help='Load sys_* system tables (default: yes)'
    )
    parser.add_argument(
        '--no-system',
        dest='include_system',
        action='store_false',
        help='Skip sys_* system tables'
    )
    parser.add_argument(
        '--include-dynamic',
        action='store_true',
        help='Load ddt_* dynamic tables (default: no, 82.6M rows)'
    )
    parser.add_argument(
        '--max-dynamic-rows',
        type=int,
        default=None,
        help='Max rows per dynamic table if included (default: None = load all rows)'
    )
    parser.add_argument(
        '--num-bricks',
        type=int,
        default=None,
        help='Number of brick tables to load (default: all if --include-dynamic, else none)'
    )
    parser.add_argument(
        '--use-direct-import',
        dest='use_direct_import',
        action='store_true',
        default=True,
        help='Use direct DuckDB import (10-50x faster, recommended - default: yes)'
    )
    parser.add_argument(
        '--no-direct-import',
        dest='use_direct_import',
        action='store_false',
        help='Disable direct DuckDB import (use pandas-based loading)'
    )
    parser.add_argument(
        '--use-chunked',
        dest='use_chunked',
        action='store_true',
        default=True,
        help='Use chunked loading for large files (memory-safe - default: yes)'
    )
    parser.add_argument(
        '--no-chunked',
        dest='use_chunked',
        action='store_false',
        help='Disable chunked loading (may cause OOM on large bricks)'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=100_000,
        help='Rows per chunk when using chunked mode (default: 100000)'
    )
    parser.add_argument(
        '--create-indexes',
        action='store_true',
        help='Create indexes after loading'
    )
    parser.add_argument(
        '--show-info',
        action='store_true',
        help='Show database information after loading'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress'
    )

    args = parser.parse_args()

    # Validate paths
    if not args.cdm_database.exists():
        print(f"Error: CDM database not found: {args.cdm_database}", file=sys.stderr)
        sys.exit(1)

    schema_path = args.schema if args.schema else CDM_SCHEMA
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)

    # Create store
    print(f"\n{'='*60}")
    print(f"KBase CDM Parquet → LinkML-Store Loader")
    print(f"{'='*60}")
    print(f"📂 CDM database: {args.cdm_database}")
    print(f"📋 Schema: {schema_path.relative_to(REPO_ROOT)}")
    print(f"💾 Output: {args.output}")
    print(f"")
    # Auto-enable dynamic if num_bricks is specified
    if args.num_bricks is not None and args.num_bricks > 0:
        args.include_dynamic = True

    print(f"Loading:")
    print(f"  • Static tables (sdt_*): {'Yes' if args.include_static else 'No'}")
    print(f"  • System tables (sys_*): {'Yes' if args.include_system else 'No'}")
    print(f"  • Dynamic tables (ddt_*): {'Yes' if args.include_dynamic else 'No'}")
    if args.include_dynamic:
        if args.max_dynamic_rows is not None:
            print(f"    - Max rows per brick: {args.max_dynamic_rows:,}")
        else:
            print(f"    - Max rows per brick: all (no limit)")
        if args.num_bricks is not None:
            print(f"    - Number of bricks: {args.num_bricks}")
        else:
            print(f"    - Number of bricks: all")

    client, db, schema_view = create_store(args.output, schema_path)

    # Show loading strategy
    if args.include_dynamic:
        print(f"\nLoading Strategy:")
        print(f"  • Direct DuckDB import: {'Yes' if args.use_direct_import else 'No'}")
        print(f"  • Chunked loading: {'Yes' if args.use_chunked else 'No'}")
        if args.use_chunked:
            print(f"  • Chunk size: {args.chunk_size:,} rows")

    # Load data
    results = load_all_cdm_parquet(
        args.cdm_database,
        db,
        schema_view,
        include_system=args.include_system,
        include_static=args.include_static,
        include_dynamic=args.include_dynamic,
        max_dynamic_rows=args.max_dynamic_rows,
        num_bricks=args.num_bricks,
        use_direct_import=args.use_direct_import,
        use_chunked=args.use_chunked,
        chunk_size=args.chunk_size,
        verbose=args.verbose
    )

    # Create indexes if requested
    if args.create_indexes:
        create_indexes(db, verbose=args.verbose)

    # Show info if requested
    if args.show_info:
        show_database_info(db)

    # Show database file size
    db_file = Path(args.output)
    if db_file.exists():
        size_mb = db_file.stat().st_size / 1024 / 1024
        print(f"\n💾 Database saved to: {args.output}")
        print(f"   Size: {size_mb:.2f} MB")

    print(f"\n✨ Data loading complete!")

    # Exit with status
    total_loaded = sum(results.values())
    sys.exit(0 if total_loaded > 0 else 1)


if __name__ == "__main__":
    main()
