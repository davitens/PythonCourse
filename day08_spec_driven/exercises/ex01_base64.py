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
    raise NotImplementedError


def b64decode(text):
    raise NotImplementedError
