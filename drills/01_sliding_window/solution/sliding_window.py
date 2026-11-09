"""Sliding-window algorithms. Each docstring is the spec."""
from collections import deque


def max_sum_window(nums, k):
    """Largest sum of k consecutive elements. ValueError if k <= 0 or k > len(nums)."""
    if k <= 0 or k > len(nums):
        raise ValueError("bad window size")
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best


def longest_unique_substring(s):
    """The longest substring of s with no repeated character. If several have the
    maximum length, return the one that starts FIRST. "" -> ""."""
    last = {}
    left = 0
    best_start, best_len = 0, 0
    for right, c in enumerate(s):
        if c in last and last[c] >= left:
            left = last[c] + 1
        last[c] = right
        if right - left + 1 > best_len:
            best_start, best_len = left, right - left + 1
    return s[best_start:best_start + best_len]


def min_subarray_len(nums, target):
    """Length of the shortest contiguous subarray whose sum is >= target, or 0 if none.
    All numbers are positive."""
    left = total = 0
    best = None
    for right, x in enumerate(nums):
        total += x
        while total >= target:
            length = right - left + 1
            if best is None or length < best:
                best = length
            total -= nums[left]
            left += 1
    return best if best is not None else 0


def window_max(nums, k):
    """List with the maximum of every window of k consecutive elements, in order
    (len(nums) - k + 1 values). ValueError if k <= 0 or k > len(nums). O(n) with a deque."""
    if k <= 0 or k > len(nums):
        raise ValueError("bad window size")
    dq = deque()  # indices; their values decrease from front to back
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def anagram_starts(s, p):
    """Start indices of every substring of s that is an anagram of p (same characters
    with the same counts), in increasing order. p == "" or len(p) > len(s) -> []."""
    k = len(p)
    if k == 0 or k > len(s):
        return []
    need = {}
    for c in p:
        need[c] = need.get(c, 0) + 1
    window = {}
    for c in s[:k]:
        window[c] = window.get(c, 0) + 1
    out = [0] if window == need else []
    for i in range(k, len(s)):
        window[s[i]] = window.get(s[i], 0) + 1
        leaving = s[i - k]
        window[leaving] -= 1
        if window[leaving] == 0:
            del window[leaving]
        if window == need:
            out.append(i - k + 1)
    return out
