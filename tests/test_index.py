import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_engine.indexing.index import InvertedIndex


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


def test_doc_count_and_lengths():
    with tempfile.TemporaryDirectory() as tmp:
        corpus_path = Path(tmp) / "corpus.jsonl"
        make_toy_corpus(corpus_path)
        index = InvertedIndex.build(str(corpus_path))

        assert index.doc_count == 4
        # doc 4: title "empty doc" -> tokens ["empti", "doc"], text is empty
        assert index.doc_lengths[4] == 2


def test_term_frequency_and_positions():
    with tempfile.TemporaryDirectory() as tmp:
        corpus_path = Path(tmp) / "corpus.jsonl"
        make_toy_corpus(corpus_path)
        index = InvertedIndex.build(str(corpus_path))

        # "python" appears in doc 1 and doc 2 only
        assert "python" in index.postings
        doc_ids_with_python = {p.doc_id for p in index.postings["python"]}
        assert doc_ids_with_python == {1, 2}

        # doc 1 tokens: [python, list, python, list, append, work]
        doc1_posting = next(p for p in index.postings["python"] if p.doc_id == 1)
        assert doc1_posting.term_frequency == 2
        assert doc1_posting.positions == [0, 2]


def test_list_term_across_docs():
    with tempfile.TemporaryDirectory() as tmp:
        corpus_path = Path(tmp) / "corpus.jsonl"
        make_toy_corpus(corpus_path)
        index = InvertedIndex.build(str(corpus_path))

        # "list" appears in doc 1 and doc 3 only
        doc_ids_with_list = {p.doc_id for p in index.postings["list"]}
        assert doc_ids_with_list == {1, 3}

        # doc 3 tokens: [java, list, java, list, add, method]
        doc3_posting = next(p for p in index.postings["list"] if p.doc_id == 3)
        assert doc3_posting.term_frequency == 2
        assert doc3_posting.positions == [1, 3]


def test_save_and_load_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        corpus_path = Path(tmp) / "corpus.jsonl"
        index_path = Path(tmp) / "index.pkl"
        make_toy_corpus(corpus_path)

        index = InvertedIndex.build(str(corpus_path))
        index.save(str(index_path))

        loaded = InvertedIndex.load(str(index_path))
        assert loaded.doc_count == index.doc_count
        assert loaded.postings.keys() == index.postings.keys()