# Drill 5 — Union-Find (Disjoint Set Union) and Kruskal's MST

## The problem

Imagine you're connecting computers with cables, one cable at a time. After each new cable, someone asks: *"can computer
x talk to computer y now?"*. Or you're processing a list of friendships one by one, and want to know at any moment how
many separate friend circles there are.

These are all the same situation: elements get **grouped together** over time (groups only ever merge, never split), and
you need to answer **"are these two in the same group?"** very quickly, many times.

Why not just run a BFS (drill 2) each time? Because BFS answers one question by exploring the whole graph. With thousands
of questions, that's far too slow. You could keep a dict saying which group each element belongs to, but merging two groups
would then mean relabelling every member of one of them, which is also slow for big groups.

**Union-Find** (also called *Disjoint Set Union*, because the groups never overlap) makes both operations almost
instantaneous:
- `find(x)`: return the **representative** (root) of x's group. Same root ⇔ same group.
- `union(a, b)`: merge the groups of a and b.

The **representative** is one member chosen to stand for the whole group, like a team captain. Two elements are in the same
group exactly when they have the same representative.

---

## How it works: a forest of little trees

Each group is stored as a **tree**: every element points to a **parent** element in its group, and following the parents
upward always ends at the group's **root**, which points to itself. The root is the representative.

```
parent: a->a  b->a  c->a  d->d  e->d        groups {a, b, c} and {d, e}
find(c) = a     find(e) = d
union(c, e): roots a and d differ -> make one root the parent of the other: parent[d] = a
```

In this example:
- `a` is its own parent, so it's a root. `b` and `c` point to `a`. That's the group `{a, b, c}`, represented by `a`.
- `d` is a root, and `e` points to it. That's the group `{d, e}`.
- `find(c)` follows `c → a` and stops, because `a` is a root. `find(e)` follows `e → d`.
- `union(c, e)` finds the two roots, `a` and `d`, and makes one point to the other: `parent[d] = a`. That single change
  merges the groups. From now on, `find(e)` goes `e → d → a`.

The key insight: a group doesn't need to be stored as a list of members. It's enough that every member can **walk up** to a
common root. And merging two groups touches just *one* pointer, however many members they have.

The tree is stored very simply, as a dict `parent` from each element to its parent. A second dict, `size`, records how many
elements each root's group contains.

Two improvements keep the trees short, so `find` stays fast.

### Improvement 1: union by size

**1. Union by size.** Hang the **smaller** tree under the root of the **larger** one (and add the sizes). Otherwise
you can build a long chain and `find` becomes O(n).

Without this rule, an unlucky sequence of unions, like `union(1, 2)`, `union(2, 3)`, `union(3, 4)` with the new element
always becoming the root, builds one long chain: `1 → 2 → 3 → 4 → ...`. Then `find(1)` has to walk the whole chain. By
always hanging the smaller group under the larger one, an element only gets one level deeper when its group joins a group
at least as big, so its group at least doubles. A group can't double more than about log₂(n) times, so no element is ever
more than about log₂(n) steps from its root (20 steps for a million elements).

```python
def union(self, a, b):
    ra, rb = self.find(a), self.find(b)
    if ra == rb:
        return False               # already together: nothing changes (group count stays!)
    if self.size[ra] < self.size[rb]:
        ra, rb = rb, ra            # ra is now the bigger root
    self.parent[rb] = ra
    self.size[ra] += self.size[rb]
    self.count -= 1                # one group fewer
    return True
```

Line by line:
- Find both roots.
- **If they're the same, the two elements are already in one group: change nothing and return `False`.** This guard
  matters. Without it, the group count would go down even though no groups merged, and Kruskal's algorithm (below), which
  uses the return value, would take edges it should skip.
- Swap the names if necessary, so that `ra` is the root of the bigger group.
- Hang `rb` under `ra`.
- `ra`'s group now also contains all of `rb`'s members, so add `rb`'s size to `ra`'s. Only the sizes of roots are kept up to
  date. Sizes of non-roots don't matter.
