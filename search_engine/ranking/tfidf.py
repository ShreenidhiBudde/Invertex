import math

from search_engine.indexing.index import InvertedIndex
from search_engine.indexing.tokenizer import tokenize


def term_frequency(term: str, doc_id: int, index: InvertedIndex) -> float:
    postings = index.postings.get(term, [])
    for posting in postings:
        if posting.doc_id == doc_id:
            return float(posting.term_frequency)
    return 0.0


def inverse_document_frequency(term: str, index: InvertedIndex) -> float:
    postings = index.postings.get(term, [])
    df = len(postings)
    if df == 0:
        return 0.0
    return math.log(index.doc_count / df)


def score_document(query_terms: list[str], doc_id: int, index: InvertedIndex) -> float:
    score = 0.0
    for term in query_terms:
        tf = term_frequency(term, doc_id, index)
        if tf == 0.0:
            continue
        idf = inverse_document_frequency(term, index)
        score += tf * idf
    return score


def search_tfidf(query: str, index: InvertedIndex, k: int = 10) -> list[tuple[int, float]]:
    query_terms = tokenize(query)

    scores: dict[int, float] = {}
    for term in query_terms:
        postings = index.postings.get(term, [])
        if not postings:
            continue
        idf = inverse_document_frequency(term, index)
        for posting in postings:
            scores[posting.doc_id] = scores.get(posting.doc_id, 0.0) + posting.term_frequency * idf

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:k]