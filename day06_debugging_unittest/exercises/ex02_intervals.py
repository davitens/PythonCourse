"""Day 6 - Exercise 2: closed intervals [start, end] with start <= end. 5 bugs.
Intervals that overlap OR touch ([1, 3] and [3, 5]) are merged.
Run: python run.py 6 -k ex02"""


def merge_intervals(intervals):
    """Return a sorted list of disjoint merged intervals (as lists). Don't mutate input."""
    result = []
    for start, end in intervals:
        if result and start < result[-1][1]:
            result[-1][1] = end
        else:
            result.append([start, end])
    return result


def total_covered(intervals):
    """Total length covered by the union of the intervals (length of [a, b] is b - a)."""
    return sum(end - start for start, end in intervals)


def find_gaps(intervals, lo, hi):
    """Sub-intervals of [lo, hi] not covered by any interval, as a list of [a, b] with
    a < b, in order. Assume all intervals lie inside [lo, hi]."""
    gaps = []
    cursor = lo
    for start, end in merge_intervals(intervals):
        if start > cursor:
            gaps.append([cursor, start])
        cursor = max(cursor, end)
    return gaps
