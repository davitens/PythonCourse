"""Day 8 - Exercise 2: varints (unsigned LEB128) and zigzag.

encode_uvarint(n) -> bytes
    n >= 0 (else ValueError). Emit 7 bits at a time, LEAST significant group first.
    Every byte except the last has the high bit (0x80) set. 0 -> b"\\x00".
    300 -> b"\\xac\\x02"

decode_uvarint(data, pos=0) -> (value, new_pos)
    Read one varint starting at data[pos]. Raise ValueError if the data ends before a
    byte without the high bit is found, or if the varint is longer than 10 bytes.

zigzag_encode(n) -> int:  0->0, -1->1, 1->2, -2->3, 2->4 ...
zigzag_decode(z) -> int:  inverse

encode_svarint(n) = encode_uvarint(zigzag_encode(n))
decode_svarint(data, pos=0) -> (value, new_pos)

encode_stream(values) -> bytes: uvarint(count) followed by each value as an svarint.
decode_stream(data) -> list: inverse; raise ValueError on truncated data or trailing bytes.
"""


def encode_uvarint(n):
    if n < 0:
        raise ValueError("negative")
    out = bytearray()
    while True:
        byte = n & 0x7F
        n >>= 7
        if n:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def decode_uvarint(data, pos=0):
    result = 0
    shift = 0
    for count in range(10):
        if pos >= len(data):
            raise ValueError("truncated varint")
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            return result, pos
    raise ValueError("varint too long")


def zigzag_encode(n):
    return 2 * n if n >= 0 else -2 * n - 1


def zigzag_decode(z):
    return z // 2 if z % 2 == 0 else -(z + 1) // 2


def encode_svarint(n):
    return encode_uvarint(zigzag_encode(n))


def decode_svarint(data, pos=0):
    z, pos = decode_uvarint(data, pos)
    return zigzag_decode(z), pos


def encode_stream(values):
    return encode_uvarint(len(values)) + b"".join(encode_svarint(v) for v in values)


def decode_stream(data):
    count, pos = decode_uvarint(data, 0)
    out = []
    for _ in range(count):
        v, pos = decode_svarint(data, pos)
        out.append(v)
    if pos != len(data):
        raise ValueError("trailing bytes")
    return out
