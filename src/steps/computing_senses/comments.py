import re

from lex.oed.resources.comments import commentmanager


def get_comments(entry_id: str, element_id: str) -> str | None:
    if not get_comments.thesaurus_comments:
        get_comments.thesaurus_comments = _load_comments()

    entry_id = str(entry_id)
    element_id = str(element_id)
    if entry_id not in get_comments.thesaurus_comments:
        return None

    comments = []
    for comment in get_comments.thesaurus_comments[entry_id]:
        if comment.element_id == element_id:
            comments.append(comment.text)
    return " | ".join(comments)[0:500]


get_comments.thesaurus_comments = {}


def thesfilter(comment: commentmanager.CommentRow) -> bool:
    if comment.text and re.search(r"suggested thes", comment.text, re.I):
        return True
    return False


def _load_comments() -> dict[str, list[commentmanager.CommentRow]]:
    return commentmanager.comments_per_entry(filterfunc=thesfilter)
