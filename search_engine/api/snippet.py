import string

from nltk.stem import PorterStemmer

_STEMMER = PorterStemmer()
_PUNCT_TABLE = str.maketrans("", "", string.punctuation)


def extract_snippet(text: str, query_terms: list[str], window: int = 18) -> str:
    """
    Find the first word in `text` whose stem matches a query term, and return
    a short excerpt of `window` words on each side with matches wrapped in
    <mark> tags. Falls back to a leading excerpt if no match is found.
    """
    words = text.split()
    stemmed_words = [_STEMMER.stem(w.lower().translate(_PUNCT_TABLE)) for w in words]
    query_term_set = set(query_terms)

    match_index = None
    for i, stemmed in enumerate(stemmed_words):
        if stemmed in query_term_set:
            match_index = i
            break

    if match_index is None:
        excerpt_words = words[: window * 2]
        return " ".join(excerpt_words)

    start = max(0, match_index - window)
    end = min(len(words), match_index + window + 1)

    excerpt_words = []
    for i in range(start, end):
        if stemmed_words[i] in query_term_set:
            excerpt_words.append(f"<mark>{words[i]}</mark>")
        else:
            excerpt_words.append(words[i])

    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(words) else ""
    return prefix + " ".join(excerpt_words) + suffix