import unittest

from ex04_fix_me import Basket, Playlist, Point, Rectangle, Team, Temperature


class TestFixMe(unittest.TestCase):
    def test_team_members_independent(self):
        a, b = Team("a"), Team("b")
        a.add("x")
        self.assertEqual(a.members, ["x"])
        self.assertEqual(b.members, [])

    def test_basket_independent(self):
        b1, b2 = Basket(), Basket()
        b1.add("egg")
        self.assertEqual(b2.items, [])

    def test_basket_copies_input(self):
        source = ["milk"]
        b = Basket(source)
        b.add("egg")
        self.assertEqual(source, ["milk"])
        self.assertEqual(b.items, ["milk", "egg"])

    def test_point_in_set(self):
        self.assertEqual(len({Point(1, 2), Point(1, 2)}), 1)

    def test_rectangle(self):
        self.assertEqual(Rectangle(2, 3).describe(), "rectangle with area 6")

    def test_temperature(self):
        t = Temperature(100)
        self.assertEqual(t.fahrenheit, 212)
        t.celsius = 0
        self.assertEqual(t.fahrenheit, 32)
        with self.assertRaises(ValueError):
            Temperature(-300)

    def test_playlist(self):
        p = Playlist().add("a").add("b")
        self.assertEqual(len(p), 2)
        self.assertEqual(list(p), ["a", "b"])


if __name__ == "__main__":
    unittest.main()
