"""
Labeled evaluation query set.

HOW TO FILL THIS IN:
1. Pick a query relevant to this corpus (Stack Overflow Q&A).
2. Run it manually, e.g.:
     python -c "from search_engine.indexing.index import InvertedIndex; from search_engine.ranking.bm25 import search_bm25; idx = InvertedIndex.load('data/index.pkl'); print(search_bm25('your query', idx, k=20))"
3. For each of the top-20 doc_ids returned, open it up (look up its title/text
   in data/corpus.jsonl by doc_id) and judge: is this genuinely relevant to
   the query, or not?
4. Hardcode the doc_ids you judged as relevant into the "relevant" list below.
5. Repeat for 20-30 queries. Aim for a mix of specific/broad, single-word/
   multi-word queries.

Only queries with at least 1 relevant doc_id should be included (queries with
zero relevant results in top-20 aren't useful for precision/recall/MRR).
"""

EVAL_SET = [
    {
        "query": "python list append",
        "relevant": [
            37708370,
            37210060,
            22650590,
            26911770,
            21792590
        ], 
    },
    {
        "query": "java null pointer exception",
        "relevant": [
            27084960,
            25326680,
            22161740,
            14484070,
            14278640,
            2586290,
            8682820,
            21445970,
            28649310,
            10681290
        ],
    },
    {
        "query": "sql join multiple tables",
        "relevant": [
            25507590,
            12389480,
            35163300,
            13795520,
            30407780,
            3156230,
            31744930,
            26118750,
            24447130
        ],
    },
    {
        "query": "javascript async await",
        "relevant": [],
    },
    {
        "query": "git merge conflict",
        "relevant": [
            18162930,
            29395570,
            8133350,
            33651970,
            28107200,
            19232530,
            11738200,
            33219260,
            34683120,
            15823730
        ],
    },
    # Add 15-25 more entries in this same format.
]


def main():
    incomplete = [e["query"] for e in EVAL_SET if not e["relevant"]]
    print(f"Total queries: {len(EVAL_SET)}")
    print(f"Queries still needing relevant doc_ids filled in: {len(incomplete)}")
    for q in incomplete:
        print(f"  - {q}")


if __name__ == "__main__":
    main()