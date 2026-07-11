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