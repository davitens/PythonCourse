# Drill 7 — Answer key (SPOILERS)

| # | Function | Broken | Fixed | How to find it fast |
|---|---|---|---|---|
| 1 | `knapsack_01` | `range(capacity)` | `range(capacity + 1)` | The answer cell `dp[n][capacity]` is never filled → value 0 even for `[(5, 10)], 5`. |
| 2 | `knapsack_01` | `dp[i][c - w]` | `dp[i - 1][c - w]` | Same row = item reusable = unbounded knapsack. `[(1, 10)], 5` gives 50 instead of 10. |
| 3 | `knapsack_01` | weight not subtracted in reconstruction | `c -= items[i - 1][0]` | `chosen` is inconsistent with `value` (random test checks `sum(values) == best`). |
| 4 | `min_coins` | no base case `dp[0] = 0` | `[0] + [INF] * amount` | Everything is built on `dp[0]`; with INF there, every answer is -1. |
| 5 | `count_ways` | amounts outer, coins inner | coins outer | Counts ordered sequences: `[1, 2], 3` gives 3 (1+1+1, 1+2, 2+1) instead of 2. |
