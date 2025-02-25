from lex.oed.thesaurus.taxonomymanager import TaxonomyManager
import dataclassio

import config
from . import models


_INPUT_FILE = config.PARTIALS_TRIAGE_DIR / "partial.csv"
_OUTPUT_DIR = config.PARTIALS_SUBCATEGORIES_DIR
_PARTIALS_CATEGORIES = {
    "food": "45970",
    "drink": "50237",
    "inhabited_place": "158520",
    "politics": "168151",
}


def subcategorize_partials() -> None:
    buckets = {c: [] for c in _PARTIALS_CATEGORIES.keys()}
    taxonomy_manager = TaxonomyManager()
    thesaurus_records = dataclassio.convert_csv_file_to_dataclasses(
        _INPUT_FILE,
        models.ThesaurusRecord,
    )
    for record in thesaurus_records:
        category_id = record.thesaurus_id
        category = taxonomy_manager.find_class(category_id)
        if category:
            for (
                parent_category_label,
                parent_category_id,
            ) in _PARTIALS_CATEGORIES.items():
                if category.is_descendant_of(parent_category_id):
                    buckets[parent_category_label].append(record)
        else:
            for parent_category_label in _PARTIALS_CATEGORIES.keys():
                if _breadcrumb_matches(
                    record.revision_file_comment, parent_category_label
                ):
                    buckets[parent_category_label].append(record)

    for parent_category_label, records in buckets.items():
        filepath = _OUTPUT_DIR / f"{parent_category_label}.csv"
        dataclassio.write_dataclasses_to_csv(records, filepath)


def _breadcrumb_matches(revision_file_comment: str, category: str) -> bool:
    if not revision_file_comment:
        return False
    category = category.replace("_", " ")
    if (
        f"> {category} >" in revision_file_comment
        or f"» {category} »" in revision_file_comment
    ):
        return True
    return False
