# Debugging Assessment: Keyword Scanner

**Time allowed:** 120 minutes  
**Language:** Python 3, standard library only  
**Score:** the number of tests that pass, out of 66

## The task

`scanner.py` is a program that searches text for many keywords at once. It used to work, but it has been broken in several
places. Your job is to fix it so that it behaves the way `SPEC.md` describes.

You won't need to design anything from scratch. The structure of the program is right, and most of it is correct. The problems
are mistakes in the details, and they're spread across the file.

## What's in this folder

| File | What it is |
|---|---|
| `SPEC.md` | How the program should behave, with the algorithm explained step by step. Start here. |
| `scanner.py` | The broken program. This is the only file you should change. |
| `test_scanner.py` | The tests that decide your score. You can read them, and you should. |
| `answer_key/` | The corrected program and a list of the bugs. **Don't open this until your time is up.** |

## Rules

- You may not use AI assistants, autocomplete suggestions, web search or code from anywhere else. Type every fix yourself.
- You may use Python's built-in help (`help()` and `dir()`), `print`, and the `pdb` debugger.
- Don't change the tests.
- Code style doesn't count. An ugly fix that passes is worth just as much as a tidy one.
- If the spec and the tests seem to disagree, or the spec doesn't cover something, the tests are the final word. Don't spend
  time on cases that no test checks.

## Before you start

Keep a clean copy of the program, in case you want to undo something or try the exam again later:

```bash
cp scanner.py scanner.original.py
```

## Running the tests

Run these from inside this folder. To run all the tests:

```bash
python -m unittest
```

The last lines show how many tests ran, then how many had `failures` and `errors`. A failure means a check gave the wrong answer, and an
error means the code crashed. Your score is the number of tests that ran, minus both of those. For example, `Ran 66 tests` with
`failures=25, errors=5` is a score of 36.

To run one group of tests, which is much easier to read:

```bash
python -m unittest test_scanner.TestUtf8Offsets
```

To run a single test:

```bash
python -m unittest test_scanner.TestFindAll.test_classic_example
```

To stop at the first failure, or to see the name of every test as it runs:

```bash
python -m unittest -f
```

```bash
python -m unittest -v
```

To pause inside the program and look around, add the line `breakpoint()` where you want to stop, then run a test. Type `p name` to
print a variable, `n` to go to the next line, `c` to continue, and `q` to quit. Remember to remove the line afterwards.

## Using your time well

Spend the first 10 minutes reading `SPEC.md` and `scanner.py` without changing anything. You'll save that time many times over.

Many tests fail for the same few reasons, because the functions depend on each other. If a small helper is broken, everything
that uses it fails too. So start with the small pieces, and run the whole suite again after each fix. Often one fix makes several
failures disappear.

You don't need a perfect score to do well. If one bug is taking too long, move on and come back to it.

When your time is up, write down your score, then compare your work with `answer_key/`.
