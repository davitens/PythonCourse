import unittest

from dijkstra import dijkstra, shortest_path, validate, within

G = {
    "s": [("a", 1), ("b", 4)],
    "a": [("b", 2), ("c", 6)],
    "b": [("c", 1)],
}

# Popping in the wrong order makes "b" final with cost 4 before the cheaper route via "a" is seen.
TRAP = {
    "s": [("a", 1), ("b", 4)],
    "a": [("b", 1)],
    "b": [("c", 1)],
}


class TestDijkstra(unittest.TestCase):
    def test_distances(self):
        dist, _ = dijkstra(G, "s")
        self.assertEqual(dist, {"s": 0, "a": 1, "b": 3, "c": 4})

    def test_prev(self):
        _, prev = dijkstra(G, "s")
        self.assertEqual(prev, {"a": "s", "b": "a", "c": "b"})

    def test_pop_order_matters(self):
        dist, _ = dijkstra(TRAP, "s")
        self.assertEqual(dist["c"], 3)

    def test_unreachable_not_in_dist(self):
        g = {"s": [("a", 1)], "x": [("s", 1)]}
        dist, _ = dijkstra(g, "s")
        self.assertEqual(dist, {"s": 0, "a": 1})

    def test_target_only_node(self):
        dist, _ = dijkstra({"s": [("t", 5)]}, "t")
        self.assertEqual(dist, {"t": 0})

    def test_zero_weights(self):
        dist, _ = dijkstra({"s": [("a", 0)], "a": [("b", 0)]}, "s")
        self.assertEqual(dist, {"s": 0, "a": 0, "b": 0})

    def test_tie_keeps_first_found(self):
        # s->a->t and s->b->t both cost 2; a is finalized first, so t keeps prev "a"
        g = {"s": [("a", 1), ("b", 1)], "a": [("t", 1)], "b": [("t", 1)]}
        _, prev = dijkstra(g, "s")
        self.assertEqual(prev["t"], "a")

    def test_negative_weight(self):
        with self.assertRaises(ValueError):
            dijkstra({"s": [("a", -1)]}, "s")
        with self.assertRaises(ValueError):
            validate({"s": [("a", 1)], "a": [("b", -3)]})


class TestShortestPath(unittest.TestCase):
    def test_path(self):
        self.assertEqual(shortest_path(G, "s", "c"), (4, ["s", "a", "b", "c"]))

    def test_one_edge(self):
        self.assertEqual(shortest_path(G, "a", "b"), (2, ["a", "b"]))

    def test_same_node(self):
        self.assertEqual(shortest_path(G, "b", "b"), (0, ["b"]))

    def test_unreachable(self):
        self.assertIsNone(shortest_path(G, "c", "s"))


class TestWithin(unittest.TestCase):
    def test_within(self):
        self.assertEqual(within(G, "s", 3), [(0, "s"), (1, "a"), (3, "b")])

    def test_sorted_by_cost_then_node(self):
        g = {"s": [("z", 1), ("y", 1), ("x", 2)]}
        self.assertEqual(within(g, "s", 10), [(0, "s"), (1, "y"), (1, "z"), (2, "x")])

    def test_zero_budget(self):
        self.assertEqual(within(G, "s", 0), [(0, "s")])


if __name__ == "__main__":
    unittest.main()
