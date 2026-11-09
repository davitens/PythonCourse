# Drill 1 — Sliding Window

## The kind of problem it solves

Many questions are about **consecutive** stretches of a list or a string:
- "Over 7 consecutive days, what's the highest total rainfall?"
- "What's the longest piece of this text that has no repeated letter?"
- "What's the shortest run of consecutive purchases that adds up to at least 100 euros?"

A stretch of consecutive items is called a **window**. In a list it's also called a *subarray*, and in a string a
*substring*. `[5, 1, 3]` is a window of `[2, 1, 5, 1, 3, 2]`, but `[2, 5, 3]` is not, because it skips items.

### The slow way, and why it's slow

The obvious approach is to look at every possible window: every start position combined with every end position, and
compute its sum (or whatever you need) from scratch. For a list of 1,000 items there are about 500,000 windows, and
summing each one means adding up to 1,000 numbers. That's hundreds of millions of operations for a modest input.

Programmers describe this growth with **big-O notation**. "O(n)" means the work grows in proportion to the input size `n`:
twice the input, twice the work. "O(n²)" means it grows with the *square*: twice the input, four times the work. The slow
approach is O(n²) windows, each costing up to O(n), so O(n³) in total.

### The idea of a sliding window

Look at two neighbouring windows of size 3:

```text
[2, 1, 5, 1, 3, 2]
 ^^^^^^^              window A = [2, 1, 5]
    ^^^^^^^           window B = [1, 5, 1]
```

They share two of their three items. To go from A to B, exactly one item **left** (the `2` at the front) and one item
**entered** (the `1` at the back). So instead of re-adding everything, you can take A's sum, subtract what left and add
what entered. It's like a frame sliding along the list one step at a time.

That's the whole technique: **keep a running summary of the current window (a sum, a dict of counts, a set...), and
update it with only what enters and what leaves.** Each item enters once and leaves once, so the total work is O(n).

### Where you'll meet it

