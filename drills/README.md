# Algorithm Bug-Hunt Drills

Eight classic algorithms, each as a **~100-line implementation with exactly 5 hidden bugs** and a
**15-test suite**. This is the core of the exam skill: someone else's algorithm code, a spec, failing
tests, and you.

Each folder contains:

| File | What |
|---|---|
| `README.md` | **Theory**: what the algorithm does, a worked example by hand, a clean Python template, and the classic places bugs hide. Read it *before* the drill. |
| `exam/<name>.py` | The broken implementation. Its docstrings are the spec. |
| `exam/test_<name>.py` | 15 tests. |
| `solution/<name>.py` | Reference implementation (don't open during the drill). |
| `solution/BUGS.md` | Answer key: the 5 bugs, and what would have led you to each one. |

| # | Folder | Algorithm | Difficulty |
|---|---|---|---|
| 1 | `01_sliding_window` | Sliding window / two pointers | ★☆☆ |
| 2 | `02_bfs_dfs` | Graph traversal: BFS, DFS, shortest path in grids, cycle detection | ★★☆ |
| 3 | `03_dijkstra` | Weighted shortest paths with a heap (`heapq`) | ★★☆ |
| 4 | `04_toposort` | Topological sort (Kahn's algorithm), dependency levels, longest chain | ★★☆ |
| 5 | `05_union_find` | Disjoint sets (union by size + path compression), Kruskal's MST | ★★☆ |
| 6 | `06_lru_cache` | LRU cache with a hash map + doubly linked list | ★★★ |
| 7 | `07_knapsack` | Dynamic programming: 0/1 knapsack, coin change | ★★★ |
| 8 | `08_lcs` | Dynamic programming on two strings: LCS, edit distance | ★★★ |

## The routine (one drill per evening, ~45–60 min)

1. **Theory (15–20 min).** Read the folder's `README.md`. Do the worked example on paper yourself.
2. **Drill (30 min timer).** Keep a pristine copy first, then go:
   ```bash
   cd drills/03_dijkstra
   cp exam/dijkstra.py exam/dijkstra.original.py
   cd exam && python -m unittest 2>&1 | tail -3
   ```
   (or from the course root: `python run.py d3`). Plain editor, no AI, no autocomplete if you can manage it.
   Use the Day 6 workflow: read the spec, run the tests, start with the lowest-level function.
3. **Review (10 min).** Read `solution/BUGS.md`. For every bug you missed: *which test pointed at it, and
   what would have found it faster?* Add it to your bug journal.

Suggested schedule: fit drills in **after** the day's main work. Drills 1–2 from day 3, one or two per day after that.
Drills 6–8 are the hardest; do them after Day 7 (bug catalog).

## More rounds after these
Once you've used up the 8 drills, keep going with the same format: ask an AI (outside the exam!) for
*"a ~100-line Python implementation of X with a 15-test unittest suite, then introduce 5 subtle bugs (off-by-one,
wrong comparison, mutation, wrong base case, wrong tie-break). Give me only the buggy code and the tests."*
Fix it by hand, then ask for the bug list. Or re-do these drills a week later from the `.original.py` copies.
