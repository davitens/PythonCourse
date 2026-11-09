# Day X — Prototype Exam: Broken Huffman Compressor (120 minutes)

This is a third full rehearsal, using an algorithm you haven't seen in the course. Save it for a day or two before the real test,
when you'd like a fresh idea of where you stand.

I built it only from what the invitation email says: you fix a broken program so that it matches a spec and passes its unit tests,
in plain Python, with lists, dicts, objects, functions, strings and UTF-8. Nobody outside the test knows what the real algorithm or
format will be, so treat this as practice and not as a preview.

## Rules

- **Set a 120-minute timer.** Close everything except an editor, a terminal and `exam/`.
- No AI, no web search, no looking at `solution/`. `help()` and `dir()` in a Python REPL are allowed.
- Turn Copilot and any other inline suggestions off, and type every fix yourself.
- Only edit `exam/huffman.py`. Don't change the tests.
- Your score is the number of passing tests out of 64.

## Before the timer: what you need to know

You can read this part before you start the clock. It explains the idea behind the program, so you don't lose time working
out what it's for. The exact rules are in `exam/SPEC.md`, and reading that is part of the timed work.

### The idea behind Huffman coding

Normally, every byte of a file takes up 8 bits, whether it's a letter you use all the time or one you hardly ever see. That's
a bit wasteful. Morse code had a better idea long ago: the most common letter in English, E, is a single dot, while a rare
letter like Q takes four symbols. Common things get short codes and rare things get long ones, so messages come out shorter
overall.

**Huffman coding** does the same with bytes. In the word `"abracadabra"` the letter `a` appears 5 times, so it gets a code of
just one bit, `0`. The letter `d` appears once, so it can afford a longer code, `1111`.

You might wonder how a decoder knows where one code ends and the next begins, since there's nothing between them. The trick is
that no code is ever the beginning of another. If `0` is a code, then nothing else can start with `0`. So the decoder reads one
bit at a time, and the moment the bits it has collected match a code, it knows that letter is finished.

### What the program does, step by step

To compress, the program counts how often each byte appears, uses those counts to decide how long each code should be, works out
the codes themselves, and packs them all together into bytes. To decompress, it goes the other way: it reads the code lengths
from the start of the file, works out the same codes, and reads the bits back into bytes, then into text.

The next three sections look at the harder parts of that.

### Deciding how long each code is: the tree

To decide the code lengths, you build a tree from the bottom up. Each byte starts as its own small node, with its count as its
weight. Then you keep doing one thing: take the two lightest nodes and join them under a new parent, whose weight is their sum.
You stop when only one node is left. Here it is for `"abracadabra"`:

```text
start with:     c:1  d:1  b:2  r:2  a:5
join c and d    -> a new node "cd" with weight 2
join b and cd   -> a new node "bcd" with weight 4
join r and bcd  -> a new node "rbcd" with weight 6
join a and rbcd -> the root, with weight 11
```

Look at what happened. The rare letters `c` and `d` were joined first, so they ended up at the very bottom of the tree. The common
letter `a` was joined last, so it sits right under the top. A byte's code length is simply how far down the tree it is, which gives
`a` length 1, `r` length 2, `b` length 3, and `c` and `d` length 4.

You probably noticed that there were ties. After the first join, `b`, `r` and `cd` all weigh 2, and any two of them could go next.
The choice changes the tree, and so it changes the output, which is why the spec gives an exact rule for breaking ties. Expect the
tests to check it.

### Working out the codes from the lengths

The compressed file doesn't store the tree or the codes, only each byte's code **length**. That's enough, because both sides can
work out the same codes with the same recipe, known as **canonical codes**. "Canonical" just means there's one agreed way of doing
it.

Sort the bytes by length, and by value when lengths are equal. Start from zero. For each new byte, add 1 to the previous code, and
if this byte's code needs to be longer, put zeros on the end until it's long enough:

```text
a  length 1:  start at 0                          -> 0
r  length 2:  0 plus 1 is 1, make it 2 digits     -> 10
b  length 3:  10 plus 1 is 11, make it 3 digits   -> 110
c  length 4:  110 plus 1 is 111, make it 4 digits -> 1110
d  length 4:  1110 plus 1 is 1111, long enough    -> 1111
```

### Packing bits into bytes

Python can only write whole bytes to a file, not single bits, so the codes have to be packed together. `BitWriter` collects bits
until it has 8, then turns them into one byte, with the first bit in the highest position.

The last byte usually isn't full, so it gets topped up with zeros on the right. That causes a small problem: the decoder can't tell
real bits from padding, and might read an extra letter or two. So the file also stores how many bytes the original text had, and
the decoder stops when it reaches that number.

### Lines of Python worth a second look

You've seen everything in `huffman.py` during the course, but a few lines are dense. Take a minute with these before you start, so
that they don't slow you down later.

In `canonical_codes` you'll see this:

```python
f"{code:0{length}b}"
```

It writes `code` in binary, with enough leading zeros to fill `length` digits. The inner `{length}` gets filled in first, so if
`length` is 4, Python reads it as `f"{code:04b}"`, and 5 comes out as `"0101"`.

In `decompress` there's this line, which looks odd until you remember that going through a `bytes` object gives you numbers (Day 5).
Here, `take(2)` returns two bytes, and each name gets one of them as a number:

```python
symbol, length = take(2)
```

`take` itself is a helper function defined inside `decompress`. It moves the shared position forward each time it's called, which is
why it needs `nonlocal pos` (Day 10).

`code_lengths` also has a function inside it, called `walk`, which calls itself to go down both sides of the tree (recursion, Day 3).
It fills in the outer function's `lengths` dict. That doesn't need `nonlocal`, because it only adds to the dict and never assigns a
new value to the name `lengths`.

`decompress` needs to look up codes and get bytes back, which is the opposite of what `canonical_codes` returns. This line flips the
dict around:

```python
{code: symbol for symbol, code in codes.items()}
```

In `BitReader`, `self.pos` counts bits from the start of the data. Since there are 8 bits in a byte, `self.pos // 8` tells you which
byte you're in, and `self.pos % 8` tells you how far along that byte you are.

### Where to start

The functions depend on each other, like this:

```text
compress      uses byte_frequencies, build_tree, code_lengths, canonical_codes, BitWriter
decompress    uses canonical_codes, BitReader
format_table  uses byte_frequencies, build_tree, code_lengths, canonical_codes
truncate_utf8 uses utf8_chars
Archive       uses compress, decompress
```

So one bug in a small helper can make dozens of tests fail, even in functions that are fine. Don't start with the scariest failure.
Start with the small pieces at the bottom (`TestFrequencies`, `TestNode`, `TestBitWriter`, `TestBitReader`). Many of the other failures
will disappear as you fix those.

## Start

Keep a pristine copy, so that you can retry later:

```bash
cp exam/huffman.py exam/huffman.original.py
```

Then start the timer. From the course root:

```bash
python run.py x
```

Or the way you'd do it in the real assessment:

```bash
cd dayX_prototype_exam/exam
python -m unittest
```

To run one group of tests from inside `exam/`:

```bash
python -m unittest test_huffman.TestBitWriter
```

Read `exam/SPEC.md` and the code first, for about 10 minutes, before fixing anything (the Day 6 workflow).

## After the timer

1. Write down your score and how long you took.
2. Read `solution/BUGS.md`, and compare your fixes with `solution/huffman.py`.
3. For every bug you missed: which test pointed at it, and what would have got you there faster? Add it to your
   `bug_journal.md`.

To check that the tests themselves pass against the reference:

```bash
python run.py x --solutions
```
