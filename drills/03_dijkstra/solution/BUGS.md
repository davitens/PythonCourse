# Drill 3 — Answer key (SPOILERS)

| # | Function | Broken | Fixed | How to find it fast |
|---|---|---|---|---|
| 1 | `dijkstra` | `validate(graph)` never called | call it first | `test_negative_weight`: `validate` alone works, `dijkstra` doesn't raise → the call is missing. |
| 2 | `dijkstra` | `heap.pop()` | `heapq.heappop(heap)` | A heap list isn't sorted; `pop()` takes the last element. `TRAP` finalizes `b` with cost 4 too early. |
| 3 | `dijkstra` | `nd <= dist[v]` | `nd < dist[v]` | Spec: "only a strictly cheaper path replaces"; `test_tie_keeps_first_found` gets `prev["t"] == "b"`. |
| 4 | `shortest_path` | `while prev[path[-1]] != source` | `while path[-1] != source` | Path lacks the source; `source == target` raises `KeyError` (the source has no `prev`). |
| 5 | `within` | `d < max_cost` | `<=` | Spec says "<= max_cost"; budget 0 must still include the source. |
