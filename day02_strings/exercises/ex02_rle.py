"""Day 2 - Exercise 2: run-length encoding.

Format: each run of identical characters becomes <count><char>, e.g.
    "aaabccdddd" -> "3a1b2c4d"
Counts can have several digits: "a" * 12 -> "12a".
The input to rle_encode never contains digits.
"""


def rle_encode(s):
    """Encode s with the format above. "" -> ""."""
    raise NotImplementedError


def rle_decode(s):
    """Inverse of rle_encode. Raise ValueError if the input is malformed: a char without
    a preceding count, a count of 0, or a trailing count with no char.

    rle_decode("12a1b") -> "aaaaaaaaaaaab"
    """
    raise NotImplementedError
