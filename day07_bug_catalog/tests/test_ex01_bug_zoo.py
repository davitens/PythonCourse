import unittest

import ex01_bug_zoo as z


class TestBugZoo(unittest.TestCase):
    def test_make_grid(self):
        g = z.make_grid(2, 3, 0)
        g[0][0] = 1
        self.assertEqual(g, [[1, 0, 0], [0, 0, 0]])

    def test_sorted_copy(self):
        data = [3, 1, 2]
        self.assertEqual(z.sorted_copy(data), [1, 2, 3])
        self.assertEqual(data, [3, 1, 2])

    def test_collect(self):
        self.assertEqual(z.collect(1), [1])
        self.assertEqual(z.collect(2), [2])
        b = [0]
        self.assertIs(z.collect(5, b), b)

    def test_get_or_default(self):
        self.assertEqual(z.get_or_default({"a": 0}, "a", 9), 0)
        self.assertEqual(z.get_or_default({"a": ""}, "a", "x"), "")
        self.assertEqual(z.get_or_default({}, "a", 9), 9)

    def test_remove_negatives(self):
        nums = [-1, -2, 3, -4, -5, 6]
        out = z.remove_negatives(nums)
        self.assertIs(out, nums)
        self.assertEqual(nums, [3, 6])

    def test_find_index(self):
        self.assertEqual(z.find_index([5, 6, 7], 7), 2)
        self.assertEqual(z.find_index([5, 6, 7], 8), -1)

    def test_count_in_range(self):
        self.assertEqual(z.count_in_range([1, 2, 3, 4, 5], 2, 4), 3)

    def test_last_word_length(self):
        self.assertEqual(z.last_word_length("fly me   to   the moon  "), 4)
        self.assertEqual(z.last_word_length(""), 0)
        self.assertEqual(z.last_word_length("   "), 0)

    def test_median(self):
        self.assertEqual(z.median([3, 1, 2]), 2)
        self.assertEqual(z.median([4, 1, 3, 2]), 2.5)

    def test_same_contents(self):
        self.assertTrue(z.same_contents([1, 2], [1, 2]))
        self.assertFalse(z.same_contents([1, 2], [2, 1]))

    def test_round_half_up(self):
        self.assertEqual([z.round_half_up(x) for x in (0.5, 1.5, 2.5, 2.4, 2.6)], [1, 2, 3, 2, 3])

    def test_parse_bool(self):
        self.assertTrue(z.parse_bool(" TRUE "))
        self.assertTrue(z.parse_bool("yes"))
        self.assertTrue(z.parse_bool("1"))
        self.assertFalse(z.parse_bool("false"))
        self.assertFalse(z.parse_bool("0"))
        self.assertFalse(z.parse_bool(""))

    def test_sort_people(self):
        people = [("bob", 30), ("amy", 25), ("cat", 30), ("dan", 25)]
        self.assertEqual(z.sort_people(people),
                         [("bob", 30), ("cat", 30), ("amy", 25), ("dan", 25)])

    def test_join_numbers(self):
        self.assertEqual(z.join_numbers([1, 2, 3]), "1,2,3")
        self.assertEqual(z.join_numbers([]), "")

    def test_word_counts(self):
        self.assertEqual(z.word_counts(["a", "b", "a"]), {"a": 2, "b": 1})

    def test_clone_config(self):
        cfg = {"db": {"port": 1}}
        c = z.clone_config(cfg)
        c["db"]["port"] = 2
        self.assertEqual(cfg, {"db": {"port": 1}})

    def test_first_byte(self):
        self.assertEqual(z.first_byte(b"abc"), b"a")
        self.assertEqual(z.first_byte(b""), b"")

    def test_utf8_size(self):
        self.assertEqual(z.utf8_size("abc"), 3)
        self.assertEqual(z.utf8_size("é€😀"), 9)

    def test_factorial(self):
        self.assertEqual(z.factorial(5), 120)
        self.assertEqual(z.factorial(1), 1)
        self.assertEqual(z.factorial(0), 1)

    def test_merge_sorted(self):
        self.assertEqual(z.merge_sorted([1, 4, 9], [2, 3]), [1, 2, 3, 4, 9])
        self.assertEqual(z.merge_sorted([], [1]), [1])

    def test_is_leap(self):
        self.assertEqual([y for y in (1900, 2000, 2023, 2024, 2100) if z.is_leap(y)], [2000, 2024])

    def test_swap_pairs(self):
        self.assertEqual(z.swap_pairs([1, 2, 3, 4, 5]), [2, 1, 4, 3, 5])
        self.assertEqual(z.swap_pairs([1, 2]), [2, 1])

    def test_strip_lines(self):
        self.assertEqual(z.strip_lines("  a \n b\n"), ["a", "b"])


if __name__ == "__main__":
    unittest.main()
