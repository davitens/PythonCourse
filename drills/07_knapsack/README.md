# Drill 7 — Dynamic Programming I: Knapsack and Coin Change

## What is dynamic programming (DP)?

**Dynamic programming** is a technique for problems whose answer can be built from the answers to **smaller versions of the
same problem**, where those smaller problems come up again and again. Instead of solving the same smaller problem many
times, you solve each one once, **store** its answer in a table, and look it up when you need it again.

The name is historical and not very descriptive. A better mental label would be "fill in a table of answers to smaller
questions, in the right order".

### A first example, in plain words

You need to pay 11 euros using as few coins as possible, and the coins available are 1, 2 and 5 euros. How many coins do
you need?

Trying every combination of coins gets out of hand quickly. But here's a useful observation: **whatever the best solution
is, its last coin is either a 1, a 2 or a 5.**
- If the last coin is a 1, the rest of the coins pay 10 euros, using as few coins as possible for 10.
- If it's a 2, the rest pay 9.
- If it's a 5, the rest pay 6.

So: *fewest coins for 11 = 1 + the smallest of (fewest for 10, fewest for 9, fewest for 6)*.

Those are the same question again, for smaller amounts. And they keep coming back: "fewest coins for 6" is needed by 7
(7 − 1), 8 (8 − 2) and 11 (11 − 5). So we work **from the bottom up**. Compute the answer for 0, then 1, then 2, and so on up
to 11, storing each one. Every new answer is then just a `min` over three numbers we've already stored.

```text
amount:        0  1  2  3  4  5  6  7  8  9  10  11
fewest coins:  0  1  1  2  2  1  2  2  3  3   2   3
```

Check a couple. For 4: the options are 1 + fewest(3) = 3, or 1 + fewest(2) = 2 (the 5 is too big). So 2 coins: 2 + 2. For
11: 1 + min(fewest(10), fewest(9), fewest(6)) = 1 + min(2, 3, 2) = 3 coins, for example 5 + 5 + 1.

### When does DP apply?

Two conditions make a problem suitable:
- **The best answer is built from best answers to smaller problems.** Above, the best way to pay 11 contains the best way to
  pay 10, 9 or 6. This is called *optimal substructure*.
- **The same smaller problems are needed many times.** Without storing answers, a simple recursive solution would recompute
  them over and over, and the number of calls would explode as the input grows. This is called *overlapping sub-problems*.

DP is used in route and budget optimisation, scheduling, comparing texts (`diff`, spell checkers, DNA analysis, drill 8),
and many puzzle-style questions. In exam code you'll recognise it by a **table**, a list or a list of lists, filled by
loops, where each cell is computed from cells filled earlier.

### The recipe

Every DP solution, simple or complicated, is built in the same five steps. When you're debugging DP code, check them one by
one:

1. **Define the state**: what does `dp[...]` mean, in one sentence? (This is 80% of the work.)
2. **Base cases**: the smallest states, whose answer is obvious.
3. **Transition**: how `dp[state]` is computed from smaller states.
4. **Order**: fill the table so smaller states are ready before they're needed.
5. **Answer**: which cell holds the final result?

For the coin example: (1) `dp[a]` = fewest coins that pay exactly `a`; (2) `dp[0] = 0`, since paying nothing takes no coins;
(3) `dp[a] = 1 + min(dp[a - coin])` over the coins that fit; (4) `a` from 1 upwards; (5) `dp[11]`.

### The warm-up: Fibonacci

Warm-up — Fibonacci: `dp[i]` = i-th Fibonacci number; base `dp[0]=0, dp[1]=1`; transition
`dp[i] = dp[i-1] + dp[i-2]`; order: i increasing; answer `dp[n]`. Without the table, the naive recursion recomputes
the same values exponentially many times.

(The Fibonacci numbers are 0, 1, 1, 2, 3, 5, 8, 13, ...: each one is the sum of the previous two.)

```python
def fib(n):
    dp = [0] * (n + 1)          # one cell per state 0..n
    if n >= 1:
        dp[1] = 1               # base cases (dp[0] = 0 already)
    for i in range(2, n + 1):   # order: smaller i first
        dp[i] = dp[i - 1] + dp[i - 2]   # transition
    return dp[n]                # answer
```

