# Drill 3 — Dijkstra's Shortest Paths (with `heapq`)

## The problem

In drill 2, every edge counted the same: one step. BFS found the path with the **fewest edges**. Real routes aren't like
that. Roads have different lengths, flights have different prices, network links have different delays. When each edge
has a **cost** (also called a *weight*), the question becomes: **what's the cheapest way to get from the start to every
other node?** A graph with costs on its edges is called a **weighted graph**.

BFS can't answer this, because a path with *more* edges can be *cheaper*:

```text
a → b costs 10
a → c costs 1,  c → b costs 2
```

BFS would say the best route from `a` to `b` is the direct edge (one step). But that costs 10, while going through `c`
costs 1 + 2 = 3.

**Dijkstra's algorithm** solves this, as long as **no edge has a negative cost**. (That's why the exam code must reject
negative weights. The reason is explained below.) It's what route planners, network routing protocols and games use to
find cheapest paths.

---

## The idea

Dijkstra is BFS with one change. Instead of exploring nodes in the order they were discovered, it always explores the node
that is **cheapest to reach so far**.

It keeps a dict `dist` of **tentative distances**: the cheapest cost found *so far* to reach each node. "Tentative" means it
might still improve. At the start, only the source is known: `dist[source] = 0`. Every other node is "infinitely far",
which here simply means it isn't in `dist` yet.

Then it repeats:
1. take the **not-yet-finalized node with the smallest tentative distance**;
2. that distance is now final (no cheaper way can exist, because every other route goes through a node that is
   already at least as far, and weights are non-negative);
3. **relax** its edges: for each edge `u → v` with weight `w`, if `dist[u] + w` is smaller than what we know for `v`,
   update `dist[v]` and remember `prev[v] = u`.

"Relax" is just the standard name for this check: "is going through `u` a cheaper way to reach `v` than anything I've found
so far?". The `prev` dict plays the same role as `parent` in BFS: it remembers which node we came from, so the path itself
can be rebuilt at the end.

### Why can step 2 declare a distance final?

