"""Day 5 - Exercise 1: bit manipulation. Bits are numbered from 0 (least significant).
All inputs n are non-negative ints. Do not use bin() / format() except in to_binary
if you want (try without!)."""


def get_bit(n, i):
    """Return bit i of n (0 or 1)."""
    return (n >> i) & 1


def set_bit(n, i):
    """Return n with bit i set to 1."""
    return n | (1 << i)


def clear_bit(n, i):
    """Return n with bit i set to 0."""
    return n & ~(1 << i)


def toggle_bit(n, i):
    """Return n with bit i flipped."""
    return n ^ (1 << i)


def count_set_bits(n):
    """Number of 1 bits in n."""
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def to_binary(n, width):
    """Zero-padded binary string of exactly `width` digits. to_binary(5, 8) -> "00000101".
    Raise ValueError if n does not fit in `width` bits."""
    if n >= (1 << width):
        raise ValueError("does not fit")
    return "".join(str((n >> i) & 1) for i in range(width - 1, -1, -1))


def extract_bits(n, start, length):
    """Return the integer formed by `length` bits of n starting at bit `start`.
    extract_bits(0b110110, 1, 3) -> 0b011 == 3"""
    return (n >> start) & ((1 << length) - 1)


def is_power_of_two(n):
    """True if n is 1, 2, 4, 8, ...  (0 is not)."""
    return n > 0 and n & (n - 1) == 0


def reverse_bits(n, width):
    """Reverse the lowest `width` bits of n. reverse_bits(0b0011, 4) -> 0b1100."""
    out = 0
    for _ in range(width):
        out = (out << 1) | (n & 1)
        n >>= 1
    return out
