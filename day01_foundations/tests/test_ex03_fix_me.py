import unittest

from ex03_fix_me import (average, clamp, count_vowels, last_n, max_index, range_sum,
                         reverse_words)


class TestFixMe(unittest.TestCase):
    def test_average(self):
        self.assertEqual(average([1, 2]), 1.5)
        self.assertEqual(average([]), 0.0)

    def test_count_vowels(self):
        self.assertEqual(count_vowels("Hello World"), 3)
        self.assertEqual(count_vowels("AEIOU xyz"), 5)

    def test_max_index_first_occurrence(self):
        self.assertEqual(max_index([1, 9, 3, 9]), 1)
        self.assertEqual(max_index([5]), 0)
        self.assertEqual(max_index([]), -1)

    def test_range_sum(self):
        self.assertEqual(range_sum(1, 4), 10)
        self.assertEqual(range_sum(3, 3), 3)
        self.assertEqual(range_sum(5, 1), 0)

    def test_reverse_words(self):
        self.assertEqual(reverse_words("hello big world"), "world big hello")
        self.assertEqual(reverse_words("one"), "one")

    def test_clamp(self):
        self.assertEqual(clamp(5, 0, 10), 5)
        self.assertEqual(clamp(-3, 0, 10), 0)
        self.assertEqual(clamp(42, 0, 10), 10)

    def test_last_n(self):
        self.assertEqual(last_n([1, 2, 3, 4], 2), [3, 4])
        self.assertEqual(last_n([1, 2], 5), [1, 2])
        self.assertEqual(last_n([1, 2, 3], 0), [])


if __name__ == "__main__":
    unittest.main()
