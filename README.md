# From-Scratch Full-Text Search Engine

A search engine built from scratch in Python — hand-written inverted index, TF-IDF, and BM25 ranking (no Elasticsearch/Whoosh/Lucene), with boolean, phrase, and fuzzy query support, served via FastAPI and a React frontend.

## Architecture

```mermaid
graph LR
    A[Corpus<br/>Stack Overflow Q&A] --> B[Tokenizer<br/>lowercase, stopwords, stemming]
    B --> C[Inverted Index]
    C --> P[(index.pkl<br/>on-disk)]
    P --> D[BM25 Ranking]
    D --> E[Query Layer<br/>boolean / phrase / fuzzy]
    E --> F[FastAPI Backend<br/>/search endpoint]
    F --> G[React Frontend]

    P --> N[Naive Baseline]
    P --> T[TF-IDF Baseline]
    N --> V[Evaluation<br/>precision@k / recall@k / MRR]
    T --> V
    D --> V
```

## Corpus

300,000 questions sampled from the Stack Overflow StackSample dataset (Kaggle), out of 1,264,216 total. HTML and code blocks stripped from indexed text; titles + prose body indexed.

## Running Locally

### Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords')"
```

### Build the index (one-time)

```powershell
python scripts\download_data.py
python scripts\build_corpus.py
python scripts\build_index.py
```

### Run the backend

```powershell
uvicorn search_engine.api.main:app --reload --port 8000
```

### Run the frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Query Features

- **Ranked search (default):** BM25, `k1=1.5`, `b=0.75`
- **Boolean:** `term1 AND term2`, `term1 OR term2`
- **Phrase:** `"exact phrase match"`
- **Fuzzy:** automatic fallback when no query term matches the vocabulary (edit-distance correction against the stemmed vocabulary, ranked by document frequency)

## Evaluation Results

Naive keyword-match baseline vs. hand-written TF-IDF vs. hand-written BM25, evaluated on 24 manually labeled queries, k=10:

| Method | Precision@10 | Recall@10 | MRR |
|---|---|---|---|
| Naive baseline | 0.302 | 0.276 | 0.345 |
| TF-IDF | 0.062 | 0.084 | 0.153 |
| BM25 | 0.737 | 1.000 | 0.951 |

BM25 outperforms the naive baseline by ~2.4x on precision@10 and TF-IDF by ~12x. Full results in `data/eval_results.md`.

## Design Decisions

See `DESIGN_DECISIONS.md` for the full log of engineering decisions, tradeoffs, and bugs fixed during development (phase by phase).

## Tech Stack

Python 3.11+, FastAPI, React (Vite), NLTK (stopwords/stemming primitives only — no search/ranking libraries), pickle (index serialization).