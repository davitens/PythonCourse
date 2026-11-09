import unittest

from ex01_pdb_drill import moving_average, parse_matrix


class TestDrill(unittest.TestCase):
    def test_moving_average(self):
        self.assertEqual(moving_average([1, 2, 3, 4, 5], 2), [1.5, 2.5, 3.5, 4.5])
        self.assertEqual(moving_average([2, 4, 6, 8], 3), [4.0, 6.0])

    def test_moving_average_edges(self):
        self.assertEqual(moving_average([1, 2], 3), [])
        self.assertEqual(moving_average([1, 2], 0), [])
        self.assertEqual(moving_average([5], 1), [5.0])

    def test_parse_matrix(self):
        self.assertEqual(parse_matrix("1 2\n3  4\n\n5 6\n"), [[1, 2], [3, 4], [5, 6]])


if __name__ == "__main__":
    unittest.main()
