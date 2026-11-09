# Drill 4 — Answer key (SPOILERS)

| # | Function | Broken | Fixed | How to find it fast |
|---|---|---|---|---|
| 1 | `_graph` | in-degree counted from the raw `edges` | count from the de-duplicated `succ` sets | `test_duplicate_edges` raises "cycle": `b` has in-degree 2 but only one successor edge decrements it. |
| 2 | `topo_sort` | `heap.pop()` | `heapq.heappop(heap)` | Spec says "take the SMALLEST"; `[2, 3, 1, 4]` comes out starting with 4. |
| 3 | `topo_sort` | `len(order) != len(nodes)` | `len(succ)` (all nodes) | `topo_sort([], [("x", "y")])` reports a cycle: the input list omits edge-only nodes. |
| 4 | `build_order` | `(task, dep)` | `(dep, task)` | Dependencies come out *after* their dependents; check with `{"b": ["a"], "a": []}`. |
| 5 | `longest_chain` | base case 0 | 1 (a single node is a chain of 1) | `longest_chain(["solo"], [])` gives 0, and every answer is one too small. |
