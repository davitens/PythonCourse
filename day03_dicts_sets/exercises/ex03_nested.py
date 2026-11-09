"""Day 3 - Exercise 3: nested dictionaries. Paths are dotted strings like "a.b.c"."""


def get_path(d, path, default=None):
    """Follow the dotted path through nested dicts; return default if any step is
    missing or if an intermediate value is not a dict."""
    raise NotImplementedError


def set_path(d, path, value):
    """Set value at the dotted path IN PLACE, creating intermediate dicts as needed.
    An intermediate value that is not a dict is replaced by a dict. Returns None."""
    raise NotImplementedError


def flatten_dict(d, prefix=""):
    """{"a": {"b": 1, "c": {"d": 2}}, "e": 3} -> {"a.b": 1, "a.c.d": 2, "e": 3}.
    Empty nested dicts disappear. Order: depth-first in insertion order."""
    raise NotImplementedError


def unflatten_dict(flat):
    """Inverse of flatten_dict."""
    raise NotImplementedError


def deep_merge(a, b):
    """Return a NEW dict: keys of b override a, but when both values are dicts they are
    merged recursively. Neither input may be modified (also not their nested dicts)."""
    raise NotImplementedError
