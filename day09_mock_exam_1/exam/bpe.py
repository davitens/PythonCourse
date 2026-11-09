"""Byte-level BPE tokenizer. See SPEC.md."""


def get_stats(ids, counts=None):
    counts = {} if counts is None else counts
    for i in range(len(ids) - 2):
        pair = (ids[i], ids[i + 1])
        counts[pair] = counts.get(pair, 0) + 1
    return counts


def merge(ids, pair, idx):
    out = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            out.append(idx)
            i += 1
        else:
            out.append(ids[i])
            i += 1
    return out


def _is_word_char(c):
    return c.isalpha() or c.isdigit()


def _space_attaches(text, i):
    return text[i] == " " and i + 1 < len(text) and _is_word_char(text[i + 1])


def split_text(text):
    chunks = []
    i, n = 0, len(text)
    while i < n:
        start = i
        if _space_attaches(text, i):
            i += 1
        c = text[i]
        if c.isalpha():
            while i < n and text[i].isalpha():
                i += 1
        elif c.isdigit():
            while i < n and text[i].isdigit():
                i += 1
        elif c.isspace():
            while i < n and text[i].isspace():
                i += 1
        else:
            i += 1
        chunks.append(text[start:i])
    return chunks


class BPETokenizer:
    def __init__(self):
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.special_tokens = {}  # str -> id

    @property
    def vocab_size(self):
        return len(self.vocab) + len(self.special_tokens)

    # ------------------------------------------------------------------ training
    def train(self, text, vocab_size):
        if vocab_size < 256:
            raise ValueError("vocab_size must be at least 256")
        chunks = [list(ch.encode("utf-8")) for ch in split_text(text)]
        merges = {}
        vocab = {i: bytes([i]) for i in range(256)}
        for k in range(vocab_size - 256):
            stats = {}
            for ids in chunks:
                get_stats(ids, stats)
            if not stats:
                break
            pair = max(stats, key=stats.get)
            if stats[pair] < 1:
                break
            idx = len(vocab) + k
            chunks = [merge(ids, pair, idx) for ids in chunks]
            merges[pair] = idx
            vocab[idx] = vocab[pair[1]] + vocab[pair[0]]
        self.merges = merges
        self.vocab = vocab

    # ------------------------------------------------------------------ encoding
    def _encode_chunk(self, data):
        ids = list(data)
        while len(ids) >= 2:
            stats = get_stats(ids)
            pair = max(stats, key=lambda p: self.merges.get(p, -1))
            if pair not in self.merges:
                break
            ids = merge(ids, pair, self.merges[pair])
        return ids

    def encode_ordinary(self, text):
        out = []
        for chunk in split_text(text):
            out.extend(self._encode_chunk(chunk.encode("utf-8")))
        return out

    def register_special_tokens(self, tokens):
        for s, idx in tokens.items():
            if idx in self.vocab:
                raise ValueError(f"id {idx} collides with the vocabulary")
            for other, other_idx in self.special_tokens.items():
                if other_idx == idx and other != s:
                    raise ValueError(f"id {idx} already used by {other!r}")
            self.special_tokens[s] = idx

    def encode(self, text, allowed_special="none"):
        if allowed_special == "none":
            return self.encode_ordinary(text)
        if allowed_special != "all":
            raise ValueError("allowed_special must be 'none' or 'all'")
        out = []
        i = 0
        start = 0
        while i < len(text):
            best = None
            for s in self.special_tokens:
                if text.startswith(s, i):
                    best = s
                    break
            if best is None:
                i += 1
                continue
            out.extend(self.encode_ordinary(text[start:i]))
            out.append(self.special_tokens[best])
            i += len(best)
            start = i
        out.extend(self.encode_ordinary(text[start:]))
        return out

    # ------------------------------------------------------------------ decoding
    def decode(self, ids):
        inverse_special = {idx: s for s, idx in self.special_tokens.items()}
        parts = []
        for idx in ids:
            if idx in self.vocab:
                parts.append(self.vocab[idx])
            elif idx in inverse_special:
                parts.append(inverse_special[idx].encode("utf-8"))
            else:
                raise ValueError(f"unknown token id {idx}")
        return "".join(p.decode("utf-8", errors="replace") for p in parts)

    # ------------------------------------------------------------------ persistence
    def save(self):
        lines = ["bpe v1", str(len(self.merges))]
        for (a, b), _ in sorted(self.merges.items(), key=lambda kv: kv[1]):
            lines.append(f"{a} {b}")
        lines.append(str(len(self.special_tokens)))
        for s, idx in sorted(self.special_tokens.items()):
            lines.append(f"{idx} {s}")
        return "\n".join(lines)

    @classmethod
    def load(cls, text):
        lines = text.split("\n")
        if not lines or lines[0] != "bpe v1":
            raise ValueError("bad header")
        tok = cls()
        n = int(lines[1])
        for k, line in enumerate(lines[2:2 + n], 1):
            a, b = (int(x) for x in line.split())
            idx = 256 + k
            tok.merges[(a, b)] = idx
            tok.vocab[idx] = tok.vocab[a] + tok.vocab[b]
        m = int(lines[2 + n])
        specials = {}
        for line in lines[3 + n:3 + n + m]:
            idx, _, s = line.partition(" ")
            specials[s] = int(idx)
        tok.register_special_tokens(specials)
        return tok
