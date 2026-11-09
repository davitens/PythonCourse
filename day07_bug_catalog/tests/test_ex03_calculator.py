import unittest

from ex03_calculator import calculate, evaluate, to_rpn, tokenize


class TestTokenize(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(tokenize("12 + 3.5"), [12, "+", 3.5])
        self.assertIsInstance(tokenize("2")[0], int)
        self.assertIsInstance(tokenize("2.0")[0], float)

    def test_unary(self):
        self.assertEqual(tokenize("-3"), ["u-", 3])
        self.assertEqual(tokenize("2*-3"), [2, "*", "u-", 3])
        self.assertEqual(tokenize("(-3)"), ["(", "u-", 3, ")"])
        self.assertEqual(tokenize("4-1"), [4, "-", 1])
        self.assertEqual(tokenize("(1)-1"), ["(", 1, ")", "-", 1])

    def test_errors(self):
        for bad in ["1.2.3", "2 $ 3", "."]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    tokenize(bad)


class TestRPN(unittest.TestCase):
    def test_precedence(self):
        self.assertEqual(to_rpn(tokenize("1 + 2 * 3")), [1, 2, 3, "*", "+"])

    def test_left_assoc(self):
        self.assertEqual(to_rpn(tokenize("8 - 3 - 2")), [8, 3, "-", 2, "-"])

    def test_right_assoc(self):
        self.assertEqual(to_rpn(tokenize("2 ^ 3 ^ 2")), [2, 3, 2, "^", "^"])

    def test_parens(self):
        self.assertEqual(to_rpn(tokenize("(1 + 2) * 3")), [1, 2, "+", 3, "*"])

    def test_mismatched(self):
        for bad in ["(1 + 2", "1 + 2)", ")("]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    to_rpn(tokenize(bad))


class TestCalculate(unittest.TestCase):
    def test_basic(self):
        cases = {"1 + 2 * 3": 7, "(1 + 2) * 3": 9, "10 / 4": 2.5, "8 - 3 - 2": 3,
                 "2 ^ 10": 1024, "2 ^ 3 ^ 2": 512, "100 / 10 / 5": 2}
        for expr, expected in cases.items():
            with self.subTest(expr=expr):
                self.assertEqual(calculate(expr), expected)

    def test_unary(self):
        cases = {"-3 + 5": 2, "2 * -3": -6, "-2 ^ 2": -4, "2 ^ -1": 0.5, "-(2 + 3)": -5,
                 "(-3) * (-(4))": 12, "--2": 2}
        for expr, expected in cases.items():
            with self.subTest(expr=expr):
                self.assertEqual(calculate(expr), expected)

    def test_floats(self):
        self.assertAlmostEqual(calculate("1.5 * 4"), 6.0)
        self.assertAlmostEqual(calculate("0.1 + 0.2"), 0.3)

    def test_nested(self):
        self.assertEqual(calculate("((2 + 3) * (7 - 2)) / 5"), 5)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate("1 / 0")

    def test_malformed(self):
        for bad in ["1 +", "* 2", "2 3", ""]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    calculate(bad)

    def test_evaluate_direct(self):
        self.assertEqual(evaluate([5, 2, "-"]), 3)
        self.assertEqual(evaluate([2, "u-"]), -2)


if __name__ == "__main__":
    unittest.main()
