# Drill 2 — Graphs: BFS and DFS

## What a graph is

A **graph** is a set of things together with the connections between them. The things are called **nodes** (or
*vertices*), and the connections are called **edges**.

You already know many graphs, even if you've never called them that:
- a map: cities are nodes, roads are edges;
- a social network: people are nodes, friendships are edges;
- the web: pages are nodes, links are edges;
- a to-do list with dependencies: tasks are nodes, and "A must be done before B" is an edge.

Edges come in two kinds:
- **Undirected** edges work both ways: if Ana is friends with Ben, Ben is friends with Ana. A two-way road.
- **Directed** edges have a direction: a link from page A to page B doesn't mean B links to A. A one-way street.

Even a maze is a graph. Each open square is a node, connected to the open squares directly above, below, left and right
of it.

Most questions about graphs come down to one of two things: *what can I reach from here?* and *what's the best way to get
there?* **BFS** and **DFS**, the subject of this drill, are the two basic ways of systematically visiting everything you can
reach. Almost every other graph algorithm, including Dijkstra (drill 3) and topological sort (drill 4), is a variation of
one of them.

---

## Storing a graph in Python

The most convenient representation is an **adjacency list**: a dict that maps each node to the list of nodes it's
directly connected to (its **neighbours**). "Who are the neighbours of `a`?" is then a single lookup, `graph["a"]`.

A graph usually arrives as a list of edges, so the first job is to build that dict:

```python
edges = [("a", "b"), ("a", "c"), ("b", "d")]
graph = {}
for u, v in edges:
    graph.setdefault(u, []).append(v)
    graph.setdefault(v, []).append(u)     # undirected: add both directions
    # directed: still do graph.setdefault(v, []) so that v exists as a node!
# {'a': ['b', 'c'], 'b': ['a', 'd'], 'c': ['a'], 'd': ['b']}
```

What each line does:
- `graph.setdefault(u, [])` returns the neighbour list of `u`, creating an empty one first if `u` is new (Day 3). Then
  `.append(v)` adds `v` to it.
- For an **undirected** graph, each edge is added in both directions, so `b` also lists `a` as a neighbour.
- For a **directed** graph, only `u → v` is added. But `v` still needs an entry, even an empty one. Otherwise a node with
  no outgoing edges (like `d` in a directed version) is missing from the dict, and when a search reaches it,
  `graph["d"]` raises a `KeyError`. This is a typical planted bug.

The order of the neighbours in each list is the order in which the edges were given. That order decides the order in
which BFS and DFS visit nodes, and tests check that order exactly.

---

## BFS: Breadth-First Search

### The idea

BFS explores the graph **in layers**, like ripples spreading out when you drop a stone in water. First the start node,
then every node one edge away, then every node two edges away, and so on. It never goes to distance 3 before it has
finished distance 2.

To do that, it keeps a **queue** of nodes that have been discovered but not yet explored. A queue is *first in, first out*,
like a queue at a shop: new arrivals join at the back, and you always serve the one at the front. Because the nodes at
distance 1 join the queue before any node at distance 2, they're always explored first.

Python's best tool for a queue is `collections.deque` (drill 1): `append` adds at the back and `popleft` removes from the
front, both fast.

### In code

```python
from collections import deque
def bfs(graph, start):
    order = []
    seen = {start}                 # mark when ENQUEUED, not when popped
    queue = deque([start])
    while queue:
        node = queue.popleft()     # popleft = FIFO. pop() would make it a stack (DFS-like)!
        order.append(node)
        for nb in graph[node]:
            if nb not in seen:
                seen.add(nb)
                queue.append(nb)
    return order
```

Line by line:
- `seen` is a set of every node that has already been discovered. Without it, in a graph with cycles (a → b → a → b...) the
  search would go round forever.
- The queue starts with just the start node.
- Each pass through the loop takes the node at the **front** of the queue, records it, and looks at its neighbours. Any
  neighbour not yet seen is marked as seen and added to the **back** of the queue.

