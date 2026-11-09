# Drill 4 — Topological Sort

## The problem

You have a set of tasks, and some tasks must be done before others:
- put on socks before shoes;
- compile the code before linking it;
- take Calculus I before Calculus II.

The question is: **in what order can you do all the tasks so that nothing is done before something it needs?** Such an
order is called a **topological order**, and finding one is called **topological sorting**.

As a graph (drill 2), each task is a node, and each requirement is a **directed** edge: `a → b` means *a must come before
b*. A topological order is a list of all the nodes in which every edge points forward, from earlier in the list to later.

Usually there are many valid orders. In the morning, socks-then-shirt and shirt-then-socks both work. That's why exam specs
add a rule for choosing, like "when several tasks are available, take the alphabetically smallest", so the tests can expect
one exact answer.

### When it's impossible

A topological order exists **if and only if the graph has no cycle**. If A needs B, B needs C, and C needs A, none of them
can go first. A directed graph without cycles has a name you'll see in specs: a **DAG**, short for *directed acyclic graph*.

### Where it's used

Build systems (which files to compile first), package managers (which libraries to install first), spreadsheets (which cells
to recalculate first), course planning and project scheduling.

---

## Kahn's algorithm

The algorithm is exactly what you'd do by hand. Start with the tasks that need nothing. Every time you finish a task, cross
it off the requirement lists of the tasks waiting for it. Any task whose list becomes empty is now ready.

To make "how many unmet requirements does this task have?" quick to answer, we keep a count per node called its
**in-degree**: the number of edges pointing *into* it.

1. Compute the in-degree of every node.
2. Every node with in-degree 0 is *available* (nothing has to come before it).
3. Repeatedly take an available node, append it to the order, and "remove" its outgoing edges: decrement the
   in-degree of each successor; any successor that reaches 0 becomes available.
4. If at the end the order doesn't contain **all** nodes, the leftover nodes are stuck in (or behind) a cycle.

(A **successor** of a node is a node its edges point to, i.e. a task that was waiting for it.)

Worked example — edges `a→c, b→c, c→d, b→d`:
```
in-degree: a0 b0 c2 d2        available {a, b}
take a: c -> 1                 available {b}
take b: c -> 0, d -> 1         available {c}
take c: d -> 0                 available {d}
take d                         order: a b c d
```

In words: `c` needs both `a` and `b`, so its in-degree is 2. `d` needs `c` and `b`, so its in-degree is also 2. Only `a` and
`b` need nothing. Taking `a` satisfies one of `c`'s two requirements. Taking `b` satisfies `c`'s other requirement and one of
`d`'s. Now `c` is ready. Taking `c` makes `d` ready.

### How step 4 detects cycles

Look at what happens to nodes in a cycle like `x → y → z → x`. Each of them has an incoming edge from another node in the
same cycle. For `x` to become available, `z` must be taken first, which needs `y` first, which needs `x` first. None of
them can ever be the first to reach in-degree 0, so none is ever taken, and neither is anything that depends on them. So
the algorithm doesn't need a separate cycle search: if the final order is shorter than the number of nodes, there's a cycle.

### Choosing among available nodes

**Deterministic order:** when several nodes are available, a spec usually says which to take — e.g. "the
smallest". Use a heap (`heapq`) of available nodes: always `heappop` the smallest. (`list.pop()` takes the last one
added — a common bug.)

(`heapq` is explained in drill 3: it always gives you the smallest item.)

---

## The template

```python
import heapq
def topo_sort(nodes, edges):
    succ = {n: set() for n in nodes}
    for a, b in edges:
        succ.setdefault(a, set()).add(b)       # sets: duplicate edges ignored
        succ.setdefault(b, set())
    indeg = {n: 0 for n in succ}
    for a in succ:
        for b in succ[a]:
            indeg[b] += 1                     # count from the de-duplicated sets!
    heap = [n for n in succ if indeg[n] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        n = heapq.heappop(heap)
        order.append(n)
        for m in succ[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                heapq.heappush(heap, m)
    if len(order) != len(succ):               # compare with ALL nodes
        raise ValueError("cycle")
    return order
```
Complexity: O((V + E) log V) with the heap, O(V + E) with a plain queue.

