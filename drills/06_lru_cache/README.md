# Drill 6 — LRU Cache (hash map + doubly linked list)

## The problem

A **cache** stores the results of slow operations so they can be reused instead of recomputed: web pages your browser has
already downloaded, database rows recently read, results of expensive function calls. The catch is that memory is limited.
A cache can hold only so many items, its **capacity**. When it's full and a new item arrives, some existing item must be
thrown out. That's called **eviction**.

Which item should go? A simple and very effective rule is **Least Recently Used (LRU)**: throw out the item that hasn't
been used for the longest time. The reasoning is that something you used a moment ago is likely to be needed again soon,
while something untouched for a long time probably isn't. CPUs, browsers, databases and Python's own `functools.lru_cache`
all use this rule.

### What "used" means

Requirements: `get(key)` and `put(key, value)` in **O(1)**, and every successful `get` or `put` makes that key
the **most recently used** (MRU).

Two things to notice:
- **O(1)** means "takes the same small amount of time however big the cache is" (see drill 1 for big-O). A cache that slows
  down as it fills would defeat its purpose.
- **Reading counts as using.** A `get` protects the item from eviction, just like a `put`.

### An example

```
capacity 2
put a 1        order (LRU -> MRU): a
put b 2        a b
get a -> 1     b a          (a refreshed)
put c 3        a c          (full: evict the LRU = b)
get b -> None
```

The right-hand column shows the items from least recently used to most recently used. Follow it carefully:
1. After putting `a` and then `b`, `a` is the oldest.
2. `get a` uses `a`, so `a` becomes the most recent, and now `b` is the oldest.
3. Putting `c` into a full cache evicts the oldest, which is `b`, not `a`.

If `get` forgot to refresh `a`, the cache would wrongly evict `a` here. That's the most common LRU bug.

---

## Why two data structures?

The cache needs two things to be fast at the same time:
1. **Find an item by its key**, for `get`.
2. **Know the order of use**, and change it quickly: move an item to "most recent", and find and remove the oldest.

No single built-in structure does both in O(1):
- A **dict** gives O(1) lookup `key -> node`, but no cheap "which key is oldest?".
- A **doubly linked list** keeps the recency order: moving a node to the end or removing a node is O(1) *if you
  already have the node* — which the dict gives you.

So the cache uses both, and they work as a team. The dict maps each key to its **node** in the list, and the list keeps the
nodes in order of use.

### Linked lists, briefly

You met a linked list in Day 4's exercises: a chain of small **node** objects, each holding a value and a reference to the
next node. A **doubly** linked list has references in both directions, `prev` and `next`. That's what makes removal fast:
a node can remove itself from the chain by telling its left neighbour "your next is now my next", and its right neighbour
"your prev is now my prev". No searching, no shifting, just two pointer changes.

### Sentinels: removing the special cases

Each node has `prev` and `next`. Two **sentinel** (dummy) nodes, `head` and `tail`, avoid all the
"is the list empty / is this the first node" special cases:
```
head <-> [a] <-> [b] <-> [c] <-> tail
          LRU                MRU
head.next is the LRU, tail.prev is the MRU
```

A **sentinel** is a fake node that is always there and never holds real data. With one at each end, every real node always
has a real `prev` and a real `next`, even when it's the first or last real node, so the code never needs to check for `None`.
Fewer special cases means fewer places for bugs.

The convention here: the front of the list (just after `head`) is the **least** recently used, and the back (just before
`tail`) is the **most** recently used.

### The two list operations

```python
class Node:
    def __init__(self, key, value):
        self.key, self.value = key, value
        self.prev = self.next = None

def unlink(node):                        # remove node from the list
    node.prev.next = node.next
    node.next.prev = node.prev

def append_mru(tail, node):              # insert just before the tail sentinel
    node.prev, node.next = tail.prev, tail
    tail.prev.next = node
    tail.prev = node
```

(The exam file's node class also has a line `__slots__ = ("key", "value", "prev", "next")`. It tells Python that
nodes will only ever have these four attributes, which saves memory when there are many of them. It doesn't change how the
code behaves, except that assigning a misspelled attribute, like `node.nxt = ...`, raises `AttributeError` instead of
silently creating a new attribute.)

**`unlink`** makes the node's two neighbours point at each other, which cuts the node out of the chain. The node's own
pointers can stay as they are: nothing in the list leads to it any more.

**`append_mru`** inserts a node just before `tail`, making it the most recent:
1. The new node points back to the current last node (`tail.prev`) and forward to `tail`.
2. The current last node's `next` now points to the new node.
3. `tail.prev` now points to the new node.

The order of steps 2 and 3 matters. Step 2 uses `tail.prev` to find the *old* last node. If step 3 ran first, `tail.prev`
would already be the new node, and step 2 would make the new node point to itself, corrupting the list.

### The cache operations

Operations:
- `get(key)`: node = map.get(key); if found: unlink + append_mru (refresh), return value.
- `put(key, value)`: if the key exists: update the value, refresh. Otherwise: create a node, add it to the map and
  append_mru; if `len(map) > capacity`: evict `head.next` (unlink it **and** `del map[node.key]` — the node stores
  its key precisely so you can do this).
- `delete(key)`: pop from the map **and** unlink from the list.

Note why each node stores its **key**, not just its value. When we evict `head.next`, we have the node, but we also need to
remove its entry from the dict, and for that we need its key.

### The rule that keeps everything consistent

**The invariant to keep in your head:** every key in the dict has exactly one node in the list, and every node in the
list (except sentinels) has its key in the dict. Most LRU bugs break this invariant in one place (deleting from one
structure but not the other).

An **invariant** is a statement that must be true after every operation. Here it's "the dict and the list always describe
the same set of keys". If `delete` removes the key from the dict but leaves the node in the list, the next eviction might
pick that ghost node. If eviction unlinks the node but forgets the dict, `get` will find an item that should have gone.

When debugging, check the invariant directly. Walk the list from `head.next` to `tail` collecting keys, and compare with
`set(self.map)`. If they differ, the last operation broke it.

(In everyday Python you'd use `collections.OrderedDict` with `move_to_end` and `popitem(last=False)`. The exam
code is more likely to show the hand-made version, so practise that.)

---

## Where bugs hide
- forgetting to refresh on `get` (or on updating an existing key)
- evicting the wrong end (`tail.prev` = MRU instead of `head.next` = LRU)
- off-by-one in the capacity check (`>=` vs `>` after inserting)
- removing from the dict but not the list, or vice versa
- read-only operations (`peek`, `in`, `len`) accidentally changing the order
- pointer updates in the wrong order inside `unlink` / `append` (can corrupt the list)

## Drill
`exam/lru_cache.py` — an `LRUCache` class, 5 bugs, 15 tests. Timer: 30 minutes.
Tip: write a tiny `dump()` that prints `keys()` and `list(self.map)` after each step of a failing test.
