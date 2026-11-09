# Mock Exam #2 — Answer Key (SPOILERS)

12 planted bugs in `exam/kvstore.py`.

| # | Where | Broken | Fixed | Catalog |
|---|---|---|---|---|
| 1 | `_lookup` | searches layers oldest-first | `reversed(self._layers)` (innermost first) | E3/order |
| 2 | `set` | writes into `self._layers[0]` (outermost) | `self._layers[-1]` (innermost) | A-index |
| 3 | `delete` | existence check `key not in self._data` (ignores transactions, tombstones) | `self._lookup(key) is None` | B10 |
| 4 | `_visible` | tombstones skipped with `continue` → deleted keys stay visible | `view.pop(key, None)` | B12 |
| 5 | `count` | counts `self._data` only | counts `self._visible()` | B10 |
| 6 | `commit` | merges only the innermost layer (and copies tombstones into data) | `self._data = self._visible(); self._layers = []` | spec |
| 7 | `rollback` | no check → `IndexError` instead of `RuntimeError("NO TRANSACTION")` | add the check | C17 |
| 8 | `serialize` | key length = `len(str)` (characters) and sort by `str` | encode key first: length in **bytes**, sort by bytes | D4 |
| 9 | `serialize` | value length written in 2 bytes | 4 bytes | D11/spec |
| 10 | `deserialize` | no trailing-bytes check | `if pos != len(data): raise ValueError` | spec |
| 11 | `execute` SET | value = `parts[2]` (only first word) | `line.strip().split(None, 2)[2]` | D1 |
| 12 | `execute` GET | `str(value)` → `"None"` | `"NULL" if value is None else value` | spec |

**Suggested order:** 1–4 (core reads/writes; every transaction test depends on them) → 5–7 → serialization 8–10
(use `test_exact_bytes` and print `serialize()` with `.hex(" ")`) → commands 11–12.
