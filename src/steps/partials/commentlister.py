from lex.entryiterator import OedEntryIterator
import dataclassio

import config
from . import attnthescomments, models


def list_attnthes_comments() -> None:
    results: list[models.AttnThesComment] = []
    iterator = OedEntryIterator(
        filepath=config.OEDLATEST_DIRECTORY,
        progress_bar="multiple",
    )
    for entry in iterator.iterate():
        for sense in entry.sense_units():
            comments = attnthescomments.get_comments(
                entry.id,
                sense.element_id,
            )
            if not comments and sense.definition_manager:
                comments = attnthescomments.get_comments(
                    entry.id,
                    sense.definition_manager.element_id,
                )
            if not comments:
                continue
            results.append(
                models.AttnThesComment(
                    entry_id=entry.id,
                    element_id=sense.element_id,
                    comment=comments,
                )
            )
    dataclassio.write_dataclasses_to_csv(results, config.PARTIALS_COMMENTS_FILE)
