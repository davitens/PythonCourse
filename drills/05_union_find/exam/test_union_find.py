import random
import unittest

from union_find import UnionFind, kruskal


class TestUnionFind(unittest.TestCase):
    def test_singletons(self):
        uf = UnionFind("abc")
        self.assertEqual(uf.count, 3)
        self.assertFalse(uf.connected("a", "b"))
        self.assertEqual(uf.find("a"), "a")

    def test_union_and_connected(self):
        uf = UnionFind("abcd")
        self.assertTrue(uf.union("a", "b"))
        self.assertTrue(uf.union("c", "d"))
        self.assertTrue(uf.connected("b", "a"))
        self.assertFalse(uf.connected("a", "c"))
        self.assertEqual(uf.count, 2)

    def test_union_same_set(self):
        uf = UnionFind("abc")
        uf.union("a", "b")
        self.assertFalse(uf.union("b", "a"))
        self.assertFalse(uf.union("a", "a"))
        self.assertEqual(uf.count, 2)

    def test_sizes(self):
        uf = UnionFind(range(6))
        uf.union(0, 1)
        uf.union(2, 3)
        uf.union(0, 2)
        uf.union(4, 0)
        self.assertEqual(uf.size_of(3), 5)
        self.assertEqual(uf.size_of(5), 1)

    def test_union_by_size_root(self):
        uf = UnionFind("abcd")
        uf.union("a", "b")   # equal sizes: b's root goes under a -> root a
        self.assertEqual(uf.find("b"), "a")
        uf.union("c", "a")   # {c} is smaller than {a, b}: c goes under a
        self.assertEqual(uf.find("c"), "a")

    def test_find_returns_root_on_deep_path(self):
        uf = UnionFind("abcd")
        uf.union("a", "b")
        uf.union("c", "d")
        uf.union("a", "c")   # c's root (c) goes under a; d -> c -> a is a path of length 2
        self.assertEqual(uf.find("d"), "a")
        self.assertEqual(uf.parent["d"], "a")   # path compressed

    def test_unknown_element(self):
        with self.assertRaises(KeyError):
            UnionFind("ab").find("z")

    def test_add(self):
        uf = UnionFind()
        uf.add(1)
        uf.add(1)
        uf.add(2)
        self.assertEqual(uf.count, 2)

    def test_groups(self):
        uf = UnionFind([5, 3, 1, 4, 2])
        uf.union(5, 1)
        uf.union(4, 2)
        self.assertEqual(uf.groups(), [[1, 5], [2, 4], [3]])

    def test_random_against_naive(self):
        rng = random.Random(4)
        for _ in range(50):
            n = 12
            uf = UnionFind(range(n))
            label = list(range(n))          # naive: relabel whole groups
            for _ in range(15):
                a, b = rng.randrange(n), rng.randrange(n)
                expected_merge = label[a] != label[b]
                self.assertEqual(uf.union(a, b), expected_merge)
                old, new = label[b], label[a]
                label = [new if x == old else x for x in label]
            self.assertEqual(uf.count, len(set(label)))
            for x in range(n):
                self.assertEqual(uf.size_of(x), label.count(label[x]))


class TestKruskal(unittest.TestCase):
    def test_example(self):
        edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4)]
        self.assertEqual(kruskal(4, edges), (7, [(0, 1, 1), (1, 2, 2), (2, 3, 4)]))

    def test_unsorted_input(self):
        edges = [(2, 3, 4), (0, 2, 3), (1, 2, 2), (0, 1, 1)]
        self.assertEqual(kruskal(4, edges)[0], 7)

    def test_ties(self):
        edges = [(1, 2, 5), (0, 1, 5), (0, 2, 5)]
        self.assertEqual(kruskal(3, edges), (10, [(0, 1, 5), (0, 2, 5)]))

    def test_disconnected(self):
        with self.assertRaises(ValueError):
            kruskal(3, [(0, 1, 1)])

    def test_single_node(self):
        self.assertEqual(kruskal(1, []), (0, []))


if __name__ == "__main__":
    unittest.main()
