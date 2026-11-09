import random
import unittest

from ex03_utf8_decode import UTF8DecodeError, decode_replace, utf8_decode


class TestDecodeValid(unittest.TestCase):
    def test_ascii(self):
        self.assertEqual(utf8_decode(b"hello"), "hello")
        self.assertEqual(utf8_decode(b""), "")

    def test_multibyte(self):
        for s in ["é", "héllo", "€", "日本語", "😀", "a😀b€cé", "\u0080߿ࠀ￿\U00010000\U0010ffff"]:
            with self.subTest(s=s):
                self.assertEqual(utf8_decode(s.encode("utf-8")), s)

    def test_random_valid(self):
        rng = random.Random(42)
        for _ in range(300):
            chars = []
            for _ in range(rng.randrange(1, 20)):
                cp = rng.choice([rng.randrange(0x80), rng.randrange(0x80, 0x800),
                                 rng.randrange(0x800, 0xD800), rng.randrange(0x10000, 0x110000)])
                chars.append(chr(cp))
            s = "".join(chars)
            self.assertEqual(utf8_decode(s.encode("utf-8")), s)


class TestDecodeErrors(unittest.TestCase):
    def check(self, data, reason, position):
        with self.assertRaises(UTF8DecodeError) as ctx:
            utf8_decode(data)
        self.assertEqual(ctx.exception.reason, reason)
        self.assertEqual(ctx.exception.position, position)

    def test_is_value_error(self):
        self.assertTrue(issubclass(UTF8DecodeError, ValueError))

    def test_invalid_start(self):
        self.check(b"ab\x80", "invalid start byte", 2)
        self.check(b"\xbf", "invalid start byte", 0)
        self.check(b"x\xf8\x80\x80\x80", "invalid start byte", 1)
        self.check(b"\xff", "invalid start byte", 0)

    def test_truncated(self):
        self.check(b"a\xc3", "truncated sequence", 1)
        self.check(b"\xe2\x82", "truncated sequence", 0)
        self.check(b"ok\xf0\x9f\x98", "truncated sequence", 2)

    def test_invalid_continuation(self):
        self.check(b"\xc3A", "invalid continuation byte", 0)
        self.check(b"z\xe2\x82\xc3", "invalid continuation byte", 1)

    def test_overlong(self):
        self.check(b"\xc0\xaf", "overlong encoding", 0)      # '/' in 2 bytes
        self.check(b"\xc1\xbf", "overlong encoding", 0)
        self.check(b"\xe0\x80\xaf", "overlong encoding", 0)  # '/' in 3 bytes
        self.check(b"\xf0\x80\x80\xaf", "overlong encoding", 0)

    def test_surrogates(self):
        self.check(b"\xed\xa0\x80", "surrogate", 0)   # U+D800
        self.check(b"\xed\xbf\xbf", "surrogate", 0)   # U+DFFF

    def test_surrogate_neighbours_ok(self):
        self.assertEqual(utf8_decode(b"\xed\x9f\xbf"), "퟿")
        self.assertEqual(utf8_decode(b"\xee\x80\x80"), "")

    def test_out_of_range(self):
        self.check(b"\xf4\x90\x80\x80", "out of range", 0)   # U+110000
        self.check(b"\xf7\xbf\xbf\xbf", "out of range", 0)


class TestDecodeReplaceBonus(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(decode_replace(b"a\xffb"), "a�b")
        self.assertEqual(decode_replace(b"\xe2\x82"), "�")
        self.assertEqual(decode_replace(b"\xe2\x82a"), "�a")

    def test_against_python_random(self):
        rng = random.Random(7)
        interesting = [0x00, 0x41, 0x7F, 0x80, 0x8F, 0x9F, 0xA0, 0xBF, 0xC0, 0xC1, 0xC2, 0xDF,
                       0xE0, 0xE1, 0xED, 0xEE, 0xEF, 0xF0, 0xF1, 0xF4, 0xF5, 0xFF]
        for _ in range(3000):
            data = bytes(rng.choice(interesting) for _ in range(rng.randrange(1, 8)))
            self.assertEqual(decode_replace(data), data.decode("utf-8", errors="replace"),
                             data.hex(" "))


if __name__ == "__main__":
    unittest.main()
