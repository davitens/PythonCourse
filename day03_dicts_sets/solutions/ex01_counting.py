"""Day 3 - Exercise 1: counting."""

PUNCTUATION = ".,!?;:\"'()"


def word_frequencies(text):
    """Return {word: count}. Words are split on whitespace, lowercased, and have the
    characters in PUNCTUATION stripped from both ends; words that become empty are
    dropped. Keys must be in order of first appearance.

    word_frequencies("Hi! hi, there.") -> {"hi": 2, "there": 1}
    """
    freq = {}
    for raw in text.split():
        w = raw.strip(PUNCTUATION).lower()
        if w:
            freq[w] = freq.get(w, 0) + 1
    return freq


def top_k_words(text, k):
    """Return the k most frequent words (as defined in word_frequencies) as a list of
    (word, count) tuples, sorted by count DESCENDING, ties broken ALPHABETICALLY."""
    freq = word_frequencies(text)
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:k]


def first_unique_char(s):
    """Index of the first character that appears exactly once in s, or -1."""
    counts = {}
    for c in s:
        counts[c] = counts.get(c, 0) + 1
    for i, c in enumerate(s):
        if counts[c] == 1:
            return i
    return -1


def most_common_char(s):
    """The most frequent character in s; ties -> the one that appears FIRST in s.
    Empty string -> None."""
    if not s:
        return None
    counts = {}
    for c in s:
        counts[c] = counts.get(c, 0) + 1
    return max(counts, key=counts.get)  # dict keeps first-seen order; max keeps first on ties


def common_elements(a, b):
    """Sorted list of distinct elements present in both lists."""
    return sorted(set(a) & set(b))