Moving averages of prices or sensor readings, "best week" statistics, rate limiters ("at most 100 requests in any
60-second window"), streaming data, and many text-search problems. In exam code you'll recognise it when you see two
positions (often called `left` and `right`, or `i` and `i - k`) that **only ever move forward**, and a variable that's
*updated* each step rather than recomputed.

### Why bugs here are easy to plant and easy to spot

The window is only correct if both updates are exactly right: the correct item leaves, and the correct item enters. If
either one is off by a position, *every* window after that point is wrong. So a typical failing test shows correct values
at the beginning and wrong values from some point on. That's a strong hint that one of the two updates is wrong.

---

## 1. Fixed-size windows

When the window size `k` is given, the recipe is: compute the first window directly, then slide it one step at a time,
adding the item that enters and removing the one that leaves.

```
nums = [2, 1, 5, 1, 3, 2], k = 3
window [2 1 5] sum 8
slide: +1 (enters, index 3) -2 (leaves, index 0)   -> [1 5 1] sum 7
slide: +3 (index 4)         -1 (index 1)           -> [5 1 3] sum 9   <- max
slide: +2 (index 5)         -5 (index 2)           -> [1 3 2] sum 6
```

### Which item leaves?

When the element at index `i` enters, the one leaving is at index **`i - k`** (the most common bug is
`i - k + 1`).

Let's work it out rather than memorise it. After the item at position `i` enters, the window ends at `i` and holds `k`
items, so it covers positions `i-k+1` up to `i`. With `i = 3` and `k = 3`, that's positions 1, 2, 3. The item that just
dropped out is the one right before the window's new start: position `i - k` = 0. Position `i - k + 1` = 1 is the *first
item of the new window*, which must stay.

### In code

```python
def max_sum(nums, k):
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best
```

- `sum(nums[:k])` adds up the first `k` items, the first window, directly. It's the only time we add a whole window.
- The loop starts at `i = k`, the first position *not* in the first window. Each pass is one slide.
- `window += nums[i] - nums[i - k]` does both updates on one line: add the entering item, subtract the leaving one.
- `best` remembers the largest sum seen so far.

A spec will also say what happens in the edge cases, for example when `k` is larger than the list (there's no complete
window at all), or when `k` is 0 or negative. Check those lines too.

---

## 2. Windows that grow and shrink

Often the window size isn't given. Instead, you're looking for the **longest** or **shortest** window that satisfies some
condition. Then the window has two independent edges:
- `right` moves forward one step at a time, adding a new item to the window;
- `left` moves forward only when needed, removing items from the front.

There are two variants:
- **Longest-window problems:** when adding an item makes the window *invalid*, move `left` forward until it's valid again.
  Then record the window's length.
- **Shortest-window problems:** while the window is still *valid*, record its length and move `left` forward to try a
  shorter one.

You might worry that a loop for `left` inside the loop for `right` makes this slow again. It doesn't. `left` only moves
forward and never passes `right`, so over the whole run it moves at most `n` steps *in total*. Each item enters once and
leaves at most once.

The **length** of the window from `left` to `right`, both included, is `right - left + 1`. With `left = 2` and `right = 4`
the window is positions 2, 3, 4, which is 3 items. Forgetting the `+ 1` is a classic bug.

### Example: the longest piece of text with no repeated character

For `"abcabcbb"`, the answer is 3 (`"abc"`). We move `right` along the string. Whenever the new character already appears
*inside the current window*, the window must shrink so that it starts just after that earlier occurrence. To do that in
one jump, we keep a dict `last` that remembers the most recent position of each character:

```python
def longest_unique(s):
    last = {}
    left = best = 0
    for right, c in enumerate(s):
        if c in last and last[c] >= left:   # repeat INSIDE the window
            left = last[c] + 1
        last[c] = right
        best = max(best, right - left + 1)  # window length is right - left + 1
    return best
```

Line by line:
- `last` maps each character to the last position where we saw it.
- `enumerate(s)` gives each position `right` together with its character `c` (Day 1).
- If `c` was seen before **and** that earlier position is inside the current window (`>= left`), the window now contains
  `c` twice. So we move `left` to just past the earlier occurrence.
- We record that `c` is now at position `right`.
- We update `best` with the current window's length.

Why does the check need `last[c] >= left`? Trace `"abba"`: r=0 a, r=1 b, r=2 b → left=2, r=3 a: `last['a']=0` is **outside** the window (0 < 2), so left
stays 2. Without the `>= left` check (or `left = max(left, last[c] + 1)`), left would jump *back* to 1. Classic bug.

In words: at `right = 3` the window is `"b"` (position 2 only). The `a` we saw earlier, at position 0, is no longer in the
window, so it isn't a repeat. Without the check, the code would set `left = 0 + 1 = 1`, moving the window's start
*backwards* to include the second `b` again, and the answer would be wrong.

### Example: the shortest stretch whose sum reaches a target

"Given positive numbers, find the length of the shortest window with a sum of at least `target`." For
`[2, 3, 1, 2, 4, 3]` and target 7, the answer is 2 (`[4, 3]`).

```python
def min_len(nums, target):
    left = total = 0
    best = None
    for right, x in enumerate(nums):
        total += x
        while total >= target:              # valid: try to shrink
            length = right - left + 1
            best = length if best is None else min(best, length)
            total -= nums[left]
            left += 1
    return best or 0
```

- `total` is the sum of the current window, kept up to date by adding the entering item and subtracting the leaving one.
- After adding `nums[right]`, if the window is valid (its sum reaches the target), we record its length, then drop the
  front item and check again. It's a `while`, not an `if`, because after adding one big number we may be able to drop
  *several* small ones from the front and still be valid. Each of those shorter windows is a candidate.
- `best = None` means "no valid window found yet". The last line turns that into 0, as the spec requires.

This only works because the numbers are **positive**. Removing an item then always makes the sum smaller, so once the
window stops being valid, shrinking it further can never make it valid again.

---

## 3. The maximum of every window

"For every window of size `k`, what's the largest item?" Here we hit a problem. A sum is easy to update: subtract what
leaves. A maximum isn't. When the current maximum leaves the window, what's the next largest? Rescanning the window every
time would be slow again.

The trick is to keep a short list of **candidates**: items that could still become the maximum of some future window.
Here's the key observation. If an older item is *smaller than or equal to* a newer one, the older one can **never** be the
maximum again: the newer item is at least as big, and it will stay in the window longer. So the older one can be thrown
away immediately.

If we keep throwing away such items, the candidates that remain are always in **decreasing** order, and the first
candidate is always the current maximum.

We store the candidates in a **deque** (pronounced "deck", short for "double-ended queue"), from the `collections` module.
A deque is like a list that's fast at adding and removing at **both** ends: `append` and `pop` at the back, `popleft` at
the front. We store **positions** rather than values, so we can tell when a candidate has slid out of the window.

```python
from collections import deque
def window_max(nums, k):
    dq, out = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

Step by step, for each new item `x` at position `i`:
1. **Remove hopeless candidates from the back:** while the last candidate's value is `<= x`, it can never be a maximum
   again, so `pop()` it.
2. **Add the new item** as a candidate.
3. **Remove an expired candidate from the front:** the window now covers positions `i-k+1` to `i`, so a candidate at
   position `i - k` or earlier has left. Since positions are added in increasing order, only the front one can have
   expired.
4. **Record the answer** once the first complete window exists (`i >= k - 1`): the front candidate is the maximum.

Trace `[1, 3, -1, -3, 5]` with `k = 3` on paper. When the window `[3, -1, -3]` is complete, the deque holds positions
`1, 2, 3` (values 3, -1, -3, in decreasing order), and the answer is 3. Then 5 arrives and removes all three.

---

## 4. Anagram windows (a fixed window of counts)

An **anagram** is a rearrangement of the same letters: `"abc"`, `"bca"` and `"cab"` are anagrams of each other. Two strings
are anagrams exactly when they contain each letter the same number of times. So you can compare them by their *letter
counts*: a dict like `{'a': 1, 'b': 1, 'c': 1}`.

To find every position in a text where an anagram of a pattern starts, slide a window of the pattern's length along the
text, and keep the window's letter counts up to date: add 1 for the entering letter and subtract 1 for the leaving letter.
Whenever the window's counts equal the pattern's counts, record the window's start.

Two details matter:
- When a letter's count drops to 0, **delete the key**. Python considers `{'a': 0, 'b': 1}` and `{'b': 1}` different dicts,
  so leftover zeros would make the comparison fail.
- Make sure the *last* window is checked. Windows start at positions `0` up to `len(text) - len(pattern)`, inclusive.

---

## Where bugs hide

All of these come from the two updates (what enters, what leaves) and from the window's boundaries:
- index of the leaving element (`i - k` vs `i - k + 1`)
- window length (`right - left + 1`)
- `while` vs `if` when shrinking; `>` vs `>=` in the validity condition
- `left` moving backwards (`max(left, ...)`)
- the first window or the last window not being counted (`range` bounds)
- counts that reach 0 but stay in the dict
- stale indices in the deque (`<` vs `<=` in the expiry check)

## Drill
`exam/sliding_window.py` — 5 functions, 5 bugs, 15 tests. Timer: 30 minutes.
