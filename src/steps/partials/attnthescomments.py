from lex.oed.resources.comments import commentmanager


_THES_COMMENTS = None


def get_comments(entry_id: str, element_id: str) -> str | None:
    _load_comments()
    entry_id = str(entry_id)
    element_id = str(element_id)
    comments = []
    if entry_id in _THES_COMMENTS:
        for comment in _THES_COMMENTS[entry_id]:
            if comment.element_id == element_id:
                comments.append(comment.text)
    if comments:
        return " | ".join(comments)[0:500]
    return None


def _thesfilter(comment) -> bool:
    if comment.text and "attnthes" in comment.text.lower():
        return True
    if comment.topic and "attnthes" in comment.topic.lower():
        return True
    return False


def _load_comments() -> None:
    global _THES_COMMENTS
    if _THES_COMMENTS is None:
        _THES_COMMENTS = commentmanager.comments_per_entry(
            filterfunc=_thesfilter,
        )
