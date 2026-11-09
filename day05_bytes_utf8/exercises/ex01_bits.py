"""Day 5 - Exercise 1: bit manipulation. Bits are numbered from 0 (least significant).
All inputs n are non-negative ints. Do not use bin() / format() except in to_binary
if you want (try without!)."""


def get_bit(n, i):
    """Return bit i of n (0 or 1)."""
    raise NotImplementedError


def set_bit(n, i):
    """Return n with bit i set to 1."""
    raise NotImplementedError


def clear_bit(n, i):
    """Return n with bit i set to 0."""
    raise NotImplementedError


def toggle_bit(n, i):
    """Return n with bit i flipped."""
    raise NotImplementedError


def count_set_bits(n):
    """Number of 1 bits in n."""
    raise NotImplementedError


def to_binary(n, width):
    """Zero-padded binary string of exactly `width` digits. to_binary(5, 8) -> "00000101".
    Raise ValueError if n does not fit in `width` bits."""
    raise NotImplementedError


def extract_bits(n, start, length):
    """Return the integer formed by `length` bits of n starting at bit `start`.
    extract_bits(0b110110, 1, 3) -> 0b011 == 3"""
    raise NotImplementedError


def is_power_of_two(n):
    """True if n is 1, 2, 4, 8, ...  (0 is not)."""
    raise NotImplementedError


def reverse_bits(n, width):
    """Reverse the lowest `width` bits of n. reverse_bits(0b0011, 4) -> 0b1100."""
    raise NotImplementedError
