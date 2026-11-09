"""Day 1 - Exercise 2: numbers. Implement each function to match its docstring."""


def fizzbuzz(n):
    """Return a list of strings for 1..n: "Fizz" for multiples of 3, "Buzz" for multiples
    of 5, "FizzBuzz" for both, otherwise the number as a string. n <= 0 -> [].
    """
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return out


def digit_sum(n):
    """Sum of the decimal digits of n; the sign is ignored. digit_sum(-123) -> 6."""
    return sum(int(c) for c in str(abs(n)))


def is_prime(n):
    """True if n is a prime number. Numbers < 2 are not prime."""
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def collatz_steps(n):
    """Number of steps to reach 1 using: n even -> n/2, n odd -> 3n+1.
    collatz_steps(1) -> 0, collatz_steps(6) -> 8. Raise ValueError if n < 1.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


def int_to_base(n, base):
    """Convert integer n to a string in `base` (2..16), lowercase digits, '-' for negatives.

    int_to_base(255, 16) -> "ff";  int_to_base(-5, 2) -> "-101";  int_to_base(0, 7) -> "0"
    Raise ValueError if base is outside 2..16. Do not use bin/hex/format.
    """
    if not 2 <= base <= 16:
        raise ValueError("bad base")
    if n == 0:
        return "0"
    digits = "0123456789abcdef"
    neg = n < 0
    n = abs(n)
    out = []
    while n:
        n, r = divmod(n, base)
        out.append(digits[r])
    return ("-" if neg else "") + "".join(reversed(out))
