"""Day 7 - Exercise 3: expression calculator (reference solution). Fixes marked # FIX.

SPEC
====
tokenize(expr) -> list of tokens
    - numbers: a run of digits and '.'; with a '.' -> float, else int. "1.2.3" or "." -> ValueError
    - operators/parens: + - * / ^ ( )   (as 1-char strings)
    - a '-' is UNARY (token "u-") when it is the first token, or follows an operator,
      "u-", or "(". Otherwise it's binary "-".
    - whitespace is skipped; any other character -> ValueError
to_rpn(tokens) -> list in Reverse Polish Notation (shunting-yard).
    precedence: + - : 1,   * / : 2,   u- : 3,   ^ : 4
    ^ is right-associative ("2^3^2" == 2^(3^2)); + - * / are left-associative.
    u- is a prefix operator: it is pushed on the operator stack without popping anything.
    So "-2^2" == -(2^2) == -4 and "2^-1" == 0.5.
    Mismatched parentheses -> ValueError.
evaluate(rpn) -> number.  "/" is true division, "^" is exponentiation.
    Not enough operands, or not exactly one value left at the end -> ValueError.
calculate(expr) = evaluate(to_rpn(tokenize(expr)))
"""

PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "u-": 3, "^": 4}
RIGHT_ASSOC = {"^"}


def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c.isdigit() or c == ".":
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == "."):
                j += 1
            text = expr[i:j]
            if text.count(".") > 1 or text == ".":
                raise ValueError(f"bad number {text!r}")
            tokens.append(float(text) if "." in text else int(text))  # FIX: was always int()
            i = j
            continue
        if c in "+-*/^()":
            prev = tokens[-1] if tokens else None
            if c == "-" and (prev is None or prev in PREC or prev == "("):  # FIX: "(" case missing
                tokens.append("u-")
            else:
                tokens.append(c)
            i += 1
            continue
        raise ValueError(f"unexpected character {c!r}")
    return tokens


def to_rpn(tokens):
    out, stack = [], []
    for t in tokens:
        if isinstance(t, (int, float)):
            out.append(t)
        elif t == "(":
            stack.append(t)
        elif t == ")":
            while stack and stack[-1] != "(":
                out.append(stack.pop())
            if not stack:
                raise ValueError("mismatched ')'")
            stack.pop()  # FIX: the "(" was never popped
        elif t == "u-":
            stack.append(t)
        else:
            while stack and stack[-1] != "(" and (
                    PREC[stack[-1]] > PREC[t]
                    or (PREC[stack[-1]] == PREC[t] and t not in RIGHT_ASSOC)):  # FIX: was >= only
                out.append(stack.pop())
            stack.append(t)
    while stack:
        op = stack.pop()
        if op == "(":
            raise ValueError("mismatched '('")
        out.append(op)
    return out


def evaluate(rpn):
    st = []
    for t in rpn:
        if isinstance(t, (int, float)):
            st.append(t)
        elif t == "u-":
            if not st:
                raise ValueError("missing operand")
            st.append(-st.pop())
        else:
            if len(st) < 2:
                raise ValueError("missing operand")
            b = st.pop()  # FIX: operands were popped in the wrong order (a first)
            a = st.pop()
            if t == "+":
                st.append(a + b)
            elif t == "-":
                st.append(a - b)
            elif t == "*":
                st.append(a * b)
            elif t == "/":
                st.append(a / b)
            elif t == "^":
                st.append(a ** b)  # FIX: was a ^ b (XOR)
    if len(st) != 1:  # FIX: extra values were silently ignored (returned st[-1])
        raise ValueError("malformed expression")
    return st[0]


def calculate(expr):
    return evaluate(to_rpn(tokenize(expr)))
