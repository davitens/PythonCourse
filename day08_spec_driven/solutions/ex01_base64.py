"""Day 8 - Exercise 1: base64 (RFC 4648, standard alphabet). Don't use the base64 module.

b64encode(data: bytes) -> str
    Process 3 bytes (24 bits) at a time -> 4 characters of 6 bits each, most significant
    first, using ALPHABET. A final group of 1 byte -> 2 chars + "==";
    of 2 bytes -> 3 chars + "=". Missing bits are zero.

b64decode(text: str) -> bytes
    Inverse of b64encode. Raise ValueError if:
      - len(text) is not a multiple of 4
      - a character is not in ALPHABET (except '=' padding)
      - '=' appears anywhere other than the last 1 or 2 positions
"""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def b64encode(data):
    out = []
    for i in range(0, len(data), 3):
        group = data[i:i + 3]
        n = int.from_bytes(group.ljust(3, b"\x00"), "big")
        chars = [ALPHABET[(n >> shift) & 0x3F] for shift in (18, 12, 6, 0)]
        keep = len(group) + 1
        out.append("".join(chars[:keep]) + "=" * (4 - keep))
    return "".join(out)


def b64decode(text):
    if len(text) % 4:
        raise ValueError("length must be a multiple of 4")
    pad = len(text) - len(text.rstrip("="))
    if pad > 2:
        raise ValueError("too much padding")
    body = text[:len(text) - pad]
    out = bytearray()
    for i in range(0, len(text), 4):
        chunk = body[i:i + 4]
        n = 0
        for c in chunk:
            idx = ALPHABET.find(c)
            if idx < 0:
                raise ValueError(f"invalid character {c!r}")
            n = (n << 6) | idx
        n <<= 6 * (4 - len(chunk))
        nbytes = len(chunk) - 1 if len(chunk) < 4 else 3
        out += n.to_bytes(3, "big")[:nbytes]
    return bytes(out)
