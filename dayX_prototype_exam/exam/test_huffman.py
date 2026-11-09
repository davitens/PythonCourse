import random
import unittest

from huffman import (Archive, BitReader, BitWriter, Node, build_tree, byte_frequencies, canonical_codes,
                     code_lengths, compress, decompress, format_table, truncate_utf8, utf8_chars)

ABRA_BYTES = bytes.fromhex("48 55 46 31 00 05 61 01 62 03 63 04 64 04 72 02 00 00 00 0b 69 cf 68")
SAMPLES = [
    "", "a", "aaaa", "ab", "abracadabra", "hello world", "é", "café crème", "日本語のテキスト",
    "😀😀 👍🏽", "\x00\x00a", "line one\nline two\n", "€uro €uro €uro", "aé€😀" * 20,
]


def lengths_of(freqs):
    return code_lengths(build_tree(freqs))


class TestFrequencies(unittest.TestCase):
    def test_ascii(self):
        self.assertEqual(byte_frequencies("aab"), {97: 2, 98: 1})

    def test_empty(self):
        self.assertEqual(byte_frequencies(""), {})

    def test_counts_utf8_bytes(self):
        self.assertEqual(byte_frequencies("é"), {0xC3: 1, 0xA9: 1})


class TestNode(unittest.TestCase):
    def test_leaf(self):
        n = Node(3, 65)
        self.assertTrue(n.is_leaf())
        self.assertEqual((n.weight, n.symbol, n.low), (3, 65, 65))

    def test_symbol_zero_is_a_leaf(self):
        self.assertTrue(Node(1, 0).is_leaf())

    def test_internal(self):
        n = Node(2, left=Node(1, 70), right=Node(1, 60))
        self.assertFalse(n.is_leaf())
        self.assertEqual(n.low, 60)


class TestBuildTree(unittest.TestCase):
    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            build_tree({})

    def test_root_weight(self):
        self.assertEqual(build_tree({97: 5, 98: 2, 99: 1}).weight, 8)

    def test_child_order(self):
        root = build_tree({97: 1, 98: 2})
        self.assertEqual((root.left.symbol, root.right.symbol), (97, 98))

    def test_ties_broken_by_low(self):
        # Inserted in reverse order: the result must not depend on the order of the dict.
        root = build_tree({99: 1, 98: 1, 97: 1})
        self.assertEqual(root.left.symbol, 99)
        self.assertEqual((root.right.left.symbol, root.right.right.symbol), (97, 98))


class TestCodeLengths(unittest.TestCase):
    def test_abracadabra(self):
        self.assertEqual(lengths_of(byte_frequencies("abracadabra")),
                         {97: 1, 114: 2, 98: 3, 99: 4, 100: 4})

    def test_single_symbol(self):
        self.assertEqual(lengths_of({97: 4}), {97: 1})

    def test_symbol_zero(self):
        self.assertEqual(lengths_of({0: 1, 97: 1}), {0: 1, 97: 1})

    def test_balanced(self):
        self.assertEqual(lengths_of({97: 1, 98: 1, 99: 1, 100: 1}), {97: 2, 98: 2, 99: 2, 100: 2})


