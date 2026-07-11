from search_engine.indexing.index import InvertedIndex
from search_engine.indexing.tokenizer import tokenize


def _positions_for(term: str, doc_id: int, index: InvertedIndex) -> list[int]:
    postings = index.postings.get(term, [])
    for posting in postings:
        if posting.doc_id == doc_id:
            return posting.positions
    return []


def phrase_search(phrase: str, index: InvertedIndex) -> list[int]:
    """
    Given a phrase (e.g. from a quoted query like "null pointer exception"),
    returns doc_ids where the terms appear in consecutive positions in order.
    """
    terms = tokenize(phrase)
    if not terms:
        return []

    if len(terms) == 1:
        postings = index.postings.get(terms[0], [])
        return sorted(p.doc_id for p in postings)

    candidate_doc_ids = None
    for term in terms:
        doc_ids = {p.doc_id for p in index.postings.get(term, [])}
        if candidate_doc_ids is None:
            candidate_doc_ids = doc_ids
        else:
            candidate_doc_ids &= doc_ids

    if not candidate_doc_ids:
        return []

    matching_doc_ids = []
    for doc_id in candidate_doc_ids:
        first_term_positions = _positions_for(terms[0], doc_id, index)

        for start_pos in first_term_positions:
            match = True
            for offset, term in enumerate(terms[1:], start=1):
                term_positions = _positions_for(term, doc_id, index)
                if (start_pos + offset) not in term_positions:
                    match = False
                    break
            if match:
                matching_doc_ids.append(doc_id)
                break

    return sorted(matching_doc_ids)