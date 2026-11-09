"""Huffman text compressor and document archive. See SPEC.md."""

MAGIC = b"HUF1"


# ---------------------------------------------------------------- the tree
def byte_frequencies(text):
    freqs = {}
    for b in text:
        freqs[ord(b)] = freqs.get(ord(b), 0) + 1
    return freqs


class Node:
    def __init__(self, weight, symbol=None, left=None, right=None):
        self.weight = weight
        self.symbol = symbol
        self.left = left
        self.right = right
        self.low = symbol if symbol is not None else min(left.low, right.low)

    def is_leaf(self):
        return bool(self.symbol)


def build_tree(freqs):
    if not freqs:
        raise ValueError("no symbols")
    nodes = [Node(weight, symbol) for symbol, weight in freqs.items()]
    while len(nodes) > 1:
        nodes.sort(key=lambda n: n.weight)
        a, b = nodes[0], nodes[1]
        parent = Node(a.weight + b.weight, left=a, right=b)
        nodes = nodes[2:] + [parent]
    return nodes[0]


def code_lengths(root):
    lengths = {}

    def walk(node, depth):
        if node.is_leaf():
            lengths[node.symbol] = depth
        else:
            walk(node.left, depth + 1)
            walk(node.right, depth + 1)

    walk(root, 0)
    return lengths


def canonical_codes(lengths):
    codes = {}
    code = 0
    prev = 0
    for symbol, length in sorted(lengths.items(), key=lambda kv: kv[1]):
        code <<= length - prev
        codes[symbol] = f"{code:b}"
        code += 1
        prev = length
    return codes


# ---------------------------------------------------------------- bits
class BitWriter:
    def __init__(self):
        self.data = bytearray()
        self.current = 0
        self.used = 0

    def write_bit(self, bit):
        self.current = (self.current << 1) | bit
        self.used += 1
        if self.used == 8:
            self.data.append(self.current)
            self.current = 0
            self.used = 0

    def write_code(self, code):
        for c in code:
            self.write_bit(int(c))

    def getvalue(self):
        out = bytes(self.data)
        if self.used:
            out += bytes([self.current])
        return out


class BitReader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def read_bit(self):
        if self.pos > len(self.data) * 8:
            raise ValueError("out of bits")
        byte = self.data[self.pos // 8]
        bit = (byte >> (self.pos % 8)) & 1
        self.pos += 1
        return bit

    def bytes_used(self):
        return (self.pos + 7) // 8


# ---------------------------------------------------------------- the format
def compress(text):
    raw = text.encode("utf-8")
    freqs = byte_frequencies(text)
    lengths = code_lengths(build_tree(freqs)) if freqs else {}
    codes = canonical_codes(lengths)

    out = bytearray(MAGIC)
    out += len(lengths).to_bytes(2, "big")
    for symbol in sorted(lengths):
        out.append(symbol)
        out.append(lengths[symbol])
    out += len(text).to_bytes(4, "big")

    writer = BitWriter()
    for b in raw:
        writer.write_code(codes[b])
    out += writer.getvalue()
    return bytes(out)


def decompress(data):
    pos = 0

    def take(n):
        nonlocal pos
        if pos + n > len(data):
            raise ValueError("truncated")
        chunk = data[pos:pos + n]
        pos += n
        return chunk

    if take(4) != MAGIC:
        raise ValueError("bad magic")
    count = int.from_bytes(take(2), "big")
    lengths = {}
    for _ in range(count):
        symbol, length = take(2)
        if symbol in lengths:
            raise ValueError("bad code table")
        lengths[symbol] = length
    size = int.from_bytes(take(4), "big")

    table = {code: symbol for symbol, code in canonical_codes(lengths).items()}
    reader = BitReader(data[pos:])
    out = bytearray()
    current = ""
    while len(out) < size:
        current += str(reader.read_bit())
        if current in table:
            out.append(table[current])
            current = ""
    return out.decode("utf-8")


# ---------------------------------------------------------------- text helpers
def utf8_chars(data):
    chars = []
    i = 0
    while i < len(data):
        b0 = data[i]
        if b0 < 0x80:
            width = 1
        elif b0 & 0xE0 == 0xC0:
            width = 2
        elif b0 & 0xE0 == 0xE0:
            width = 3
        elif b0 & 0xF8 == 0xF0:
            width = 4
        else:
            raise ValueError(f"bad lead byte at {i}")
        if i + width > len(data):
            raise ValueError(f"truncated character at {i}")
        for b in data[i + 1:i + width]:
            if b & 0xC0 != 0x80:
                raise ValueError(f"bad continuation byte after {i}")
        chars.append(data[i:i + width])
        i += width
    return chars


def truncate_utf8(text, max_bytes):
    kept = []
    total = 0
    for chunk in utf8_chars(text.encode("utf-8")):
        if total + len(chunk) >= max_bytes:
            break
        kept.append(chunk)
        total += len(chunk)
    return b"".join(kept).decode("utf-8")


def format_table(text):
    freqs = byte_frequencies(text)
    if not freqs:
        return ""
    codes = canonical_codes(code_lengths(build_tree(freqs)))
    lines = []
    for symbol, count in sorted(freqs.items(), key=lambda kv: (-kv[1], kv[0])):
        label = chr(symbol) if 33 <= symbol <= 126 else f"0x{symbol:X}"
        lines.append(f"{label} {count} {codes[symbol]}")
    return "\n".join(lines)


# ---------------------------------------------------------------- the archive
class Archive:
    _docs = {}

    def __init__(self):
        self._sizes = {}

    def add(self, name, text):
        if not name:
            raise ValueError("empty name")
        self._docs[name] = compress(text)
        self._sizes[name] = len(text.encode("utf-8"))

    def get(self, name):
        if name not in self._docs:
            raise KeyError(name)
        return decompress(self._docs[name])

    def remove(self, name):
        if name not in self._docs:
            raise KeyError(name)
        del self._docs[name]

    def names(self):
        return sorted(self._docs)

    def stats(self):
        return {
            "documents": len(self._docs),
            "original_bytes": sum(self._sizes.values()),
            "stored_bytes": sum(len(d) for d in self._docs.values()),
        }

    def __len__(self):
        return len(self._docs)

    def __contains__(self, name):
        return name in self._docs

    def __iter__(self):
        return iter(self.names())
