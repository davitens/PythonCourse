# Drill 8 — Answer key (SPOILERS)

| # | Function | Broken | Fixed | How to find it fast |
|---|---|---|---|---|
| 1 | `lcs_table` | match uses `dp[i - 1][j] + 1` | diagonal `dp[i - 1][j - 1] + 1` | `"aa"` vs `"a"` gives 2: the same `b` char is matched twice. A match must consume one char of **each** string. |
| 2 | `lcs` | `dp[i - 1][j] > dp[i][j - 1]` | `>=` | Spec says move UP on ties; `lcs("ab", "ba")` returns `"b"` instead of `"a"`. |
| 3 | `edit_distance` | base `dp[i][0] = 0` | `= i` | Turning `"abc"` into `""` costs 3 deletions; the symmetric test also fails (`dp[0][j]` is still right). |
| 4 | `edit_distance` | substitution missing from `min` | add `dp[i - 1][j - 1]` | `"cat"` → `"cut"` gives 2 (delete + insert) instead of 1. |
| 5 | `longest_common_substring` | `>= best_len` | `>` | Returns the **last** longest substring (`"cd"`) instead of the first (`"ab"`). |
