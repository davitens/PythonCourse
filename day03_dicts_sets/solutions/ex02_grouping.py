"""Day 3 - Exercise 2: grouping."""


def group_anagrams(words):
    """Group words that are anagrams of each other (case-sensitive).
    Groups are ordered by the first appearance of any member; words inside a group keep
    input order. group_anagrams(["eat","tea","tan","ate","nat","bat"])
    -> [["eat","tea","ate"], ["tan","nat"], ["bat"]]
    """
    groups = {}
    for w in words:
        groups.setdefault("".join(sorted(w)), []).append(w)
    return list(groups.values())


def invert_dict(d):
    """Map each value to the SORTED list of keys that had it.
    invert_dict({"a": 1, "b": 2, "c": 1}) -> {1: ["a", "c"], 2: ["b"]}"""
    out = {}
    for k, v in d.items():
        out.setdefault(v, []).append(k)
    return {v: sorted(ks) for v, ks in out.items()}


def group_by(items, key_fn):
    """Return {key_fn(item): [items with that key, in input order]}."""
    out = {}
    for x in items:
        out.setdefault(key_fn(x), []).append(x)
    return out


def two_sum(nums, target):
    """Return (i, j) with i < j and nums[i] + nums[j] == target, choosing the pair with
    the smallest j (and for that j the smallest i). Return None if no pair exists.
    Must be O(n): use a dict."""
    first_index = {}
    for j, x in enumerate(nums):
        need = target - x
        if need in first_index:
            return (first_index[need], j)
        if x not in first_index:
            first_index[x] = j
    return None


def build_graph(edges):
    """Undirected graph from a list of (a, b) edges: {node: sorted list of neighbours}.
    Duplicate edges are ignored; self-loops list the node once as its own neighbour."""
    adj = {}
    for a, b in edges:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return {n: sorted(ns) for n, ns in adj.items()}
