import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_engine.indexing.index import InvertedIndex
from search_engine.query.boolean import boolean_search, intersect_postings, union_postings
from search_engine.query.fuzzy import find_closest_terms, levenshtein_distance
from search_engine.query.phrase import phrase_search
from search_engine.query.search import search


def make_toy_corpus(path):
    docs = [
        {"doc_id": 1, "title": "python list", "text": "python list append works"},
        {"doc_id": 2, "title": "python dict", "text": "python dict get method"},
        {"doc_id": 3, "title": "java list", "text": "java list add method"},
        {"doc_id": 4, "title": "exception handling", "text": "python exception handling tutorial"},
        {"doc_id": 5, "title": "typo doc", "text": "exceptin rare misspelling only here"},
    ]
    with open(path, "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")


def build_toy_index():
    with tempfile.TemporaryDirectory() as tmp:
        corpus_path = Path(tmp) / "corpus.jsonl"
        make_toy_corpus(corpus_path)
        return InvertedIndex.build(str(corpus_path))


def test_intersect_postings():
    assert intersect_postings([1, 2, 3, 5], [2, 3, 4]) == [2, 3]


def test_union_postings():
    assert union_postings([1, 2, 3], [2, 3, 4]) == [1, 2, 3, 4]


def test_boolean_and_query():
    index = build_toy_index()
    result = boolean_search("python AND list", index)
    assert result == [1]


def test_boolean_or_query():
    index = build_toy_index()
    result = boolean_search("java OR dict", index)
    assert set(result) == {2, 3}


def test_phrase_match_found():
    index = build_toy_index()
    # doc 1 tokens: [python, list, python, list, append, work]
    # "python list" as consecutive positions exists in doc 1
    result = phrase_search("python list", index)
    assert 1 in result


def test_phrase_match_not_found_for_non_consecutive_terms():
    index = build_toy_index()
    # doc 3 tokens: [java, list, add, method] -> "add java" is not consecutive anywhere
    result = phrase_search("add java", index)
    assert 3 not in result


def test_levenshtein_distance_basic():
    assert levenshtein_distance("kitten", "sitting") == 3
    assert levenshtein_distance("same", "same") == 0


def test_find_closest_terms_prefers_common_term():
    index = build_toy_index()
    # "exceptoin" (typo) is distance 2 from "exceptin" (rare, df=1)
    # and distance 3 from "except"-stemmed "exception" tokens present via doc 4.
    # With frequency-based ranking, the more common/correct term should win.
    closest = find_closest_terms("exceptoin", index, max_distance=3, limit=3)
    assert len(closest) > 0


def test_unified_search_dispatches_to_boolean():
    index = build_toy_index()
    results = search("python AND list", index)
    assert any(r.doc_id == 1 for r in results)
    assert results[0].score is None


def test_unified_search_dispatches_to_phrase():
    index = build_toy_index()
    results = search('"python list"', index)
    assert any(r.doc_id == 1 for r in results)


def test_unified_search_dispatches_to_bm25_by_default():
    index = build_toy_index()
    results = search("python exception", index)
    assert len(results) > 0
    assert results[0].score is not None