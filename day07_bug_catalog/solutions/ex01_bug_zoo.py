"""Day 7 - Exercise 1: bug zoo (reference solution). Each fix is marked with its catalog code."""
import copy


def make_grid(rows, cols, fill):
    """rows x cols grid (list of lists) filled with `fill`; rows are independent."""
    return [[fill] * cols for _ in range(rows)]  # FIX C4: was [[fill] * cols] * rows


def sorted_copy(items):
    """Return a sorted copy; don't modify items."""
    return sorted(items)  # FIX C5: was `return list(items).sort()`


def collect(item, bucket=None):
    """Append item to bucket (a new list if none given) and return the bucket."""
    if bucket is None:  # FIX C1: was bucket=[] default
        bucket = []
    bucket.append(item)
    return bucket


def get_or_default(d, key, default):
    """d[key] if key is in d (even if the value is falsy), else default."""
    return d[key] if key in d else default  # FIX B9: was d.get(key) or default


def remove_negatives(nums):
    """Remove negative numbers IN PLACE and return the same list."""
    nums[:] = [x for x in nums if x >= 0]  # FIX C12: was removing while iterating
    return nums


def find_index(items, target):
    """Index of the first occurrence of target, or -1."""
    for i, x in enumerate(items):
        if x == target:
            return i
    return -1  # FIX C13/E6: `return -1` was inside the loop (else branch)


def count_in_range(nums, lo, hi):
    """How many numbers x satisfy lo <= x <= hi."""
    return sum(1 for x in nums if lo <= x <= hi)  # FIX A2: was lo < x < hi


def last_word_length(s):
    """Length of the last word; words are separated by any whitespace. "" -> 0."""
    words = s.split()  # FIX D1: was s.split(" ")
    return len(words[-1]) if words else 0


def median(nums):
    """Median of a non-empty list (average of the two middle values for even length)."""
    s = sorted(nums)  # FIX: list was not sorted
    n = len(s)
    if n % 2:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


def same_contents(a, b):
    """True if the two lists have equal contents."""
    return a == b  # FIX B8: was `a is b`


def round_half_up(x):
    """Round a NON-NEGATIVE number to the nearest int, halves going up: 2.5 -> 3."""
    return int(x + 0.5)  # FIX B6: was round(x) (banker's rounding)


def parse_bool(s):
    """"true"/"yes"/"1" (any case, surrounding spaces ok) -> True; anything else -> False."""
    return s.strip().lower() in ("true", "yes", "1")  # FIX: was bool(s)


def sort_people(people):
    """people: list of (name, age). Sort by age DESCENDING, then name ascending."""
    return sorted(people, key=lambda p: (-p[1], p[0]))  # FIX B3: was (p[1], p[0]), reverse=True


def join_numbers(nums):
    """Comma-separated string of the numbers: [1, 2, 3] -> "1,2,3"."""
    return ",".join(str(n) for n in nums)  # FIX: join needs strings


def word_counts(words):
    """{word: count}."""
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1  # FIX: was counts[w] += 1 (KeyError)
    return counts


def clone_config(cfg):
    """Return a fully independent copy of a nested config dict."""
    return copy.deepcopy(cfg)  # FIX C4: was dict(cfg)


def first_byte(data):
    """The first byte of `data` as a bytes object of length 1 (b"" for empty data)."""
    return data[:1]  # FIX D5: was data[0] (an int) with an empty-data check


def utf8_size(s):
    """Number of bytes s takes in UTF-8."""
    return len(s.encode("utf-8"))  # FIX D4: was len(s)


def factorial(n):
    """n! for n >= 0."""
    if n <= 1:  # FIX E1: was n == 1 (factorial(0) never ended)
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
    out.extend(a[i:])  # FIX A5: the leftovers were not appended
    out.extend(b[j:])
    return out


def is_leap(year):
    """Gregorian leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)  # FIX B4: precedence


def swap_pairs(items):
    """Swap elements pairwise: [1,2,3,4,5] -> [2,1,4,3,5]. Returns a new list."""
    out = list(items)
    for i in range(0, len(out) - 1, 2):  # FIX A3: was range(0, len(out), 2)
        out[i], out[i + 1] = out[i + 1], out[i]
    return out


def strip_lines(text):
    """List of lines with surrounding whitespace removed."""
    return [line.strip() for line in text.splitlines()]  # FIX C7: was line.strip (no call)
