import base64
import random
import unittest

from ex01_base64 import b64decode, b64encode


class TestEncode(unittest.TestCase):
    def test_rfc_vectors(self):
        vectors = {b"": "", b"f": "Zg==", b"fo": "Zm8=", b"foo": "Zm9v", b"foob": "Zm9vYg==",
                   b"fooba": "Zm9vYmE=", b"foobar": "Zm9vYmFy"}
        for raw, enc in vectors.items():
            with self.subTest(raw=raw):
                self.assertEqual(b64encode(raw), enc)

    def test_utf8_text(self):
        self.assertEqual(b64encode("é".encode()), "w6k=")

    def test_random(self):
        rng = random.Random(0)
        for _ in range(300):
            raw = bytes(rng.randrange(256) for _ in range(rng.randrange(20)))
            self.assertEqual(b64encode(raw), base64.b64encode(raw).decode())


class TestDecode(unittest.TestCase):
    def test_vectors(self):
        self.assertEqual(b64decode("Zm9vYmE="), b"fooba")
        self.assertEqual(b64decode("Zg=="), b"f")
        self.assertEqual(b64decode(""), b"")

    def test_roundtrip_random(self):
        rng = random.Random(1)
        for _ in range(300):
            raw = bytes(rng.randrange(256) for _ in range(rng.randrange(20)))
            self.assertEqual(b64decode(b64encode(raw)), raw)
            self.assertEqual(b64decode(base64.b64encode(raw).decode()), raw)

    def test_errors(self):
        for bad in ["Zg=", "Zm9", "Zm9v!A==", "Z===", "Zg==Zg==", "=Zg="]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    b64decode(bad)


if __name__ == "__main__":
    unittest.main()
