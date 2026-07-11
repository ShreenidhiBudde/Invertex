from dataclasses import dataclass

from search_engine.indexing.index import InvertedIndex
from search_engine.indexing.tokenizer import tokenize
from search_engine.query.boolean import boolean_search
from search_engine.query.fuzzy import find_closest_terms
from search_engine.query.phrase import phrase_search
from search_engine.ranking.bm25 import search_bm25


@dataclass
class Result:
    doc_id: int
    score: float | None = None


def _is_phrase_query(query: str) -> bool:
    stripped = query.strip()
    return stripped.startswith('"') and stripped.endswith('"') and len(stripped) > 1


def _is_boolean_query(query: str) -> bool:
    upper = query.upper()
    return " AND " in upper or " OR " in upper


def search(query: str, index: InvertedIndex, mode: str = "auto", k: int = 10) -> list[Result]:
    if mode == "phrase" or (mode == "auto" and _is_phrase_query(query)):
        phrase_text = query.strip().strip('"')
        doc_ids = phrase_search(phrase_text, index)
        return [Result(doc_id=doc_id) for doc_id in doc_ids[:k]]

    if mode == "boolean" or (mode == "auto" and _is_boolean_query(query)):
        doc_ids = boolean_search(query, index)
        return [Result(doc_id=doc_id) for doc_id in doc_ids[:k]]

    query_terms = tokenize(query)
    unmatched = [t for t in query_terms if t not in index.postings]

    if query_terms and len(unmatched) == len(query_terms):
        # every query term is unmatched -> fuzzy fallback
        expanded_terms = []
        for term in query_terms:
            closest = find_closest_terms(term, index, max_distance=3, limit=1)
            expanded_terms.extend(closest)

        if not expanded_terms:
            return []

        expanded_query = " ".join(expanded_terms)
        results = search_bm25(expanded_query, index, k=k)
        return [Result(doc_id=doc_id, score=score) for doc_id, score in results]

    results = search_bm25(query, index, k=k)
    return [Result(doc_id=doc_id, score=score) for doc_id, score in results]