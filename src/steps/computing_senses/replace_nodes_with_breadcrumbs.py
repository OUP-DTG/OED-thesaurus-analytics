from lex.oed.thesaurus import thesaurusdb
import dataclassio

from src import config
from . import models


def replace_nodes() -> None:
    computing_senses = dataclassio.convert_csv_file_to_dataclasses(
        config.COMPUTING_SENSES_NODES_FILE,
        models.ComputingSense,
    )
    _replace_thesaurus_nodes(computing_senses)
    dataclassio.write_dataclasses_to_csv(
        computing_senses,
        config.COMPUTING_SENSES_FINAL_FILE,
    )


def _replace_thesaurus_nodes(computing_senses: list[models.ComputingSense]) -> None:
    for sense in computing_senses:
        sense.thesaurus_category1 = _get_breadcrumb(sense.thesaurus_category1)
        sense.thesaurus_category2 = _get_breadcrumb(sense.thesaurus_category2)
        sense.thesaurus_category3 = _get_breadcrumb(sense.thesaurus_category3)
        sense.thesaurus_category4 = _get_breadcrumb(sense.thesaurus_category4)


def _get_breadcrumb(category_id: str | None) -> str | None:
    if not category_id:
        return None
    category = thesaurusdb.get_thesclass(category_id)
    if not category:
        return category_id
    return f"{category.breadcrumb} ({category_id})"
