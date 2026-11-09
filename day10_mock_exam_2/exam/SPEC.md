# Transactional Key-Value Store — Specification

`kvstore.py` implements an in-memory key-value store with nested transactions, a binary snapshot format,
and a tiny command language. **The implementation is broken.** Fix it so it matches this spec.
The test suite `test_kvstore.py` is the final word where this spec is ambiguous.

Keys and values are `str`.

## `KVStore` — data operations

- `set(key, value)` — store `value` under `key` (overwriting).
- `get(key)` → the value, or `None` if the key is absent.
- `delete(key)` → `True` if the key existed (was visible) and was removed, `False` otherwise.
- `count(value)` → number of visible keys whose value equals `value`.
- `keys(prefix="")` → sorted list of visible keys that start with `prefix`.

"Visible" always means: as seen from inside the innermost open transaction (or the committed state if no
transaction is open).

## Transactions

- `begin()` opens a new transaction. Transactions can be **nested**.
- `rollback()` discards every change made in the **innermost** open transaction only.
  With no open transaction → `RuntimeError("NO TRANSACTION")`.
- `commit()` makes the changes of **all** open transactions permanent and closes them all.
  With no open transaction → `RuntimeError("NO TRANSACTION")`.
- `depth` (property) → number of currently open transactions.
- Changes made inside a transaction are visible immediately (to `get`, `count`, `keys`, ...), both
  inside that transaction and in transactions nested inside it.

Example:
```
set a 10; begin; set a 20; begin; delete a; get a -> None
rollback; get a -> 20; rollback; get a -> 10
```

## Snapshot format — `serialize()` / `KVStore.deserialize(data)`

`serialize()` returns `bytes` describing the **visible** state:
```
b"KV1"                       3 bytes, magic
N                            4 bytes, unsigned big-endian: number of entries
then N entries, sorted by the UTF-8 bytes of the key, each:
    key length               2 bytes, unsigned big-endian, length in BYTES of the UTF-8 key
    key                      UTF-8
    value length             4 bytes, unsigned big-endian, length in BYTES of the UTF-8 value
    value                    UTF-8
```
`KVStore.deserialize(data)` (a classmethod) returns a new store (no open transactions) holding those
entries. It raises `ValueError` if: the magic is wrong, the data ends early (anywhere), there are
bytes left after the last entry, a key/value isn't valid UTF-8, or keys are not strictly increasing
(by bytes) — this also rejects duplicates.

## Command language — `execute(line)` and `run_script(lines)`

`store.execute(line)` runs one command and returns its output as a `str`. The command word is
case-insensitive; keys are case-sensitive. Words are separated by any whitespace.

| Command | Output |
|---|---|
| `SET <key> <value>` | `""`. The value is **everything after the key** with surrounding whitespace removed; it may contain spaces (internal whitespace is kept exactly). |
| `GET <key>` | the value, or `NULL` if absent |
| `DELETE <key>` | `1` if deleted, `0` otherwise |
| `COUNT <value>` | the count, as a decimal string. The value is everything after `COUNT` (stripped), like in `SET`. |
| `KEYS [<prefix>]` | the matching keys joined by `,` (empty string if none) |
| `BEGIN` | `""` |
| `ROLLBACK` / `COMMIT` | `""`, or `NO TRANSACTION` if none is open |
| an empty / blank line | `""` |
| anything else (unknown command, wrong number of words) | `ERROR` |

`run_script(lines)` runs the lines on a **new** store and returns the list of the **non-empty** outputs,
in order.
