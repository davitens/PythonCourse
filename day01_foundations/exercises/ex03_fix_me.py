"""Day 1 - Exercise 3: FIX ME.

Each function below has exactly ONE bug. Don't rewrite them: run the tests
(python run.py 1 -k ex03), read the failure, find the wrong line, fix it.
"""


def average(nums):
    """Arithmetic mean as a float. Empty list -> 0.0."""
    if not nums:
        return 0.0
    return sum(nums) // len(nums)


def count_vowels(s):
    """Count vowels a, e, i, o, u in s, case-insensitive."""
    return sum(1 for c in s if c in "aeiou")


def max_index(nums):
    """Index of the maximum value; if it appears several times, the FIRST index.
    Empty list -> -1."""
    if not nums:
        return -1
    best = 0
    for i in range(1, len(nums)):
        if nums[i] >= nums[best]:
            best = i
    return best


def range_sum(a, b):
    """Sum of all integers from a to b INCLUSIVE. If a > b return 0."""
    total = 0
    for i in range(a, b):
        total += i
    return total


def reverse_words(s):
    """Reverse the order of words. Words are separated by single spaces.
    reverse_words("hello big world") -> "world big hello"."""
    return " ".join(s[::-1].split(" "))


def clamp(x, lo, hi):
    """Return x limited to the range [lo, hi]."""
    return min(lo, max(x, hi))


def last_n(items, n):
    """Return a list of the last n items (all items if n > len). n == 0 -> []."""
    return items[-n:]
