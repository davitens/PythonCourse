import unittest

from ex02_intervals import find_gaps, merge_intervals, total_covered


class TestMerge(unittest.TestCase):
    def test_sorted_input(self):
        self.assertEqual(merge_intervals([[1, 3], [2, 6], [8, 10]]), [[1, 6], [8, 10]])

    def test_unsorted_input(self):
        self.assertEqual(merge_intervals([[8, 10], [1, 3], [2, 6]]), [[1, 6], [8, 10]])

    def test_touching(self):
        self.assertEqual(merge_intervals([[1, 3], [3, 5]]), [[1, 5]])

    def test_contained(self):
        self.assertEqual(merge_intervals([[1, 10], [2, 3]]), [[1, 10]])

    def test_does_not_mutate(self):
        data = [[1, 3], [2, 4]]
        merge_intervals(data)
        self.assertEqual(data, [[1, 3], [2, 4]])

    def test_empty(self):
        self.assertEqual(merge_intervals([]), [])


class TestCovered(unittest.TestCase):
    def test_overlap_counted_once(self):
        self.assertEqual(total_covered([[0, 5], [3, 8]]), 8)

    def test_disjoint(self):
        self.assertEqual(total_covered([[0, 1], [5, 7]]), 3)


class TestGaps(unittest.TestCase):
    def test_gaps(self):
        self.assertEqual(find_gaps([[2, 3], [5, 6]], 0, 10), [[0, 2], [3, 5], [6, 10]])

    def test_no_gaps(self):
        self.assertEqual(find_gaps([[0, 4], [4, 10]], 0, 10), [])

    def test_empty(self):
        self.assertEqual(find_gaps([], 0, 3), [[0, 3]])


if __name__ == "__main__":
    unittest.main()
