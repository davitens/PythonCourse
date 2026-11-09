import unittest

from ex04_utf8_tools import (byte_to_char_index, char_boundaries, char_to_byte_index,
                             count_code_points, hex_dump, truncate_bytes, truncate_str)


class TestTruncate(unittest.TestCase):
    def test_truncate_str(self):
        self.assertEqual(truncate_str("héllo", 2), "h")
        self.assertEqual(truncate_str("héllo", 3), "hé")
        self.assertEqual(truncate_str("héllo", 100), "héllo")
        self.assertEqual(truncate_str("😀a", 3), "")
        self.assertEqual(truncate_str("", 0), "")

    def test_truncate_bytes(self):
        data = "a€b".encode()  # 61 e2 82 ac 62
        self.assertEqual(truncate_bytes(data, 1), b"a")
        self.assertEqual(truncate_bytes(data, 2), b"a")
        self.assertEqual(truncate_bytes(data, 3), b"a")
        self.assertEqual(truncate_bytes(data, 4), "a€".encode())
        self.assertEqual(truncate_bytes(data, 5), data)
        self.assertEqual(truncate_bytes(data, 0), b"")

    def test_truncate_bytes_always_valid(self):
        data = "naïve café 日本 😀!".encode()
        for n in range(len(data) + 2):
            out = truncate_bytes(data, n)
            self.assertLessEqual(len(out), n)
            out.decode("utf-8")  # must not raise
            self.assertTrue(data.startswith(out))


class TestCounting(unittest.TestCase):
    def test_count(self):
        for s in ["", "abc", "héllo", "日本語", "😀👍🏽"]:
            self.assertEqual(count_code_points(s.encode()), len(s))

    def test_boundaries(self):
        self.assertEqual(char_boundaries("aé€".encode()), [0, 1, 3])
        self.assertEqual(char_boundaries("😀x".encode()), [0, 4])
        self.assertEqual(char_boundaries(b""), [])


class TestOffsets(unittest.TestCase):
    def test_byte_to_char(self):
        s = "aé€b"  # bytes: a(0) é(1,2) €(3,4,5) b(6) ; total 7
        self.assertEqual([byte_to_char_index(s, o) for o in (0, 1, 3, 6, 7)], [0, 1, 2, 3, 4])

    def test_byte_to_char_errors(self):
        s = "aé€b"
        for bad in (2, 4, 5, 8, -1):
            with self.subTest(offset=bad):
                with self.assertRaises(ValueError):
                    byte_to_char_index(s, bad)

    def test_char_to_byte(self):
        s = "aé€b"
        self.assertEqual([char_to_byte_index(s, i) for i in range(5)], [0, 1, 3, 6, 7])
        with self.assertRaises(ValueError):
            char_to_byte_index(s, 5)


class TestHexDump(unittest.TestCase):
    def test_hex(self):
        self.assertEqual(hex_dump(b"h\xc3\xa9"), "68 c3 a9")
        self.assertEqual(hex_dump(b"\x00\x0f"), "00 0f")
        self.assertEqual(hex_dump(b""), "")


if __name__ == "__main__":
    unittest.main()
