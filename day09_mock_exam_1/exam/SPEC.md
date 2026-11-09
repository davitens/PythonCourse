# Byte-Level BPE Tokenizer — Specification

`bpe.py` implements a byte-level Byte Pair Encoding tokenizer. **The implementation is broken.**
Your task is to fix it so that it matches this spec. The test suite in `test_bpe.py` is the final word on
requirements where this spec is ambiguous.

## Token ids

- Ids `0..255` are the 256 single-byte tokens: `vocab[i] == bytes([i])`.
- The `k`-th merge learned during training (k = 0, 1, 2, ...) creates the token id `256 + k`.
- `vocab[id]` is the `bytes` that a token stands for. For a merge `(a, b) -> id`,
  `vocab[id] == vocab[a] + vocab[b]`.
- Special tokens (see below) have ids chosen by the user.

## Helper functions

### `get_stats(ids, counts=None) -> dict`
Counts every pair of **consecutive** ids in the list `ids`: `{(ids[i], ids[i+1]): count}`. Overlapping
pairs all count (`[1, 1, 1]` → `{(1, 1): 2}`). If a `counts` dict is passed, it is updated in place and
returned; otherwise a new dict is returned. Keys appear in the order of their first occurrence.

### `merge(ids, pair, idx) -> list`
Returns a new list in which every occurrence of `pair` (scanning **left to right, non-overlapping**) is
replaced by `idx`. Example: `merge([1, 1, 1, 2], (1, 1), 9) == [9, 1, 2]`. Must not modify `ids`.

### `split_text(text) -> list[str]`
Pre-tokenization. Splits `text` into chunks; merges never cross a chunk boundary. The concatenation of the
chunks is always exactly `text`. Scanning left to right, the next chunk is:

1. a single space `' '` **immediately followed by** a letter or digit attaches to the run that follows:
   `' '` + a maximal run of letters (`str.isalpha`) or a maximal run of digits (`str.isdigit`);
2. otherwise, a maximal run of letters, or a maximal run of digits;
3. otherwise, a maximal run of whitespace (`str.isspace`) — but the run stops **before** a `' '` that is
   immediately followed by a letter or digit (that space belongs to the next chunk per rule 1);
4. otherwise, a single character (punctuation, symbols, emoji, ...).

Examples:
```
"Hello  world!! 42"  -> ["Hello", " ", " world", "!", "!", " 42"]
"abc123"             -> ["abc", "123"]
"\n\nhi there"       -> ["\n\n", "hi", " there"]
"é😀 x"              -> ["é", "😀", " x"]
```

## `BPETokenizer`

### `train(text, vocab_size)`
- `vocab_size` is the total number of non-special tokens wanted. It must be `>= 256`
  (`ValueError` otherwise); `256` means no merges.
- Split `text` with `split_text`, encode each chunk as UTF-8, and turn each chunk into a list of byte ids.
- Repeat `vocab_size - 256` times:
  1. Count pairs over **all** chunks (pairs never span two chunks).
  2. If there are no pairs at all, stop.
  3. Choose the pair with the **highest count**. On ties choose the **smallest pair** (ordinary tuple
     comparison: smallest first id, then smallest second id).
  4. If the chosen pair's count is less than 2, stop (training ends early).
  5. Assign it the next id (`256 + k`), replace it in every chunk with `merge`, record it in `merges`
     and `vocab`.
- After training: `self.merges` is a dict `{(a, b): id}` in the order learned and `self.vocab` is
  `{id: bytes}` for every non-special id.
- Training replaces any previous training (but keeps registered special tokens).

### `encode_ordinary(text) -> list[int]`
Ignores special tokens. Split with `split_text`; for each chunk (as UTF-8 byte ids), repeatedly:
find, among the pairs present in the chunk, the one with the **lowest merge id** (i.e. learned
earliest); if no present pair is in `merges`, stop; otherwise `merge` it. Concatenate the results of all
chunks.

### `register_special_tokens(tokens: dict[str, int])`
Adds special tokens, e.g. `{"<|endoftext|>": 1000}`. `ValueError` if an id collides with an id in
`vocab` or with an already-registered special token (with a different string).

### `encode(text, allowed_special="none") -> list[int]`
- `allowed_special == "none"`: exactly `encode_ordinary(text)` (special-token strings are treated as plain text).
- `allowed_special == "all"`: scan `text` left to right; at each position, if one or more special token
  strings start there, take the **longest** one, emit its id, and continue after it. The text between
  special tokens is encoded with `encode_ordinary`.
- Any other value → `ValueError`.

### `decode(ids) -> str`
Concatenate the **bytes** of all tokens (a special token's bytes are its string encoded as UTF-8), then
decode the whole byte string as UTF-8 with `errors="replace"`. Unknown id → `ValueError`.

### `save() -> str` and `BPETokenizer.load(text) -> BPETokenizer`
`save()` returns this text format (lines separated by `"\n"`, no trailing newline):
```
bpe v1
<number of merges N>
<a> <b>          # N lines, the merges in the order learned (merge k creates id 256 + k)
<number of special tokens M>
<id> <string>    # M lines, sorted by id; the string is everything after the first space
```
`load(text)` rebuilds an equivalent tokenizer (merges, vocab, special tokens). `ValueError` if the first
line is not `bpe v1`.

### `vocab_size` (property)
Number of non-special tokens plus number of special tokens.
