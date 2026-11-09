import unittest

from ex01_counting import (common_elements, first_unique_char, most_common_char, top_k_words,
                           word_frequencies)


class TestWordFrequencies(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(word_frequencies("Hi! hi, there."), {"hi": 2, "there": 1})

    def test_order_of_first_appearance(self):
        self.assertEqual(list(word_frequencies("b a b c a")), ["b", "a", "c"])

    def test_drops_pure_punctuation(self):
        self.assertEqual(word_frequencies("wait ... what?!"), {"wait": 1, "what": 1})

    def test_inner_punctuation_kept(self):
        self.assertEqual(word_frequencies("don't 'quote'"), {"don't": 1, "quote": 1})


class TestTopK(unittest.TestCase):
    def test_tie_break_alphabetical(self):
        text = "b b a a c d d d"
        self.assertEqual(top_k_words(text, 3), [("d", 3), ("a", 2), ("b", 2)])

    def test_k_larger(self):
        self.assertEqual(top_k_words("x y", 10), [("x", 1), ("y", 1)])


class TestFirstUnique(unittest.TestCase):
    def test_values(self):
        self.assertEqual(first_unique_char("leetcode"), 0)
        self.assertEqual(first_unique_char("loveleetcode"), 2)
        self.assertEqual(first_unique_char("aabb"), -1)
        self.assertEqual(first_unique_char(""), -1)


class TestMostCommonChar(unittest.TestCase):
    def test_values(self):
        self.assertEqual(most_common_char("banana"), "a")
        self.assertEqual(most_common_char("abcabc"), "a")
        self.assertEqual(most_common_char("xyzzyx"), "x")
        self.assertIsNone(most_common_char(""))


class TestCommon(unittest.TestCase):
    def test_values(self):
        self.assertEqual(common_elements([3, 1, 2, 3], [3, 4, 1]), [1, 3])
        self.assertEqual(common_elements([], [1]), [])


if __name__ == "__main__":
    unittest.main()
