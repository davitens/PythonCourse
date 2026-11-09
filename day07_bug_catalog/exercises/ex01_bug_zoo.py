"""Day 7 - Exercise 1: bug zoo. 22 functions, ONE bug each (all from the README catalog).
Target: under 2 minutes per bug. Write the catalog code (A4, C1, ...) next to each fix.
Run: python run.py 7 -k ex01
"""
import copy


def make_grid(rows, cols, fill):
    """rows x cols grid (list of lists) filled with `fill`; rows are independent."""
    return [[fill] * cols] * rows


def sorted_copy(items):
    """Return a sorted copy; don't modify items."""
    return list(items).sort()


def collect(item, bucket=[]):
    """Append item to bucket (a new list if none given) and return the bucket."""
    bucket.append(item)
    return bucket


def get_or_default(d, key, default):
    """d[key] if key is in d (even if the value is falsy), else default."""
    return d.get(key) or default


def remove_negatives(nums):
    """Remove negative numbers IN PLACE and return the same list."""
    for x in nums:
        if x < 0:
            nums.remove(x)
    return nums


def find_index(items, target):
    """Index of the first occurrence of target, or -1."""
    for i, x in enumerate(items):
        if x == target:
            return i
        else:
            return -1
    return -1


def count_in_range(nums, lo, hi):
    """How many numbers x satisfy lo <= x <= hi."""
    return sum(1 for x in nums if lo < x < hi)


def last_word_length(s):
    """Length of the last word; words are separated by any whitespace. "" -> 0."""
    words = s.split(" ")
    return len(words[-1]) if words else 0


def median(nums):
    """Median of a non-empty list (average of the two middle values for even length)."""
    s = list(nums)
    n = len(s)
    if n % 2:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


def same_contents(a, b):
    """True if the two lists have equal contents."""
    return a is b


def round_half_up(x):
    """Round a NON-NEGATIVE number to the nearest int, halves going up: 2.5 -> 3."""
    return round(x)


def parse_bool(s):
    """"true"/"yes"/"1" (any case, surrounding spaces ok) -> True; anything else -> False."""
    return bool(s.strip())


def sort_people(people):
    """people: list of (name, age). Sort by age DESCENDING, then name ascending."""
    return sorted(people, key=lambda p: (p[1], p[0]), reverse=True)


def join_numbers(nums):
    """Comma-separated string of the numbers: [1, 2, 3] -> "1,2,3"."""
    return ",".join(nums)


def word_counts(words):
    """{word: count}."""
    counts = {}
    for w in words:
        counts[w] += 1
    return counts


def clone_config(cfg):
    """Return a fully independent copy of a nested config dict."""
    return dict(cfg)


def first_byte(data):
    """The first byte of `data` as a bytes object of length 1 (b"" for empty data)."""
    return data[0] if data else b""


def utf8_size(s):
    """Number of bytes s takes in UTF-8."""
    return len(s)


def factorial(n):
    """n! for n >= 0."""
    if n == 1:
        return 1
    return n * factorial(n - 1)


def merge_sorted(a, b):
    """Merge two sorted lists into one sorted list."""
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out


def is_leap(year):
    """Gregorian leap year."""
    return year % 4 == 0 or year % 100 != 0 and year % 400 == 0


def swap_pairs(items):
    """Swap elements pairwise: [1,2,3,4,5] -> [2,1,4,3,5]. Returns a new list."""
    out = list(items)
    for i in range(0, len(out), 2):
        out[i], out[i + 1] = out[i + 1], out[i]
    return out


def strip_lines(text):
    """List of lines with surrounding whitespace removed."""
    return [line.strip for line in text.splitlines()]
