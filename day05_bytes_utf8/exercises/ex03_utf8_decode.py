"""Day 5 - Exercise 3: UTF-8 decoder. Do NOT use bytes.decode / codecs."""


class UTF8DecodeError(ValueError):
    """Raised by utf8_decode. `position` is the index of the FIRST byte of the
    offending sequence (the lead byte), and `reason` is one of:
    "invalid start byte", "invalid continuation byte", "truncated sequence",
    "overlong encoding", "surrogate", "out of range"."""

    def __init__(self, reason, position):
        super().__init__(f"{reason} at position {position}")
        self.reason = reason
        self.position = position


def utf8_decode(data):
    """Strictly decode UTF-8 bytes into a str.

    Check, in this order, for each sequence starting at position i:
      1. lead byte: 0xxxxxxx (1 byte), 110xxxxx (2), 1110xxxx (3), 11110xxx (4);
         anything else -> "invalid start byte"
      2. if fewer bytes remain than the sequence needs -> "truncated sequence"
      3. every following byte must be 10xxxxxx -> else "invalid continuation byte"
      4. code point too small for its length -> "overlong encoding"
      5. 0xD800..0xDFFF -> "surrogate"
      6. > 0x10FFFF -> "out of range"
    """
    raise NotImplementedError


def decode_replace(data):
    """BONUS (hard). Decode like data.decode("utf-8", errors="replace"), i.e. replace
    each "maximal subpart of an ill-formed subsequence" by U+FFFD:

    - Valid second-byte ranges depend on the lead byte (this rules out overlongs,
      surrogates and > U+10FFFF early):
          C2..DF : 80..BF            E0 : A0..BF        E1..EC, EE..EF : 80..BF
          ED     : 80..9F            F0 : 90..BF        F1..F3 : 80..BF     F4 : 80..8F
      All further continuation bytes are 80..BF.
    - Bytes 80..C1 and F5..FF as lead bytes -> one U+FFFD each.
    - If a sequence breaks off (bad byte or end of data) after a valid prefix,
      emit ONE U+FFFD for the whole prefix and resume at the byte that broke it.
    """
    raise NotImplementedError
