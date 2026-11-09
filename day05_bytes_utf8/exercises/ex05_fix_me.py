"""Day 5 - Exercise 5: FIX ME - a UTF-8 decoder with 6 planted bugs.

Target time: 20 minutes. Run: python run.py 5 -k ex05
Tip: start with the simplest failing test (one character), compute the expected bytes
by hand from the README table, and print cp in binary inside the loop.
"""


def decode(data):
    """Strictly decode UTF-8. Any invalid input raises ValueError:
    invalid start byte, missing/invalid continuation byte, truncated sequence,
    overlong encoding, surrogate (U+D800..U+DFFF), or > U+10FFFF."""
    out = []
    i = 0
    while i < len(data):
        b0 = data[i]
        if b0 < 0x80:
            n, cp, minimum = 1, b0, 0
        elif b0 < 0xC0:
            raise ValueError(f"unexpected continuation byte at {i}")
        elif b0 >= 0xF8:
            raise ValueError(f"invalid start byte at {i}")
        elif b0 >= 0xC0:
            n, cp, minimum = 2, b0 & 0x1F, 0x80
        elif b0 >= 0xE0:
            n, cp, minimum = 3, b0 & 0x0F, 0x80
        else:
            n, cp, minimum = 4, b0 & 0x07, 0x10000

        if i + n >= len(data):
            raise ValueError(f"truncated sequence at {i}")
        for k in range(1, n):
            b = data[i + k]
            if b & 0xC0 != 0xC0:
                raise ValueError(f"invalid continuation byte at {i + k}")
            cp = (cp << 6) | (b & 0x3F)

        if cp < minimum:
            raise ValueError(f"overlong encoding at {i}")
        if 0xD800 < cp < 0xDFFF:
            raise ValueError(f"surrogate at {i}")
        if cp > 0x10FFFF:
            raise ValueError(f"code point out of range at {i}")
        out.append(chr(cp))
        i += n
    return "".join(out)


def count_chars(data):
    """Number of characters in VALID UTF-8 data without decoding it."""
    return sum(1 for b in data if b & 0xC0 == 0x80)
