"""Day 3 - Exercise 3: nested dictionaries. Paths are dotted strings like "a.b.c"."""


def get_path(d, path, default=None):
    """Follow the dotted path through nested dicts; return default if any step is
    missing or if an intermediate value is not a dict."""
    cur = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def set_path(d, path, value):
    """Set value at the dotted path IN PLACE, creating intermediate dicts as needed.
    An intermediate value that is not a dict is replaced by a dict. Returns None."""
    parts = path.split(".")
    cur = d
    for part in parts[:-1]:
        if not isinstance(cur.get(part), dict):
            cur[part] = {}
        cur = cur[part]
    cur[parts[-1]] = value


def flatten_dict(d, prefix=""):
    """{"a": {"b": 1, "c": {"d": 2}}, "e": 3} -> {"a.b": 1, "a.c.d": 2, "e": 3}.
    Empty nested dicts disappear. Order: depth-first in insertion order."""
    out = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten_dict(v, key))
        else:
            out[key] = v
    return out


def unflatten_dict(flat):
    """Inverse of flatten_dict."""
    out = {}
    for k, v in flat.items():
        set_path(out, k, v)
    return out


def deep_merge(a, b):
    """Return a NEW dict: keys of b override a, but when both values are dicts they are
    merged recursively. Neither input may be modified (also not their nested dicts)."""
    out = {}
    for k, v in a.items():
        out[k] = deep_merge(v, {}) if isinstance(v, dict) else v
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        elif isinstance(v, dict):
            out[k] = deep_merge(v, {})
        else:
            out[k] = v
    return out
