from pathlib import Path
# from .linkml_coral import *  # Commented out due to schema validation issues

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "linkml_coral.yaml"
