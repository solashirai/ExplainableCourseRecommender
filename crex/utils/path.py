from pathlib import Path

SRC_ROOT = Path(__file__).parent.parent
SPARQL_J2_DIR = (SRC_ROOT / "query_templates").resolve()
PROJECT_ROOT = SRC_ROOT.parent
DATA_DIR = (SRC_ROOT.parent / "data").resolve()
