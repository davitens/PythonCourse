"""Day 3 - Exercise 1: counting."""

PUNCTUATION = ".,!?;:\"'()"


def word_frequencies(text):
    """Return {word: count}. Words are split on whitespace, lowercased, and have the
    characters in PUNCTUATION stripped from both ends; words that become empty are
    dropped. Keys must be in order of first appearance.

    word_frequencies("Hi! hi, there.") -> {"hi": 2, "there": 1}
    """
    raise NotImplementedError


def top_k_words(text, k):
    """Return the k most frequent words (as defined in word_frequencies) as a list of
    (word, count) tuples, sorted by count DESCENDING, ties broken ALPHABETICALLY."""
    raise NotImplementedError


def first_unique_char(s):
    """Index of the first character that appears exactly once in s, or -1."""
    raise NotImplementedError


def most_common_char(s):
    """The most frequent character in s; ties -> the one that appears FIRST in s.
    Empty string -> None."""
    raise NotImplementedError


def common_elements(a, b):
    """Sorted list of distinct elements present in both lists."""
    raise NotImplementedError
