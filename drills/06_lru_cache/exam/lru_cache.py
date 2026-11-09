"""LRU cache with a dict + doubly linked list. Each docstring is the spec."""


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key, value):
        self.key, self.value = key, value
        self.prev = self.next = None


class LRUCache:
    """LRUCache(capacity) - capacity < 1 raises ValueError.

    get(key, default=None) -> value, and the key becomes the most recently used (MRU).
                              Missing key -> default, nothing changes.
    peek(key, default=None) -> like get but does NOT change the recency order.
    put(key, value)        -> existing key: update value, make it MRU, return None.
                              new key: insert as MRU; if that exceeds capacity, evict the
                              least recently used (LRU) key and return it; else return None.
    delete(key)            -> True if the key was present (and is now removed), else False.
    len(cache), key in cache  (neither changes the recency order)
    keys()                 -> list of keys from LRU to MRU
    resize(capacity)       -> set a new capacity (< 1: ValueError); evict LRU keys until the
                              size fits; return the list of evicted keys in eviction order.
    """

    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self.map = {}
        self.head = _Node(None, None)   # head.next is the LRU
        self.tail = _Node(None, None)   # tail.prev is the MRU
        self.head.next = self.tail
        self.tail.prev = self.head

    # -- linked-list helpers
    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _append(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def _touch(self, node):
        self._unlink(node)
        self._append(node)

    def _evict(self):
        lru = self.tail.prev
        self._unlink(lru)
        del self.map[lru.key]
        return lru.key

    # -- public API
    def get(self, key, default=None):
        node = self.map.get(key)
        if node is None:
            return default
        return node.value

    def peek(self, key, default=None):
        node = self.map.get(key)
        return default if node is None else node.value

    def put(self, key, value):
        node = self.map.get(key)
        if node is not None:
            node.value = value
            self._touch(node)
            return None
        node = _Node(key, value)
        self.map[key] = node
        self._append(node)
        if len(self.map) >= self.capacity:
            return self._evict()
        return None

    def delete(self, key):
        node = self.map.pop(key, None)
        if node is None:
            return False
        return True

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return self.get(key) is not None

    def keys(self):
        out = []
        node = self.head.next
        while node is not self.tail:
            out.append(node.key)
            node = node.next
        return out

    def resize(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        evicted = []
        while len(self.map) > capacity:
            evicted.append(self._evict())
        return evicted
