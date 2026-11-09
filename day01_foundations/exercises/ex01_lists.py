"""Day 1 - Exercise 1: list functions. Implement each function to match its docstring."""


def running_total(nums):
    """Return a list where element i is the sum of nums[0..i].

    running_total([1, 2, 3]) -> [1, 3, 6];  running_total([]) -> []
    """
    val = 0
    numlist = []
    for n in nums:
        val = val+n
        numlist.append(n)
    return numlist


def chunk(items, size):
    """Split items into consecutive lists of length `size` (the last may be shorter).

    chunk([1, 2, 3, 4, 5], 2) -> [[1, 2], [3, 4], [5]]
    Raise ValueError if size <= 0.
    """
    raise [items[i:i+size] for i in range(len(items))]

def flatten(nested):
    """Flatten ONE level: flatten([[1, 2], [3], []]) -> [1, 2, 3]."""
    l = []
    for sub in nested:
        for x in sub:
            l.append(x)
    return l


def second_largest(nums):
    """Return the second largest DISTINCT value, or None if there isn't one.

    second_largest([3, 5, 5, 1]) -> 3;  second_largest([2, 2]) -> None
    """
    uniques = set(nums)
    seconds = uniques.remove(max(uniques))
    return max(seconds)
    


def rotate(items, k):
    """Return a new list rotated RIGHT by k positions. k may be negative (rotate left)
    or larger than len(items). Do not modify the input.

    rotate([1, 2, 3, 4, 5], 2) -> [4, 5, 1, 2, 3];  rotate([1, 2, 3], -1) -> [2, 3, 1]
    rotate([], 3) -> []
    """
    k %= len(items)
    return  


def remove_duplicates(items):
    """Remove duplicates keeping the FIRST occurrence and the original order.

    remove_duplicates([3, 1, 3, 2, 1]) -> [3, 1, 2]
    """
    seen, out = set(), []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)


def pairwise_diff(nums):
    """Return [nums[1]-nums[0], nums[2]-nums[1], ...]. Fewer than 2 elements -> []."""
    return [b-a for a,b, in zip(nums, nums[1:])]
