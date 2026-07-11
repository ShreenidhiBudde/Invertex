import json
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from search_engine.api.snippet import extract_snippet
from search_engine.indexing.index import InvertedIndex
from search_engine.indexing.tokenizer import tokenize
from search_engine.query.search import search

app = FastAPI(title="Search Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

state = {"index": None, "docs": None}


@app.on_event("startup")
def load_index():
    state["index"] = InvertedIndex.load("data/index.pkl")

    docs = {}
    with open("data/corpus.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            docs[record["doc_id"]] = record
    state["docs"] = docs


@app.get("/search")
def search_endpoint(q: str, k: int = 10):
    start = time.time()

    index = state["index"]
    docs = state["docs"]

    query_terms = tokenize(q)
    results = search(q, index, k=k)

    response_results = []
    for r in results:
        doc = docs.get(r.doc_id, {})
        title = doc.get("title", "<unknown>")
        text = doc.get("text", "")
        snippet = extract_snippet(text, query_terms)

        response_results.append({
            "doc_id": r.doc_id,
            "score": r.score,
            "title": title,
            "snippet": snippet,
        })

    latency_ms = (time.time() - start) * 1000

    return {
        "query": q,
        "results": response_results,
        "latency_ms": round(latency_ms, 2),
    }