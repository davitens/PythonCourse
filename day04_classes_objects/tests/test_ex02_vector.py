import unittest

from ex02_vector import Vector2D


class TestVector(unittest.TestCase):
    def test_add_sub(self):
        self.assertEqual(Vector2D(1, 2) + Vector2D(3, 4), Vector2D(4, 6))
        self.assertEqual(Vector2D(1, 2) - Vector2D(3, 4), Vector2D(-2, -2))

    def test_add_non_vector(self):
        with self.assertRaises(TypeError):
            Vector2D(1, 2) + 5

    def test_scale(self):
        self.assertEqual(Vector2D(1, -2) * 3, Vector2D(3, -6))
        self.assertEqual(3 * Vector2D(1, -2), Vector2D(3, -6))

    def test_abs(self):
        self.assertAlmostEqual(abs(Vector2D(3, 4)), 5.0)

    def test_eq(self):
        self.assertEqual(Vector2D(1, 1), Vector2D(1, 1))
        self.assertNotEqual(Vector2D(1, 1), Vector2D(1, 2))
        self.assertNotEqual(Vector2D(1, 1), (1, 1))

    def test_hashable(self):
        s = {Vector2D(1, 1), Vector2D(1, 1), Vector2D(2, 0)}
        self.assertEqual(len(s), 2)
        d = {Vector2D(0, 0): "origin"}
        self.assertEqual(d[Vector2D(0, 0)], "origin")

    def test_unpack(self):
        x, y = Vector2D(7, 8)
        self.assertEqual((x, y), (7, 8))

    def test_dot(self):
        self.assertEqual(Vector2D(1, 2).dot(Vector2D(3, 4)), 11)

    def test_repr(self):
        self.assertEqual(repr(Vector2D(1, 2)), "Vector2D(1, 2)")
        self.assertEqual(repr([Vector2D(0, 1.5)]), "[Vector2D(0, 1.5)]")


if __name__ == "__main__":
    unittest.main()
