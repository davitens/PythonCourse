"""Day 2 - Exercise 3: text formatting."""


def wrap(text, width):
    """Greedy word-wrap. Split `text` into words (any whitespace), then fill lines
    left-to-right: a word goes on the current line if the line length (words joined
    by single spaces) stays <= width; otherwise it starts a new line.
    A word longer than `width` goes on a line of its own (not broken).
    Returns a list of lines. Empty/blank text -> [].

    wrap("the quick brown fox", 10) -> ["the quick", "brown fox"]
    """
    raise NotImplementedError


def justify_line(words, width):
    """Return a string of exactly `width` chars containing `words` separated by spaces,
    where extra spaces are distributed as evenly as possible between words and the
    LEFTMOST gaps get one more space when it doesn't divide evenly.
    A single word is left-aligned and padded with spaces on the right.
    You may assume the words fit (sum of lengths + gaps <= width).

    justify_line(["a", "bb", "c"], 9) -> "a   bb  c"
    """
    raise NotImplementedError


def justify(text, width):
    """Wrap `text` with wrap(), then fully justify every line except the LAST one,
    which is left-aligned and padded with spaces to `width`.
    (Assume no word is longer than width.)
    """
    raise NotImplementedError
