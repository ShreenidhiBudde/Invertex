import math

from search_engine.indexing.index import InvertedIndex
from search_engine.indexing.tokenizer import tokenize


def bm25_score(term: str, doc_id: int, index: InvertedIndex, k1: float = 1.5, b: float = 0.75) -> float:
    postings = index.postings.get(term, [])
    df = len(postings)
    if df == 0:
        return 0.0

    posting = next((p for p in postings if p.doc_id == doc_id), None)
    if posting is None:
        return 0.0

    tf = posting.term_frequency
    doc_length = index.doc_lengths.get(doc_id, 0)
    avg_doc_length = index.avg_doc_length if index.avg_doc_length else 1.0

    idf = math.log((index.doc_count - df + 0.5) / (df + 0.5) + 1)

    numerator = tf * (k1 + 1)
    denominator = tf + k1 * (1 - b + b * (doc_length / avg_doc_length))

    return idf * (numerator / denominator)


def search_bm25(query: str, index: InvertedIndex, k: int = 10, k1: float = 1.5, b: float = 0.75) -> list[tuple[int, float]]:
    query_terms = tokenize(query)
    avg_doc_length = index.avg_doc_length if index.avg_doc_length else 1.0

    scores: dict[int, float] = {}
    for term in query_terms:
        postings = index.postings.get(term, [])
        if not postings:
            continue

        df = len(postings)
        idf = math.log((index.doc_count - df + 0.5) / (df + 0.5) + 1)

        for posting in postings:
            tf = posting.term_frequency
            doc_length = index.doc_lengths.get(posting.doc_id, 0)

            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (doc_length / avg_doc_length))
            term_score = idf * (numerator / denominator)

            scores[posting.doc_id] = scores.get(posting.doc_id, 0.0) + term_score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:k]