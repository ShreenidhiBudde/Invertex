from search_engine.indexing.index import InvertedIndex
from search_engine.indexing.tokenizer import tokenize


def intersect_postings(doc_ids_a: list[int], doc_ids_b: list[int]) -> list[int]:
    """AND: merge two sorted doc_id lists, keeping only common elements."""
    result = []
    i, j = 0, 0
    while i < len(doc_ids_a) and j < len(doc_ids_b):
        if doc_ids_a[i] == doc_ids_b[j]:
            result.append(doc_ids_a[i])
            i += 1
            j += 1
        elif doc_ids_a[i] < doc_ids_b[j]:
            i += 1
        else:
            j += 1
    return result


def union_postings(doc_ids_a: list[int], doc_ids_b: list[int]) -> list[int]:
    """OR: merge two sorted doc_id lists, keeping all elements (deduplicated)."""
    result = []
    i, j = 0, 0
    while i < len(doc_ids_a) and j < len(doc_ids_b):
        if doc_ids_a[i] == doc_ids_b[j]:
            result.append(doc_ids_a[i])
            i += 1
            j += 1
        elif doc_ids_a[i] < doc_ids_b[j]:
            result.append(doc_ids_a[i])
            i += 1
        else:
            result.append(doc_ids_b[j])
            j += 1
    result.extend(doc_ids_a[i:])
    result.extend(doc_ids_b[j:])
    return result


def _sorted_doc_ids(term: str, index: InvertedIndex) -> list[int]:
    postings = index.postings.get(term, [])
    return sorted(p.doc_id for p in postings)


def boolean_search(query: str, index: InvertedIndex) -> list[int]:
    """
    Parses a simple query like "term1 AND term2 OR term3" (left-to-right,
    no precedence/parens) and returns matching doc_ids via postings merges.
    """
    parts = query.split()

    operators = []
    terms = []
    for part in parts:
        upper = part.upper()
        if upper in ("AND", "OR"):
            operators.append(upper)
        else:
            stemmed = tokenize(part)
            if stemmed:
                terms.append(stemmed[0])

    if not terms:
        return []

    result = _sorted_doc_ids(terms[0], index)
    for i, op in enumerate(operators):
        if i + 1 >= len(terms):
            break
        next_doc_ids = _sorted_doc_ids(terms[i + 1], index)
        if op == "AND":
            result = intersect_postings(result, next_doc_ids)
        else:
            result = union_postings(result, next_doc_ids)

    return result