# Design Decisions
Started: 2026-07-10

## Dataset Validation (Phase 0a)
- Source: Kaggle StackSample (stackoverflow/stacksample), Questions.csv + Answers.csv + Tags.csv.
- Sample: 3,000 questions (random, seed=42) validated for structure and quality.
- 100% of question bodies contain HTML markup (as expected from SO's stored format).
- 50.2% of questions contain <code> blocks.
- Dataset version does not include AcceptedAnswerId. Using highest-scored answer
  (via ParentId linkage in Answers.csv) as the ground-truth relevance signal instead
  of "accepted answer."
- Code-block handling for v1: strip code from indexed text (index title + prose body only).
- Question-only vs. question+answer: index questions only for v1; answers deferred.

## Full Corpus Build (Phase 0b)
- Subsampled 300,000 questions (random, seed=42) from full dataset of 1,264,216.
- Full pipeline (HTML/code strip via BeautifulSoup) ran in 171.7s for 300k records.
- Corpus stats (pre-stemming, whitespace tokenization):
  - Vocab size: 765,461
  - Doc length (tokens): min 0, median 74, mean 90.9, max 1857
- Known issue: some docs have 0 tokens after code-stripping (code-only bodies with
  no prose). Decision on drop-vs-keep deferred to Phase 1 tokenization review.
- Tags not yet joined (Tags.csv unused in loader v1) — tags: [] stub in all records.

## Inverted Index (Phase 2)

- In-memory build: single-pass streaming over corpus.jsonl, tokenizing via
  Phase 1 tokenizer, populating term -> list[Posting] with term_frequency
  and positions per doc.
- Serialization: pickle for v1 (stated as intentional starting point in
  project spec; may upgrade to custom binary format later if time allows).
- Build time: 264.0s for 300,000 docs.
- Unique terms: 436,213.
- On-disk index size: 339.8 MB.

## TF-IDF Ranking Baseline (Phase 3)

- Formula: tf(t,d) * idf(t), where idf(t) = log(N / df(t)).
- search_tfidf lives in search_engine/ranking/tfidf.py.
- Scoring aggregation: for each query term, its postings list is scanned once
  and scores accumulated into a doc_id -> score dict, then sorted descending
  and truncated to top-k.
- Performance fix: initial implementation called term_frequency() per
  candidate doc per query term (linear scan of postings each time), causing
  35-64s query latency. Rewrote search_tfidf to iterate each term's postings
  list once and accumulate directly, dropping latency to 3-37ms with
  identical rankings.
- Manual sanity check on 5 queries: results topically reasonable overall,
  with some noise on shorter/ambiguous queries (expected for a
  vector-space/no-normalization baseline; BM25 in Phase 4 should improve this).

## BM25 Ranking (Phase 4)

- Standard BM25 formula: idf(t) * (tf * (k1+1)) / (tf + k1 * (1 - b + b * (doc_len / avg_doc_len))).
- idf uses the smoothed variant: log((N - df + 0.5) / (df + 0.5) + 1), avoids
  negative idf for very common terms.
- Defaults: k1=1.5, b=0.75 (standard literature defaults).
- search_bm25 lives in search_engine/ranking/bm25.py, same postings-iterate-once
  pattern as search_tfidf to avoid the earlier latency bug.
- Parameter experiment: ran k1/b in {(1.2, 0.75), (1.5, 0.75), (2.0, 0.5)} across
  5 manual queries. Ranking order was largely stable across combinations;
  score magnitudes and top-5 ordering shifted slightly (e.g. tf-heavy docs rank
  marginally higher with k1=2.0). No combination broke relevance.
- Qualitative note: BM25 results are noticeably more topically precise than the
  Phase 3 TF-IDF baseline on the same 5 queries — will be quantified properly
  in Phase 7 eval.