- There's now one group fewer.

### Improvement 2: path compression

**2. Path compression.** After finding the root, point every node on the path **directly** at the root.
```python
def find(self, x):
    root = x
    while self.parent[root] != root:     # 1) walk up to the root
        root = self.parent[root]
    while self.parent[x] != root:        # 2) re-point the path
        nxt = self.parent[x]
        self.parent[x] = root
        x = nxt
    return root                          # return the ROOT (not x!)
```
Recursive version: `if self.parent[x] != x: self.parent[x] = self.find(self.parent[x]); return self.parent[x]`.

`find` works in two passes:
1. The first loop walks up from `x` until it reaches a node that is its own parent: the root.
2. The second loop walks the *same* path again and makes every node on it point **directly** at the root. The next `find` on
   any of them takes a single step. It's a free improvement, since we had to walk that path anyway.

The second loop is careful about order. It saves `parent[x]` in `nxt` *before* overwriting it, because overwriting first would
lose the way up. And the function must return `root`. Returning `x`, or `parent[x]`, would return some node on the path,
which isn't necessarily the representative.

With both optimizations, operations are "practically constant" (inverse Ackermann, α(n) ≤ 4 for any real n).

(That's a mathematical way of saying that, in practice, each operation takes a handful of steps, no matter how many elements
there are.)

---

## An application: the cheapest way to connect everything

### Spanning trees

Imagine several buildings that must all be connected by cables, and each possible cable has a price. You want every
building connected, directly or indirectly, at the lowest total cost.

A **spanning tree** of a connected weighted graph connects all nodes using exactly n−1 edges with no cycle. The
**minimum** spanning tree (MST) has the smallest total weight (e.g. the cheapest way to cable all buildings).

Why exactly n − 1 edges and no cycle? Connecting n buildings takes at least n − 1 cables. Any extra cable would close a loop
between buildings that were already connected, which costs money without connecting anything new.

### Kruskal's algorithm

Kruskal's algorithm is *greedy*: it always takes the cheapest cable that is still *useful*, i.e. one that connects two
buildings that aren't connected yet. Union-Find answers "are they connected yet?" instantly, which is why the two always
appear together.

Kruskal's algorithm:
1. Sort all edges by weight (ascending).
2. For each edge (u, v): if u and v are in **different** groups, take the edge and `union(u, v)`;
   otherwise skip it (it would close a cycle).
3. Stop when you have n−1 edges (or edges run out → the graph is disconnected).

Example, nodes 0..3, edges (weight, u, v): `(1,0,1) (2,1,2) (3,0,2) (4,2,3)`
→ take (1,0,1), take (2,1,2), skip (3,0,2) (0 and 2 already connected), take (4,2,3). Total 7.

Traced: the cheapest edge connects 0 and 1. The next connects 1 and 2, so now 0, 1 and 2 are one group. The edge (0, 2)
costs 3 but would connect two nodes that are already in the same group, so it's skipped. The edge (2, 3) brings in node 3.
That's 3 edges for 4 nodes, so we're done, at a total cost of 1 + 2 + 4 = 7.

Notice that `union` already tells you whether the edge was useful: it returns `True` if it merged two groups and `False` if
they were already one. So the code can simply be "if `uf.union(u, v)`: take the edge". The edges must be sorted by **weight**.
If they're stored as `(u, v, weight)`, sorting them directly sorts by `u` instead, which is a typical bug.

---

## Where bugs hide
- `union` decrementing the count (or returning True) when both are already in the same set
- size bookkeeping: `size[ra] += size[ra]` instead of `size[rb]`; attaching the bigger under the smaller
- `find` returning `x` (or `parent[x]`) instead of the root after compression; recursion without assigning
- Kruskal: sorting by the wrong tuple field; adding edges without checking `union`'s result
- forgetting that `find` on an unknown element should raise (spec) instead of silently creating it

## Drill
`exam/union_find.py` — a `UnionFind` class + `kruskal`, 5 bugs, 15 tests. Timer: 30 minutes.
