import unittest

from ex04_bencode import decode, encode


class TestEncode(unittest.TestCase):
    def test_ints(self):
        self.assertEqual(encode(42), b"i42e")
        self.assertEqual(encode(-7), b"i-7e")
        self.assertEqual(encode(0), b"i0e")

    def test_strings(self):
        self.assertEqual(encode("spam"), b"4:spam")
        self.assertEqual(encode(""), b"0:")
        self.assertEqual(encode(b"\x00\xff"), b"2:\x00\xff")

    def test_utf8_length_is_bytes(self):
        self.assertEqual(encode("é"), b"2:\xc3\xa9")
        self.assertEqual(encode("日本"), b"6:" + "日本".encode())

    def test_list(self):
        self.assertEqual(encode(["spam", 42]), b"l4:spami42ee")
        self.assertEqual(encode([]), b"le")
        self.assertEqual(encode([[1], []]), b"lli1eelee")

    def test_dict_sorted(self):
        self.assertEqual(encode({"spam": "eggs", "cow": "moo"}), b"d3:cow3:moo4:spam4:eggse")
        self.assertEqual(encode({}), b"de")

    def test_dict_sorted_by_raw_bytes(self):
        # "Z" (0x5a) < "a" (0x61) < "é" (0xc3 0xa9)
        self.assertEqual(encode({"é": 1, "a": 2, "Z": 3}), b"d1:Zi3e1:ai2e2:\xc3\xa9i1ee")

    def test_type_errors(self):
        for bad in (True, 1.5, None, {1: 2}, (1, 2)):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    encode(bad)


class TestDecode(unittest.TestCase):
    def test_values(self):
        self.assertEqual(decode(b"i42e"), 42)
        self.assertEqual(decode(b"i-7e"), -7)
        self.assertEqual(decode(b"4:spam"), "spam")
        self.assertEqual(decode(b"l4:spami42ee"), ["spam", 42])
        self.assertEqual(decode(b"d3:cow3:moo4:spam4:eggse"), {"cow": "moo", "spam": "eggs"})

    def test_bytes_when_not_utf8(self):
        self.assertEqual(decode(b"2:\x00\xff"), b"\x00\xff")
        self.assertEqual(decode(b"2:\xc3\xa9"), "é")

    def test_nested_roundtrip(self):
        value = {"info": {"name": "日本.txt", "pieces": b"\x01\x02\xff", "length": 12345},
                 "list": [1, -2, ["x", {}], []], "z": 0}
        self.assertEqual(decode(encode(value)), value)

    def test_errors(self):
        bad_inputs = [
            b"", b"i42", b"ie", b"i-0e", b"i03e", b"i4x2e", b"x", b"5:abc", b"03:abc",
            b"4spam", b"l", b"li1e", b"d3:cowe", b"di1ei2ee", b"d1:b0:1:a0:e",
            b"d1:a0:1:a0:e", b"i1ei2e", b"4:spamX",
        ]
        for bad in bad_inputs:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    decode(bad)


if __name__ == "__main__":
    unittest.main()