Two details matter a lot:
- **`popleft()`, not `pop()`.** `pop()` takes from the *back*, which turns the queue into a stack, and the search becomes
  depth-first instead of breadth-first. The visiting order changes, and shortest paths stop being shortest.
- **Mark a node as seen when you add it to the queue, not when you take it out.** If you mark late, a node that is a
  neighbour of several already-discovered nodes gets added to the queue several times. The output then contains
  duplicates, and on large graphs the queue can grow enormously.

### A trace

Example: `a: [b, c], b: [a, d], c: [a, e], d: [b], e: [c]` from `a` → `a, b, c, d, e` (layer 0: a,
layer 1: b c, layer 2: d e).

| Take from front | Its new neighbours | Queue afterwards | Order so far |
|---|---|---|---|
| a | b, c | b, c | a |
| b | d (`a` is already seen) | c, d | a b |
| c | e | d, e | a b c |
| d | none | e | a b c d |
| e | none | (empty) | a b c d e |

### Shortest paths with BFS

**Key property:** in an unweighted graph, BFS reaches every node by a path with the **fewest edges**. That makes it
the algorithm for "shortest path in a maze". To recover the path itself, remember each node's **parent** (the node
it was discovered from), then walk back from the goal and **reverse**:
```python
parent = {start: None}
...  # when discovering nb from node: parent[nb] = node
path = []
node = goal
while node is not None:
    path.append(node)
    node = parent[node]
path.reverse()                     # forgetting this returns goal -> start
```

Why are BFS paths the shortest? Because BFS discovers nodes in order of distance. The first time it reaches a node, it
must have come by a shortest route, since all shorter distances were finished first. And once a node is in `seen`, no
later (longer) route can overwrite its `parent`.

To rebuild the path, start at the goal and keep following `parent` back toward the start, whose parent is `None`, which ends
the loop. That collects the path **backwards**, from goal to start, so it has to be reversed at the end. If the goal was never
reached, it isn't in `parent` at all, and the spec will say what to return in that case (often `None` or an empty list).

### Mazes and grids

**Grids:** neighbours of `(r, c)` are `(r+1, c), (r-1, c), (r, c+1), (r, c-1)`, valid only if
`0 <= r < rows and 0 <= c < cols` (strict `<`!) and the cell isn't a wall. Store the distance per cell
(`dist[(r, c)] = dist[current] + 1`).

For a grid you don't build a dict of neighbours. You compute them on the fly from the coordinates: one row up or down, one
column left or right. Each cell is a tuple `(row, col)`, which can be a dict key or a set element (Day 3).

The bounds check has to come **before** reading the grid. The subtle part is negative numbers: Python happily accepts
`grid[-1]`, which is the *last* row (Day 1). So if the code forgets the `0 <= r` half of the check, it doesn't crash: moving
"up" from the top row silently wraps around to the bottom row, and the search finds paths that don't exist.

---

## DFS: Depth-First Search

### The idea

DFS goes **as deep as possible** along one path before backing up, like exploring a maze by always taking the first
corridor you haven't tried, and turning back only at a dead end. It doesn't find shortest paths. You use it when you need
to explore *everything*, or when the shape of the exploration matters: detecting cycles, ordering tasks, or finding
groups of connected nodes.

DFS is most naturally written with **recursion**, a function that calls itself:

```python
def dfs(graph, start):
    order, seen = [], set()
    def visit(node):
        seen.add(node)
        order.append(node)               # "preorder": record on first arrival
        for nb in graph[node]:
            if nb not in seen:
                visit(nb)
    visit(start)
    return order
```

`visit` is a function defined *inside* `dfs`. A nested function can use the variables of the function around it, so
`visit` sees `order`, `seen` and `graph` without taking them as parameters, and every recursive call shares the same
`order` list and `seen` set. It only calls methods on them (`add`, `append`), which changes the objects themselves. It never
assigns `order = ...` or `seen = ...`, so it doesn't need the `nonlocal` declaration you'll meet on Day 10.

