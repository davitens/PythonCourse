"""Day 2 - Exercise 2: run-length encoding.

Format: each run of identical characters becomes <count><char>, e.g.
    "aaabccdddd" -> "3a1b2c4d"
Counts can have several digits: "a" * 12 -> "12a".
The input to rle_encode never contains digits.
"""


def rle_encode(s):
    """Encode s with the format above. "" -> ""."""
    out = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append(f"{j - i}{s[i]}")
        i = j
    return "".join(out)


def rle_decode(s):
    """Inverse of rle_encode. Raise ValueError if the input is malformed: a char without
    a preceding count, a count of 0, or a trailing count with no char.

    rle_decode("12a1b") -> "aaaaaaaaaaaab"
    """
    out = []
    num = ""
    for c in s:
        if c.isdigit():
            num += c
        else:
            if not num or int(num) == 0:
                raise ValueError(f"bad count before {c!r}")
            out.append(c * int(num))
            num = ""
    if num:
        raise ValueError("trailing count")
    return "".join(out)