Suppose the cheapest unfinished node is `u`, at cost 5. Could there be a cheaper route to `u` that we haven't found yet? Any
such route would have to pass through some other unfinished node first, and every unfinished node costs at least 5 to reach
(that's why `u` was picked). Adding more edges can only add cost, never remove it, so the route would cost at least 5. So 5
really is the best.

The argument relies on "adding edges can only add cost". With a **negative** edge, a longer detour could end up cheaper, and
the algorithm would declare distances final too early. That's why negative weights are rejected.

---

## Picking the cheapest node fast: the heap

Step 1 needs "the unfinished node with the smallest distance", over and over. Searching through all the nodes each time
would be slow. A **priority queue** is a structure designed for exactly this: you can add items, and you can always take
out the *smallest* one, both quickly.

Python provides a priority queue as the module `heapq`. It works on an ordinary list that it keeps in a special order called
a **heap**. In a heap, the smallest item is always at position 0, but the rest is *not* fully sorted, only arranged so that
finding the next-smallest is quick.

```python
import heapq
h = []
heapq.heappush(h, (5, "x"))
heapq.heappush(h, (2, "y"))
heapq.heappush(h, (9, "z"))
heapq.heappop(h)      # (2, 'y')  smallest first; tuples compare element by element
h[0]                  # peek at the smallest without removing
```

- `heapq.heappush(h, item)` adds an item and keeps the heap order.
- `heapq.heappop(h)` removes and returns the smallest item.
- `h[0]` looks at the smallest item without removing it.

**Never** use `h.pop()` or `h.pop(0)` on a heap: a heap list is not sorted, those return arbitrary elements.
Put the **priority first** in the tuple: `(distance, node)`.

Why the order inside the tuple matters: tuples are compared element by element (Day 3), so `(distance, node)` puts the
smallest *distance* first, and only uses the node name to break ties. With `(node, distance)`, the heap would hand out nodes
in alphabetical order, and the distances would come out wrong.

---

## A worked example

Here's a small graph. Node `s` is the start.

```
s→a 1    s→b 4    a→b 2    a→c 6    b→c 1
```

| step | pop (dist, node) | relax | dist after |
|---|---|---|---|
| 0 | (0, s) | a=1, b=4 | s0 a1 b4 |
| 1 | (1, a) | b: 1+2=3 < 4 → b=3; c=1+6=7 | s0 a1 b3 c7 |
| 2 | (3, b) | c: 3+1=4 < 7 → c=4 | s0 a1 b3 c4 |
| 3 | (4, b) | stale entry from step 0 (b is already final with 3): **skip** | unchanged |
| 4 | (4, c) | — | final |
| 5 | (7, c) | stale: skip | heap empty → done |

Shortest path to c: follow `prev`: c ← b ← a ← s → reversed: `s, a, b, c`, cost 4.

Read it row by row:
- **Step 0.** We take `s` (cost 0) and look at its edges. We can reach `a` for 1 and `b` for 4, so both go into the heap.
- **Step 1.** The cheapest in the heap is `a` (1). From `a` we can reach `b` for 1 + 2 = 3. That beats the 4 we had, so `b`
  is improved to 3, and `(3, b)` is pushed. `c` is reached for the first time, at 1 + 6 = 7.
- **Step 2.** The cheapest is now `b` (3). From `b`, `c` costs 3 + 1 = 4, which beats 7.
- **Steps 3–5.** The heap still contains `(4, b)` and `(7, c)`, old entries pushed before those nodes were improved. These are
  called **stale entries**. When they come out, the node is already finished, so they're skipped.

This example shows exactly why BFS fails. The direct edge `s → b` (cost 4) is beaten by the longer route `s → a → b` (cost 3).

### Lazy deletion

**Lazy deletion:** when `dist[v]` improves we just push a new `(new_dist, v)`; the old, larger entry stays in the
heap. When it's popped later, skip it (`if node in done: continue` or `if d > dist[node]: continue`).

Removing the old entry from the middle of a heap would be awkward and slow. So we leave it there and recognise it later.
That's why the code must check "is this node already finished?" after every pop. Without that check, a stale entry would
be processed as if it were real.

---

## The template

```python
import heapq

def dijkstra(graph, source):          # graph: {u: [(v, w), ...]}
    dist, prev = {source: 0}, {}
    heap, done = [(0, source)], set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, w in graph.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:     # strictly better only
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev
```
Complexity: O((V + E) log V).

Line by line:
- `graph` maps each node to a list of `(neighbour, cost)` pairs.
- `dist` holds the best known cost to each node, `prev` the node we came from, `heap` the candidates as `(cost, node)`, and
  `done` the nodes whose distance is final.
- Each pass takes the cheapest candidate. If its node is already finished, it's a stale entry, so skip it.
- Otherwise the node is finished now. For each outgoing edge, compute the cost of reaching the neighbour through this node
  (`nd`). If the neighbour has never been reached, or this route is strictly cheaper, record it and push a new candidate.
- `graph.get(u, [])` handles nodes with no outgoing edges.
- Nodes that are never reached simply don't appear in `dist`. That's how "unreachable" is represented. The spec will say what
  to return for them.

The complexity line says the work grows roughly with the size of the graph, times a small factor (`log V`) for the heap
operations. See drill 1 for what big-O notation means.

### Ties between equally cheap paths

**Ties:** with `nd < dist[v]` the *first* path found to `v` is kept when another path has equal cost. With `<=`,
a later equal-cost path overwrites `prev[v]`. Specs often pin this down, and tests check the exact path.

Both versions give the same *distances*. Only the *path* reported can differ. So a bug here passes the distance tests and
fails only the path tests, which is a useful clue.

---

## Where bugs hide
- `heap.pop()` instead of `heapq.heappop(heap)`; `(node, dist)` instead of `(dist, node)`
- forgetting to skip stale entries, or finalizing a node when it's *pushed* instead of when it's *popped*
- `<=` vs `<` in the relaxation (tie-breaking of paths)
- path reconstruction: not reversed, or missing the source
- not validating negative weights; unreachable nodes reported with a distance
- off-by-one in "within distance D" (`<` vs `<=`)

## Drill
`exam/dijkstra.py` — 4 functions, 5 bugs, 15 tests. Timer: 30 minutes.
