"""Day 6 - Exercise 1: pdb drill. Two buggy functions. Follow the walkthrough in the README."""


def moving_average(nums, k):
    """Average of every window of k consecutive numbers, as floats.
    moving_average([1, 2, 3, 4, 5], 2) -> [1.5, 2.5, 3.5, 4.5]
    k <= 0 or k > len(nums) -> []"""
    if k <= 0 or k > len(nums):
        return []
    window = sum(nums[:k])
    out = [window / k]
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k + 1]
        out.append(window / k)
    return out


def parse_matrix(text):
    """Parse rows of space-separated ints, one row per line. Blank lines are ignored.
    parse_matrix("1 2\\n3 4\\n") -> [[1, 2], [3, 4]]"""
    rows = []
    for line in text.split("\n"):
        rows.append([int(x) for x in line.split(" ")])
    return rows


if __name__ == "__main__":
    print(moving_average([1, 2, 3, 4, 5], 2))
    print(parse_matrix("1 2\n3  4\n\n5 6\n"))
