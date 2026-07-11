from search_engine.indexing.index import InvertedIndex
from search_engine.indexing.tokenizer import tokenize


def search_naive(query: str, index: InvertedIndex, k: int = 10) -> list[int]:
    """
    Naive keyword-match baseline: returns doc_ids containing ALL query terms
    (exact boolean AND match), no ranking/weighting. Order is arbitrary
    (insertion order from postings), not relevance-sorted.
    """
    query_terms = tokenize(query)
    if not query_terms:
        return []

    matching_doc_ids = None
    for term in query_terms:
        doc_ids = {p.doc_id for p in index.postings.get(term, [])}
        if matching_doc_ids is None:
            matching_doc_ids = doc_ids
        else:
            matching_doc_ids &= doc_ids

    if not matching_doc_ids:
        return []

    return sorted(matching_doc_ids)[:k]