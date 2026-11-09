import unittest

from ex02_grouping import build_graph, group_anagrams, group_by, invert_dict, two_sum


class TestGroupAnagrams(unittest.TestCase):
    def test_example(self):
        self.assertEqual(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]),
                         [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]])

    def test_empty(self):
        self.assertEqual(group_anagrams([]), [])

    def test_case_sensitive(self):
        self.assertEqual(group_anagrams(["ab", "Ba", "ba"]), [["ab", "ba"], ["Ba"]])


class TestInvert(unittest.TestCase):
    def test_example(self):
        self.assertEqual(invert_dict({"c": 1, "b": 2, "a": 1}), {1: ["a", "c"], 2: ["b"]})


class TestGroupBy(unittest.TestCase):
    def test_by_length(self):
        self.assertEqual(group_by(["a", "bb", "c", "dd", "eee"], len),
                         {1: ["a", "c"], 2: ["bb", "dd"], 3: ["eee"]})

    def test_parity(self):
        self.assertEqual(group_by([1, 2, 3, 4], lambda x: x % 2), {1: [1, 3], 0: [2, 4]})


class TestTwoSum(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), (0, 1))

    def test_smallest_j(self):
        self.assertEqual(two_sum([1, 4, 3, 2, 5], 6), (1, 3))

    def test_duplicates(self):
        self.assertEqual(two_sum([3, 3, 3], 6), (0, 1))

    def test_none(self):
        self.assertIsNone(two_sum([1, 2], 10))

    def test_not_same_element(self):
        self.assertIsNone(two_sum([5], 10))


class TestGraph(unittest.TestCase):
    def test_graph(self):
        g = build_graph([("a", "b"), ("b", "c"), ("a", "b"), ("c", "c")])
        self.assertEqual(g, {"a": ["b"], "b": ["a", "c"], "c": ["b", "c"]})


if __name__ == "__main__":
    unittest.main()
