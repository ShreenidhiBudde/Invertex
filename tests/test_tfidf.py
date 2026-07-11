import json
import math
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_engine.indexing.index import InvertedIndex
from search_engine.ranking.tfidf import (
    inverse_document_frequency,
    search_tfidf,
    term_frequency,
)


def make_toy_corpus(path):
    docs = [
        {"doc_id": 1, "title": "python list", "text": "python list append works"},
        {"doc_id": 2, "title": "python dict", "text": "python dict get method"},
        {"doc_id": 3, "title": "java list", "text": "java list add method"},
        {"doc_id": 4, "title": "empty doc", "text": ""},
    ]
    with open(path, "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")


def build_toy_index():
    with tempfile.TemporaryDirectory() as tmp:
        corpus_path = Path(tmp) / "corpus.jsonl"
        make_toy_corpus(corpus_path)
        return InvertedIndex.build(str(corpus_path))


def test_term_frequency():
    index = build_toy_index()
    # doc 1 tokens: [python, list, python, list, append, work] -> python tf=2
    assert term_frequency("python", 1, index) == 2.0
    assert term_frequency("python", 3, index) == 0.0


def test_idf_higher_for_rarer_terms():
    index = build_toy_index()
    # "java" appears in 1 doc, "list" appears in 2 docs -> java should have higher idf
    idf_java = inverse_document_frequency("java", index)
    idf_list = inverse_document_frequency("list", index)
    assert idf_java > idf_list


def test_idf_zero_for_unknown_term():
    index = build_toy_index()
    assert inverse_document_frequency("nonexistent", index) == 0.0


def test_search_tfidf_ranks_relevant_doc_first():
    index = build_toy_index()
    results = search_tfidf("java list", index, k=5)
    result_doc_ids = [doc_id for doc_id, _ in results]

    # doc 3 (java list) should rank highest for query "java list"
    assert result_doc_ids[0] == 3


def test_search_tfidf_respects_k():
    index = build_toy_index()
    results = search_tfidf("python", index, k=1)
    assert len(results) == 1


def test_search_tfidf_no_match_returns_empty():
    index = build_toy_index()
    results = search_tfidf("nonexistent term", index, k=5)
    assert results == []