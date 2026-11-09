import unittest

from toposort import build_order, levels, longest_chain, topo_sort


def respects(order, edges):
    pos = {n: i for i, n in enumerate(order)}
    return all(pos[a] < pos[b] for a, b in edges)


class TestTopoSort(unittest.TestCase):
    def test_example(self):
        edges = [("a", "c"), ("b", "c"), ("c", "d"), ("b", "d")]
        self.assertEqual(topo_sort(["a", "b", "c", "d"], edges), ["a", "b", "c", "d"])

    def test_smallest_available_first(self):
        edges = [(3, 1), (2, 1)]
        self.assertEqual(topo_sort([1, 2, 3, 4], edges), [2, 3, 1, 4])

    def test_nodes_only_in_edges(self):
        self.assertEqual(topo_sort([], [("x", "y")]), ["x", "y"])

    def test_isolated_nodes(self):
        self.assertEqual(topo_sort(["c", "a", "b"], []), ["a", "b", "c"])

    def test_duplicate_edges(self):
        self.assertEqual(topo_sort(["a", "b"], [("a", "b"), ("a", "b")]), ["a", "b"])

    def test_cycle(self):
        with self.assertRaises(ValueError):
            topo_sort(["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")])
        with self.assertRaises(ValueError):
            topo_sort([], [("a", "a")])

    def test_cycle_among_edge_only_nodes(self):
        with self.assertRaises(ValueError):
            topo_sort(["z"], [("p", "q"), ("q", "p")])

    def test_order_valid_on_bigger_graph(self):
        edges = [(i, j) for i in range(10) for j in range(i + 1, 10) if (i * j) % 3 == 1]
        order = topo_sort(list(range(10)), edges)
        self.assertEqual(sorted(order), list(range(10)))
        self.assertTrue(respects(order, edges))


class TestBuildOrder(unittest.TestCase):
    def test_dependencies_first(self):
        order = build_order({"shoes": ["socks", "pants"], "pants": ["underwear"],
                             "socks": [], "underwear": []})
        self.assertEqual(order, ["socks", "underwear", "pants", "shoes"])

    def test_simple(self):
        self.assertEqual(build_order({"b": ["a"], "a": []}), ["a", "b"])


class TestLevels(unittest.TestCase):
    def test_levels(self):
        edges = [("a", "c"), ("b", "c"), ("c", "d"), ("b", "e")]
        self.assertEqual(levels(["a", "b", "c", "d", "e"], edges), [["a", "b"], ["c", "e"], ["d"]])

    def test_levels_cycle(self):
        with self.assertRaises(ValueError):
            levels(["a"], [("a", "b"), ("b", "a")])


class TestLongestChain(unittest.TestCase):
    def test_chain(self):
        edges = [("a", "b"), ("b", "c"), ("a", "c"), ("c", "d")]
        self.assertEqual(longest_chain(["a", "b", "c", "d"], edges), 4)

    def test_single_and_empty(self):
        self.assertEqual(longest_chain(["solo"], []), 1)
        self.assertEqual(longest_chain([], []), 0)

    def test_branches(self):
        edges = [("s", "a"), ("a", "b"), ("b", "t"), ("s", "t")]
        self.assertEqual(longest_chain([], edges), 4)


if __name__ == "__main__":
    unittest.main()
