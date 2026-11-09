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
    keep = UNRESERVED | set(safe)
    out = []
    for b in s.encode("utf-8"):
        c = chr(b)
        if b < 0x80 and c in keep:
            out.append(c)
        else:
            out.append(f"%{b:02X}")
    return "".join(out)


def percent_decode(s):
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == "%":
            h = s[i + 1:i + 3]
            if len(h) != 2 or h[0] not in HEX or h[1] not in HEX:
                raise ValueError(f"bad escape at {i}")
            out.append(int(h, 16))
            i += 3
        else:
            out += c.encode("utf-8")
            i += 1
    return out.decode("utf-8")
