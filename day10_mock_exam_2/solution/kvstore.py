"""Transactional key-value store. See SPEC.md."""

_DELETED = object()  # tombstone marking a key deleted inside a transaction


class KVStore:
    def __init__(self):
        self._data = {}     # committed state
        self._layers = []   # one dict of changes per open transaction (innermost last)

    # ---------------------------------------------------------------- reads
    def _lookup(self, key):
        for layer in reversed(self._layers):
            if key in layer:
                value = layer[key]
                return None if value is _DELETED else value
        return self._data.get(key)

    def _visible(self):
        view = dict(self._data)
        for layer in self._layers:
            for key, value in layer.items():
                if value is _DELETED:
                    view.pop(key, None)
                else:
                    view[key] = value
        return view

    def get(self, key):
        return self._lookup(key)

    def count(self, value):
        return sum(1 for v in self._visible().values() if v == value)

    def keys(self, prefix=""):
        return sorted(k for k in self._visible() if k.startswith(prefix))

    # ---------------------------------------------------------------- writes
    def set(self, key, value):
        if self._layers:
            self._layers[-1][key] = value
        else:
            self._data[key] = value

    def delete(self, key):
        if self._lookup(key) is None:
            return False
        if self._layers:
            self._layers[-1][key] = _DELETED
        else:
            del self._data[key]
        return True

    # ---------------------------------------------------------------- transactions
    @property
    def depth(self):
        return len(self._layers)

    def begin(self):
        self._layers.append({})

    def rollback(self):
        if not self._layers:
            raise RuntimeError("NO TRANSACTION")
        self._layers.pop()

    def commit(self):
        if not self._layers:
            raise RuntimeError("NO TRANSACTION")
        self._data = self._visible()
        self._layers = []

    # ---------------------------------------------------------------- snapshots
    def serialize(self):
        items = sorted((k.encode("utf-8"), v.encode("utf-8")) for k, v in self._visible().items())
        out = bytearray(b"KV1")
        out += len(items).to_bytes(4, "big")
        for kb, vb in items:
            out += len(kb).to_bytes(2, "big")
            out += kb
            out += len(vb).to_bytes(4, "big")
            out += vb
        return bytes(out)

    @classmethod
    def deserialize(cls, data):
        if data[:3] != b"KV1":
            raise ValueError("bad magic")
        pos = 3

        def take(n):
            nonlocal pos
            if pos + n > len(data):
                raise ValueError("truncated snapshot")
            chunk = data[pos:pos + n]
            pos += n
            return chunk

        count = int.from_bytes(take(4), "big")
        store = cls()
        prev = None
        for _ in range(count):
            kb = take(int.from_bytes(take(2), "big"))
            vb = take(int.from_bytes(take(4), "big"))
            if prev is not None and kb <= prev:
                raise ValueError("keys not strictly increasing")
            prev = kb
            store._data[kb.decode("utf-8")] = vb.decode("utf-8")
        if pos != len(data):
            raise ValueError("trailing bytes")
        return store

    # ---------------------------------------------------------------- commands
    def execute(self, line):
        parts = line.split()
        if not parts:
            return ""
        cmd = parts[0].upper()
        if cmd == "SET":
            if len(parts) < 3:
                return "ERROR"
            self.set(parts[1], line.strip().split(None, 2)[2])
            return ""
        if cmd == "GET":
            if len(parts) != 2:
                return "ERROR"
            value = self.get(parts[1])
            return "NULL" if value is None else value
        if cmd == "DELETE":
            if len(parts) != 2:
                return "ERROR"
            return "1" if self.delete(parts[1]) else "0"
        if cmd == "COUNT":
            if len(parts) < 2:
                return "ERROR"
            return str(self.count(line.strip().split(None, 1)[1]))
        if cmd == "KEYS":
            if len(parts) > 2:
                return "ERROR"
            return ",".join(self.keys(parts[1] if len(parts) == 2 else ""))
        if cmd in ("BEGIN", "ROLLBACK", "COMMIT"):
            if len(parts) != 1:
                return "ERROR"
            try:
                {"BEGIN": self.begin, "ROLLBACK": self.rollback, "COMMIT": self.commit}[cmd]()
            except RuntimeError as e:
                return str(e)
            return ""
        return "ERROR"


def run_script(lines):
    store = KVStore()
    outputs = []
    for line in lines:
        out = store.execute(line)
        if out:
            outputs.append(out)
    return outputs
