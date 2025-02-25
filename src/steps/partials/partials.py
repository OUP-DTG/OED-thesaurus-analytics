import json
import csv
import dataclasses
from collections import defaultdict

from lex.oed.thesaurus.taxonomymanager import TaxonomyManager
from lex.entryiterator import OedEntryIterator
import dataclassio

from src import config
from . import attnthescomments, models


_TAXONOMY_MANAGER = TaxonomyManager()


def partials_to_csv() -> None:
    _results_to_csv("partial")


def approved_to_csv() -> None:
    _results_to_csv("correct")


def incorrect_to_csv() -> None:
    _results_to_csv("incorrect")


def _results_to_csv(mode: str) -> None:
    data = _load_data(mode)
    if mode == "partial":
        data.extend(_load_comment_data())
    sense_log: dict[str, dict[str, models.ThesaurusRecord]] = defaultdict(dict)
    for thesaurus_record in data:
        if (
            thesaurus_record.entry_id in sense_log
            and thesaurus_record.element_id in sense_log[thesaurus_record.entry_id]
        ):
            continue
        sense_log[thesaurus_record.entry_id][
            thesaurus_record.element_id
        ] = thesaurus_record

    results: list[models.ThesaurusRecord] = []
    iterator = OedEntryIterator(
        filepath=config.OEDLATEST_DIRECTORY,
        include_entry_ids=sense_log.keys(),
        progress_bar="single",
    )
    for entry in iterator.iterate():
        for sense in entry.sense_units():
            if sense.element_id not in sense_log[entry.id]:
                continue
            thesaurus_record = sense_log[entry.id][sense.element_id]
            thesaurus_record = dataclasses.replace(
                thesaurus_record,
                url=sense.dictionary_browser_url(entry.id),
                entry=entry.title(),
                lemma=sense.lemma,
                part_of_speech=sense.wordclasses[0].ode,
                definition=_clean_definition(sense.definition(length=100)),
                start_year=sense.date.start,
                end_year=sense.date.end,
                obsolete=sense.is_marked_obsolete(),
            )
            results.append(thesaurus_record)

    filepath = config.PARTIALS_TRIAGE_DIR / f"{mode}.csv"
    dataclassio.write_dataclasses_to_csv(results, filepath)


def _load_data(mode: str) -> list[models.ThesaurusRecord]:
    data: list[models.ThesaurusRecord] = []
    directory = config.NEW_CLASSIFICATION_DIR
    filepaths = directory.glob(f"{mode}*.json")
    for filepath in filepaths:
        with filepath.open() as filehandle:
            for instance in json.load(filehandle):
                record = models.ThesaurusRecord(
                    entry_id=str(instance[0]),
                    element_id=str(instance[1]),
                    thesaurus_id=str(instance[2]),
                )
                try:
                    record.htclassifier_comment = _clean_comment(instance[3])
                except IndexError:
                    pass
                try:
                    record.thesaurus_breadcrumb = _TAXONOMY_MANAGER.breadcrumb(
                        record.thesaurus_id
                    )
                except ValueError:
                    pass
                record.revision_file_comment = attnthescomments.get_comments(
                    record.entry_id,
                    record.element_id,
                )
                data.append(record)
    return data


def _load_comment_data() -> list[models.ThesaurusRecord]:
    data: list[models.ThesaurusRecord] = []
    with config.PARTIALS_COMMENTS_FILE.open() as filehandle:
        reader = csv.reader(filehandle)
        for row in reader:
            comment_text = row[2]
            if "suggested thes no specific class" in comment_text.lower():
                record = models.ThesaurusRecord(
                    entry_id=row[0],
                    element_id=row[1],
                    revision_file_comment=row[2],
                )
                data.append(record)
    return data


def _clean_comment(comment: str | None) -> str:
    if not comment or comment.lower() == "none":
        comment = ""
    for before, after in (
        ("\n", " "),
        ("\r", " "),
        ("  ", " "),
    ):
        comment = comment.replace(before, after)
    return comment


def _clean_definition(definition: str | None) -> str | None:
    if not definition:
        return definition
    if definition.startswith("="):
        return "_" + definition
    return definition
