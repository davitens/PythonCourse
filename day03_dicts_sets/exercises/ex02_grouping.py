"""Day 3 - Exercise 2: grouping."""


def group_anagrams(words):
    """Group words that are anagrams of each other (case-sensitive).
    Groups are ordered by the first appearance of any member; words inside a group keep
    input order. group_anagrams(["eat","tea","tan","ate","nat","bat"])
    -> [["eat","tea","ate"], ["tan","nat"], ["bat"]]
    """
    raise NotImplementedError


def invert_dict(d):
    """Map each value to the SORTED list of keys that had it.
    invert_dict({"a": 1, "b": 2, "c": 1}) -> {1: ["a", "c"], 2: ["b"]}"""
    raise NotImplementedError


def group_by(items, key_fn):
    """Return {key_fn(item): [items with that key, in input order]}."""
    raise NotImplementedError


def two_sum(nums, target):
    """Return (i, j) with i < j and nums[i] + nums[j] == target, choosing the pair with
    the smallest j (and for that j the smallest i). Return None if no pair exists.
    Must be O(n): use a dict."""
    raise NotImplementedError


def build_graph(edges):
    """Undirected graph from a list of (a, b) edges: {node: sorted list of neighbours}.
    Duplicate edges are ignored; self-loops list the node once as its own neighbour."""
    raise NotImplementedError
