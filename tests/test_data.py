"""Data test."""
import os
import glob
import pytest
from pathlib import Path

import importlib.util
import sys
from linkml_runtime.loaders import yaml_loader

DATA_DIR_VALID = Path(__file__).parent / "data" / "valid"
DATA_DIR_INVALID = Path(__file__).parent / "data" / "invalid"

VALID_EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR_VALID, '*.yaml'))
INVALID_EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR_INVALID, '*.yaml'))

# Import the datamodel module using importlib.util.spec_from_file_location
datamodel_path = Path(__file__).parent.parent / "src" / "linkml_coral" / "datamodel" / "linkml_coral.py"
spec = importlib.util.spec_from_file_location("datamodel", datamodel_path)
datamodel = importlib.util.module_from_spec(spec)
sys.modules["datamodel"] = datamodel
spec.loader.exec_module(datamodel)


@pytest.mark.parametrize("filepath", VALID_EXAMPLE_FILES)
def test_valid_data_files(filepath):
    """Test loading of all valid data files."""
    target_class_name = Path(filepath).stem.split("-")[0]
    tgt_class = getattr(
        datamodel,
        target_class_name,
    )
    obj = yaml_loader.load(filepath, target_class=tgt_class)
    assert obj
