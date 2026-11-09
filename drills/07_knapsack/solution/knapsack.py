"""Dynamic programming: knapsack and coin change. Each docstring is the spec."""

INF = float("inf")


def knapsack_01(items, capacity):
    """items: list of (weight, value) with positive integer weights; capacity >= 0.
    Each item can be taken at most once. Return (best_value, chosen) where chosen is the
    sorted list of item indices, found by walking back from i = n to 1 and taking item i-1
    whenever dp[i][c] != dp[i-1][c]."""
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = items[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if w <= c and dp[i - 1][c - w] + v > dp[i][c]:
                dp[i][c] = dp[i - 1][c - w] + v
    chosen = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            chosen.append(i - 1)
            c -= items[i - 1][0]
    return dp[n][capacity], sorted(chosen)


def knapsack_unbounded(items, capacity):
    """Like knapsack_01 but each item can be used any number of times. Return the best value."""
    best = [0] * (capacity + 1)
    for c in range(1, capacity + 1):
        for w, v in items:
            if w <= c:
                best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


def min_coins(coins, amount):
    """Fewest coins (unlimited supply of each value) that sum to amount; -1 if impossible.
    amount 0 -> 0."""
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and dp[a - coin] + 1 < dp[a]:
                dp[a] = dp[a - coin] + 1
    return dp[amount] if dp[amount] != INF else -1


def count_ways(coins, amount):
    """Number of different multisets of coins that sum to amount (order does NOT matter:
    1+2 and 2+1 are the same way). amount 0 -> 1."""
    ways = [1] + [0] * amount
    for coin in coins:
        for a in range(coin, amount + 1):
            ways[a] += ways[a - coin]
    return ways[amount]
