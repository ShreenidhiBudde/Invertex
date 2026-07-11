Status: Phase 0 in progress — environment setup complete.

## Tokenization Design Decisions
- Stemming (Porter) chosen over lemmatization: faster, no POS tagging or
  dictionary lookups needed, deterministic. Slightly cruder normalization,
  acceptable for search recall.
- Stopword list: NLTK's fixed English list (~180 words). Fixed, not
  learned/corpus-specific, so it's consistent and reproducible across runs.

  