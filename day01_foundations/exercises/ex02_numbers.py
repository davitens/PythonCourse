"""Day 1 - Exercise 2: numbers. Implement each function to match its docstring."""


def fizzbuzz(n):
    """Return a list of strings for 1..n: "Fizz" for multiples of 3, "Buzz" for multiples
    of 5, "FizzBuzz" for both, otherwise the number as a string. n <= 0 -> [].
    """
    raise NotImplementedError


def digit_sum(n):
    """Sum of the decimal digits of n; the sign is ignored. digit_sum(-123) -> 6."""
    raise NotImplementedError


def is_prime(n):
    """True if n is a prime number. Numbers < 2 are not prime."""
    raise NotImplementedError


def collatz_steps(n):
    """Number of steps to reach 1 using: n even -> n/2, n odd -> 3n+1.
    collatz_steps(1) -> 0, collatz_steps(6) -> 8. Raise ValueError if n < 1.
    """
    raise NotImplementedError


def int_to_base(n, base):
    """Convert integer n to a string in `base` (2..16), lowercase digits, '-' for negatives.

    int_to_base(255, 16) -> "ff";  int_to_base(-5, 2) -> "-101";  int_to_base(0, 7) -> "0"
    Raise ValueError if base is outside 2..16. Do not use bin/hex/format.
    """
    raise NotImplementedError
