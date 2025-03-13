"""
list_long_category_headers()
    Create a ranked list oif the 1000 longest category headers in
    the historical thesaurus.
"""

import dataclasses

from lex.oed.thesaurus.thesaurusiterator import ThesaurusIterator
import dataclassio
from src import config


_OUTPUT_FILE = config.LONG_CATEGORIES_FILE


@dataclasses.dataclass
class CategoryStats:
    """
    Information about a thesaurus category with a long heading.
    """

    category_id: int
    heading: str
    heading_length: int
    breadcrumb_length: int
    level: int
    url: str


def list_long_category_headers() -> None:
    """
    Create a ranked list oif the 1000 longest category headers in
    the historical thesaurus.

    Returns
    -------
        None
    """
    categories: list[CategoryStats] = []
    thesaurus_iterator = ThesaurusIterator()
    for category in thesaurus_iterator:
        if not category.label or len(category.label) < 10:
            continue
        categories.append(
            CategoryStats(
                category_id=int(category.id),
                heading=category.label,
                heading_length=len(category.label) or 0,
                breadcrumb_length=len(category.breadcrumb) or 0,
                level=category.level,
                url=category.thesaurus_browser_url,
            )
        )

    categories.sort(key=lambda category: category.category_id)
    categories.sort(key=lambda category: category.heading_length, reverse=True)

    dataclassio.write_dataclasses_to_csv(categories[0:1000], _OUTPUT_FILE)
