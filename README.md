# 10-Day Python Debugging Course — Anthropic Fellowship Technical Test Prep

**Target:** a 120-minute CodeSignal assessment where you get a *broken implementation of
an algorithm*, a *spec*, and a *unittest suite*. You score points for every test that passes.
You can't use AI, web search, or external libraries.

This course takes you from zero to that level in 10 days, with one folder per day.
Day 11 is the exam.

## Schedule

| Day | Folder | Topic | Time |
|-----|--------|-------|------|
| 1 | `day01_foundations` | Python core: types, control flow, functions, lists, running unittest | 2–3 h |
| 2 | `day02_strings` | Strings: slicing, methods, formatting, text algorithms | 2–3 h |
| 3 | `day03_dicts_sets` | Dictionaries, sets, counting, grouping, nested data | 2–3 h |
| 4 | `day04_classes_objects` | Classes, dunder methods, exceptions, mutability traps | 2–3 h |
| 5 | `day05_bytes_utf8` | **Bytes, bit operations, UTF-8 encoding/decoding by hand** | 3 h |
| 6 | `day06_debugging_unittest` | unittest in depth, pdb, a systematic debugging workflow | 2–3 h |
| 7 | `day07_bug_catalog` | The ~30 bugs you'll actually meet + bug hunts | 2–3 h |
| 8 | `day08_spec_driven` | Implementing encoders/parsers from a spec (base64, varint, percent-encoding, bencode) | 3 h |
| 9 | `day09_mock_exam_1` | **Timed mock exam #1 (120 min)**: broken BPE tokenizer | 2 h + review |
| 10 | `day10_mock_exam_2` | **Timed mock exam #2 (120 min)**: broken transactional key-value store + exam strategy | 2 h + review |
| X | `dayX_prototype_exam` | **Extra timed exam (120 min)**: broken Huffman compressor. Run with `python run.py x` | 2 h + review |

## Algorithm drills (`drills/`)

Eight extra bug hunts on classic algorithms you'll want to recognise: sliding window, BFS/DFS, Dijkstra,
topological sort, union-find, LRU cache, knapsack/coin change, LCS/edit distance. Each folder has a **theory
README** (no prior knowledge assumed), a broken ~100-line implementation with 5 hidden bugs, and 15 tests.
Do one per evening **after** the day's main work, from day 3 on (drills 6–8 after day 7). See
[drills/README.md](drills/README.md).
```bash
python run.py d1              # drill 1 against the broken code
python run.py d1 --solutions  # the reference solution
```

## Daily routine

1. Read the day's `README.md` (theory). Type the examples into a Python REPL (`python3`) — don't just read.
2. Open the files in `exercises/`. Each function has a docstring = the spec. Some exercises ask you to
   **implement**; files named `*_fix_me.py` / `*_buggy` ask you to **debug existing code** (the exam skill).
3. Run the tests often:
   ```bash
   python run.py 1            # run day-1 tests against your code
   python run.py 1 -k ex02    # only one exercise file
   python run.py 1 -v -f      # full tracebacks, stop at first failure
   ```
   The output lists every function of your code with its status:
   ```text
   ex01_lists.py
     ✔  running_total   3/3 tests
     ✘  chunk           1/3 tests   -> TestChunk.test_bad_size: ValueError not raised
     ·  flatten         not started
   ```
   ✔ means every test that calls the function passes; ✘ shows the first failing test and its message;
   · means the function still raises `NotImplementedError`. Add `-v` when you need the full traceback.
4. Only when you're stuck for >15 minutes on something, peek at `solutions/`.
   `python run.py 1 --solutions` proves the reference solution passes.
5. Write down every bug you made or found in a personal `bug_journal.md`. Re-read it on day 10.

## Rules to practise under (same as the real test)

- No AI, no web search, no copying code from anywhere. The Python docs in your head + `help()` in the REPL only.
  (`help(str.split)`, `dir(bytes)` are allowed and extremely useful — practise using them.)
- Standard library only; you'll rarely need even that.
- Tests are the final word on requirements. If the docstring and a test disagree, the test wins.

## Tools

- Python 3.10+ (you have 3.12). Nothing to install.
- Optional: `pip install pdbpp` for a nicer debugger at home — but practise with plain `pdb` / `breakpoint()`
  too, since you can't count on installing anything in CodeSignal.
- Before exam day: run CodeSignal's environment/compatibility check, on the machine and network you will use.
  Use a big monitor (spec on one side, code on the other).
