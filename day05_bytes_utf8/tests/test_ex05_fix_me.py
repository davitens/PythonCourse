import unittest

from ex05_fix_me import count_chars, decode


class TestDecode(unittest.TestCase):
    def test_ascii(self):
        self.assertEqual(decode(b"hello"), "hello")

    def test_two_byte(self):
        self.assertEqual(decode("héllo".encode()), "héllo")
        self.assertEqual(decode("ñ".encode()), "ñ")

    def test_three_byte(self):
        self.assertEqual(decode("€".encode()), "€")
        self.assertEqual(decode("日本".encode()), "日本")

    def test_four_byte(self):
        self.assertEqual(decode("😀".encode()), "😀")

    def test_mixed(self):
        s = "a€é😀z"
        self.assertEqual(decode(s.encode()), s)

    def test_truncated(self):
        for bad in (b"\xc3", b"ab\xe2\x82", b"\xf0\x9f\x98"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    decode(bad)

    def test_bad_continuation(self):
        for bad in (b"\xc3A", b"\xe2\x82Z", b"\xc3\xc3"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    decode(bad)

    def test_bad_start(self):
        for bad in (b"\x80", b"\xff", b"a\xbfb"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    decode(bad)

    def test_overlong(self):
        for bad in (b"\xc0\xaf", b"\xe0\x80\xaf", b"\xe0\x9f\xbf"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    decode(bad)

    def test_surrogates(self):
        for bad in (b"\xed\xa0\x80", b"\xed\xbf\xbf", b"\xed\xb0\x80"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    decode(bad)

    def test_count_chars(self):
        self.assertEqual(count_chars(b"abc"), 3)
        self.assertEqual(count_chars("a€é😀".encode()), 4)


if __name__ == "__main__":
    unittest.main()
