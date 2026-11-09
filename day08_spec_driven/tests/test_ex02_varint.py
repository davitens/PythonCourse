import random
import unittest

from ex02_varint import (decode_stream, decode_svarint, decode_uvarint, encode_stream,
                         encode_svarint, encode_uvarint, zigzag_decode, zigzag_encode)


class TestUvarint(unittest.TestCase):
    def test_vectors(self):
        vectors = {0: b"\x00", 1: b"\x01", 127: b"\x7f", 128: b"\x80\x01", 300: b"\xac\x02",
                   16384: b"\x80\x80\x01", 2 ** 63: b"\x80" * 9 + b"\x01"}
        for n, enc in vectors.items():
            with self.subTest(n=n):
                self.assertEqual(encode_uvarint(n), enc)
                self.assertEqual(decode_uvarint(enc), (n, len(enc)))

    def test_negative(self):
        with self.assertRaises(ValueError):
            encode_uvarint(-1)

    def test_decode_at_position(self):
        data = b"\xff" + b"\xac\x02" + b"\x05"
        self.assertEqual(decode_uvarint(data, 1), (300, 3))
        self.assertEqual(decode_uvarint(data, 3), (5, 4))

    def test_truncated(self):
        for bad in (b"", b"\x80", b"\xac"):
            with self.assertRaises(ValueError):
                decode_uvarint(bad)

    def test_too_long(self):
        with self.assertRaises(ValueError):
            decode_uvarint(b"\x80" * 10 + b"\x01")


class TestZigzag(unittest.TestCase):
    def test_mapping(self):
        self.assertEqual([zigzag_encode(n) for n in (0, -1, 1, -2, 2, -64)], [0, 1, 2, 3, 4, 127])

    def test_roundtrip(self):
        for n in range(-1000, 1000):
            self.assertEqual(zigzag_decode(zigzag_encode(n)), n)

    def test_svarint(self):
        self.assertEqual(encode_svarint(-1), b"\x01")
        self.assertEqual(encode_svarint(-65), b"\x81\x01")
        self.assertEqual(decode_svarint(b"\x81\x01"), (-65, 2))


class TestStream(unittest.TestCase):
    def test_example(self):
        self.assertEqual(encode_stream([1, -1, 300]), b"\x03\x02\x01\xd8\x04")
        self.assertEqual(decode_stream(b"\x03\x02\x01\xd8\x04"), [1, -1, 300])
        self.assertEqual(decode_stream(encode_stream([])), [])

    def test_random_roundtrip(self):
        rng = random.Random(5)
        for _ in range(200):
            values = [rng.randint(-10 ** 12, 10 ** 12) for _ in range(rng.randrange(10))]
            self.assertEqual(decode_stream(encode_stream(values)), values)

    def test_errors(self):
        good = encode_stream([5, 6])
        with self.assertRaises(ValueError):
            decode_stream(good[:-1])
        with self.assertRaises(ValueError):
            decode_stream(good + b"\x00")


if __name__ == "__main__":
    unittest.main()
