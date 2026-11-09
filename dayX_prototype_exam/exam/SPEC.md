# Huffman text compressor and document archive: specification

`huffman.py` compresses text with Huffman coding, stores it in a small binary format, and keeps compressed documents in
an in-memory archive. The implementation is broken. Make it match this spec.

Where this spec is ambiguous, the tests in `test_huffman.py` are the final word.

All text is handled as its **UTF-8 bytes**. A "symbol" is one byte value, an integer from 0 to 255.

## 1. The tree

**`byte_frequencies(text)`** returns a dict `{byte value: number of occurrences}` counted over the UTF-8 encoding of
`text`. `byte_frequencies("é")` is `{0xC3: 1, 0xA9: 1}`. Empty text gives `{}`.

**`Node(weight, symbol=None, left=None, right=None)`** is a tree node with those attributes, plus `low`:
- A **leaf** has a `symbol`, and `low` equals that symbol. Symbol `0` is a valid symbol.
- An **internal node** has `left` and `right`, no symbol, and `low` is the smaller of its children's `low`.
- `is_leaf()` returns `True` for a leaf and `False` for an internal node.

**`build_tree(freqs)`** returns the root of the Huffman tree. Empty `freqs` raises `ValueError`. Otherwise:
1. Make one leaf per symbol, whose weight is its frequency.
2. While more than one node remains, order the nodes by **weight, then by `low`**, both ascending. Remove the first two,
   `a` and then `b`, and add a new internal node with weight `a.weight + b.weight`, `left=a`, `right=b`.
3. The last remaining node is the root.

**`code_lengths(root)`** returns `{symbol: depth}`, where depth is the number of edges from the root to the symbol's leaf.
If the root is itself a leaf (the text has only one distinct byte), the result is `{symbol: 1}`.

**`canonical_codes(lengths)`** returns `{symbol: code}`, where a code is a string of `"0"` and `"1"` characters:
1. Order the symbols by **length, then by symbol value**, both ascending.
2. The first symbol's code is all zeros, of its length.
3. Each following code is the previous code plus 1 (as a binary number), then shifted left until it has the symbol's length.

Codes keep their leading zeros: `{97: 2, 98: 2}` gives `{97: "00", 98: "01"}`. `{}` gives `{}`.

Example, for `"abracadabra"`:

| Symbol | Frequency | Length | Code |
|---|---|---|---|
| `a` (97) | 5 | 1 | `0` |
| `r` (114) | 2 | 2 | `10` |
| `b` (98) | 2 | 3 | `110` |
| `c` (99) | 1 | 4 | `1110` |
| `d` (100) | 1 | 4 | `1111` |

## 2. Bits

**`BitWriter`** collects bits and packs them into bytes, **most significant bit first**.
- `write_bit(bit)` adds one bit (0 or 1).
- `write_code(code)` adds each bit of a string such as `"101"`, left to right.
- `getvalue()` returns the bytes written so far. An incomplete last byte is padded **on the right** with zero bits, so
  writing `"101"` gives `b"\xa0"` (`1010 0000`). Writing nothing gives `b""`.

**`BitReader(data)`** reads those bits back, in the same order.
- `read_bit()` returns the next bit. When no bits are left, it raises `ValueError`.
- `bytes_used()` returns the number of bytes touched so far: 0 before any read, 1 after reading 1 to 8 bits, 2 after 9 bits.

## 3. The compressed format

**`compress(text)`** returns bytes laid out like this. All integers are big-endian.

| Field | Size | Contents |
|---|---|---|
| magic | 4 bytes | `b"HUF1"` |
| count | 2 bytes | number of distinct symbols |
| table | 2 × count bytes | for each symbol, ascending by symbol value: 1 byte symbol, 1 byte code length |
| size | 4 bytes | number of bytes in the UTF-8 encoding of the text |
| payload | the rest | the canonical code of every byte of the text, packed with `BitWriter` |

`compress("")` is the magic, count 0, size 0, and no payload.

**`decompress(data)`** is the exact inverse, and returns the original `str`. It raises `ValueError` when:
- the magic is wrong;
- the data ends before the header is complete (the header is everything before the payload);
- a table entry has code length 0, or a symbol is listed twice;
- the payload ends before `size` bytes have been decoded;
- there are bytes left over after the last byte needed for decoding;
- the decoded bytes aren't valid UTF-8. (`UnicodeDecodeError` is a `ValueError`, so this needs no extra code.)

## 4. Text helpers

**`utf8_chars(data)`** splits bytes into a list of `bytes` objects, one per UTF-8 character. The lead byte gives the width:

| Lead byte | Width |
|---|---|
| `0xxxxxxx` | 1 |
| `110xxxxx` | 2 |
| `1110xxxx` | 3 |
| `11110xxx` | 4 |

It raises `ValueError` for any other lead byte, for a character cut off by the end of the data, and for a following byte
that isn't `10xxxxxx`. It doesn't need to reject overlong forms or surrogates.

**`truncate_utf8(text, max_bytes)`** returns the longest prefix of `text` whose UTF-8 encoding fits in at most `max_bytes`
bytes, without ever splitting a character. `truncate_utf8("héllo", 2)` is `"h"`, and `truncate_utf8("héllo", 3)` is `"hé"`.

**`format_table(text)`** returns a human-readable code table. There's one line per symbol, ordered by **count descending,
then symbol ascending**, joined with `"\n"` and with no trailing newline. Each line is `<label> <count> <code>`, where the
label is the character itself for symbols 33 to 126, and otherwise `0x` followed by exactly two **uppercase** hex digits.
Empty text gives `""`.

```text
>>> print(format_table("aab c"))
a 2 0
0x20 1 110
b 1 111
c 1 10
```

## 5. The archive

**`Archive()`** stores named documents in compressed form. Each archive is independent of every other.

| Method | Behaviour |
|---|---|
| `add(name, text)` | Stores `text`, replacing any document with that name. An empty name raises `ValueError`. |
| `get(name)` | Returns the original text. An unknown name raises `KeyError`. |
| `remove(name)` | Removes the document. An unknown name raises `KeyError`. |
| `names()` | Returns all names as a sorted list. |
| `stats()` | Returns a dict, described below. |
| `len(a)` | The number of documents. |
| `name in a` | Whether a document with that name exists. |
| `for name in a` | Visits the names in sorted order. |

`stats()` returns `{"documents": n, "original_bytes": x, "stored_bytes": y}`, where `x` is the total size of the current
documents' texts in **UTF-8 bytes** and `y` is the total length of their compressed forms.
