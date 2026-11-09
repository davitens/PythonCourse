import unittest

from ex04_fix_me import (add_item, build_index, low_stock, merge_inventories, remove_item,
                         total_units)


class TestInventory(unittest.TestCase):
    def test_add_item(self):
        inv = {"apple": 2}
        add_item(inv, "apple", 3)
        add_item(inv, "pear", 1)
        self.assertEqual(inv, {"apple": 5, "pear": 1})

    def test_remove_item(self):
        inv = {"apple": 5, "pear": 1}
        remove_item(inv, "apple", 2)
        remove_item(inv, "pear", 1)
        self.assertEqual(inv, {"apple": 3})

    def test_remove_errors(self):
        inv = {"apple": 1}
        with self.assertRaises(KeyError):
            remove_item(inv, "kiwi", 1)
        with self.assertRaises(ValueError):
            remove_item(inv, "apple", 2)

    def test_merge_new_dict(self):
        a, b = {"x": 1}, {"x": 2, "y": 3}
        self.assertEqual(merge_inventories(a, b), {"x": 3, "y": 3})
        self.assertEqual(a, {"x": 1})
        self.assertEqual(b, {"x": 2, "y": 3})

    def test_low_stock(self):
        inv = {"d": 1, "c": 2, "b": 1, "a": 9}
        self.assertEqual(low_stock(inv, 3), ["b", "d", "c"])

    def test_build_index(self):
        stores = {"north": {"apple": 1, "pear": 2}, "south": {"apple": 4}, "east": {"kiwi": 1}}
        self.assertEqual(build_index(stores),
                         {"apple": ["north", "south"], "pear": ["north"], "kiwi": ["east"]})

    def test_total_units(self):
        self.assertEqual(total_units({"n": {"a": 2, "b": 3}, "s": {"a": 10}}), 15)


if __name__ == "__main__":
    unittest.main()
