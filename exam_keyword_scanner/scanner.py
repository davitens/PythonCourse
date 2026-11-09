"""Multi-keyword text scanner (Aho-Corasick). The behaviour is defined in SPEC.md."""


def _char_width(lead):
    if lead < 0x80:
        return 1
    if lead & 0xE0 == 0xC0:
        return 2
    if lead & 0xE0 == 0xE0:
        return 3
    if lead & 0xF8 == 0xF0:
        return 4
    raise ValueError(f"invalid lead byte {lead:#04x}")


def utf8_offsets(data):
    offsets = []
    char_index = 0
    i = 0
    while i < len(data):
        width = _char_width(data[i])
        if i + width > len(data):
            raise ValueError("truncated character")
        offsets.extend([char_index] * width)
        char_index += 1
        i += width
    offsets.append(char_index)
    return offsets


class Match:
    def __init__(self, keyword, start, end):
        self.keyword = keyword
        self.start = start
        self.end = end

    @property
    def length(self):
        return self.end - self.start

    def __eq__(self, other):
        if not isinstance(other, Match):
            return NotImplemented
        return (self.keyword, self.start, self.end) == (other.keyword, other.start, other.end)

    def __repr__(self):
        return f"Match({self.keyword!r}, {self.start}, {self.end})"


class _Node:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.own = []
        self.outputs = []


class KeywordScanner:
    def __init__(self, keywords=(), ignore_case=False):
        self.ignore_case = ignore_case
        self._root = _Node()
        self._keywords = []
        self._seen = set()
        self._built = False
        for keyword in keywords:
            self.add(keyword)

    def _fold(self, data):
        return data.lower() if self.ignore_case else data

    # ------------------------------------------------------------ building
    def add(self, keyword):
        if not isinstance(keyword, str):
            raise TypeError("keyword must be a str")
        if not keyword:
            raise ValueError("keyword must not be empty")
        key = keyword.encode("utf-8")
        self._seen.add(key)
        self._keywords.append(keyword)
        node = self._root
        for byte in key:
            if byte not in node.children:
                node.children[byte] = _Node()
            node = node.children[byte]
        node.own = [keyword]

    def keywords(self):
        return list(self._keywords)

    def build(self):
        root = self._root
        root.outputs = []
        queue = []
        for child in root.children.values():
            child.fail = root
            child.outputs = list(child.own)
            queue.append(child)
        while queue:
            node = queue.pop()
            for byte, child in node.children.items():
                fallback = node.fail
                while fallback is not root and byte not in fallback.children:
                    fallback = fallback.fail
                child.fail = fallback.children.get(byte, root)
                child.outputs = list(child.own)
                queue.append(child)
        self._built = True

    def _ensure_built(self):
        if not self._built:
            self.build()

    def _step(self, node, byte):
        if node is not self._root and byte not in node.children:
            node = node.fail
        return node.children.get(byte, self._root)

    # ------------------------------------------------------------ searching
    def _scan(self, data):
        self._ensure_built()
        node = self._root
        for i, byte in enumerate(self._fold(data)):
            node = self._step(node, byte)
            for keyword in node.outputs:
                yield keyword, i + 1

    def find_all(self, text):
        data = text.encode("utf-8")
        offsets = utf8_offsets(data)
        matches = []
        for keyword, end in self._scan(data):
            start = end - len(keyword)
            matches.append(Match(keyword, offsets[start], offsets[end]))
        return matches

    def contains_any(self, text):
        self._ensure_built()
        node = self._root
        for byte in self._fold(text.encode("utf-8")):
            node = self._step(node, byte)
            if node.own:
                return True
        return False

    def find_non_overlapping(self, text):
        ordered = sorted(self.find_all(text), key=lambda m: m.start)
        chosen = []
        last_end = 0
        for match in ordered:
            if match.start > last_end:
                chosen.append(match)
                last_end = match.end
        return chosen

    def first(self, text):
        chosen = self.find_non_overlapping(text)
        return chosen[0] if chosen else None

    def count(self, text):
        counts = {keyword: 0 for keyword in self._keywords}
        for match in self.find_all(text):
            counts[match.keyword] += 1
        return counts

    # ------------------------------------------------------------ rewriting
    def replace(self, text, replacements):
        pieces = []
        pos = 0
        for match in self.find_non_overlapping(text):
            if match.keyword in replacements:
                pieces.append(text[pos:match.start])
                pieces.append(replacements[match.keyword])
                pos = match.end
        return "".join(pieces)

    def highlight(self, text, before="[", after="]"):
        pieces = []
        pos = 0
        for match in self.find_non_overlapping(text):
            pieces.append(text[pos:match.start])
            pieces.append(before + text[match.start:match.end] + after)
            pos = match.end
        pieces.append(text[pos:])
        return "".join(pieces)

    def summary(self, text):
        found = [(keyword, n) for keyword, n in self.count(text).items() if n > 0]
        found.sort(key=lambda item: item[1], reverse=True)
        return "\n".join(f"{keyword}: {n}" for keyword, n in found)

    def stream(self):
        self._ensure_built()
        return StreamScanner(self)


class StreamScanner:
    def __init__(self, scanner):
        self._scanner = scanner
        self._node = scanner._root
        self.position = 0

    def feed(self, chunk):
        results = []
        self._node = self._scanner._root
        for byte in self._scanner._fold(chunk):
            self._node = self._scanner._step(self._node, byte)
            self.position += 1
            for keyword in self._node.outputs:
                length = len(keyword.encode("utf-8"))
                results.append((keyword, self.position - length, self.position))
        return results

    def reset(self):
        self.position = 0
