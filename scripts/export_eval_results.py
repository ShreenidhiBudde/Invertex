import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_eval_set import EVAL_SET
from run_evaluation import bm25_wrapper, evaluate_method, naive_wrapper, tfidf_wrapper
from search_engine.indexing.index import InvertedIndex

INDEX_PATH = "data/index.pkl"
OUTPUT_PATH = "data/eval_results.md"
K = 10


def main():
    print("Loading index...")
    index = InvertedIndex.load(INDEX_PATH)

    usable_queries = [e for e in EVAL_SET if e["relevant"]]

    methods = [
        ("Naive baseline", naive_wrapper),
        ("TF-IDF", tfidf_wrapper),
        ("BM25", bm25_wrapper),
    ]

    results = {}
    for name, fn in methods:
        results[name] = evaluate_method(name, fn, index, EVAL_SET)

    lines = [
        "# Evaluation Results",
        "",
        f"Evaluated on {len(usable_queries)} of {len(EVAL_SET)} labeled queries, k=10.",
        "",
        "| Method | Precision@10 | Recall@10 | MRR | N queries |",
        "|---|---|---|---|---|",
    ]
    for name, metrics in results.items():
        lines.append(
            f"| {name} | {metrics['precision@10']:.3f} | {metrics['recall@10']:.3f} "
            f"| {metrics['mrr']:.3f} | {metrics['n_queries']} |"
        )

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote results to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()