"""Day 2 - Exercise 1: string basics. Implement each function to match its docstring."""


def is_palindrome(s):
    """True if s reads the same backwards, ignoring case and any non-alphanumeric chars.

    is_palindrome("A man, a plan, a canal: Panama") -> True;  is_palindrome("") -> True
    """
    raise NotImplementedError


def caesar(s, shift):
    """Shift every ASCII letter by `shift` positions in the alphabet (wrapping around),
    preserving case. Other characters are unchanged. shift may be negative or > 26.

    caesar("Hello, World!", 3) -> "Khoor, Zruog!"
    """
    raise NotImplementedError


def title_case(s, minor_words=("a", "an", "the", "of", "and", "in")):
    """Capitalize the first letter of each word and lowercase the rest, except that
    words in `minor_words` are fully lowercase - unless they are the FIRST word.
    Words are separated by single spaces; keep the spacing as is.

    title_case("the lord OF the rings") -> "The Lord of the Rings"
    """
    raise NotImplementedError


def count_overlapping(s, sub):
    """Number of (possibly overlapping) occurrences of sub in s.
    count_overlapping("aaaa", "aa") -> 3. An empty `sub` -> 0."""
    raise NotImplementedError


def reverse_each_word(s):
    """Reverse the characters of every word but keep words in place and keep ALL
    whitespace exactly as it is (multiple spaces included).

    reverse_each_word("hello  world ") -> "olleh  dlrow "
    """
    raise NotImplementedError


def longest_common_prefix(words):
    """Longest common prefix of all the words; [] -> ""."""
    raise NotImplementedError


def parse_key_values(s):
    """Parse "key=value" pairs separated by ';' into a list of (key, value) tuples.
    Whitespace around keys and values is stripped; empty segments are skipped;
    values may contain '='; a segment without '=' gets value "".

    parse_key_values(" a = 1; b=x=y ;; c") -> [("a", "1"), ("b", "x=y"), ("c", "")]
    """
    raise NotImplementedError
