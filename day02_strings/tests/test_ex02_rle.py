import unittest

from ex02_rle import rle_decode, rle_encode


class TestRLE(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(rle_encode("aaabccdddd"), "3a1b2c4d")
        self.assertEqual(rle_encode(""), "")
        self.assertEqual(rle_encode("z"), "1z")

    def test_encode_multidigit(self):
        self.assertEqual(rle_encode("a" * 12 + "b"), "12a1b")

    def test_encode_non_adjacent_repeats(self):
        self.assertEqual(rle_encode("abab"), "1a1b1a1b")

    def test_decode(self):
        self.assertEqual(rle_decode("3a1b2c4d"), "aaabccdddd")
        self.assertEqual(rle_decode("12a1b"), "a" * 12 + "b")
        self.assertEqual(rle_decode(""), "")

    def test_decode_spaces_and_symbols(self):
        self.assertEqual(rle_decode("2 3!"), "  !!!")

    def test_roundtrip(self):
        for s in ["hello world", "  ", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab", "ñññé"]:
            with self.subTest(s=s):
                self.assertEqual(rle_decode(rle_encode(s)), s)

    def test_decode_errors(self):
        for bad in ["a", "3a4", "0a", "3a00b"]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    rle_decode(bad)


if __name__ == "__main__":
    unittest.main()