`visit(node)` marks the node, records it, and then, for each unvisited neighbour, *immediately* visits that neighbour, which
visits *its* neighbours, and so on. Only when a branch is exhausted does the function return, and the loop in the previous
call moves on to the next neighbour.

Same example from `a` → `a, b, d, c, e`.

Traced as a chain of calls:

```text
visit(a): record a
  visit(b): record b          (a's first neighbour)
    visit(d): record d        (b's unvisited neighbour)
    back in b: nothing left
  back in a: next neighbour c
  visit(c): record c
    visit(e): record e
```

At any moment, the chain of `visit` calls in progress is exactly the path from the start to the current node. The cycle
detection below relies on that.

(Iterative version: use a list as a stack, `append` and `pop()`. Note that the order differs from the recursive
version unless you push neighbours in reverse.)

**Connected components** (undirected): loop over all nodes; every node not yet seen starts a new BFS/DFS, and
everything that traversal reaches is one component.

A **connected component** is a group of nodes that can all reach each other: an island in the graph. Counting components
answers questions like "how many separate friend circles are there?".

---

## Detecting a cycle in a directed graph

A **cycle** is a path that leads back to where it started, following the edge directions: `a → b → c → a`. Detecting cycles
matters for dependencies: if task A needs B, B needs C, and C needs A, nothing can ever be done (drill 4).

You might think "if DFS reaches a node it has already seen, there's a cycle". In a directed graph that's wrong. Take the
diamond `a → b`, `a → c`, `b → d`, `c → d`. DFS reaches `d` from `b`, and later reaches it again from `c`, but there's no
cycle: you can't get from `d` back to `a`.

The correct test uses **three states** for each node:
- WHITE: not visited yet
- GREY: on the current recursion path (we're "inside" it)
- BLACK: completely finished

Reaching a **GREY** node = you came back to a node on your own path = **cycle**. Reaching a BLACK node is fine.

In the diamond, when `c` reaches `d`, `d` is already BLACK: it was finished while exploring `b`. So that's not a cycle. In
`a → b → a`, when `b` looks at `a`, `a` is still GREY (we're still inside `visit(a)`), so it's a cycle.

```python
def has_cycle(graph):
    state = {}                       # missing = white
    def visit(u):
        state[u] = "grey"
        for v in graph[u]:
            if state.get(v) == "grey":
                return True
            if v not in state and visit(v):
                return True
        state[u] = "black"
        return False
    return any(visit(u) for u in graph if u not in state)
```

- A node with no entry in `state` is white.
- On entering `visit(u)`, `u` becomes grey: "we're inside it".
- Meeting a grey neighbour means we've come back round to a node on our own path, which is a cycle.
- When all of `u`'s neighbours are done, `u` becomes black. If the code forgets this line, finished nodes stay grey forever,
  and the harmless diamond gets reported as a cycle.
- The last line starts a search from every node that hasn't been visited yet, because a cycle might not be reachable from
  the first node. `any(...)` stops as soon as one search finds a cycle.

---

## Complexity

BFS and DFS each visit every node and edge once: **O(V + E)**.

(V is the number of nodes, from *vertices*, and E is the number of edges. "O(V + E)" means the work grows in proportion to
the size of the graph. See drill 1 for big-O notation.)

## Where bugs hide
- `pop()` vs `popleft()` (stack vs queue): order and shortest paths break
- marking `seen` too late (when popping): nodes are enqueued several times (order/dupes); in cyclic graphs
  memory can explode
- nodes that only appear as edge targets never added to the dict → `KeyError`
- path reconstruction not reversed, or missing start/goal
- grid bounds `<=` instead of `<`; rows vs columns swapped (`grid[r][c]`, `len(grid)` rows, `len(grid[0])` cols)
- cycle detection with only a `seen` set (diamond false positive) or forgetting to mark BLACK

## Drill
`exam/graph_search.py` — 6 functions, 5 bugs, 15 tests. Timer: 30 minutes.