class TestCanonicalCodes(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(canonical_codes({}), {})

    def test_leading_zeros(self):
        self.assertEqual(canonical_codes({97: 2, 98: 2}), {97: "00", 98: "01"})

    def test_mixed_lengths(self):
        self.assertEqual(canonical_codes({97: 1, 98: 2, 99: 3, 100: 3}),
                         {97: "0", 98: "10", 99: "110", 100: "111"})

    def test_symbol_order_within_a_length(self):
        self.assertEqual(canonical_codes({100: 2, 99: 2, 98: 2, 97: 2}),
                         {97: "00", 98: "01", 99: "10", 100: "11"})

    def test_abracadabra(self):
        self.assertEqual(canonical_codes(lengths_of(byte_frequencies("abracadabra"))),
                         {97: "0", 114: "10", 98: "110", 99: "1110", 100: "1111"})


class TestBitWriter(unittest.TestCase):
    def test_nothing(self):
        self.assertEqual(BitWriter().getvalue(), b"")

    def test_padding_on_the_right(self):
        w = BitWriter()
        w.write_code("101")
        self.assertEqual(w.getvalue(), b"\xa0")

    def test_full_byte(self):
        w = BitWriter()
        w.write_code("11000011")
        self.assertEqual(w.getvalue(), b"\xc3")

    def test_two_bytes(self):
        w = BitWriter()
        w.write_code("111111111")
        self.assertEqual(w.getvalue(), b"\xff\x80")


class TestBitReader(unittest.TestCase):
    def test_most_significant_bit_first(self):
        r = BitReader(b"\xa0")
        self.assertEqual([r.read_bit() for _ in range(8)], [1, 0, 1, 0, 0, 0, 0, 0])

    def test_out_of_bits(self):
        r = BitReader(b"\xff")
        for _ in range(8):
            r.read_bit()
        with self.assertRaises(ValueError):
            r.read_bit()

    def test_empty(self):
        with self.assertRaises(ValueError):
            BitReader(b"").read_bit()

    def test_bytes_used(self):
        r = BitReader(b"\x00\x00")
        self.assertEqual(r.bytes_used(), 0)
        r.read_bit()
        self.assertEqual(r.bytes_used(), 1)
        for _ in range(7):
            r.read_bit()
        self.assertEqual(r.bytes_used(), 1)
        r.read_bit()
        self.assertEqual(r.bytes_used(), 2)


class TestCompress(unittest.TestCase):
    def test_exact_bytes(self):
        self.assertEqual(compress("abracadabra"), ABRA_BYTES)

    def test_empty(self):
        self.assertEqual(compress(""), b"HUF1\x00\x00\x00\x00\x00\x00")

    def test_single_symbol(self):
        self.assertEqual(compress("aaa"), b"HUF1\x00\x01a\x01\x00\x00\x00\x03\x00")

    def test_size_counts_bytes(self):
        data = compress("é")
        self.assertEqual(data[10:14], b"\x00\x00\x00\x02")


class TestDecompress(unittest.TestCase):
    def test_known_bytes(self):
        self.assertEqual(decompress(ABRA_BYTES), "abracadabra")

    def test_round_trips(self):
        for text in SAMPLES:
            with self.subTest(text=text):
                self.assertEqual(decompress(compress(text)), text)

    def test_random_round_trips(self):
        rng = random.Random(7)
        alphabet = "abcdefgh é€😀\n\x00"
        for _ in range(50):
            text = "".join(rng.choice(alphabet) for _ in range(rng.randrange(1, 200)))
            self.assertEqual(decompress(compress(text)), text)

    def test_bad_magic(self):
        with self.assertRaises(ValueError):
            decompress(b"NOPE" + ABRA_BYTES[4:])

    def test_truncated_header(self):
        for cut in (2, 5, 8, 16, 18):
            with self.subTest(cut=cut):
                with self.assertRaises(ValueError):
                    decompress(ABRA_BYTES[:cut])

    def test_truncated_payload(self):
        with self.assertRaises(ValueError):
            decompress(ABRA_BYTES[:-1])

    def test_trailing_bytes(self):
        with self.assertRaises(ValueError):
            decompress(ABRA_BYTES + b"\x00")

    def test_zero_code_length(self):
        with self.assertRaises(ValueError):
            decompress(b"HUF1\x00\x01a\x00\x00\x00\x00\x00")

    def test_duplicate_symbol(self):
        with self.assertRaises(ValueError):
            decompress(b"HUF1\x00\x02a\x01a\x01\x00\x00\x00\x01\x00")

    def test_invalid_utf8(self):
        # One symbol (0xFF), which can never appear in valid UTF-8.
        with self.assertRaises(ValueError):
            decompress(b"HUF1\x00\x01\xff\x01\x00\x00\x00\x01\x00")


class TestUtf8Chars(unittest.TestCase):
    def test_all_widths(self):
        self.assertEqual(utf8_chars("aé€😀".encode()),
                         [b"a", "é".encode(), "€".encode(), "😀".encode()])

    def test_empty(self):
        self.assertEqual(utf8_chars(b""), [])

    def test_bad_lead(self):
        for data in (b"\x80", b"\xff", b"a\xf8\x80\x80\x80"):
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    utf8_chars(data)

    def test_truncated(self):
        with self.assertRaises(ValueError):
            utf8_chars("€".encode()[:2])

    def test_bad_continuation(self):
        with self.assertRaises(ValueError):
            utf8_chars(b"\xc3a")


class TestTruncate(unittest.TestCase):
    def test_does_not_split(self):
        self.assertEqual(truncate_utf8("héllo", 2), "h")

    def test_exact_fit(self):
        self.assertEqual(truncate_utf8("héllo", 3), "hé")

    def test_everything_fits(self):
        self.assertEqual(truncate_utf8("héllo", 6), "héllo")

    def test_zero(self):
        self.assertEqual(truncate_utf8("héllo", 0), "")


class TestFormatTable(unittest.TestCase):
    def test_example(self):
        self.assertEqual(format_table("aab c"), "a 2 0\n0x20 1 110\nb 1 111\nc 1 10")

    def test_empty(self):
        self.assertEqual(format_table(""), "")

    def test_non_ascii_labels(self):
        self.assertEqual(format_table("é"), "0xA9 1 0\n0xC3 1 1")

    def test_small_values_have_two_digits(self):
        self.assertEqual(format_table("\x07"), "0x07 1 0")


class TestArchive(unittest.TestCase):
    def test_add_get(self):
        a = Archive()
        a.add("doc", "héllo")
        self.assertEqual(a.get("doc"), "héllo")

    def test_stores_compressed_form(self):
        a = Archive()
        a.add("doc", "abracadabra")
        self.assertEqual(a.stats()["stored_bytes"], len(ABRA_BYTES))

    def test_replace(self):
        a = Archive()
        a.add("doc", "one")
        a.add("doc", "three")
        self.assertEqual(a.get("doc"), "three")
        self.assertEqual(len(a), 1)
        self.assertEqual(a.stats()["original_bytes"], 5)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Archive().add("", "x")

    def test_unknown_names(self):
        a = Archive()
        with self.assertRaises(KeyError):
            a.get("nope")
        with self.assertRaises(KeyError):
            a.remove("nope")

    def test_archives_are_independent(self):
        a, b = Archive(), Archive()
        a.add("only_in_a", "x")
        self.assertNotIn("only_in_a", b)
        self.assertEqual(len(b), 0)

    def test_names_and_iteration_sorted(self):
        a = Archive()
        for name in ("c", "a", "b"):
            a.add(name, name)
        self.assertEqual(a.names(), ["a", "b", "c"])
        self.assertEqual(list(a), ["a", "b", "c"])

    def test_contains(self):
        a = Archive()
        a.add("doc", "x")
        self.assertIn("doc", a)
        self.assertNotIn("other", a)

    def test_stats_counts_utf8_bytes(self):
        a = Archive()
        a.add("x", "é")
        a.add("y", "€")
        self.assertEqual(a.stats()["documents"], 2)
        self.assertEqual(a.stats()["original_bytes"], 5)

    def test_stats_after_remove(self):
        a = Archive()
        a.add("x", "abc")
        a.add("y", "de")
        a.remove("x")
        self.assertEqual(a.stats(), {"documents": 1, "original_bytes": 2, "stored_bytes": len(compress("de"))})
        self.assertNotIn("x", a)


if __name__ == "__main__":
    unittest.main()
