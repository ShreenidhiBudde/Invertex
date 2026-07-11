import json
import pickle

from search_engine.indexing.tokenizer import tokenize


class Posting:
    __slots__ = ("doc_id", "term_frequency", "positions")

    def __init__(self, doc_id: int, term_frequency: int, positions: list[int]):
        self.doc_id = doc_id
        self.term_frequency = term_frequency
        self.positions = positions

    def __repr__(self):
        return f"Posting(doc_id={self.doc_id}, tf={self.term_frequency}, positions={self.positions})"


class InvertedIndex:
    def __init__(self):
        self.postings: dict[str, list[Posting]] = {}
        self.doc_count: int = 0
        self.avg_doc_length: float = 0.0
        self.doc_lengths: dict[int, int] = {}

    @classmethod
    def build(cls, corpus_path: str) -> "InvertedIndex":
        index = cls()
        term_postings: dict[str, dict[int, Posting]] = {}
        total_length = 0

        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                doc_id = record["doc_id"]
                tokens = tokenize(record["title"] + " " + record["text"])

                doc_length = len(tokens)
                index.doc_lengths[doc_id] = doc_length
                total_length += doc_length
                index.doc_count += 1

                for position, term in enumerate(tokens):
                    if term not in term_postings:
                        term_postings[term] = {}
                    if doc_id not in term_postings[term]:
                        term_postings[term][doc_id] = Posting(doc_id, 0, [])
                    posting = term_postings[term][doc_id]
                    posting.term_frequency += 1
                    posting.positions.append(position)

        for term, doc_map in term_postings.items():
            index.postings[term] = list(doc_map.values())

        index.avg_doc_length = total_length / index.doc_count if index.doc_count else 0.0

        return index

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path: str) -> "InvertedIndex":
        with open(path, "rb") as f:
            return pickle.load(f)