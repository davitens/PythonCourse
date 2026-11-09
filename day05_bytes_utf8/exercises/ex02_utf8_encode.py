"""Day 5 - Exercise 2: UTF-8 encoder. Do NOT use str.encode / bytes.decode / codecs."""


def utf8_length(cp):
    """Number of bytes needed to encode code point cp (1..4).
    Raise ValueError for cp < 0 or cp > 0x10FFFF."""
    raise NotImplementedError


def encode_code_point(cp):
    """Return the UTF-8 bytes for code point cp.
    Raise ValueError for surrogates (0xD800..0xDFFF), negatives and cp > 0x10FFFF."""
    raise NotImplementedError


def utf8_encode(s):
    """Encode the string s to UTF-8 bytes (use ord() and encode_code_point)."""
    raise NotImplementedError
