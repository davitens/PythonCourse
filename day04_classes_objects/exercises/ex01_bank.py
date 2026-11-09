"""Day 4 - Exercise 1: BankAccount. Implement the class to match the docstrings."""


class InsufficientFunds(Exception):
    """Raised when a withdrawal or transfer exceeds the balance."""


class BankAccount:
    """A simple bank account.

    - BankAccount(owner, balance=0). A negative initial balance raises ValueError.
    - history is a list of (operation, amount) tuples, in order. Operations are
      "deposit", "withdraw", "transfer_out", "transfer_in". Failed operations are
      NOT recorded and must not change the balance.
    - repr(acc) == "BankAccount(owner='Ana', balance=10)"
    """

    def __init__(self, owner, balance=0):
        raise NotImplementedError

    def deposit(self, amount):
        """Add amount (> 0, else ValueError). Return the new balance."""
        raise NotImplementedError

    def withdraw(self, amount):
        """Remove amount (> 0, else ValueError; > balance -> InsufficientFunds).
        Return the new balance."""
        raise NotImplementedError

    def transfer_to(self, other, amount):
        """Move amount from self to other. Same validation as withdraw. Transferring to
        the same account raises ValueError. Records "transfer_out" on self and
        "transfer_in" on other."""
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError
