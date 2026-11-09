import random
import unittest

from lru_cache import LRUCache


class TestLRU(unittest.TestCase):
    def test_capacity_validation(self):
        with self.assertRaises(ValueError):
            LRUCache(0)
        with self.assertRaises(ValueError):
            LRUCache(-3)

    def test_put_get(self):
        c = LRUCache(2)
        self.assertIsNone(c.put("a", 1))
        self.assertEqual(c.get("a"), 1)
        self.assertEqual(len(c), 1)

    def test_missing(self):
        c = LRUCache(2)
        self.assertIsNone(c.get("x"))
        self.assertEqual(c.get("x", "dflt"), "dflt")

    def test_evicts_lru(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        self.assertEqual(c.put("c", 3), "a")
        self.assertIsNone(c.get("a"))
        self.assertEqual(c.keys(), ["b", "c"])

    def test_fills_to_capacity(self):
        c = LRUCache(3)
        for k in "abc":
            self.assertIsNone(c.put(k, k))
        self.assertEqual(len(c), 3)

    def test_get_refreshes(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        c.get("a")
        self.assertEqual(c.put("c", 3), "b")
        self.assertEqual(c.keys(), ["a", "c"])

    def test_update_refreshes(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        self.assertIsNone(c.put("a", 10))
        self.assertEqual(len(c), 2)
        self.assertEqual(c.put("c", 3), "b")
        self.assertEqual(c.get("a"), 10)

    def test_peek_does_not_refresh(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        self.assertEqual(c.peek("a"), 1)
        self.assertEqual(c.put("c", 3), "a")

    def test_contains_does_not_refresh(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        self.assertIn("a", c)
        self.assertNotIn("z", c)
        self.assertEqual(c.keys(), ["a", "b"])

    def test_delete(self):
        c = LRUCache(3)
        for k in "abc":
            c.put(k, k)
        self.assertTrue(c.delete("b"))
        self.assertFalse(c.delete("b"))
        self.assertEqual(len(c), 2)
        self.assertEqual(c.keys(), ["a", "c"])

    def test_delete_then_evict(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        c.delete("a")
        self.assertIsNone(c.put("c", 3))
        self.assertEqual(c.put("d", 4), "b")
        self.assertEqual(c.keys(), ["c", "d"])

    def test_capacity_one(self):
        c = LRUCache(1)
        c.put("a", 1)
        self.assertEqual(c.put("b", 2), "a")
        self.assertEqual(c.keys(), ["b"])

    def test_resize(self):
        c = LRUCache(4)
        for k in "abcd":
            c.put(k, k)
        c.get("a")
        self.assertEqual(c.resize(2), ["b", "c"])
        self.assertEqual(c.keys(), ["d", "a"])
        self.assertEqual(c.resize(5), [])

    def test_resize_invalid(self):
        with self.assertRaises(ValueError):
            LRUCache(2).resize(0)

    def test_random_against_reference(self):
        rng = random.Random(6)
        for _ in range(30):
            cap = rng.randint(1, 4)
            c = LRUCache(cap)
            ref = []                                  # list of (key, value), LRU first
            for _ in range(60):
                op, k = rng.choice("gpd"), rng.choice("abcdef")
                idx = next((i for i, (kk, _) in enumerate(ref) if kk == k), None)
                if op == "g":
                    expected = None if idx is None else ref[idx][1]
                    if idx is not None:
                        ref.append(ref.pop(idx))
                    self.assertEqual(c.get(k), expected)
                elif op == "p":
                    v = rng.randint(0, 99)
                    if idx is not None:
                        ref.pop(idx)
                    ref.append((k, v))
                    expected = ref.pop(0)[0] if len(ref) > cap else None
                    self.assertEqual(c.put(k, v), expected)
                else:
                    self.assertEqual(c.delete(k), idx is not None)
                    if idx is not None:
                        ref.pop(idx)
                self.assertEqual(c.keys(), [kk for kk, _ in ref])


if __name__ == "__main__":
    unittest.main()
