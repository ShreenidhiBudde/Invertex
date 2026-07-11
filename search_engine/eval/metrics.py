def precision_at_k(retrieved: list[int], relevant: set[int], k: int) -> float:
    top_k = retrieved[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for doc_id in top_k if doc_id in relevant)
    return hits / len(top_k)


def recall_at_k(retrieved: list[int], relevant: set[int], k: int) -> float:
    if not relevant:
        return 0.0
    top_k = retrieved[:k]
    hits = sum(1 for doc_id in top_k if doc_id in relevant)
    return hits / len(relevant)


def mean_reciprocal_rank(
    retrieved_per_query: list[list[int]], relevant_per_query: list[set[int]]
) -> float:
    reciprocal_ranks = []
    for retrieved, relevant in zip(retrieved_per_query, relevant_per_query):
        rr = 0.0
        for rank, doc_id in enumerate(retrieved, start=1):
            if doc_id in relevant:
                rr = 1.0 / rank
                break
        reciprocal_ranks.append(rr)

    if not reciprocal_ranks:
        return 0.0
    return sum(reciprocal_ranks) / len(reciprocal_ranks)