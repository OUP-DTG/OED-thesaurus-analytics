import os
import pathlib

_BASE_DIR = pathlib.Path(os.environ.get("LEX_BASE_DIR", "/data01"))

# Main directories
OEDLATEST_DIRECTORY = (
    _BASE_DIR / "OED" / "oed_data_processing" / "dictionary" / "dev" / "oedlatest_text"
)

# HT Classifier directories
HTCLASSIFIER_ROOT = _BASE_DIR / "OED" / "projects" / "thesaurus" / "htclassifier"
NEW_CLASSIFICATION_DIR = HTCLASSIFIER_ROOT / "new_classifications" / "checked_output"


ROOT_DIRECTORY = _BASE_DIR / "OED" / "projects" / "thesaurus" / "thesaurus_analytics"

# Filepaths for log files
LOGGING_DIR = ROOT_DIRECTORY.parent / "logs"
LOG_FILE = LOGGING_DIR / "thesaurus_analytics.log"

# Filepaths for 'computing_senses'
_COMPUTING_SENSES_DIR = ROOT_DIRECTORY / "computing_senses"
COMPUTING_SENSES_NODES_FILE = _COMPUTING_SENSES_DIR / "computing_senses_with_nodes.csv"
COMPUTING_SENSES_FINAL_FILE = _COMPUTING_SENSES_DIR / "computing_senses.csv"
PARTIAL_SENSES_FILE = _COMPUTING_SENSES_DIR / "partial_and_incorrect_senses.csv"

# Filepaths for 'partials'
_PARTIALS_DIR = ROOT_DIRECTORY / "partials"
PARTIALS_COMMENTS_FILE = _PARTIALS_DIR / "attnthes_comments" / "comments.csv"
PARTIALS_TRIAGE_DIR = _PARTIALS_DIR / "csv_triage"
PARTIALS_SUBCATEGORIES_DIR = _PARTIALS_DIR / "partials_subcategories"
