"""Day 5 - Exercise 4: UTF-8 utilities. Here you MAY use str.encode / bytes.decode."""


def truncate_str(s, max_bytes):
    """Longest prefix of s whose UTF-8 encoding has at most max_bytes bytes.
    truncate_str("héllo", 2) -> "h"   (the é would need bytes 2 and 3)"""
    raise NotImplementedError


def truncate_bytes(data, max_bytes):
    """data is valid UTF-8. Return its first max_bytes bytes, backing up so that no
    character is cut in half (the result is always valid UTF-8). Do it by inspecting
    bytes (find the boundary), not by decoding in a loop."""
    raise NotImplementedError


def count_code_points(data):
    """Number of characters in valid UTF-8 `data`, without decoding."""
    raise NotImplementedError


def char_boundaries(data):
    """Byte offsets at which each character of valid UTF-8 `data` starts.
    char_boundaries("aé€".encode()) -> [0, 1, 3]"""
    raise NotImplementedError


def byte_to_char_index(s, byte_offset):
    """Convert a byte offset into s.encode("utf-8") to a character index into s.
    byte_offset == total length -> len(s). Raise ValueError if the offset is in the
    middle of a character or outside 0..len(bytes)."""
    raise NotImplementedError


def char_to_byte_index(s, char_index):
    """Inverse of byte_to_char_index; char_index must be in 0..len(s) (else ValueError)."""
    raise NotImplementedError


def hex_dump(data):
    """Lowercase two-digit hex for every byte, separated by single spaces.
    hex_dump(b"h\\xc3\\xa9") -> "68 c3 a9";  hex_dump(b"") -> "" """
    raise NotImplementedError
