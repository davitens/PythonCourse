import bisect
import random
import unittest

from ex02_binary_search import (binary_search, count_occurrences, isqrt, lower_bound,
                                search_rotated, upper_bound)


class TestBounds(unittest.TestCase):
    def test_lower(self):
        a = [1, 2, 2, 2, 5]
        self.assertEqual([lower_bound(a, x) for x in (0, 1, 2, 3, 5, 6)], [0, 0, 1, 4, 4, 5])
        self.assertEqual(lower_bound([], 3), 0)

    def test_upper(self):
        a = [1, 2, 2, 2, 5]
        self.assertEqual([upper_bound(a, x) for x in (0, 1, 2, 3, 5, 6)], [0, 1, 4, 4, 5, 5])

    def test_against_bisect(self):
        rng = random.Random(3)
        for _ in range(500):
            a = sorted(rng.randrange(10) for _ in range(rng.randrange(8)))
            x = rng.randrange(-1, 11)
            self.assertEqual(lower_bound(a, x), bisect.bisect_left(a, x), (a, x))
            self.assertEqual(upper_bound(a, x), bisect.bisect_right(a, x), (a, x))


class TestSearch(unittest.TestCase):
    def test_found(self):
        self.assertEqual(binary_search([1, 3, 3, 7], 3), 1)
        self.assertEqual(binary_search([1, 3, 3, 7], 7), 3)

    def test_missing(self):
        self.assertEqual(binary_search([1, 3, 7], 4), -1)
        self.assertEqual(binary_search([1, 3, 7], 9), -1)
        self.assertEqual(binary_search([], 1), -1)

    def test_count(self):
        self.assertEqual(count_occurrences([1, 2, 2, 2, 5], 2), 3)
        self.assertEqual(count_occurrences([1, 2, 2, 2, 5], 4), 0)


class TestRotated(unittest.TestCase):
    def test_all_rotations(self):
        base = [0, 1, 2, 4, 5, 6, 7]
        for r in range(len(base)):
            a = base[r:] + base[:r]
            for x in base:
                self.assertEqual(search_rotated(a, x), a.index(x), (a, x))
            self.assertEqual(search_rotated(a, 3), -1)

    def test_small(self):
        self.assertEqual(search_rotated([3, 1], 1), 1)
        self.assertEqual(search_rotated([1], 0), -1)


class TestIsqrt(unittest.TestCase):
    def test_values(self):
        for n in range(0, 200):
            r = isqrt(n)
            self.assertTrue(r * r <= n < (r + 1) * (r + 1), n)


if __name__ == "__main__":
    unittest.main()
