# Drill 8 — Dynamic Programming II: LCS and Edit Distance

(Read Drill 7's introduction to DP first: state, base cases, transition, order, answer.)

## What these algorithms are for

This drill is about comparing two strings. Three questions come up constantly:
- **What do they have in common?** When you run `git diff`, it finds the longest sequence of lines the two versions of a file
  share. Those lines are shown as unchanged, and everything else as added or removed. That's the *longest common
  subsequence*.
- **How different are they?** A spell checker suggests the dictionary words that need the fewest single-letter changes to
  turn into what you typed. That number of changes is the *edit distance*.
- **What's the longest piece they share exactly?** That's the *longest common substring*, used in plagiarism detection and
  DNA analysis.

All three are solved with the same kind of two-dimensional DP table.

## The state: a pair of prefixes

A **prefix** of a string is a piece taken from its start: the prefixes of `"cat"` are `""`, `"c"`, `"ca"` and `"cat"`. In
Python, `a[:i]` is the prefix of length `i`.

Comparing two whole strings is hard. But comparing them **from the end, one character at a time**, breaks the problem into
the same question on shorter strings. Look at the last character of each. Either they're the same, and you can use that
match and deal with the rest, or they're different, and at least one of them has to be dealt with somehow. Either way, what
remains is a smaller pair of prefixes.

These are the DPs behind `diff`, `git`, spell checkers, DNA alignment and fuzzy search. The state is a **pair of
prefix lengths**: `dp[i][j]` describes `a[:i]` and `b[:j]`, so the table is `(len(a) + 1) × (len(b) + 1)`, where
row 0 and column 0 stand for the **empty prefix**. Inside the loops, the characters being compared are
**`a[i-1]` and `b[j-1]`** (the last character of each prefix) — the source of most off-by-one bugs.

Why `a[i-1]` and not `a[i]`? Because `dp[i][j]` is about the prefix of length `i`, and the last character of a prefix of
length `i` is at position `i - 1`. Row 0 is for the empty prefix, which has no characters at all.

---

## Longest Common Subsequence (LCS)

### What a subsequence is

A **subsequence** keeps the order but can skip characters: `"ace"` is a subsequence of `"abcde"`.
LCS of `"abcde"` and `"ace"` is `"ace"` (length 3).

In other words: cross out any characters you like, but don't rearrange the rest. `"aec"` is *not* a subsequence of
`"abcde"`, because in `"abcde"` the `c` comes before the `e`. The **longest common subsequence** of two strings is the longest
string that is a subsequence of both.

### The DP

- state: `dp[i][j]` = length of the LCS of `a[:i]` and `b[:j]`
- base: `dp[0][j] = dp[i][0] = 0` (empty prefix)
- transition:
  - if `a[i-1] == b[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1` (use this matching pair, **diagonal** + 1)
  - else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` (drop the last char of a, or of b)
- answer: `dp[len(a)][len(b)]`

The transition in words:
- **The last characters match.** Then they can be paired up as the last character of the common subsequence. The rest is
  the best common subsequence of the two prefixes *without* those characters, which is `dp[i-1][j-1]`, the cell diagonally
  up and to the left, plus 1 for this match. A match uses up one character from **each** string. That's why it must be the
  diagonal.
- **They don't match.** Then at least one of the two last characters isn't part of the common subsequence. So try dropping
  the last character of `a` (the cell above) or the last character of `b` (the cell to the left), and keep the better result.

The base case: a common subsequence with an empty string is empty, so the whole first row and column are 0.

### The filled table

For `a = "abcde"` (rows) and `b = "ace"` (columns):

```
        ""  a  c  e
   ""    0  0  0  0
   a     0  1  1  1
   b     0  1  1  1
   c     0  1  2  2
   d     0  1  2  2
   e     0  1  2  3
```

Check a few cells:
- Row `c`, column `c`: the characters match, so it's diagonal + 1 = `dp[2][1] + 1` = 1 + 1 = 2. (`"ac"` is common to `"abc"` and `"ac"`.)
- Row `d`, column `e`: no match, so it's max(above, left) = max(2, 2) = 2.
- The bottom-right cell is 3: the LCS has length 3.

### Recovering the subsequence itself

**Recovering the subsequence:** start at `(i, j) = (len(a), len(b))` and walk back:
- if `a[i-1] == b[j-1]`: that char is in the LCS, go diagonally (`i -= 1; j -= 1`)
- else go to the larger neighbour: up (`i -= 1`) if `dp[i-1][j] >= dp[i][j-1]`, else left (`j -= 1`)

You collect characters **backwards**, so reverse at the end. When there are several LCSs, the tie rule (`>=` vs `>`)
decides which one you get, and a spec will pin it down.

The table only holds *lengths*. To get the actual string, you retrace the decisions that produced the final number. On
the table above, starting at the bottom-right:

| Position (row, col) | Characters | Move | Collected |
|---|---|---|---|
| (e, e) | match | diagonal | e |
| (d, c) | d ≠ c; up = 2, left = 1 | up | e |
| (c, c) | match | diagonal | e c |
| (b, a) | b ≠ a; up = 1, left = 0 | up | e c |
| (a, a) | match | diagonal | e c a |

Reversed: `"ace"`.

When the cells above and to the left are equal, both directions lead to a valid answer, but possibly a *different* string.
For `"ab"` and `"ba"`, both `"a"` and `"b"` are longest common subsequences. The `>=` in the rule ("go up on ties") decides
which one comes out, and the tests will expect that exact one.

---

## Edit distance (Levenshtein)

### What it measures

The **edit distance** between two strings is the smallest number of single-character edits needed to turn one into the
other, where an edit is **inserting** a character, **deleting** one, or **substituting** one character for another. It's
named after the mathematician Levenshtein.

Minimum number of single-character **insertions, deletions, substitutions** to turn `a` into `b`.
`"kitten" → "sitting"` = 3 (k→s, e→i, insert g).

### The DP

- state: `dp[i][j]` = edit distance between `a[:i]` and `b[:j]`
- base: `dp[i][0] = i` (delete all i chars), `dp[0][j] = j` (insert all j chars). **Not 0!**
- transition:
  - if `a[i-1] == b[j-1]`: `dp[i][j] = dp[i-1][j-1]` (free)
  - else `dp[i][j] = 1 + min(dp[i-1][j]   (delete a[i-1]),
                              dp[i][j-1]   (insert b[j-1]),
                              dp[i-1][j-1] (substitute))`
- answer: `dp[len(a)][len(b)]`

The base cases: turning a prefix of length `i` into the empty string takes `i` deletions, and turning the empty string into
a prefix of length `j` takes `j` insertions. They're the first column and the first row of the table, and they are not 0.

The three options, for turning `a[:i]` into `b[:j]` when the last characters differ:
- **Delete** the last character of `a`, then turn `a[:i-1]` into `b[:j]`. That's the cell above.
- **Insert** `b`'s last character at the end, after turning `a[:i]` into `b[:j-1]`. That's the cell to the left.
- **Substitute** `a`'s last character with `b`'s, after turning `a[:i-1]` into `b[:j-1]`. That's the diagonal.

Each costs 1 edit plus the cost of the smaller problem, so we take the cheapest. When the last characters are the *same*,
nothing needs doing, so the diagonal is copied for free.

A small example: `"cat"` → `"cut"`. The `c`s match (free), `a` ≠ `u` (substitute, +1), and the `t`s match (free). Total: 1.

```python
def edit_distance(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1): dp[i][0] = i
    for j in range(len(b) + 1): dp[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[-1][-1]
```

The structure matches the recipe exactly: build the table, fill in the base row and column, then fill the rest in order
(row by row, left to right, so the cells above and to the left are always ready), and read the answer from the
bottom-right corner.

---

## Longest common substring (contiguous!)

### Substring vs. subsequence

A **substring** has no gaps: its characters must be **consecutive** in both strings. For `"abcde"` and `"ace"`, the longest
common *subsequence* is `"ace"` (3 characters), but the longest common *substring* is just `"a"` (or `"c"`, or `"e"`), because
no two consecutive characters of `"ace"` are also consecutive in `"abcde"`.

### The DP

Different from subsequence: the characters must be **consecutive**. State `dp[i][j]` = length of the common
substring **ending exactly at** `a[i-1]` and `b[j-1]`: `dp[i-1][j-1] + 1` on a match, **0** otherwise (the run is
broken). Track the best cell while filling. To return the *first* longest one, only replace the best on a strictly
longer length (`>`, not `>=`).

What changes compared with LCS, and why:
- **The state** is "the length of the common run that ends *exactly here*". A common substring is a run of matching
  characters, and this tracks how long the current run is.
- **On a mismatch, the cell is 0**, not the max of the neighbours. A substring can't skip characters, so a mismatch ends the
  run.
- **The answer isn't in the bottom-right corner.** The longest run could end anywhere. So while filling the table, the code
  remembers the best length seen so far and where it ended (`best_end`). At the end, the substring is
  `a[best_end - best_len : best_end]`.

---

## Complexity

All three: O(len(a) × len(b)) time and space.

In words: the work and memory grow with the size of the table, one cell per pair of prefix lengths.

## Where bugs hide
- `a[i]` vs `a[i-1]` inside the loops; table size `len(a)` vs `len(a) + 1`
- match transition using `dp[i-1][j]` or `dp[i][j-1]` instead of the diagonal `dp[i-1][j-1]`
- base cases of edit distance set to 0
- a missing option in the `min` (e.g. no substitution)
- tie-breaking in reconstruction (`>=` vs `>`), forgetting to reverse
- substring vs subsequence: not resetting to 0 on mismatch

## Drill
`exam/sequences.py` — 4 functions, 5 bugs, 15 tests. Timer: 30 minutes.
Tip: print the table for a 3×3 example and compare with one you fill by hand.
