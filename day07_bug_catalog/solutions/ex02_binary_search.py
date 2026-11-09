"""Day 7 - Exercise 2: binary search family (reference solution). Fixes marked # FIX.
All input lists are sorted ascending (except search_rotated)."""


def lower_bound(a, x):
    """First index i with a[i] >= x; len(a) if there is none."""
    lo, hi = 0, len(a)  # FIX A1: hi was len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(a, x):
    """First index i with a[i] > x; len(a) if there is none."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:  # FIX A2: was <
            lo = mid + 1
        else:
            hi = mid
    return lo


def binary_search(a, x):
    """Index of the FIRST occurrence of x in a, or -1."""
    i = lower_bound(a, x)
    if i < len(a) and a[i] == x:  # FIX A3: bounds check was missing
        return i
    return -1


def count_occurrences(a, x):
    return upper_bound(a, x) - lower_bound(a, x)


def search_rotated(a, x):
    """a is a sorted list of DISTINCT values rotated at an unknown pivot, e.g.
    [4, 5, 6, 7, 0, 1, 2]. Return the index of x or -1, in O(log n)."""
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        if a[lo] <= a[mid]:  # FIX A2: was < (fails when lo == mid)
            if a[lo] <= x < a[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if a[mid] < x <= a[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def isqrt(n):
    """floor(sqrt(n)) for n >= 0, using binary search (no math module)."""
    lo, hi, ans = 0, n, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= n:  # FIX A2: was <
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans
