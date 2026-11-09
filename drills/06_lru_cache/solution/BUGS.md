# Drill 6 — Answer key (SPOILERS)

| # | Where | Broken | Fixed | How to find it fast |
|---|---|---|---|---|
| 1 | `get` | no `self._touch(node)` | refresh on every hit | `test_get_refreshes`: after `get("a")`, `a` must not be the one evicted. |
| 2 | `_evict` | `self.tail.prev` (the MRU) | `self.head.next` (the LRU) | The key just inserted is evicted; read the sentinel comments: head side = LRU. |
| 3 | `__contains__` | `self.get(key) is not None` | `key in self.map` | `in` changes the order (spec: it must not) — and would also be wrong for a stored value `None`. |
| 4 | `put` | `len(self.map) >= self.capacity` | `>` | Evicts one item too early: a cache of 3 never holds 3 (`test_fills_to_capacity`). |
| 5 | `delete` | removed from the dict only | also `self._unlink(node)` | Breaks the invariant "dict keys == list nodes": `keys()` still shows it, later eviction hits a `KeyError`. |
