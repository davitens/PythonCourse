"""Dynamic programming on two sequences (strings). Each docstring is the spec."""


def lcs_table(a, b):
    """(len(a)+1) x (len(b)+1) table: dp[i][j] = length of the longest common subsequence
    of a[:i] and b[:j]."""
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def lcs(a, b):
    """One longest common subsequence, recovered from lcs_table by walking back from
    (len(a), len(b)): on equal characters take it and go diagonally; otherwise move UP
    (i -= 1) if dp[i-1][j] >= dp[i][j-1], else LEFT (j -= 1)."""
    dp = lcs_table(a, b)
    i, j = len(a), len(b)
    out = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


def edit_distance(a, b):
    """Levenshtein distance: minimum number of single-character insertions, deletions
    and substitutions turning a into b."""
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        dp[i][0] = 0
    for j in range(len(b) + 1):
        dp[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1])
    return dp[len(a)][len(b)]


def longest_common_substring(a, b):
    """Longest string that appears CONTIGUOUSLY in both a and b. If several have the
    maximum length, return the one that ends earliest in a. No common char -> ""."""
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    best_len, best_end = 0, 0
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] >= best_len:
                    best_len, best_end = dp[i][j], i
    return a[best_end - best_len:best_end]
