import unittest

from ex01_bits import (clear_bit, count_set_bits, extract_bits, get_bit, is_power_of_two,
                       reverse_bits, set_bit, to_binary, toggle_bit)


class TestBits(unittest.TestCase):
    def test_get_bit(self):
        self.assertEqual([get_bit(0b1011, i) for i in range(5)], [1, 1, 0, 1, 0])

    def test_set_clear_toggle(self):
        self.assertEqual(set_bit(0b1000, 1), 0b1010)
        self.assertEqual(set_bit(0b1010, 1), 0b1010)
        self.assertEqual(clear_bit(0b1010, 3), 0b0010)
        self.assertEqual(clear_bit(0b1010, 0), 0b1010)
        self.assertEqual(toggle_bit(0b1010, 0), 0b1011)
        self.assertEqual(toggle_bit(0b1010, 1), 0b1000)

    def test_count(self):
        self.assertEqual(count_set_bits(0), 0)
        self.assertEqual(count_set_bits(0xFF), 8)
        self.assertEqual(count_set_bits(0b1010001), 3)

    def test_to_binary(self):
        self.assertEqual(to_binary(5, 8), "00000101")
        self.assertEqual(to_binary(0, 3), "000")
        self.assertEqual(to_binary(255, 8), "11111111")
        with self.assertRaises(ValueError):
            to_binary(256, 8)

    def test_extract(self):
        self.assertEqual(extract_bits(0b110110, 1, 3), 0b011)
        self.assertEqual(extract_bits(0xE282AC, 8, 8), 0x82)
        self.assertEqual(extract_bits(0x20AC, 12, 4), 0x2)
        self.assertEqual(extract_bits(0x20AC, 0, 6), 0b101100)

    def test_power_of_two(self):
        self.assertEqual([x for x in range(70) if is_power_of_two(x)], [1, 2, 4, 8, 16, 32, 64])

    def test_reverse(self):
        self.assertEqual(reverse_bits(0b0011, 4), 0b1100)
        self.assertEqual(reverse_bits(0b1, 8), 0b10000000)
        self.assertEqual(reverse_bits(0b10110, 5), 0b01101)


if __name__ == "__main__":
    unittest.main()
