from search_engine.indexing.index import InvertedIndex


def levenshtein_distance(a: str, b: str) -> int:
    """Hand-written edit distance via DP (insertions, deletions, substitutions)."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # deletion
                    dp[i][j - 1],      # insertion
                    dp[i - 1][j - 1],  # substitution
                )

    return dp[m][n]


def find_closest_terms(term: str, index: InvertedIndex, max_distance: int = 2, limit: int = 5) -> list[str]:
    """
    For a term with no exact vocabulary match, find vocabulary terms within
    max_distance edit distance, ranked by document frequency (prefer common,
    likely-correct terms over rare one-off typos), with edit distance as tiebreak.
    """
    candidates = []
    for vocab_term in index.postings.keys():
        distance = levenshtein_distance(term, vocab_term)
        if distance <= max_distance:
            doc_frequency = len(index.postings[vocab_term])
            candidates.append((vocab_term, distance, doc_frequency))

    candidates.sort(key=lambda x: (-x[2], x[1]))
    return [term for term, _, _ in candidates[:limit]]