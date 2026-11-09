import unittest

from ex04_fix_me import (count_words, initials, is_anagram, mask_email, normalize_spaces,
                         strip_prefix, to_snake_case)


class TestFixMe(unittest.TestCase):
    def test_count_words(self):
        self.assertEqual(count_words("one two  three "), 3)
        self.assertEqual(count_words(""), 0)

    def test_strip_prefix(self):
        self.assertEqual(strip_prefix("abab_x", "ab"), "ab_x")
        self.assertEqual(strip_prefix("hello", "xy"), "hello")

    def test_is_anagram(self):
        self.assertTrue(is_anagram("Listen", "Silent"))
        self.assertTrue(is_anagram("Dormitory", "dirty room"))
        self.assertFalse(is_anagram("abc", "abd"))

    def test_to_snake_case(self):
        self.assertEqual(to_snake_case("HelloWorldFoo"), "hello_world_foo")
        self.assertEqual(to_snake_case("myVar"), "my_var")
        self.assertEqual(to_snake_case("x"), "x")

    def test_mask_email(self):
        self.assertEqual(mask_email("john.doe@mail.com"), "j*******@mail.com")
        self.assertEqual(mask_email("a@b.c"), "a@b.c")

    def test_normalize_spaces(self):
        self.assertEqual(normalize_spaces("  a   b \t c\n"), "a b c")

    def test_initials(self):
        self.assertEqual(initials("ada  lovelace king"), "A.L.K.")


if __name__ == "__main__":
    unittest.main()
