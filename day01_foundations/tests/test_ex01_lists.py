import unittest

from ex01_lists import (chunk, flatten, pairwise_diff, remove_duplicates, rotate,
                        running_total, second_largest)


class TestRunningTotal(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(running_total([1, 2, 3]), [1, 3, 6])

    def test_empty(self):
        self.assertEqual(running_total([]), [])

    def test_negatives(self):
        self.assertEqual(running_total([5, -5, 2]), [5, 0, 2])


class TestChunk(unittest.TestCase):
    def test_uneven(self):
        self.assertEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])

    def test_even(self):
        self.assertEqual(chunk([1, 2, 3, 4], 2), [[1, 2], [3, 4]])

    def test_bigger_than_list(self):
        self.assertEqual(chunk([1, 2], 10), [[1, 2]])

    def test_empty(self):
        self.assertEqual(chunk([], 3), [])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            chunk([1], 0)
        with self.assertRaises(ValueError):
            chunk([1], -2)


class TestFlatten(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(flatten([[1, 2], [3], []]), [1, 2, 3])

    def test_one_level_only(self):
        self.assertEqual(flatten([[1, [2]], [3]]), [1, [2], 3])


class TestSecondLargest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(second_largest([3, 5, 5, 1]), 3)

    def test_none(self):
        self.assertIsNone(second_largest([2, 2]))
        self.assertIsNone(second_largest([]))

    def test_negative(self):
        self.assertEqual(second_largest([-1, -7, -3]), -3)


class TestRotate(unittest.TestCase):
    def test_right(self):
        self.assertEqual(rotate([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3])

    def test_left(self):
        self.assertEqual(rotate([1, 2, 3], -1), [2, 3, 1])

    def test_large_k(self):
        self.assertEqual(rotate([1, 2, 3], 7), [3, 1, 2])

    def test_zero_and_full(self):
        self.assertEqual(rotate([1, 2, 3], 0), [1, 2, 3])
        self.assertEqual(rotate([1, 2, 3], 3), [1, 2, 3])

    def test_empty(self):
        self.assertEqual(rotate([], 3), [])

    def test_does_not_mutate(self):
        data = [1, 2, 3]
        rotate(data, 1)
        self.assertEqual(data, [1, 2, 3])

    def test_returns_new_list(self):
        data = [1, 2, 3]
        self.assertIsNot(rotate(data, 0), data)


class TestRemoveDuplicates(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(remove_duplicates([3, 1, 3, 2, 1]), [3, 1, 2])

    def test_strings(self):
        self.assertEqual(remove_duplicates(list("banana")), ["b", "a", "n"])


class TestPairwiseDiff(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(pairwise_diff([1, 4, 9, 16]), [3, 5, 7])

    def test_short(self):
        self.assertEqual(pairwise_diff([5]), [])
        self.assertEqual(pairwise_diff([]), [])


if __name__ == "__main__":
    unittest.main()
