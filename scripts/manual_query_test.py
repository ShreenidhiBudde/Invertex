import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_engine.indexing.index import InvertedIndex
from search_engine.query.search import search

INDEX_PATH = "data/index.pkl"
CORPUS_PATH = "data/corpus.jsonl"

QUERIES = [
    ("boolean", "python AND list"),
    ("phrase", '"null pointer exception"'),
    ("fuzzy", "exceptoin"),
    ("bm25 (default)", "javascript async await"),
]


def load_titles(corpus_path):
    titles = {}
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            titles[record["doc_id"]] = record["title"]
    return titles


def main():
    print("Loading index...")
    index = InvertedIndex.load(INDEX_PATH)
    print("Loading titles...")
    titles = load_titles(CORPUS_PATH)

    for label, query in QUERIES:
        print("=" * 80)
        print(f"[{label}] Query: {query}")
        start = time.time()
        results = search(query, index, k=5)
        elapsed = (time.time() - start) * 1000

        for r in results:
            title = titles.get(r.doc_id, "<unknown>")
            score_str = f"{r.score:.3f}" if r.score is not None else "N/A"
            print(f"  doc_id={r.doc_id}  score={score_str}  title={title}")
        print(f"  ({elapsed:.1f} ms)")


if __name__ == "__main__":
    main()