It has four parts:
1. **Build the graph.** `succ` maps each node to the *set* of its successors. A set means that if the same edge `(a, b)`
   appears twice in the input, it's stored once. Nodes that appear only in edges, not in the `nodes` list, are added too.
2. **Count in-degrees from `succ`**, not from the raw `edges` list. Here's why that matters. If `(a, b)` appears twice in
   `edges`, counting from the raw list gives `b` an in-degree of 2. But `succ[a]` holds `b` only once, so when `a` is taken,
   `b`'s count goes down by only 1. It never reaches 0, `b` is never taken, and the algorithm wrongly reports a cycle.
3. **The main loop.** `heapq.heapify(heap)` arranges the starting list into heap order. Then: take the smallest available node,
   append it to the order, decrease its successors' counts, and add any successor that reaches 0.
4. **The cycle check**, comparing against the full set of nodes `succ`. Comparing against the input `nodes` list would miss
   nodes that appeared only in edges.

---

## Two more things computed along a topological order

### Levels: what can run in parallel

**Levels (what can run in parallel):** level 0 = nodes with in-degree 0; level k+1 = nodes whose in-degree drops
to 0 after removing level k. Process a whole level at a time.

This answers: "if I had unlimited workers, which tasks could run at the same time, and in how many rounds would everything
be done?". It's the same algorithm, but instead of taking available nodes one at a time, you take *all* currently available
nodes together as one level. Then you collect every node they make available as the next level. In the worked example
above, the levels are `[a, b]`, then `[c]`, then `[d]`: three rounds.

### The longest chain: the critical path

**Longest chain (critical path):** process nodes in topological order; `longest[n]` = number of nodes in the longest
chain *ending* at n. Base case: every node alone is a chain of **1**. For each edge `n → m`:
`longest[m] = max(longest[m], longest[n] + 1)`. Answer: `max(longest.values())` (0 for an empty graph).
This is the simplest example of **dynamic programming on a DAG**: the topological order guarantees `longest[n]` is
final before it's used.

A **chain** is a sequence of tasks where each one needs the one before it. The longest chain is the project's **critical
path**: even with unlimited workers, the project can't finish in fewer rounds than this.

Traced on the worked example (order `a b c d`):

| Process | Update | longest |
|---|---|---|
| start | every node alone is a chain of 1 | a1 b1 c1 d1 |
| a | edge a→c: c = max(1, 1 + 1) = 2 | a1 b1 c2 d1 |
| b | b→c: c = max(2, 2) = 2; b→d: d = max(1, 2) = 2 | a1 b1 c2 d2 |
| c | c→d: d = max(2, 2 + 1) = 3 | a1 b1 c2 d3 |

The answer is 3: for example `a → c → d`.

Why process in topological order? Because when we use `longest[n]` to update its successors, it must already be final, and
that means all of `n`'s own predecessors have been processed. The topological order guarantees exactly that. This idea, of
computing each answer from answers already computed in an order that guarantees they're ready, is called **dynamic
programming**. Drill 7 introduces it properly.

---

## Edge direction

**Edge direction:** "`b` depends on `a`" means `a` must come first: edge **`a → b`** (dependency → dependent). Flipping this is one of
the most common bugs; check with the smallest example.

Data often arrives as "X depends on Y" or "X requires Y". It's easy to turn that into the edge `X → Y` when it should be
`Y → X`. With the edges reversed, the algorithm still runs and still returns a valid-looking order, just backwards. So check
the direction on the smallest test: with just "b depends on a", the answer must be `[a, b]`.

## Where bugs hide
- edge direction reversed when converting "depends on" data
- in-degree counted from the raw edge list while successors are a set (duplicate edges → node never reaches 0 →
  false "cycle")
- picking the wrong available node (`pop()` instead of `heappop`, or sorting in the wrong direction)
- the cycle check comparing with the input `nodes` list instead of all nodes (including nodes only seen in edges)
- DP base case 0 instead of 1

## Drill
`exam/toposort.py` — 4 functions, 5 bugs, 15 tests. Timer: 30 minutes.
