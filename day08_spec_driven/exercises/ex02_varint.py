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
    raise NotImplementedError


def decode_uvarint(data, pos=0):
    raise NotImplementedError


def zigzag_encode(n):
    raise NotImplementedError


def zigzag_decode(z):
    raise NotImplementedError


def encode_svarint(n):
    raise NotImplementedError


def decode_svarint(data, pos=0):
    raise NotImplementedError


def encode_stream(values):
    raise NotImplementedError


def decode_stream(data):
    raise NotImplementedError