Each part of the code is one step of the recipe, and each is a place where a bug can hide:
- **Is the table the right size?** States go from 0 to n, which is `n + 1` cells. With `[0] * n`, `dp[n]` doesn't exist.
- **Are the base cases right?**
- **Does the transition match the state's meaning?**
- **Does the loop reach the last state?** `range(2, n + 1)`, not `range(2, n)`.
- **Is the answer read from the right cell?**

---

## The 0/1 knapsack

### The problem

You're packing a bag that can carry at most a certain weight, its **capacity**. You have some items, each with a **weight**
and a **value**. Which items should you take to get the most total value without going over the capacity? Each item can
be taken **at most once**: you either take it (1) or leave it (0). That's where the name "0/1 knapsack" comes from. (A
knapsack is a backpack.)

### Why a simple rule doesn't work

The natural idea is to be *greedy*: take the item with the best value per kilo first, then the next best, and so on, while
they fit. It fails. Take items `(weight 3, value 4)`, `(weight 3, value 4)`, `(weight 4, value 6)` and capacity 6.

The 4-kilo item has the best value per kilo (1.5), so greedy takes it first. Now only 2 kilos are left, neither 3-kilo item
fits, and the total is 6. But taking the two 3-kilo items gives 8.

You really do have to consider combinations. DP does that efficiently, by deciding item by item, for every possible
remaining capacity at once.

### The DP

1. **State:** `dp[i][c]` = best value using only the **first i items** with capacity **c**.
2. **Base:** `dp[0][c] = 0` (no items → value 0) for every c.
3. **Transition** for item i−1 (weight w, value v):
   - skip it: `dp[i-1][c]`
   - take it (only if `w <= c`): `dp[i-1][c-w] + v` — note **`i-1`**: the remaining capacity is filled with the
     *previous* items, so this item can't be used twice.
   - `dp[i][c] = max(skip, take)`
4. **Order:** i from 1 to n, c from 0 to capacity **inclusive** (`range(capacity + 1)`).
5. **Answer:** `dp[n][capacity]`.

The transition in plain words: when you consider an item with a given capacity left, there are only two choices.
- **Skip it.** Then the best you can do is the best of the earlier items, with the same capacity.
- **Take it** (if it fits). Then you get its value, plus the best of the earlier items in the capacity *that's left*
  after packing it.

Take whichever is bigger.

A note on numbering: row `i` of the table means "the first `i` items", so row 0 is "no items" and row 1 uses the item at
position 0 in the list. That's why the item considered in row `i` is `items[i - 1]`. This shift by one is a frequent source of
off-by-one bugs.

### A filled table

Example: items `(w=1, v=1), (w=3, v=4), (w=4, v=5)`, capacity 7:
```
        c: 0 1 2 3 4 5 6 7
i=0        0 0 0 0 0 0 0 0
i=1 (1,1)  0 1 1 1 1 1 1 1
i=2 (3,4)  0 1 1 4 5 5 5 5
i=3 (4,5)  0 1 1 4 5 6 6 9      <- dp[3][7] = 9 (items 1 and 2: weight 7, value 9)
```

Check a few cells yourself:
- `dp[2][4]` considers the item `(3, 4)` with capacity 4. Skipping gives `dp[1][4] = 1`. Taking gives
  `dp[1][4 - 3] + 4 = dp[1][1] + 4 = 5`. The max is 5.
- `dp[3][7]` considers `(4, 5)` with capacity 7. Skipping gives `dp[2][7] = 5`. Taking gives `dp[2][3] + 5 = 4 + 5 = 9`. The max is 9.

When a DP test fails, filling a few cells by hand like this and comparing with the code's table is the fastest way to see
which part of the transition is wrong.

### Which items were taken?

**Which items were taken? (reconstruction)** Walk back from `dp[n][capacity]`: for i = n..1, if
`dp[i][c] != dp[i-1][c]`, item i−1 was taken: record it and **subtract its weight** from c. (In the example:
i=3: 9 ≠ 5 → take item 2, c=3; i=2: 4 ≠ 1 → take item 1, c=0; i=1: 0 == 0 → skip.)

The table only holds best *values*. To find out *which* items produced the best value, you retrace the decisions. If a
cell's value differs from the cell directly above it, the item of that row must have been taken (skipping it would have
given the value above). After taking an item, the remaining capacity shrinks by its weight. If the code forgets to subtract
it, later decisions are read from the wrong column.

### In code

```python
def knapsack(items, capacity):
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]   # NOT [[0]*(cap+1)]*(n+1) - shared rows!
    for i in range(1, n + 1):
        w, v = items[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if w <= c:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)
    return dp[n][capacity]
```

