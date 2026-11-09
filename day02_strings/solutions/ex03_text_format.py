"""Day 2 - Exercise 3: text formatting."""


def wrap(text, width):
    """Greedy word-wrap. Split `text` into words (any whitespace), then fill lines
    left-to-right: a word goes on the current line if the line length (words joined
    by single spaces) stays <= width; otherwise it starts a new line.
    A word longer than `width` goes on a line of its own (not broken).
    Returns a list of lines. Empty/blank text -> [].

    wrap("the quick brown fox", 10) -> ["the quick", "brown fox"]
    """
    lines = []
    current = ""
    for word in text.split():
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def justify_line(words, width):
    """Return a string of exactly `width` chars containing `words` separated by spaces,
    where extra spaces are distributed as evenly as possible between words and the
    LEFTMOST gaps get one more space when it doesn't divide evenly.
    A single word is left-aligned and padded with spaces on the right.
    You may assume the words fit (sum of lengths + gaps <= width).

    justify_line(["a", "bb", "c"], 9) -> "a   bb  c"
    """
    if len(words) == 1:
        return words[0].ljust(width)
    gaps = len(words) - 1
    spaces = width - sum(len(w) for w in words)
    base, extra = divmod(spaces, gaps)
    out = []
    for i, w in enumerate(words[:-1]):
        out.append(w)
        out.append(" " * (base + (1 if i < extra else 0)))
    out.append(words[-1])
    return "".join(out)


def justify(text, width):
    """Wrap `text` with wrap(), then fully justify every line except the LAST one,
    which is left-aligned and padded with spaces to `width`.
    (Assume no word is longer than width.)
    """
    lines = wrap(text, width)
    out = [justify_line(line.split(" "), width) for line in lines[:-1]]
    if lines:
        out.append(lines[-1].ljust(width))
    return out
