import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_engine.indexing.index import InvertedIndex

CORPUS_PATH = "data/corpus.jsonl"
INDEX_PATH = "data/index.pkl"


def main():
    print("Building index...")
    start = time.time()
    index = InvertedIndex.build(CORPUS_PATH)
    build_time = time.time() - start

    index.save(INDEX_PATH)
    size_mb = os.path.getsize(INDEX_PATH) / (1024 * 1024)

    print(f"Build time: {build_time:.1f}s")
    print(f"Unique terms: {len(index.postings):,}")
    print(f"On-disk index size: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()