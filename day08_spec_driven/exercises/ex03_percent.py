"""Day 8 - Exercise 3: percent-encoding. Don't use urllib.

UNRESERVED = A-Z a-z 0-9 and the four characters - . _ ~

percent_encode(s, safe="") -> str
    Encode s to UTF-8. Each byte that is an UNRESERVED ASCII char, or an ASCII char
    contained in `safe`, is kept as that char; every other byte becomes "%XX" with
    UPPERCASE hex. Example: percent_encode("a b/é") -> "a%20b%2F%C3%A9",
    percent_encode("a/b", safe="/") -> "a/b"

percent_decode(s) -> str
    Replace each "%XX" (hex digits, any case) by the byte 0xXX, keep other characters
    (encoded as UTF-8), then decode the resulting bytes as UTF-8 (strict).
    "+" is NOT special. Raise ValueError for a "%" not followed by two hex digits, and
    for invalid UTF-8 (UnicodeDecodeError is already a ValueError).
"""

UNRESERVED = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")
HEX = "0123456789abcdefABCDEF"


def percent_encode(s, safe=""):
    raise NotImplementedError


def percent_decode(s):
    raise NotImplementedError
