import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_engine.indexing.index import InvertedIndex
from search_engine.ranking.bm25 import bm25_score, search_bm25


def make_toy_corpus(path):
    docs = [
        {"doc_id": 1, "title": "python list", "text": "python list append works"},
        {"doc_id": 2, "title": "python dict", "text": "python dict get method"},
        {"doc_id": 3, "title": "java list", "text": "java list add method"},
        {
            "doc_id": 4,
            "title": "python everywhere",
            "text": "python python python python python python python python python python "
                    "list list list list list list",
        },
    ]
    with open(path, "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")


def build_toy_index():
    with tempfile.TemporaryDirectory() as tmp:
        corpus_path = Path(tmp) / "corpus.jsonl"
        make_toy_corpus(corpus_path)
        return InvertedIndex.build(str(corpus_path))


def test_bm25_score_zero_for_absent_term():
    index = build_toy_index()
    assert bm25_score("java", 1, index) == 0.0


def test_bm25_score_positive_for_present_term():
    index = build_toy_index()
    score = bm25_score("python", 1, index)
    assert score > 0.0


def test_search_bm25_ranks_relevant_doc_first():
    index = build_toy_index()
    results = search_bm25("java list", index, k=5)
    result_doc_ids = [doc_id for doc_id, _ in results]
    assert result_doc_ids[0] == 3


def test_bm25_length_normalization_dampens_long_doc():
    # doc 4 repeats "python" 10x in a much longer doc than doc 1 (2x).
    # Raw TF-IDF would let doc 4's score scale ~linearly with tf.
    # BM25's saturation + length normalization should prevent doc 4 from
    # dominating doc 1 by anywhere near a 5x margin.
    index = build_toy_index()
    score_doc1 = bm25_score("python", 1, index)
    score_doc4 = bm25_score("python", 4, index)

    assert score_doc4 > score_doc1  # more occurrences still scores higher
    assert score_doc4 < score_doc1 * 3  # but saturation prevents linear scaling


def test_search_bm25_respects_k():
    index = build_toy_index()
    results = search_bm25("python", index, k=1)
    assert len(results) == 1


def test_search_bm25_no_match_returns_empty():
    index = build_toy_index()
    results = search_bm25("nonexistent term", index, k=5)
    assert results == []