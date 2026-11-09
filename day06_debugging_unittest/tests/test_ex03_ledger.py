import unittest

from ex03_ledger import Portfolio, format_amount, parse_amount, process, report


class TestParseAmount(unittest.TestCase):
    def test_values(self):
        cases = {"150.25": 15025, "150": 15000, "0.05": 5, "7.00": 700}
        for s, cents in cases.items():
            with self.subTest(s=s):
                self.assertEqual(parse_amount(s), cents)

    def test_one_decimal(self):
        self.assertEqual(parse_amount("150.5"), 15050)

    def test_negative(self):
        self.assertEqual(parse_amount("-3.10"), -310)
        self.assertEqual(parse_amount("-0.05"), -5)

    def test_invalid(self):
        for bad in ["", "abc", "1.234", "1.2.3", "--1", "1,5"]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    parse_amount(bad)


class TestFormatAmount(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(format_amount(15025), "150.25")
        self.assertEqual(format_amount(5), "0.05")
        self.assertEqual(format_amount(0), "0.00")

    def test_negative(self):
        self.assertEqual(format_amount(-310), "-3.10")
        self.assertEqual(format_amount(-5), "-0.05")


class TestPortfolio(unittest.TestCase):
    def test_buy(self):
        p = Portfolio(10000)
        p.buy("AAPL", 2, 1000)
        p.buy("AAPL", 1, 4000)
        self.assertEqual(p.cash, 4000)
        self.assertEqual(p.avg_cost("AAPL"), 2000)

    def test_buy_exact_cash(self):
        p = Portfolio(1000)
        p.buy("X", 1, 1000)
        self.assertEqual(p.cash, 0)

    def test_buy_insufficient(self):
        p = Portfolio(999)
        with self.assertRaises(ValueError):
            p.buy("X", 1, 1000)

    def test_sell_profit(self):
        p = Portfolio(10000)
        p.buy("X", 4, 1000)
        self.assertEqual(p.sell("X", 2, 1500), 1000)
        self.assertEqual(p.cash, 9000)
        self.assertEqual(p.realized, 1000)

    def test_sell_uses_exact_cost_basis(self):
        p = Portfolio(10000)
        p.buy("X", 2, 33)
        p.buy("X", 1, 34)                  # 3 shares that cost 100 cents in total
        self.assertEqual(p.sell("X", 1, 50), 50 - 33)
        self.assertEqual(p.sell("X", 2, 50), 100 - 67)
        self.assertNotIn("X", p.positions)

    def test_sell_errors(self):
        p = Portfolio(10000)
        p.buy("X", 1, 100)
        with self.assertRaises(ValueError):
            p.sell("X", 2, 100)
        with self.assertRaises(ValueError):
            p.sell("Y", 1, 100)


SAMPLE = [
    "# my trades",
    "2024-01-02 BUY aapl 10 150.25",
    "",
    "2024-01-03 buy MSFT 5 300   # first msft",
    "2024-02-01 SELL AAPL 4 160.5",
    "2024-03-01 Dividend MSFT 7.5",
    "2024-03-02 BUY GOOG 1 99.99",
]


class TestProcess(unittest.TestCase):
    def test_sample_report(self):
        p = process(SAMPLE, parse_amount("5000"))
        self.assertEqual(report(p), "\n".join([
            "CASH 2547.01",
            "AAPL 6 @ 150.25",
            "GOOG 1 @ 99.99",
            "MSFT 5 @ 300.00",
            "REALIZED 41.00",
            "DIVIDENDS 7.50",
        ]))

    def test_empty(self):
        p = process(["", "  # nothing"], 100)
        self.assertEqual(report(p), "CASH 1.00\nREALIZED 0.00\nDIVIDENDS 0.00")

    def test_error_line_number(self):
        lines = ["# header", "2024-01-01 BUY X 1 1.00", "2024-01-02 SELL X 5 1.00"]
        with self.assertRaisesRegex(ValueError, r"^line 3: "):
            process(lines, 10000)

    def test_unknown_action(self):
        with self.assertRaisesRegex(ValueError, r"^line 1: "):
            process(["2024-01-01 HOLD X 1 1.00"], 100)

    def test_bad_field_count(self):
        with self.assertRaisesRegex(ValueError, r"^line 2: "):
            process(["", "2024-01-01 BUY X 1"], 100)

    def test_negative_realized(self):
        p = process(["d BUY X 2 10", "d SELL X 2 9.5"], 10000)
        self.assertIn("REALIZED -1.00", report(p))


if __name__ == "__main__":
    unittest.main()
