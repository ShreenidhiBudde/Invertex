import json
from collections import Counter

CORPUS_PATH = "data/corpus.jsonl"


def main():
    doc_count = 0
    lengths = []
    vocab = set()
    tag_counter = Counter()

    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            doc_count += 1

            tokens = record["text"].lower().split()
            lengths.append(len(tokens))
            vocab.update(tokens)

            for tag in record.get("tags", []):
                tag_counter[tag] += 1

    lengths.sort()
    n = len(lengths)

    print(f"Doc count: {doc_count:,}")
    print(f"Vocab size (whitespace-split, unstemmed): {len(vocab):,}")
    print(f"Doc length (tokens) — min: {lengths[0]}, "
          f"median: {lengths[n // 2]}, max: {lengths[-1]}")
    print(f"Doc length (tokens) — mean: {sum(lengths) / n:.1f}")

    if tag_counter:
        print("\nTop 20 tags:")
        for tag, count in tag_counter.most_common(20):
            print(f"  {tag}: {count:,}")
    else:
        print("\nNo tags present (Tags.csv not yet joined in loader).")


if __name__ == "__main__":
    main()