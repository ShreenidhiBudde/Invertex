import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_engine.indexing.index import InvertedIndex
from search_engine.ranking.tfidf import search_tfidf

INDEX_PATH = "data/index.pkl"
CORPUS_PATH = "data/corpus.jsonl"

QUERIES = [
    "python list append",
    "java null pointer exception",
    "sql join multiple tables",
    "javascript async await",
    "git merge conflict",
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

    for query in QUERIES:
        print("=" * 80)
        print(f"Query: {query}")
        start = time.time()
        results = search_tfidf(query, index, k=5)
        elapsed = (time.time() - start) * 1000

        for doc_id, score in results:
            title = titles.get(doc_id, "<unknown>")
            print(f"  doc_id={doc_id}  score={score:.3f}  title={title}")
        print(f"  ({elapsed:.1f} ms)")


if __name__ == "__main__":
    main()