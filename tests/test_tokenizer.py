import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_engine.indexing.tokenizer import tokenize


def test_basic_lowercase_and_split():
    assert tokenize("Hello World") == ["hello", "world"]


def test_punctuation_stripped():
    assert tokenize("Hello, World!") == ["hello", "world"]


def test_stopwords_removed():
    tokens = tokenize("this is a test of the tokenizer")
    assert "is" not in tokens
    assert "a" not in tokens
    assert "the" not in tokens
    assert "of" not in tokens


def test_stemming_applied():
    tokens = tokenize("running runs runner")
    assert all(t.startswith("run") for t in tokens)


def test_empty_string():
    assert tokenize("") == []


def test_numbers_preserved():
    tokens = tokenize("python 3.11 released")
    assert "311" in tokens