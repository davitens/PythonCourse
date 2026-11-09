"""Day 8 - Exercise 4: bencode.

encode(value) -> bytes
    int  -> b"i<decimal>e"                       (bool is NOT allowed: TypeError)
    str  -> UTF-8 encode it, then as bytes
    bytes-> b"<len>:<raw>"   (len = number of BYTES)
    list -> b"l" + items + b"e"
    dict -> b"d" + (key, value)... + b"e"; keys must be str or bytes (else TypeError);
            keys are encoded as byte strings and SORTED BY THEIR RAW BYTES.
    anything else -> TypeError

decode(data) -> value
    Byte strings are returned as str if they are valid UTF-8, otherwise as bytes.
    Dict keys are returned the same way. The whole input must be exactly one value.
    Raise ValueError for: unexpected end of data, unknown type byte, bad integer
    (empty, "-0", leading zeros like "03", non-digits), bad string length (leading
    zeros, non-digits, missing ':'), unsorted or duplicate dict keys, trailing data.
"""


def encode(value):
    if isinstance(value, bool):
        raise TypeError("bool not supported")
    if isinstance(value, int):
        return b"i" + str(value).encode() + b"e"
    if isinstance(value, str):
        value = value.encode("utf-8")
    if isinstance(value, bytes):
        return str(len(value)).encode() + b":" + value
    if isinstance(value, list):
        return b"l" + b"".join(encode(v) for v in value) + b"e"
    if isinstance(value, dict):
        items = []
        for k, v in value.items():
            if isinstance(k, str):
                k = k.encode("utf-8")
            elif not isinstance(k, bytes):
                raise TypeError("dict keys must be str or bytes")
            items.append((k, v))
        items.sort(key=lambda kv: kv[0])
        return b"d" + b"".join(encode(k) + encode(v) for k, v in items) + b"e"
    raise TypeError(f"cannot encode {type(value).__name__}")


def _as_text(raw):
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw


def _parse_int_text(text):
    if text.startswith("-"):
        digits = text[1:]
        if digits == "0":
            raise ValueError("negative zero")
    else:
        digits = text
    if not digits.isdigit() or not digits.isascii():
        raise ValueError(f"bad integer {text!r}")
    if len(digits) > 1 and digits[0] == "0":
        raise ValueError("leading zero")
    return int(text)


def _parse(data, pos):
    if pos >= len(data):
        raise ValueError("unexpected end")
    c = data[pos:pos + 1]
    if c == b"i":
        end = data.find(b"e", pos)
        if end < 0:
            raise ValueError("unterminated integer")
        return _parse_int_text(data[pos + 1:end].decode("ascii", "replace")), end + 1
    if c == b"l":
        pos += 1
        items = []
        while True:
            if pos >= len(data):
                raise ValueError("unterminated list")
            if data[pos:pos + 1] == b"e":
                return items, pos + 1
            v, pos = _parse(data, pos)
            items.append(v)
    if c == b"d":
        pos += 1
        out = {}
        prev = None
        while True:
            if pos >= len(data):
                raise ValueError("unterminated dict")
            if data[pos:pos + 1] == b"e":
                return out, pos + 1
            if not data[pos:pos + 1].isdigit():
                raise ValueError("dict key must be a string")
            raw, pos = _parse_bytes(data, pos)
            if prev is not None and raw <= prev:
                raise ValueError("keys unsorted or duplicated")
            prev = raw
            v, pos = _parse(data, pos)
            out[_as_text(raw)] = v
    if c.isdigit():
        raw, pos = _parse_bytes(data, pos)
        return _as_text(raw), pos
    raise ValueError(f"unknown type byte {c!r}")


def _parse_bytes(data, pos):
    colon = data.find(b":", pos)
    if colon < 0:
        raise ValueError("missing ':'")
    text = data[pos:colon].decode("ascii", "replace")
    if not text.isdigit() or (len(text) > 1 and text[0] == "0"):
        raise ValueError(f"bad length {text!r}")
    n = int(text)
    start = colon + 1
    if start + n > len(data):
        raise ValueError("string runs past end")
    return data[start:start + n], start + n


def decode(data):
    value, pos = _parse(data, 0)
    if pos != len(data):
        raise ValueError("trailing data")
    return value
