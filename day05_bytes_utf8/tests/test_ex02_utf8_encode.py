import random
import unittest

from ex02_utf8_encode import encode_code_point, utf8_encode, utf8_length


class TestUtf8Length(unittest.TestCase):
    def test_boundaries(self):
        cases = [(0, 1), (0x7F, 1), (0x80, 2), (0x7FF, 2), (0x800, 3), (0xFFFF, 3),
                 (0x10000, 4), (0x10FFFF, 4)]
        for cp, n in cases:
            with self.subTest(cp=hex(cp)):
                self.assertEqual(utf8_length(cp), n)

    def test_out_of_range(self):
        for cp in (-1, 0x110000):
            with self.assertRaises(ValueError):
                utf8_length(cp)


class TestEncodeCodePoint(unittest.TestCase):
    def test_worked_examples(self):
        self.assertEqual(encode_code_point(ord("A")), b"A")
        self.assertEqual(encode_code_point(0xE9), b"\xc3\xa9")
        self.assertEqual(encode_code_point(0x20AC), b"\xe2\x82\xac")
        self.assertEqual(encode_code_point(0x1F600), b"\xf0\x9f\x98\x80")

    def test_boundaries(self):
        for cp in (0, 0x7F, 0x80, 0x7FF, 0x800, 0xD7FF, 0xE000, 0xFFFF, 0x10000, 0x10FFFF):
            with self.subTest(cp=hex(cp)):
                self.assertEqual(encode_code_point(cp), chr(cp).encode("utf-8"))

    def test_invalid(self):
        for cp in (0xD800, 0xDABC, 0xDFFF, -5, 0x110000):
            with self.subTest(cp=hex(cp)):
                with self.assertRaises(ValueError):
                    encode_code_point(cp)

    def test_random_against_python(self):
        rng = random.Random(1234)
        for _ in range(3000):
            cp = rng.randrange(0x110000)
            if 0xD800 <= cp <= 0xDFFF:
                continue
            self.assertEqual(encode_code_point(cp), chr(cp).encode("utf-8"), hex(cp))


class TestUtf8Encode(unittest.TestCase):
    def test_strings(self):
        for s in ["", "hello", "héllo", "€100", "日本語", "😀 emoji 👍🏽", "mixé€😀a"]:
            with self.subTest(s=s):
                self.assertEqual(utf8_encode(s), s.encode("utf-8"))

    def test_returns_bytes(self):
        self.assertIsInstance(utf8_encode("é"), bytes)


if __name__ == "__main__":
    unittest.main()
