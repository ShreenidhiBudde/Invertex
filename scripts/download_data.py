import pandas as pd

TARGET_SIZE = 300_000
RANDOM_STATE = 42

QUESTIONS_PATH = "data/raw/Questions.csv"
OUTPUT_PATH = "data/raw/Questions_sample.csv"
ENCODING = "ISO-8859-1"


def main():
    print(f"Reading {QUESTIONS_PATH} ...")
    questions = pd.read_csv(
        QUESTIONS_PATH,
        encoding=ENCODING,
        usecols=["Id", "Title", "Body", "Score"],
    )
    print(f"Full dataset: {len(questions):,} questions")

    sample = questions.sample(n=TARGET_SIZE, random_state=RANDOM_STATE)
    sample.to_csv(OUTPUT_PATH, index=False, encoding=ENCODING)

    print(f"Wrote {len(sample):,} questions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()