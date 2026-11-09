"""Day 5 - Exercise 5: FIX ME (reference solution). Fixes marked # FIX (6 bugs)."""


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
        elif b0 >= 0xF0:  # FIX: checks were in ascending order (>= 0xC0 first)
            n, cp, minimum = 4, b0 & 0x07, 0x10000
        elif b0 >= 0xE0:
            n, cp, minimum = 3, b0 & 0x0F, 0x800
        else:
            n, cp, minimum = 2, b0 & 0x1F, 0x80

        if i + n > len(data):  # FIX: was >= (rejected a valid char at the very end)
            raise ValueError(f"truncated sequence at {i}")
        for k in range(1, n):
            b = data[i + k]
            if b & 0xC0 != 0x80:  # FIX: was != 0xC0
                raise ValueError(f"invalid continuation byte at {i + k}")
            cp = (cp << 6) | (b & 0x3F)

        if cp < minimum:  # FIX: 3-byte minimum was 0x80 instead of 0x800
            raise ValueError(f"overlong encoding at {i}")
        if 0xD800 <= cp <= 0xDFFF:  # FIX: was 0xD800 < cp < 0xDFFF
            raise ValueError(f"surrogate at {i}")
        if cp > 0x10FFFF:
            raise ValueError(f"code point out of range at {i}")
        out.append(chr(cp))
        i += n
    return "".join(out)


def count_chars(data):
    """Number of characters in VALID UTF-8 data without decoding it."""
    return sum(1 for b in data if b & 0xC0 != 0x80)  # FIX: was == 0x80 (counted continuations)
