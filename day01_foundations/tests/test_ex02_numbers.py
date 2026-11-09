import unittest

from ex02_numbers import collatz_steps, digit_sum, fizzbuzz, int_to_base, is_prime


class TestFizzBuzz(unittest.TestCase):
    def test_15(self):
        self.assertEqual(
            fizzbuzz(15),
            ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
             "11", "Fizz", "13", "14", "FizzBuzz"],
        )

    def test_zero(self):
        self.assertEqual(fizzbuzz(0), [])


class TestDigitSum(unittest.TestCase):
    def test_values(self):
        for n, expected in [(0, 0), (7, 7), (123, 6), (-123, 6), (9999, 36)]:
            with self.subTest(n=n):
                self.assertEqual(digit_sum(n), expected)


class TestIsPrime(unittest.TestCase):
    def test_small(self):
        primes = [x for x in range(-5, 30) if is_prime(x)]
        self.assertEqual(primes, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def test_squares_of_primes(self):
        self.assertFalse(is_prime(49))
        self.assertFalse(is_prime(121))

    def test_large(self):
        self.assertTrue(is_prime(7919))


class TestCollatz(unittest.TestCase):
    def test_values(self):
        self.assertEqual(collatz_steps(1), 0)
        self.assertEqual(collatz_steps(6), 8)
        self.assertEqual(collatz_steps(27), 111)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            collatz_steps(0)


class TestIntToBase(unittest.TestCase):
    def test_values(self):
        cases = [(255, 16, "ff"), (10, 2, "1010"), (-5, 2, "-101"), (0, 7, "0"),
                 (35, 16, "23"), (8, 8, "10")]
        for n, b, expected in cases:
            with self.subTest(n=n, base=b):
                self.assertEqual(int_to_base(n, b), expected)

    def test_roundtrip(self):
        for b in range(2, 17):
            for n in (-1000, -1, 1, 12345):
                self.assertEqual(int(int_to_base(n, b), b), n)

    def test_invalid_base(self):
        with self.assertRaises(ValueError):
            int_to_base(5, 1)
        with self.assertRaises(ValueError):
            int_to_base(5, 17)


if __name__ == "__main__":
    unittest.main()
