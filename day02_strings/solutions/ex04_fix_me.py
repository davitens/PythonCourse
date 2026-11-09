"""Day 2 - Exercise 4: FIX ME (reference solution). One bug per function; fixes marked # FIX."""


def count_words(s):
    """Number of words; words are separated by any amount of whitespace."""
    return len(s.split())  # FIX: was s.split(" ")


def strip_prefix(s, prefix):
    """Remove `prefix` from the start of s if present (exactly once)."""
    if s.startswith(prefix):
        return s[len(prefix):]  # FIX: was s.lstrip(prefix)
    return s


def is_anagram(a, b):
    """True if a and b contain the same letters (case-insensitive, spaces ignored)."""
    clean_a = sorted(a.replace(" ", "").lower())
    clean_b = sorted(b.replace(" ", "").lower())  # FIX: .lower() was missing
    return clean_a == clean_b


def to_snake_case(name):
    """Convert CamelCase / camelCase to snake_case. "parseHTTPResponse" is not tested;
    only simple words: "HelloWorldFoo" -> "hello_world_foo", "myVar" -> "my_var"."""
    out = []
    for i, c in enumerate(name):
        if c.isupper() and i > 0:  # FIX: was `i >= 0` (leading underscore)
            out.append("_")
        out.append(c.lower())
    return "".join(out)


def mask_email(email):
    """Keep the first character of the local part, replace the rest of the local part
    with '*', keep the domain. "john.doe@mail.com" -> "j*******@mail.com"."""
    local, domain = email.split("@", 1)
    return local[0] + "*" * (len(local) - 1) + "@" + domain  # FIX: was len(local)


def normalize_spaces(s):
    """Collapse every run of whitespace into ONE space and strip the ends."""
    s = " ".join(s.split())  # FIX: result of s.strip() was discarded / never collapsed
    return s


def initials(full_name):
    """Uppercase initials followed by dots: "ada  lovelace king" -> "A.L.K."."""
    return "".join(w[0].upper() + "." for w in full_name.split())  # FIX: was split(" ")
