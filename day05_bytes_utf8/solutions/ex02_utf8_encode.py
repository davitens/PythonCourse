"""Day 5 - Exercise 2: UTF-8 encoder. Do NOT use str.encode / bytes.decode / codecs."""


def utf8_length(cp):
    """Number of bytes needed to encode code point cp (1..4).
    Raise ValueError for cp < 0 or cp > 0x10FFFF."""
    if cp < 0 or cp > 0x10FFFF:
        raise ValueError("code point out of range")
    if cp < 0x80:
        return 1
    if cp < 0x800:
        return 2
    if cp < 0x10000:
        return 3
    return 4


def encode_code_point(cp):
    """Return the UTF-8 bytes for code point cp.
    Raise ValueError for surrogates (0xD800..0xDFFF), negatives and cp > 0x10FFFF."""
    if 0xD800 <= cp <= 0xDFFF:
        raise ValueError("surrogate")
    n = utf8_length(cp)
    if n == 1:
        return bytes([cp])
    if n == 2:
        return bytes([0xC0 | (cp >> 6), 0x80 | (cp & 0x3F)])
    if n == 3:
        return bytes([0xE0 | (cp >> 12), 0x80 | ((cp >> 6) & 0x3F), 0x80 | (cp & 0x3F)])
    return bytes([0xF0 | (cp >> 18), 0x80 | ((cp >> 12) & 0x3F),
                  0x80 | ((cp >> 6) & 0x3F), 0x80 | (cp & 0x3F)])


def utf8_encode(s):
    """Encode the string s to UTF-8 bytes (use ord() and encode_code_point)."""
    out = bytearray()
    for ch in s:
        out += encode_code_point(ord(ch))
    return bytes(out)
