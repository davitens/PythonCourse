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

# Hint: write a recursive helper  _parse(data, pos) -> (value, new_pos)  that looks at
# data[pos:pos+1] (b"i", b"l", b"d" or a digit) and dispatches. Note data[pos] is an int!


def encode(value):
    raise NotImplementedError


def decode(data):
    raise NotImplementedError
