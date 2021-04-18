from pathlib import Path

SRC_ROOT = Path(__file__).parent.parent
SPARQL_J2_DIR = (SRC_ROOT / "query_templates").resolve()
PROJECT_ROOT = SRC_ROOT.parent
DATA_DIR = (SRC_ROOT.parent / "data/rdf").resolve()
INTEREST_TO_VEC = (SRC_ROOT.parent / "data/interest_profile_setup/interest_topic_vectors.pkl").resolve()
URI_TO_VEC = (SRC_ROOT.parent / "data/interest_profile_setup/output_courseuri_topic_vectors.pkl").resolve()
