from lex.oed.resources.comments import commentmanager


def get_comments(entry_id: str, element_id: str) -> str | None:
    if not get_comments.comments:
        get_comments.comments = _load_comments()

    entry_id = str(entry_id)
    if entry_id not in get_comments.comments:
        return None

    element_id = str(element_id)
    comments: list[str] = []
    for comment in get_comments.comments[entry_id]:
        if comment.element_id == element_id:
            comments.append(comment.text)
    if not comments:
        return None
    return " | ".join(comments)[0:500]


get_comments.comments = {}


def _thesfilter(comment: commentmanager.CommentRow) -> bool:
    if comment.text and "attnthes" in comment.text.lower():
        return True
    if comment.topic and "attnthes" in comment.topic.lower():
        return True
    return False


def _load_comments() -> dict[str, list[commentmanager.CommentRow]]:
    return commentmanager.comments_per_entry(filterfunc=_thesfilter)
