# Drill 2 — Answer key (SPOILERS)

| # | Function | Broken | Fixed | How to find it fast |
|---|---|---|---|---|
| 1 | `build_graph` | sink nodes only added when undirected | always `graph.setdefault(v, set())` | `KeyError: 'b'` in traversal tests of directed graphs; `test_directed_includes_sinks` shows `b`/`c` missing. |
| 2 | `bfs_order` | `queue.pop()` (stack) | `queue.popleft()` (FIFO) | Order comes out depth-first-ish; BFS must use a queue. |
| 3 | `shortest_path` | returns `path` | `path[::-1]` | Output is exactly the expected list reversed. |
| 4 | `grid_distance` | missing `0 <= nc` | `0 <= nc < cols` | Python negative indices **wrap around**: column -1 is the last column, so no IndexError at first — the search "teleports" and finally crashes further left. Always check both bounds. |
| 5 | `has_cycle` | never marks nodes black | `state[u] = "black"` before returning | The diamond `a→b→d, a→c→d` is reported as a cycle: `d` is still grey when reached the second time. |
