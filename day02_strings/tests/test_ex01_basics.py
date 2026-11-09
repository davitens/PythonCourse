import unittest

from ex01_basics import (caesar, count_overlapping, is_palindrome, longest_common_prefix,
                         parse_key_values, reverse_each_word, title_case)


class TestPalindrome(unittest.TestCase):
    def test_true(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))
        self.assertTrue(is_palindrome(""))
        self.assertTrue(is_palindrome("No 'x' in Nixon"))

    def test_false(self):
        self.assertFalse(is_palindrome("race a car"))
        self.assertFalse(is_palindrome("ab"))


class TestCaesar(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(caesar("Hello, World!", 3), "Khoor, Zruog!")

    def test_wrap(self):
        self.assertEqual(caesar("xyz XYZ", 3), "abc ABC")

    def test_negative_and_large(self):
        self.assertEqual(caesar("abc", -1), "zab")
        self.assertEqual(caesar("abc", 27), "bcd")

    def test_roundtrip(self):
        msg = "The Quick Brown Fox, 2024!"
        self.assertEqual(caesar(caesar(msg, 11), -11), msg)

    def test_non_ascii_unchanged(self):
        self.assertEqual(caesar("ñé", 5), "ñé")


class TestTitleCase(unittest.TestCase):
    def test_minor_words(self):
        self.assertEqual(title_case("the lord OF the rings"), "The Lord of the Rings")

    def test_first_word_minor(self):
        self.assertEqual(title_case("a tale of two cities"), "A Tale of Two Cities")

    def test_custom_minor(self):
        self.assertEqual(title_case("war and peace", minor_words=()), "War And Peace")

    def test_keeps_spacing(self):
        self.assertEqual(title_case("hello  world"), "Hello  World")


class TestCountOverlapping(unittest.TestCase):
    def test_values(self):
        self.assertEqual(count_overlapping("aaaa", "aa"), 3)
        self.assertEqual(count_overlapping("abcabc", "abc"), 2)
        self.assertEqual(count_overlapping("abc", "abcd"), 0)
        self.assertEqual(count_overlapping("abc", ""), 0)


class TestReverseEachWord(unittest.TestCase):
    def test_values(self):
        self.assertEqual(reverse_each_word("hello  world "), "olleh  dlrow ")
        self.assertEqual(reverse_each_word(" ab\tcd"), " ba\tdc")
        self.assertEqual(reverse_each_word(""), "")


class TestLCP(unittest.TestCase):
    def test_values(self):
        self.assertEqual(longest_common_prefix(["flower", "flow", "flight"]), "fl")
        self.assertEqual(longest_common_prefix(["dog", "racecar"]), "")
        self.assertEqual(longest_common_prefix(["same"]), "same")
        self.assertEqual(longest_common_prefix([]), "")


class TestParseKeyValues(unittest.TestCase):
    def test_example(self):
        self.assertEqual(parse_key_values(" a = 1; b=x=y ;; c"),
                         [("a", "1"), ("b", "x=y"), ("c", "")])

    def test_empty(self):
        self.assertEqual(parse_key_values(""), [])
        self.assertEqual(parse_key_values(" ; ;"), [])


if __name__ == "__main__":
    unittest.main()
