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
        if balance < 0:
            raise ValueError("negative initial balance")
        self.owner = owner
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        """Add amount (> 0, else ValueError). Return the new balance."""
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.balance += amount
        self.history.append(("deposit", amount))
        return self.balance

    def withdraw(self, amount):
        """Remove amount (> 0, else ValueError; > balance -> InsufficientFunds).
        Return the new balance."""
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self.balance:
            raise InsufficientFunds(f"balance {self.balance} < {amount}")
        self.balance -= amount
        self.history.append(("withdraw", amount))
        return self.balance

    def transfer_to(self, other, amount):
        """Move amount from self to other. Same validation as withdraw. Transferring to
        the same account raises ValueError. Records "transfer_out" on self and
        "transfer_in" on other."""
        if other is self:
            raise ValueError("cannot transfer to the same account")
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self.balance:
            raise InsufficientFunds(f"balance {self.balance} < {amount}")
        self.balance -= amount
        other.balance += amount
        self.history.append(("transfer_out", amount))
        other.history.append(("transfer_in", amount))

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"
