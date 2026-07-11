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
    {
    "query": "regex match email address",
    "relevant": [
        27989090,
        19513550,
        32751540,
        30804290,
        4508540,
        35908060,
        28866880,
        9764930
    ],
    },
    {
    "query": "python dictionary iteration",
    "relevant": [
        36162490,
        13103510,
        23393230,
        38320480,
        37643520,
        33309660,
        22591270,
        2926580
    ],
},
    {
    "query": "css flexbox center div",
    "relevant": [
        35535710,
        24754000,
        25832340,
        36382360,
        15726740,
        28662580
    ],
},
    {
    "query": "java arraylist vs linkedlist",
    "relevant": [
        29584600,
        22937880,
        23108120,
        35814450,
        1561860,
        17255880
    ],
},
    {
    "query": "python virtual environment setup",
    "relevant": [
        38148620,
        33545330,
        35833260,
        10062320,
        40087910,
        33515920,
        37108370,
        28463510,
        38933360
    ],
},
    {
    "query": "sql delete duplicate rows",
    "relevant": [
        32961870,
        20937170,
        12963480,
        23122890,
        23252020,
        12756800,
        29694310
    ],
},
    {
    "query": "node.js file system read",
    "relevant": [
        31938790,
        11986350,
        10459770,
        38133130,
        22295290
    ],
},
    {
    "query": "git rebase vs merge",
    "relevant": [
        18685420,
        32589970,
        33397600,
        34678950,
        33651970,
        13051200,
        25079370,
        10851720,
        24412980,
        16129380
    ],
},
    {
    "query": "python exception handling",
    "relevant": [
        7549120,
        16244200,
        34951110,
        12330590,
        18544510,
        3880750,
        11451520,
        31106890,
        19968780
    ],
},
    {
    "query": "javascript promise chaining",
    "relevant": [
        36420800,
        29268790,
        23788410,
        38018030,
        35630340,
        35182600,
        39092030,
        31112050,
        32326470,
        37771100
    ],
},
    {
    "query": "mysql index performance",
    "relevant": [
        23695410,
        3274630,
        7260920,
        3605530,
        3146930,
        14419090,
        13097070,
        15719710,
        28490650,
        7560820
    ],
},
    {
    "query": "python string formatting",
    "relevant": [
        19732110,
        8325840,
        8152820,
        29044940
    ],
},
    {
    "query": "java multithreading synchronized",
    "relevant": [
        11526460,
        37100100,
        28460170,
        23131810,
        6309430
    ],
},
    {
    "query": "bash script command line arguments",
    "relevant": [
        36793860,
        28583500,
        19742180,
        25841910
    ],
},
    {
    "query": "python pandas dataframe filter",
    "relevant": [
        17609540,
        36525020,
        35187830,
        34957620,
        20262290,
        31478420
    ],
},
    {
    "query": "git undo last commit",
    "relevant": [
        11149020,
        14627340,
        28617950,
        5189560,
        33388210,
        12672370
    ],
},
    {
    "query": "javascript array sort custom",
    "relevant": [
        2784230,
        12634300,
        37056250,
        10258880,
        21043760,
        12137690,
        30543890,
        3730510
    ],
},
    {
    "query": "sql foreign key constraint",
    "relevant": [
        6506460,
        33461800,
        38558700,
        21889890,
        37266320,
        34244530,
        23579560,
        24575780,
        26081760,
        11185470
    ],
},
    {
    "query": "python unit testing mock",
    "relevant": [
        24767030,
        8821910,
        18023350,
        37110150,
        32684810
    ],
},
    {
    "query": "c++ memory leak pointer",
    "relevant": [
        24566660,
        21471130,
        12549060,
        9422980,
        6231520,
        32653090,
        26400640
    ],
},
]


def main():
    incomplete = [e["query"] for e in EVAL_SET if not e["relevant"]]
    print(f"Total queries: {len(EVAL_SET)}")
    print(f"Queries still needing relevant doc_ids filled in: {len(incomplete)}")
    for q in incomplete:
        print(f"  - {q}")


if __name__ == "__main__":
    main()