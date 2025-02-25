import dataclasses


@dataclasses.dataclass
class ComputingSense:
    entry_id: str
    element_id: str
    entry_title: str
    sense_number: str
    url: str
    lemma: str
    link: str
    definition: str | None
    frequency: str | None
    thesaurus_category1: str | None = None
    thesaurus_category2: str | None = None
    thesaurus_category3: str | None = None
    thesaurus_category4: str | None = None
    suggested_thesaurus_category: str | None = None
    comment: str | None = None
