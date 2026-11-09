import random
import unittest
import urllib.parse

from ex03_percent import percent_decode, percent_encode


class TestEncode(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(percent_encode("a b/é"), "a%20b%2F%C3%A9")
        self.assertEqual(percent_encode("a/b", safe="/"), "a/b")
        self.assertEqual(percent_encode("AZaz09-._~"), "AZaz09-._~")
        self.assertEqual(percent_encode(""), "")

    def test_uppercase_hex(self):
        self.assertEqual(percent_encode("\n"), "%0A")

    def test_emoji(self):
        self.assertEqual(percent_encode("😀"), "%F0%9F%98%80")

    def test_against_urllib(self):
        rng = random.Random(9)
        alphabet = "ab Z9-_.~!*'();:@&=+$,/?#[]%é€😀日\t"
        for _ in range(300):
            s = "".join(rng.choice(alphabet) for _ in range(rng.randrange(12)))
            self.assertEqual(percent_encode(s), urllib.parse.quote(s, safe=""), s)
            self.assertEqual(percent_encode(s, safe="/:"), urllib.parse.quote(s, safe="/:"), s)


class TestDecode(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(percent_decode("a%20b%2F%C3%A9"), "a b/é")
        self.assertEqual(percent_decode("%c3%a9"), "é")
        self.assertEqual(percent_decode("a+b"), "a+b")
        self.assertEqual(percent_decode("café"), "café")

    def test_roundtrip(self):
        for s in ["hello world", "100% sure", "😀/日本?x=1&y=2", ""]:
            self.assertEqual(percent_decode(percent_encode(s)), s)

    def test_bad_escapes(self):
        for bad in ["%", "%2", "%G1", "abc%-1", "%%"]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    percent_decode(bad)

    def test_bad_utf8(self):
        for bad in ["%C3", "%FF", "%C3%28"]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    percent_decode(bad)


if __name__ == "__main__":
    unittest.main()
