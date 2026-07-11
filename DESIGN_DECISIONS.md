# Design Decisions

Started: 2026-07-10

## Phase 0 — Dataset

- Source: Kaggle StackSample (`stackoverflow/stacksample`) — Questions.csv, Answers.csv, Tags.csv.
- Validated on a 3,000-question random sample (seed=42) before full build.
  - 100% of question bodies contain HTML markup.
  - 50.2% contain `<code>` blocks.
- Dataset version does not include `AcceptedAnswerId`. Using highest-scored answer (via `ParentId` linkage in Answers.csv) as the ground-truth relevance signal instead of "accepted answer."
- Code-block handling: strip code from indexed text for v1 — index title + prose body only.
- Question-only vs. question+answer: index questions only for v1; answers deferred.
- Full corpus: subsampled 300,000 questions (seed=42) from 1,264,216 total. Pipeline (HTML/code strip via BeautifulSoup) ran in 171.7s.
- Corpus stats (pre-stemming, whitespace tokenization): vocab size 765,461; doc length (tokens) — min 0, median 74, mean 90.9, max 1857.
- Known issue: some docs have 0 tokens after code-stripping (code-only bodies, no prose). Kept as-is — can still match on title.
- Tags not joined in v1 (`tags: []` stub in all records).

## Phase 1 — Tokenization

- Stemming (Porter) chosen over lemmatization: faster, no POS tagging or dictionary lookups, deterministic. Slightly cruder normalization, acceptable for search recall.
- Stopword list: NLTK's fixed English list (~180 words) — fixed, not corpus-learned, reproducible across runs.

## Phase 2 — Inverted Index

- Single-pass streaming build over `corpus.jsonl`, tokenizing via Phase 1 tokenizer, populating `term -> list[Posting]` with term_frequency and positions per doc.
- Serialization: pickle for v1 (may upgrade to custom binary format later if time allows).
- Build time: 264.0s for 300,000 docs.
- Unique terms: 436,213.
- On-disk index size: 339.8 MB.

## Phase 3 — TF-IDF Ranking Baseline

- Formula: `tf(t,d) * idf(t)`, where `idf(t) = log(N / df(t))`.
- Lives in `search_engine/ranking/tfidf.py`.
- Scoring aggregation: for each query term, its postings list is scanned once and scores accumulated into a `doc_id -> score` dict, then sorted descending and truncated to top-k.
- **Bug fixed:** initial implementation called `term_frequency()` per candidate doc per query term (linear scan of postings each time), causing 35-64s query latency. Rewrote `search_tfidf` to iterate each term's postings list once and accumulate directly — latency dropped to 3-37ms with identical rankings.
- Manual sanity check on 5 queries: results topically reasonable overall, with noise on shorter/ambiguous queries (expected for a vector-space/no-normalization baseline).

## Phase 4 — BM25 Ranking

- Standard formula: `idf(t) * (tf * (k1+1)) / (tf + k1 * (1 - b + b * (doc_len / avg_doc_len)))`.
- Smoothed idf variant: `log((N - df + 0.5) / (df + 0.5) + 1)` — avoids negative idf for very common terms.
- Defaults: `k1=1.5`, `b=0.75` (standard literature defaults).
- `search_bm25` lives in `search_engine/ranking/bm25.py`, uses the same postings-iterate-once pattern as `search_tfidf` from the start (avoiding the Phase 3 latency bug).
- Parameter experiment: ran `k1`/`b` in `{(1.2, 0.75), (1.5, 0.75), (2.0, 0.5)}` across 5 manual queries. Ranking order stable across combinations; score magnitudes shifted slightly. No combination broke relevance.
- Qualitative note: BM25 results noticeably more topically precise than the Phase 3 TF-IDF baseline on the same 5 queries — quantified properly in Phase 7.

## Phase 5 — Query Features (Boolean, Phrase, Fuzzy)

- **Boolean AND/OR:** hand-written sorted-postings merge (`intersect_postings` / `union_postings`), O(len(a)+len(b)) per merge. Query parser is left-to-right, no operator precedence or parentheses (v1 scope).
- **Phrase queries:** use stored term positions from Phase 2; for each candidate doc (intersection of docs containing all phrase terms), checks for a consecutive-position match starting from each occurrence of the first term.
- **Fuzzy matching:** hand-written Levenshtein DP for edit distance. Candidate ranking evolved through debugging:
  - v1 (distance only): picked semantically poor matches when multiple vocab terms tied on distance.
  - v2 (distance + length-diff tiebreak): still failed — since the index vocabulary is stemmed, misspelled query terms often sit closer (by raw edit distance) to other rare misspellings already in the vocab than to the common correct stem.
  - Final: candidates within `max_distance` ranked by document frequency (descending), edit distance as secondary tiebreak. Common/correct terms reliably beat rare one-off typos.
  - `max_distance=3` used in the dispatcher's fuzzy fallback (vs. 2 elsewhere) to account for stemmed-vocab mismatches between typo and correct term.
  - Known limitation: full-vocabulary scan per fuzzy lookup (~436k terms) costs ~9-10s per query. Acceptable for v1; would need a prefix index or BK-tree to be production-viable.
- **Unified dispatcher** (`search_engine/query/search.py`): quoted string → phrase; `" AND "`/`" OR "` present → boolean; all query terms unmatched in vocab → fuzzy fallback (re-runs BM25 on corrected terms); otherwise → BM25.

## Phase 6 — API + Frontend

- FastAPI backend (`search_engine/api/main.py`): index + corpus loaded once at startup into memory (not per-request). CORS enabled for `localhost:5173`.
- `GET /search?q=...&k=...` dispatches to the unified `search()` from Phase 5, returns `doc_id`, `score`, `title`, `snippet`, and `latency_ms` per request.
- Snippet highlighting (`search_engine/api/snippet.py`): re-stems each word of the raw doc text and compares against query terms (since the index vocab is stemmed but doc text is not), wraps matches in `<mark>` tags. Window widened from 8 to 18 words each side after the initial version produced choppy, mid-sentence-cut excerpts.
- React frontend (Vite): single search page, calls `/search` on Enter or button click, renders ranked results with title/score/snippet. UI redesigned from an initial bright-yellow-highlight plain layout to a dark theme with a restrained indigo accent, card-style results, Inter + IBM Plex Mono typefaces.
- Manual end-to-end latency: ~120-150ms for standard BM25/boolean/phrase queries; fuzzy fallback queries remain slow (~9-10s, known Phase 5 limitation) — acceptable for v1 demo purposes.

## Phase 7 — Evaluation

- Naive baseline (`search_engine/ranking/naive.py`): exact boolean AND match across all query terms, no ranking/weighting, arbitrary doc_id order.
- Metrics hand-implemented (`search_engine/eval/metrics.py`): `precision_at_k`, `recall_at_k`, `mean_reciprocal_rank`.
- Eval set (`scripts/build_eval_set.py`): 24 manually judged queries — each run manually, top-20 results inspected by hand, relevant doc_ids hardcoded as ground truth.
- Compared naive baseline vs. TF-IDF vs. BM25 at k=10.

**Results (N = 24 queries):**

| Method | Precision@10 | Recall@10 | MRR |
|---|---|---|---|
| Naive baseline | 0.302 | 0.276 | 0.345 |
| TF-IDF | 0.062 | 0.084 | 0.153 |
| BM25 | 0.737 | 1.000 | 0.951 |

BM25 outperforms the naive baseline by ~2.4x on precision@10 and TF-IDF by ~12x. Full results saved to `data/eval_results.md`.