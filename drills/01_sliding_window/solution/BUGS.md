# Drill 1 — Answer key (SPOILERS)

| # | Function | Broken | Fixed | How to find it fast |
|---|---|---|---|---|
| 1 | `max_sum_window` | `nums[i - k + 1]` leaves | `nums[i - k]` | Hand-run k=3 on `[2,1,5,1,3,2]`: when index 3 enters, index 0 leaves. |
| 2 | `longest_unique_substring` | `if c in last:` | `if c in last and last[c] >= left:` | `"abba"`: on the last `a`, `last['a']=0` is outside the window, but `left` jumps back to 1. |
| 3 | `min_subarray_len` | `while total > target` | `>=` | Spec says "sum **>=** target"; `[1,4,4], 4` must give 1. |
| 4 | `window_max` | `dq[0] < i - k` | `<=` | `[9,1,1,1], k=2`: at i=2 the window is indices 1..2, index 0 must expire (0 <= 2-2). |
| 5 | `anagram_starts` | `range(k, len(s) - 1)` | `range(k, len(s))` | The match at the very end (`"xxab"`) is missed — "last window" bug (catalog A5). |
