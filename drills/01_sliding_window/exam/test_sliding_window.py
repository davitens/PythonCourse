import random
import unittest

from sliding_window import (anagram_starts, longest_unique_substring, max_sum_window,
                            min_subarray_len, window_max)


class TestMaxSum(unittest.TestCase):
    def test_example(self):
        self.assertEqual(max_sum_window([2, 1, 5, 1, 3, 2], 3), 9)

    def test_negatives_and_full_window(self):
        self.assertEqual(max_sum_window([-3, -1, -2], 1), -1)
        self.assertEqual(max_sum_window([4, -1, 2], 3), 5)

    def test_bad_k(self):
        for k in (0, 4):
            with self.assertRaises(ValueError):
                max_sum_window([1, 2, 3], k)

    def test_against_brute_force(self):
        rng = random.Random(1)
        for _ in range(200):
            nums = [rng.randint(-9, 9) for _ in range(rng.randint(1, 12))]
            k = rng.randint(1, len(nums))
            brute = max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1))
            self.assertEqual(max_sum_window(nums, k), brute, (nums, k))


class TestLongestUnique(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(longest_unique_substring("abcabcbb"), "abc")
        self.assertEqual(longest_unique_substring("pwwkew"), "wke")
        self.assertEqual(longest_unique_substring(""), "")

    def test_left_never_moves_back(self):
        self.assertEqual(longest_unique_substring("abba"), "ab")
        self.assertEqual(longest_unique_substring("tmmzuxt"), "mzuxt")

    def test_first_of_equal_length(self):
        self.assertEqual(longest_unique_substring("abab"), "ab")


class TestMinSubarray(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(min_subarray_len([2, 3, 1, 2, 4, 3], 7), 2)
        self.assertEqual(min_subarray_len([1, 1, 1], 10), 0)

    def test_exact_sum_counts(self):
        self.assertEqual(min_subarray_len([1, 4, 4], 4), 1)
        self.assertEqual(min_subarray_len([1, 2, 3], 6), 3)

    def test_shrinks_fully(self):
        self.assertEqual(min_subarray_len([1, 1, 1, 1, 10], 10), 1)
        self.assertEqual(min_subarray_len([], 1), 0)


class TestWindowMax(unittest.TestCase):
    def test_example(self):
        self.assertEqual(window_max([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7])

    def test_expiry(self):
        self.assertEqual(window_max([9, 1, 1, 1], 2), [9, 1, 1])

    def test_against_brute_force(self):
        rng = random.Random(2)
        for _ in range(200):
            nums = [rng.randint(0, 5) for _ in range(rng.randint(1, 10))]
            k = rng.randint(1, len(nums))
            brute = [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]
            self.assertEqual(window_max(nums, k), brute, (nums, k))


class TestAnagrams(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(anagram_starts("cbaebabacd", "abc"), [0, 6])
        self.assertEqual(anagram_starts("abab", "ab"), [0, 1, 2])
        self.assertEqual(anagram_starts("a", "ab"), [])

    def test_last_window(self):
        self.assertEqual(anagram_starts("baab", "ab"), [0, 2])
        self.assertEqual(anagram_starts("xxab", "ba"), [2])


if __name__ == "__main__":
    unittest.main()
