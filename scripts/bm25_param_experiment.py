import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_engine.indexing.index import InvertedIndex
from search_engine.ranking.bm25 import search_bm25

INDEX_PATH = "data/index.pkl"
CORPUS_PATH = "data/corpus.jsonl"

QUERIES = [
    "python list append",
    "java null pointer exception",
    "sql join multiple tables",
    "javascript async await",
    "git merge conflict",
]

PARAM_COMBINATIONS = [
    (1.2, 0.75),
    (1.5, 0.75),
    (2.0, 0.5),
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

    for k1, b in PARAM_COMBINATIONS:
        print("#" * 80)
        print(f"k1={k1}, b={b}")
        for query in QUERIES:
            print("=" * 80)
            print(f"Query: {query}")
            results = search_bm25(query, index, k=5, k1=k1, b=b)
            for doc_id, score in results:
                title = titles.get(doc_id, "<unknown>")
                print(f"  doc_id={doc_id}  score={score:.3f}  title={title}")


if __name__ == "__main__":
    main()