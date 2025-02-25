import csv

from lex.entryiterator import OedEntryIterator
from lex.oed.entry import Entry
from lex.oed.senseunit.senseunit import SenseUnit
import dataclassio

from src import config
from . import models, comments


def list_senses() -> None:
    partials = _load_partials_ids()
    results: list[models.ComputingSense] = []
    iterator = OedEntryIterator(
        path=config.OEDLATEST_DIRECTORY,
        progress_bar="single",
    )
    for entry in iterator.iterate():
        results.extend(_get_computing_senses(entry, partials))
    dataclassio.write_dataclasses_to_csv(results, config.COMPUTING_SENSES_NODES_FILE)


def _get_computing_senses(
    entry: Entry,
    partials: dict[tuple[str, str], str],
) -> list[models.ComputingSense]:
    results: list[models.ComputingSense] = []
    for sense in entry.sense_units():
        key = (entry.entry_id, sense.element_id)
        subjects = sense.characteristics.nodes("subject")
        if (
            "Computing" not in subjects
            and "computing" not in subjects
            and key not in partials
        ):
            continue

        suggested_category = partials.get(key, None)
        thesaurus_nodes = _get_thesaurus_nodes(sense)
        results.append(
            models.ComputingSense(
                entry_id=entry.entry_id,
                element_id=sense.element_id,
                entry_title=entry.title(),
                sense_number=_get_sense_number(sense),
                url=sense.dictionary_browser_url(entry_id=entry.entry_id),
                lemma=sense.lemma,
                link="",
                definition=_get_definition(sense),
                frequency=_get_frequency(entry, sense),
                thesaurus_category1=thesaurus_nodes[0],
                thesaurus_category2=thesaurus_nodes[1],
                thesaurus_category3=thesaurus_nodes[2],
                thesaurus_category4=thesaurus_nodes[3],
                suggested_thesaurus_category=suggested_category,
                comment=comments.get_comments(entry.entry_id, sense.element_id),
            )
        )
    return results


def _get_definition(sense: SenseUnit) -> str | None:
    defn = sense.definition(length=200)
    if not defn:
        return None
    if defn.startswith("="):
        return f"_{defn}"
    return defn


def _get_sense_number(sense: SenseUnit) -> str:
    if not sense.attribute("num"):
        return ""
    sense_num = _convert_sense_number(sense.attribute("num"), sense.source_tag())
    for parent_elt in sense.ancestor_elements:
        if parent_elt.tag not in ("s6", "s7", "s4", "s2"):
            continue
        number = _convert_sense_number(parent_elt.get("num"), parent_elt.tag)
        if not number:
            continue
        sense_num = f"{number}.{sense_num or ''}"
        sense_num = sense_num.strip(". ")
    return sense_num or ""


def _convert_sense_number(number: str | None, tag: str) -> str:
    if not number:
        return ""
    if tag == "s4":
        return number
    if tag in ("s7", "s6"):
        mappings = {
            "1": "a",
            "2": "b",
            "3": "c",
            "4": "d",
            "5": "e",
            "6": "f",
            "7": "g",
            "8": "h",
            "9": "i",
            "10": "j",
            "11": "k",
            "12": "l",
            "13": "m",
            "14": "n",
            "15": "o",
            "16": "p",
            "17": "q",
            "18": "r",
        }
        return mappings.get(number, number)
    if tag == "s2":
        mappings = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V", "6": "VI"}
        return mappings.get(number, number)
    return ""


def _get_thesaurus_nodes(sense: SenseUnit) -> list[str | None]:
    thesaurus_nodes: list[str | None] = list(
        sorted(sense.characteristics.leaves("thesaurus"))
    )
    thesaurus_nodes.extend([None, None, None, None])
    return thesaurus_nodes


def _load_partials_ids() -> dict[tuple[str, str], str]:
    partials: dict[tuple[str, str], str] = {}
    with config.PARTIAL_SENSES_FILE.open() as filehandle:
        reader = csv.reader(filehandle)
        for row in reader:
            partials[(row[0], row[1])] = row[7]
    return partials


def _get_frequency(entry: Entry, sense: SenseUnit) -> str | None:
    return sense.attribute("freqpm") or entry.attribute("freqpm") or None