- The table has `n + 1` rows (0 to n items) and `capacity + 1` columns (0 to capacity). It's built with a comprehension, so
  that each row is a separate list (the aliasing trap from Day 1).
- For each row, `w, v` are the weight and value of that row's item.
- Each cell starts as "skip" (the value above), then is replaced by "take" if the item fits and taking is better.

### Unbounded knapsack: items you can take many times

Each item can be used **any number of times**. Then "take" uses the **same row**: `dp[i][c - w] + v`, or with a
1-D table: `best[c] = max(best[c], best[c - w] + v)` iterating c **upwards**. Mixing these two up (using `dp[i]`
instead of `dp[i-1]`) turns a 0/1 knapsack into an unbounded one — a classic planted bug.

Why does the row decide it? The cell `dp[i - 1][c - w]` comes from the row *before* this item was available, so it can't
contain the item. Adding the item once gives "used at most once". The cell `dp[i][c - w]` is in *this* item's row, so it may
already include the item, and adding it again means "used two or more times".

---

## Coin change

### The fewest coins

This is the example from the beginning of this document, written as code:
- state: `dp[a]` = fewest coins summing to a; **base `dp[0] = 0`**; everything else starts at infinity;
- transition: `dp[a] = min(dp[a - coin] + 1)` over coins with `coin <= a`;
- answer: `dp[amount]`, or −1 if still infinity.

```python
INF = float("inf")
dp = [0] + [INF] * amount          # dp[0] = 0: zero coins make amount 0
for a in range(1, amount + 1):
    for coin in coins:
        if coin <= a and dp[a - coin] + 1 < dp[a]:
            dp[a] = dp[a - coin] + 1
return -1 if dp[amount] == INF else dp[amount]
```

`float("inf")` is a special float meaning "infinity". It's bigger than every number, so any real answer beats it in a `min`.
Here it means "impossible so far". With coins `[2]`, every odd amount stays at infinity, because you can't pay 3 with 2-euro
coins.

The base case `dp[0] = 0` is what everything grows from. If `dp[0]` were also infinity, then `dp[a - coin] + 1` would always be
infinity, and every amount would be reported as impossible. A wrong base case in DP tends to break *every* answer at once.

### Counting the ways

A different question with the same coins: **in how many different ways** can you pay an amount? Here, `1 + 2` and `2 + 1`
count as the *same* way, because they use the same coins.

**Number of ways** to make `amount` (order doesn't matter: 1+2 and 2+1 are the same way):
- state: `ways[a]`; **base `ways[0] = 1`** (one way to make 0: use nothing);
- loop **coins in the outer loop**, amounts in the inner loop:
```python
ways = [1] + [0] * amount
for coin in coins:                  # outer: coins
    for a in range(coin, amount + 1):
        ways[a] += ways[a - coin]
```

Why is `ways[0] = 1`? There is exactly one way to pay nothing: use no coins. And it's needed. When a coin exactly pays an
amount (coin 2 for amount 2), that way is counted through `ways[2 - 2] = ways[0]`.

If you swap the loops (amounts outside, coins inside) you count **ordered** sequences (1+2 and 2+1 twice) — a
different problem. Classic subtle bug: the code runs, gives bigger numbers.

Why the loop order makes the difference:
- **Coins in the outer loop.** First we process coin 1 completely: `ways` now counts the ways using only 1s. Then coin 2:
  `ways` now counts the ways using 1s and 2s. Every combination gets built in one fixed order (all its 1s, then all its 2s),
  so it's counted exactly once.
- **Amounts in the outer loop.** For each amount, every coin is tried as "the last coin". So `1 + 2` (last coin 2) and `2 + 1`
  (last coin 1) are both counted.

Check with coins `[1, 2]` and amount 3. The correct answer is 2 (1+1+1 and 1+2). The swapped version gives 3.

---

## Where bugs hide
- table size / loop bound `capacity` vs `capacity + 1`
- `dp[i][...]` vs `dp[i-1][...]` (0/1 vs unbounded)
- base cases: `dp[0] = 0` for min-coins, `ways[0] = 1` for counting
- reconstruction: forgetting to subtract the weight; returning indices in the wrong order
- loop order in counting problems
- `[[0] * m] * n` aliasing rows

## Drill
`exam/knapsack.py` — 4 functions, 5 bugs, 15 tests. Timer: 30 minutes.
Tip: for a failing test, print the DP table for the small example and compare with the table above.
