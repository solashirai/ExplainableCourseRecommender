from pathlib import Path

SRC_ROOT = Path(__file__).parent.parent
SPARQL_DIR = (SRC_ROOT / "query_templates").resolve()
SPARQL_J2_DIR = (SPARQL_DIR / "j2").resolve()
PROJECT_ROOT = SRC_ROOT.parent
