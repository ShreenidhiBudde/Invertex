import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

_STOPWORDS = set(stopwords.words("english"))
_STEMMER = PorterStemmer()

_PUNCT_TABLE = str.maketrans("", "", string.punctuation)


def tokenize(text: str) -> list[str]:
    """
    Lowercase, strip punctuation, split on whitespace,
    remove stopwords, apply Porter stemming.
    """
    text = text.lower()
    text = text.translate(_PUNCT_TABLE)
    raw_tokens = text.split()

    tokens = []
    for tok in raw_tokens:
        if tok in _STOPWORDS:
            continue
        tokens.append(_STEMMER.stem(tok))

    return tokens