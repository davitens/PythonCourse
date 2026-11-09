import itertools
import random
import unittest

from knapsack import count_ways, knapsack_01, knapsack_unbounded, min_coins

ITEMS = [(1, 1), (3, 4), (4, 5)]


def brute_01(items, capacity):
    best = 0
    for r in range(len(items) + 1):
        for combo in itertools.combinations(items, r):
            if sum(w for w, _ in combo) <= capacity:
                best = max(best, sum(v for _, v in combo))
    return best


class TestKnapsack01(unittest.TestCase):
    def test_example(self):
        self.assertEqual(knapsack_01(ITEMS, 7), (9, [1, 2]))

    def test_exact_capacity_used(self):
        self.assertEqual(knapsack_01([(5, 10)], 5), (10, [0]))

    def test_each_item_once(self):
        self.assertEqual(knapsack_01([(1, 10)], 5), (10, [0]))

    def test_nothing_fits(self):
        self.assertEqual(knapsack_01([(5, 10)], 4), (0, []))
        self.assertEqual(knapsack_01([], 10), (0, []))
        self.assertEqual(knapsack_01(ITEMS, 0), (0, []))

    def test_reconstruction_consistent(self):
        rng = random.Random(7)
        for _ in range(100):
            items = [(rng.randint(1, 6), rng.randint(1, 9)) for _ in range(rng.randint(1, 6))]
            cap = rng.randint(0, 15)
            value, chosen = knapsack_01(items, cap)
            self.assertEqual(value, brute_01(items, cap), (items, cap))
            self.assertEqual(sum(items[i][1] for i in chosen), value)
            self.assertLessEqual(sum(items[i][0] for i in chosen), cap)
            self.assertEqual(len(set(chosen)), len(chosen))


class TestUnbounded(unittest.TestCase):
    def test_example(self):
        self.assertEqual(knapsack_unbounded(ITEMS, 7), 9)
        self.assertEqual(knapsack_unbounded([(2, 3)], 7), 9)

    def test_reuse(self):
        self.assertEqual(knapsack_unbounded([(1, 10)], 5), 50)


class TestMinCoins(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(min_coins([1, 2, 5], 11), 3)
        self.assertEqual(min_coins([2], 3), -1)

    def test_zero(self):
        self.assertEqual(min_coins([1, 2, 5], 0), 0)
        self.assertEqual(min_coins([], 0), 0)

    def test_greedy_fails(self):
        self.assertEqual(min_coins([1, 3, 4], 6), 2)

    def test_exact_coin(self):
        self.assertEqual(min_coins([7, 3], 7), 1)


class TestCountWays(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(count_ways([1, 2, 5], 5), 4)
        self.assertEqual(count_ways([2], 3), 0)

    def test_order_does_not_matter(self):
        self.assertEqual(count_ways([1, 2], 3), 2)
        self.assertEqual(count_ways([1, 2, 3], 4), 4)

    def test_zero(self):
        self.assertEqual(count_ways([1, 2], 0), 1)

    def test_big(self):
        self.assertEqual(count_ways([1, 5, 10, 25], 100), 242)


if __name__ == "__main__":
    unittest.main()
