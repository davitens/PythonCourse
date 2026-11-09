import unittest

from graph_search import bfs_order, build_graph, dfs_order, grid_distance, has_cycle, shortest_path

EDGES = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "e"), ("d", "f"), ("e", "f")]


class TestBuildGraph(unittest.TestCase):
    def test_undirected(self):
        g = build_graph([("a", "b"), ("b", "c"), ("a", "b")])
        self.assertEqual(g, {"a": ["b"], "b": ["a", "c"], "c": ["b"]})

    def test_directed_includes_sinks(self):
        g = build_graph([("a", "b"), ("a", "c")], directed=True)
        self.assertEqual(g, {"a": ["b", "c"], "b": [], "c": []})


class TestTraversal(unittest.TestCase):
    def setUp(self):
        self.g = build_graph(EDGES)

    def test_bfs(self):
        self.assertEqual(bfs_order(self.g, "a"), ["a", "b", "c", "d", "e", "f"])

    def test_bfs_layers(self):
        g = build_graph([(1, 2), (1, 3), (2, 4), (3, 5), (4, 6)])
        self.assertEqual(bfs_order(g, 1), [1, 2, 3, 4, 5, 6])

    def test_dfs(self):
        self.assertEqual(dfs_order(self.g, "a"), ["a", "b", "d", "f", "e", "c"])

    def test_directed_bfs_from_sink(self):
        g = build_graph([("a", "b")], directed=True)
        self.assertEqual(bfs_order(g, "b"), ["b"])


class TestShortestPath(unittest.TestCase):
    def setUp(self):
        self.g = build_graph(EDGES + [("x", "y")])

    def test_path(self):
        self.assertEqual(shortest_path(self.g, "a", "f"), ["a", "b", "d", "f"])

    def test_same_node(self):
        self.assertEqual(shortest_path(self.g, "c", "c"), ["c"])

    def test_unreachable(self):
        self.assertIsNone(shortest_path(self.g, "a", "x"))


class TestGrid(unittest.TestCase):
    GRID = ["..#.",
            ".##.",
            "....",
            "#..."]

    def test_distance(self):
        self.assertEqual(grid_distance(self.GRID, (0, 0), (0, 3)), 7)

    def test_edges_of_grid(self):
        self.assertEqual(grid_distance(self.GRID, (3, 3), (3, 1)), 2)
        self.assertEqual(grid_distance(["...."], (0, 0), (0, 3)), 3)

    def test_unreachable_and_walls(self):
        self.assertEqual(grid_distance([".#."], (0, 0), (0, 2)), -1)
        self.assertEqual(grid_distance(self.GRID, (0, 0), (0, 2)), -1)


class TestCycle(unittest.TestCase):
    def test_cycle(self):
        self.assertTrue(has_cycle(build_graph([("a", "b"), ("b", "c"), ("c", "a")], directed=True)))
        self.assertTrue(has_cycle(build_graph([("a", "a")], directed=True)))

    def test_diamond_is_not_a_cycle(self):
        g = build_graph([("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")], directed=True)
        self.assertFalse(has_cycle(g))

    def test_cycle_not_reachable_from_first_node(self):
        g = build_graph([("a", "b"), ("c", "d"), ("d", "c")], directed=True)
        self.assertTrue(has_cycle(g))


if __name__ == "__main__":
    unittest.main()
