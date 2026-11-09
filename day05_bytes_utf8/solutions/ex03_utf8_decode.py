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
    out = []
    i = 0
    n = len(data)
    while i < n:
        b0 = data[i]
        if b0 < 0x80:
            out.append(chr(b0))
            i += 1
            continue
        if b0 & 0xE0 == 0xC0:
            length, cp, minimum = 2, b0 & 0x1F, 0x80
        elif b0 & 0xF0 == 0xE0:
            length, cp, minimum = 3, b0 & 0x0F, 0x800
        elif b0 & 0xF8 == 0xF0:
            length, cp, minimum = 4, b0 & 0x07, 0x10000
        else:
            raise UTF8DecodeError("invalid start byte", i)
        if i + length > n:
            raise UTF8DecodeError("truncated sequence", i)
        for k in range(1, length):
            b = data[i + k]
            if b & 0xC0 != 0x80:
                raise UTF8DecodeError("invalid continuation byte", i)
            cp = (cp << 6) | (b & 0x3F)
        if cp < minimum:
            raise UTF8DecodeError("overlong encoding", i)
        if 0xD800 <= cp <= 0xDFFF:
            raise UTF8DecodeError("surrogate", i)
        if cp > 0x10FFFF:
            raise UTF8DecodeError("out of range", i)
        out.append(chr(cp))
        i += length
    return "".join(out)


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
    out = []
    i, n = 0, len(data)
    while i < n:
        b0 = data[i]
        if b0 < 0x80:
            out.append(chr(b0))
            i += 1
            continue
        if 0xC2 <= b0 <= 0xDF:
            need, lo, hi, cp = 1, 0x80, 0xBF, b0 & 0x1F
        elif b0 == 0xE0:
            need, lo, hi, cp = 2, 0xA0, 0xBF, b0 & 0x0F
        elif 0xE1 <= b0 <= 0xEC or 0xEE <= b0 <= 0xEF:
            need, lo, hi, cp = 2, 0x80, 0xBF, b0 & 0x0F
        elif b0 == 0xED:
            need, lo, hi, cp = 2, 0x80, 0x9F, b0 & 0x0F
        elif b0 == 0xF0:
            need, lo, hi, cp = 3, 0x90, 0xBF, b0 & 0x07
        elif 0xF1 <= b0 <= 0xF3:
            need, lo, hi, cp = 3, 0x80, 0xBF, b0 & 0x07
        elif b0 == 0xF4:
            need, lo, hi, cp = 3, 0x80, 0x8F, b0 & 0x07
        else:
            out.append("�")
            i += 1
            continue
        j = i + 1
        ok = True
        for k in range(need):
            if j >= n:
                ok = False
                break
            b = data[j]
            low, high = (lo, hi) if k == 0 else (0x80, 0xBF)
            if not low <= b <= high:
                ok = False
                break
            cp = (cp << 6) | (b & 0x3F)
            j += 1
        out.append(chr(cp) if ok else "�")
        i = j
    return "".join(out)
