import pandas as pd

SAMPLE_SIZE = 3000
QUESTIONS_PATH = "data/raw/Questions.csv"
ANSWERS_PATH = "data/raw/Answers.csv"
ENCODING = "ISO-8859-1"


def load_sample():
    questions = pd.read_csv(
        QUESTIONS_PATH,
        encoding=ENCODING,
        usecols=["Id", "Title", "Body", "Score"],
        nrows=50000,
    )
    sample = questions.sample(n=SAMPLE_SIZE, random_state=42)

    answers = pd.read_csv(
        ANSWERS_PATH,
        encoding=ENCODING,
        usecols=["Id", "ParentId", "Body", "Score"],
        nrows=100000,
    )

    return sample, answers


def print_random_records(sample, answers, n=10):
    rows = sample.sample(n=n, random_state=1)
    for _, row in rows.iterrows():
        print("=" * 80)
        print(f"Id: {row['Id']}")
        print(f"Title: {row['Title']}")
        print(f"Body (first 300 chars): {row['Body'][:300]}")

        matching_answers = answers[answers["ParentId"] == row["Id"]]
        has_answer = len(matching_answers) > 0
        print(f"Has any answer: {has_answer} (count: {len(matching_answers)})")
        if has_answer:
            best = matching_answers.sort_values("Score", ascending=False).iloc[0]
            print(f"Top-scored answer (first 300 chars): {best['Body'][:300]}")
        print(f"Question Score: {row['Score']}")


def check_html_consistency(sample):
    has_html_tags = sample["Body"].str.contains(r"<[a-zA-Z]+>", regex=True, na=False)
    pct = has_html_tags.mean() * 100
    print(f"\n% of questions with HTML tags in body: {pct:.1f}%")


def check_code_block_pattern(sample):
    has_code = sample["Body"].str.contains(r"<code>", regex=True, na=False)
    pct = has_code.mean() * 100
    print(f"% of questions with <code> blocks: {pct:.1f}%")


def report_answer_rate(sample, answers):
    answered_ids = set(answers["ParentId"].unique())
    pct = sample["Id"].isin(answered_ids).mean() * 100
    print(f"% of questions with at least one answer (within sampled Answers.csv rows): {pct:.1f}%")


def main():
    sample, answers = load_sample()
    print(f"Loaded sample of {len(sample)} questions, {len(answers)} answers (subset)\n")

    print_random_records(sample, answers, n=10)
    check_html_consistency(sample)
    check_code_block_pattern(sample)
    report_answer_rate(sample, answers)


if __name__ == "__main__":
    main()