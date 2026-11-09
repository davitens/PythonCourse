# Drill 5 — Answer key (SPOILERS)

| # | Where | Broken | Fixed | How to find it fast |
|---|---|---|---|---|
| 1 | `union` | no `if ra == rb: return False` guard | add it | `test_union_same_set`: `union` of already-joined elements returns True and decrements `count`. |
| 2 | `union` | `size[ra] += size[ra]` | `+= size[rb]` | Wrong variable (catalog B10). `size_of` gives doubled sizes. |
| 3 | `union` | `if size[ra] > size[rb]` | `<` (swap so the bigger root stays root) | `test_union_by_size_root`: the big set {a, b} gets attached under the singleton c. |
| 4 | `add` | no `if x not in self.parent` check | add it | `add(1)` twice counts 2 sets; re-adding would also detach an element from its set. |
| 5 | `kruskal` | `sorted(edges)` (sorts by u) | `key=lambda e: (e[2], e[0], e[1])` | Edges are `(u, v, weight)`: plain tuple sorting uses u first. Total 8 instead of 7 on unsorted input. |

Also worth knowing (not planted here because it can make tests hang): a `find` that returns a non-root node lets
`union` link a root under its own descendant, creating a parent cycle — `find` then loops forever.
