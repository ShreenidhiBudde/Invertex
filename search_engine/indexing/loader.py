import re
from typing import Iterator

import pandas as pd
from bs4 import BeautifulSoup

ENCODING = "ISO-8859-1"


def strip_code_and_html(body_html: str) -> str:
    """Remove <code> blocks entirely, then strip remaining HTML tags."""
    soup = BeautifulSoup(body_html, "html.parser")
    for code_tag in soup.find_all("code"):
        code_tag.decompose()
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_corpus(raw_path: str) -> Iterator[dict]:
    """
    Load questions from a StackSample-format CSV and yield normalized records.

    Yields dicts with:
        doc_id: int
        title: str
        text: str          (HTML/code stripped)
        tags: list[str]     (empty for now, added later if Tags.csv is joined)
        score: int
        has_accepted_answer: bool  (always False — not available in this dataset)
    """
    df = pd.read_csv(
        raw_path,
        encoding=ENCODING,
        usecols=["Id", "Title", "Body", "Score"],
    )

    for _, row in df.iterrows():
        yield {
            "doc_id": int(row["Id"]),
            "title": str(row["Title"]),
            "text": strip_code_and_html(str(row["Body"])),
            "tags": [],
            "score": int(row["Score"]),
            "has_accepted_answer": False,
        }