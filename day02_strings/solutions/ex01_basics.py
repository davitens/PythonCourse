"""Day 2 - Exercise 1: string basics. Implement each function to match its docstring."""


def is_palindrome(s):
    """True if s reads the same backwards, ignoring case and any non-alphanumeric chars.

    is_palindrome("A man, a plan, a canal: Panama") -> True;  is_palindrome("") -> True
    """
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]


def caesar(s, shift):
    """Shift every ASCII letter by `shift` positions in the alphabet (wrapping around),
    preserving case. Other characters are unchanged. shift may be negative or > 26.

    caesar("Hello, World!", 3) -> "Khoor, Zruog!"
    """
    out = []
    for c in s:
        if "a" <= c <= "z":
            out.append(chr((ord(c) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= c <= "Z":
            out.append(chr((ord(c) - ord("A") + shift) % 26 + ord("A")))
        else:
            out.append(c)
    return "".join(out)


def title_case(s, minor_words=("a", "an", "the", "of", "and", "in")):
    """Capitalize the first letter of each word and lowercase the rest, except that
    words in `minor_words` are fully lowercase - unless they are the FIRST word.
    Words are separated by single spaces; keep the spacing as is.

    title_case("the lord OF the rings") -> "The Lord of the Rings"
    """
    words = s.split(" ")
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if i > 0 and lw in minor_words:
            out.append(lw)
        else:
            out.append(lw[:1].upper() + lw[1:])
    return " ".join(out)


def count_overlapping(s, sub):
    """Number of (possibly overlapping) occurrences of sub in s.
    count_overlapping("aaaa", "aa") -> 3. An empty `sub` -> 0."""
    if not sub:
        return 0
    return sum(1 for i in range(len(s) - len(sub) + 1) if s[i:i + len(sub)] == sub)


def reverse_each_word(s):
    """Reverse the characters of every word but keep words in place and keep ALL
    whitespace exactly as it is (multiple spaces included).

    reverse_each_word("hello  world ") -> "olleh  dlrow "
    """
    out, word = [], []
    for c in s:
        if c.isspace():
            out.append("".join(reversed(word)))
            word = []
            out.append(c)
        else:
            word.append(c)
    out.append("".join(reversed(word)))
    return "".join(out)


def longest_common_prefix(words):
    """Longest common prefix of all the words; [] -> ""."""
    if not words:
        return ""
    prefix = words[0]
    for w in words[1:]:
        while not w.startswith(prefix):
            prefix = prefix[:-1]
    return prefix


def parse_key_values(s):
    """Parse "key=value" pairs separated by ';' into a list of (key, value) tuples.
    Whitespace around keys and values is stripped; empty segments are skipped;
    values may contain '='; a segment without '=' gets value "".

    parse_key_values(" a = 1; b=x=y ;; c") -> [("a", "1"), ("b", "x=y"), ("c", "")]
    """
    out = []
    for seg in s.split(";"):
        if not seg.strip():
            continue
        key, _, value = seg.partition("=")
        out.append((key.strip(), value.strip()))
    return out
