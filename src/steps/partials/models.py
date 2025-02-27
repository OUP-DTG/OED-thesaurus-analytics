import dataclasses


@dataclasses.dataclass
class AttnThesComment:
    entry_id: str
    element_id: str
    comment: str


@dataclasses.dataclass
class ThesaurusRecord:
    entry_id: str
    element_id: str
    url: str | None = None
    entry: str | None = None
    lemma: str | None = None
    part_of_speech: str | None = None
    definition: str | None = None
    start_year: int | None = None
    end_year: int | None = None
    frequency: str | None = None
    obsolete: bool = False
    revision_file_comment: str | None = None
    htclassifier_comment: str | None = None
    thesaurus_id: str | None = None
    thesaurus_breadcrumb: str | None = None
