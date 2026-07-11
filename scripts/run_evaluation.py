import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_eval_set import EVAL_SET
from search_engine.eval.metrics import mean_reciprocal_rank, precision_at_k, recall_at_k
from search_engine.indexing.index import InvertedIndex
from search_engine.ranking.bm25 import search_bm25
from search_engine.ranking.naive import search_naive
from search_engine.ranking.tfidf import search_tfidf

INDEX_PATH = "data/index.pkl"
K = 10


def evaluate_method(name, retrieve_fn, index, eval_set):
    precisions = []
    recalls = []
    retrieved_per_query = []
    relevant_per_query = []

    for entry in eval_set:
        query = entry["query"]
        relevant = set(entry["relevant"])
        if not relevant:
            continue

        retrieved = retrieve_fn(query, index, K)
        precisions.append(precision_at_k(retrieved, relevant, K))
        recalls.append(recall_at_k(retrieved, relevant, K))
        retrieved_per_query.append(retrieved)
        relevant_per_query.append(relevant)

    if not precisions:
        return {"precision@10": 0.0, "recall@10": 0.0, "mrr": 0.0, "n_queries": 0}

    avg_precision = sum(precisions) / len(precisions)
    avg_recall = sum(recalls) / len(recalls)
    mrr = mean_reciprocal_rank(retrieved_per_query, relevant_per_query)

    return {
        "precision@10": avg_precision,
        "recall@10": avg_recall,
        "mrr": mrr,
        "n_queries": len(precisions),
    }


def naive_wrapper(query, index, k):
    return search_naive(query, index, k)


def tfidf_wrapper(query, index, k):
    return [doc_id for doc_id, _ in search_tfidf(query, index, k)]


def bm25_wrapper(query, index, k):
    return [doc_id for doc_id, _ in search_bm25(query, index, k)]


def main():
    print("Loading index...")
    index = InvertedIndex.load(INDEX_PATH)

    usable_queries = [e for e in EVAL_SET if e["relevant"]]
    print(f"Evaluating on {len(usable_queries)} of {len(EVAL_SET)} queries (with relevant docs filled in)\n")

    methods = [
        ("Naive baseline", naive_wrapper),
        ("TF-IDF", tfidf_wrapper),
        ("BM25", bm25_wrapper),
    ]

    results = {}
    for name, fn in methods:
        results[name] = evaluate_method(name, fn, index, EVAL_SET)

    print(f"{'Method':<20}{'Precision@10':<15}{'Recall@10':<15}{'MRR':<10}{'N':<5}")
    print("-" * 65)
    for name, metrics in results.items():
        print(
            f"{name:<20}{metrics['precision@10']:<15.3f}"
            f"{metrics['recall@10']:<15.3f}{metrics['mrr']:<10.3f}{metrics['n_queries']:<5}"
        )


if __name__ == "__main__":
    main()