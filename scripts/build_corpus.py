import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_engine.indexing.loader import load_corpus

RAW_PATH = "data/raw/Questions_sample.csv"
OUTPUT_PATH = "data/corpus.jsonl"


def main():
    start = time.time()
    count = 0

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for record in load_corpus(RAW_PATH):
            f.write(json.dumps(record) + "\n")
            count += 1
            if count % 25000 == 0:
                print(f"  processed {count:,} records...")

    elapsed = time.time() - start
    print(f"Done. Wrote {count:,} records to {OUTPUT_PATH} in {elapsed:.1f}s")


if __name__ == "__main__":
    main()