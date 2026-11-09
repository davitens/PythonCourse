import unittest

from ex01_bank import BankAccount, InsufficientFunds


class TestBankAccount(unittest.TestCase):
    def test_initial(self):
        acc = BankAccount("Ana")
        self.assertEqual(acc.balance, 0)
        self.assertEqual(acc.history, [])
        self.assertEqual(BankAccount("Bo", 50).balance, 50)

    def test_negative_initial(self):
        with self.assertRaises(ValueError):
            BankAccount("Ana", -1)

    def test_deposit_withdraw(self):
        acc = BankAccount("Ana", 10)
        self.assertEqual(acc.deposit(5), 15)
        self.assertEqual(acc.withdraw(15), 0)
        self.assertEqual(acc.history, [("deposit", 5), ("withdraw", 15)])

    def test_invalid_amounts(self):
        acc = BankAccount("Ana", 10)
        for bad in (0, -5):
            with self.assertRaises(ValueError):
                acc.deposit(bad)
            with self.assertRaises(ValueError):
                acc.withdraw(bad)
        self.assertEqual(acc.balance, 10)
        self.assertEqual(acc.history, [])

    def test_insufficient(self):
        acc = BankAccount("Ana", 10)
        with self.assertRaises(InsufficientFunds):
            acc.withdraw(11)
        self.assertEqual(acc.balance, 10)
        self.assertEqual(acc.history, [])

    def test_custom_exception_type(self):
        self.assertTrue(issubclass(InsufficientFunds, Exception))

    def test_transfer(self):
        a, b = BankAccount("A", 100), BankAccount("B")
        a.transfer_to(b, 30)
        self.assertEqual((a.balance, b.balance), (70, 30))
        self.assertEqual(a.history, [("transfer_out", 30)])
        self.assertEqual(b.history, [("transfer_in", 30)])

    def test_transfer_errors(self):
        a, b = BankAccount("A", 10), BankAccount("B")
        with self.assertRaises(InsufficientFunds):
            a.transfer_to(b, 11)
        with self.assertRaises(ValueError):
            a.transfer_to(a, 1)
        self.assertEqual((a.balance, b.balance), (10, 0))
        self.assertEqual(b.history, [])

    def test_histories_independent(self):
        a, b = BankAccount("A"), BankAccount("B")
        a.deposit(1)
        self.assertEqual(b.history, [])

    def test_repr(self):
        self.assertEqual(repr(BankAccount("Ana", 10)), "BankAccount(owner='Ana', balance=10)")


if __name__ == "__main__":
    unittest.main()
