"""Day 6 - Exercise 3: portfolio ledger (reference solution). Fixes marked # FIX.

SPEC
====
Money is handled as integer CENTS everywhere.

parse_amount(s) -> int cents
    "150.25" -> 15025, "150.5" -> 15050, "150" -> 15000, "-3.10" -> -310, "-0.05" -> -5
    More than 2 decimals, empty string or non-numeric -> ValueError.

format_amount(cents) -> str with exactly 2 decimals: 15025 -> "150.25", -310 -> "-3.10",
    5 -> "0.05", -5 -> "-0.05", 0 -> "0.00"

Portfolio(cash)  (cash in cents)
    buy(symbol, qty, price): cost = qty * price. If cost > cash -> ValueError (an exactly
        sufficient balance is fine). Increases the position's qty and total_cost.
    sell(symbol, qty, price) -> realized profit (cents) of this sale.
        Selling more than held (or a symbol not held) -> ValueError.
        cost_basis = total_cost * qty // held       (integer floor division)
        profit     = qty * price - cost_basis
        The position's qty and total_cost decrease by qty and cost_basis; a position
        that reaches qty 0 is removed. Cash increases by qty * price.
        Accumulate profit into `realized`.
    dividend(symbol, amount): adds amount to cash and to `dividends`.
    avg_cost(symbol) -> total_cost // qty for a held symbol (ValueError if not held).

process(lines, cash) -> Portfolio
    Each line: "<date> <ACTION> <SYMBOL> <QTY> <PRICE>" for BUY/SELL,
               "<date> DIVIDEND <SYMBOL> <AMOUNT>".
    ACTION is case-insensitive, SYMBOL is upper-cased. Fields are separated by any whitespace.
    '#' starts a comment (whole line or trailing). Blank/comment-only lines are skipped.
    Any problem (bad action, wrong field count, bad number, a ValueError from the
    Portfolio) -> ValueError whose message starts with "line N: " where N is the 1-based
    line number in `lines` (blank and comment lines count).

report(portfolio) -> str, lines joined with "\\n":
    CASH <amount>
    <SYMBOL> <qty> @ <avg_cost>      one line per position, sorted by symbol
    REALIZED <amount>
    DIVIDENDS <amount>
"""


def parse_amount(s):
    s = s.strip()
    if not s:
        raise ValueError("empty amount")
    negative = s.startswith("-")
    if negative:
        s = s[1:]
    whole, _, frac = s.partition(".")
    if not whole.isdigit() or (frac and not frac.isdigit()) or len(frac) > 2:
        raise ValueError(f"bad amount {s!r}")
    cents = int(whole) * 100 + int(frac.ljust(2, "0"))  # FIX: frac was not right-padded
    return -cents if negative else cents  # FIX: sign was applied to the whole part only


def format_amount(cents):
    sign = "-" if cents < 0 else ""
    whole, frac = divmod(abs(cents), 100)  # FIX: was divmod(cents, 100) (wrong for negatives)
    return f"{sign}{whole}.{frac:02d}"


class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.positions = {}  # symbol -> [qty, total_cost]
        self.realized = 0
        self.dividends = 0

    def buy(self, symbol, qty, price):
        cost = qty * price
        if cost > self.cash:  # FIX: was >= (exactly enough cash was rejected)
            raise ValueError("insufficient cash")
        pos = self.positions.setdefault(symbol, [0, 0])
        pos[0] += qty
        pos[1] += cost
        self.cash -= cost

    def sell(self, symbol, qty, price):
        if symbol not in self.positions or self.positions[symbol][0] < qty:
            raise ValueError("not enough shares")
        held, total_cost = self.positions[symbol]
        cost_basis = total_cost * qty // held  # FIX: was avg_cost(symbol) * qty
        profit = qty * price - cost_basis
        self.positions[symbol] = [held - qty, total_cost - cost_basis]
        if held - qty == 0:
            del self.positions[symbol]
        self.cash += qty * price
        self.realized += profit
        return profit

    def dividend(self, symbol, amount):
        self.cash += amount
        self.dividends += amount

    def avg_cost(self, symbol):
        if symbol not in self.positions:
            raise ValueError("not held")
        qty, total_cost = self.positions[symbol]
        return total_cost // qty


def process(lines, cash):
    p = Portfolio(cash)
    for n, raw in enumerate(lines, start=1):  # FIX: was enumerate(lines) (0-based)
        line = raw.split("#", 1)[0]  # FIX: trailing comments were not removed
        parts = line.split()
        if not parts:
            continue
        try:
            action = parts[1].upper() if len(parts) > 1 else ""  # FIX: action not upper-cased
            if action in ("BUY", "SELL"):
                if len(parts) != 5:
                    raise ValueError("expected 5 fields")
                symbol, qty, price = parts[2].upper(), int(parts[3]), parse_amount(parts[4])
                if action == "BUY":
                    p.buy(symbol, qty, price)
                else:
                    p.sell(symbol, qty, price)
            elif action == "DIVIDEND":
                if len(parts) != 4:
                    raise ValueError("expected 4 fields")
                p.dividend(parts[2].upper(), parse_amount(parts[3]))
            else:
                raise ValueError(f"unknown action {action!r}")
        except ValueError as e:
            raise ValueError(f"line {n}: {e}")
    return p


def report(p):
    out = [f"CASH {format_amount(p.cash)}"]
    for symbol in sorted(p.positions):  # FIX: positions were not sorted
        qty = p.positions[symbol][0]
        out.append(f"{symbol} {qty} @ {format_amount(p.avg_cost(symbol))}")
    out.append(f"REALIZED {format_amount(p.realized)}")
    out.append(f"DIVIDENDS {format_amount(p.dividends)}")
    return "\n".join(out)
