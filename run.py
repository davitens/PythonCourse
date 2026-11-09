#!/usr/bin/env python3
"""Course test runner.

Usage:
    python run.py 3                 # run day 3 tests against YOUR code (exercises/)
    python run.py 3 --solutions     # run day 3 tests against the reference solutions
    python run.py 3 -k ex02         # only test files whose name contains "ex02"
    python run.py 3 -v              # also print every test name and the full tracebacks
    python run.py 3 -f              # stop at first failure
    python run.py d2                # drill 2 (drills/02_*) against exam/ ; add --solutions for the reference
    python run.py x                 # the prototype exam (dayX_*) against exam/ ; add --solutions for the reference

The default output is a report with one line per function of your code:
    ✔ all of its tests pass   ✘ some fail (first failure shown)   · not started (still NotImplementedError)

For the mock exams (days 9 and 10) you can also do exactly what you'd do in the
real assessment:  cd day09_mock_exam_1/exam && python -m unittest -v
"""
import argparse
import importlib.util
import io
import os
import sys
import traceback
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))


def find_day_dir(target):
    if target.lower().startswith("d") and target[1:].isdigit():   # drill: d3 -> drills/03_*
        base, prefix = os.path.join(ROOT, "drills"), f"{int(target[1:]):02d}_"
    elif target.lower() == "x":                                   # the prototype exam: dayX_*
        base, prefix = ROOT, "dayX"
    elif target.isdigit():
        base, prefix = ROOT, f"day{int(target):02d}"
    else:
        sys.exit("target must be a day number (3), a drill (d3) or the prototype exam (x)")
    for name in sorted(os.listdir(base)):
        if name.startswith(prefix) and os.path.isdir(os.path.join(base, name)):
            return os.path.join(base, name)
    sys.exit(f"No folder for {target}")


class ReportResult(unittest.TextTestResult):
    """Records, for every test, which functions of the code under test it calls directly,
    and whether the test passed, failed, or hit an unimplemented function."""

    def __init__(self, *args, code_dir, tests_dir, **kwargs):
        super().__init__(*args, **kwargs)
        self.code_dir = os.path.realpath(code_dir) + os.sep
        self.tests_dir = os.path.realpath(tests_dir) + os.sep
        self.records = []          # (test_id, called functions, outcome, message)
        self._called = None
        self._bad = {}             # test id -> (outcome, message), first problem only

    def _profile(self, frame, event, arg):
        if event != "call":
            return
        code = frame.f_code
        caller = frame.f_back
        if caller is None or "<locals>" in code.co_qualname:   # skip lambdas, generators, inner helpers
            return
        if self._is_code(code.co_filename) and self._is_test(caller.f_code.co_filename):
            self._called.add((os.path.basename(code.co_filename), code.co_firstlineno, code.co_qualname))

    def _is_test(self, filename):
        path = os.path.realpath(filename)
        return path.startswith(self.tests_dir) and os.path.basename(path).startswith("test_")

    def _is_code(self, filename):
        path = os.path.realpath(filename)
        return path.startswith(self.code_dir) and not os.path.basename(path).startswith("test_")

    def startTest(self, test):
        super().startTest(test)
        self._called = set()
        sys.setprofile(self._profile)

    def stopTest(self, test):
        sys.setprofile(None)
        outcome, msg = self._bad.get(test.id(), ("ok", ""))
        self.records.append((test.id(), self._called, outcome, msg))
        super().stopTest(test)

    def _note(self, test, err):
        exc_type, exc, _ = err
        if test.id() in self._bad:
            return
        if exc_type is NotImplementedError:
            self._bad[test.id()] = ("todo", "")
            return
        if issubclass(exc_type, AssertionError):
            text = str(exc).strip().splitlines()
            msg = text[0] if text else "assertion failed"
        else:
            # A crash: point at the deepest line of YOUR code in the traceback.
            where = ""
            for fr in traceback.extract_tb(err[2]):
                if self._is_code(fr.filename):
                    where = f" (line {fr.lineno} in {fr.name})"
            msg = f"{exc_type.__name__}: {exc}{where}"
        self._bad[test.id()] = ("fail", msg)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._note(test, err)

    def addError(self, test, err):
        super().addError(test, err)
        self._note(test, err)

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            self._note(test, err)


def print_report(records):
    """One line per function: passed / failed / not started."""
    funcs = {}   # (file, line, name) -> list of (test name, outcome, msg)
    orphans = []
    for test_id, called, outcome, msg in records:
        short = test_id.rsplit(".", 2)
        short = ".".join(short[-2:])
        if not called:
            orphans.append((short, outcome, msg))
        for f in called:
            funcs.setdefault(f, []).append((short, outcome, msg))

    width = max([len(n) for (_, _, n) in funcs] + [10])
    current_file = None
    counts = {"ok": 0, "fail": 0, "todo": 0}
    for (fname, _, name) in sorted(funcs):
        if fname != current_file:
            current_file = fname
            print(f"\n{fname}")
        results = funcs[(fname, _, name)]
        passed = sum(1 for _, o, _ in results if o == "ok")
        if any(o == "todo" for _, o, _ in results) and passed == 0:
            counts["todo"] += 1
            print(f"  ·  {name:<{width}}  not started")
        elif passed == len(results):
            counts["ok"] += 1
            print(f"  ✔  {name:<{width}}  {passed}/{len(results)} tests")
        else:
            counts["fail"] += 1
            test, _, msg = next(r for r in results if r[1] != "ok")
            if not msg:
                msg = "calls a function that is not written yet"
            print(f"  ✘  {name:<{width}}  {passed}/{len(results)} tests   -> {test}: {msg}")
    for short, outcome, msg in orphans:
        if outcome == "fail":
            print(f"  ✘  (test {short} failed before calling your code: {msg})")
    print(f"\nFunctions: {counts['ok']} correct, {counts['fail']} with failures, {counts['todo']} not started")
    print("A function counts as correct only when every test that calls it passes. A function that calls a\n"
          "broken helper fails too, so fix the low-level helpers first.\n"
          "Run with -v for full tracebacks.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("day", help="day number (e.g. 3), drill (e.g. d3) or prototype exam (x)")
    p.add_argument("--solutions", action="store_true")
    p.add_argument("-k", dest="pattern", default="")
    p.add_argument("-v", dest="verbose", action="store_true")
    p.add_argument("-f", dest="failfast", action="store_true")
    a = p.parse_args()

    day_dir = find_day_dir(a.day)
    is_mock = os.path.isdir(os.path.join(day_dir, "exam"))
    if is_mock:
        code_dir = os.path.join(day_dir, "solution" if a.solutions else "exam")
        tests_dir = os.path.join(day_dir, "exam")
    else:
        code_dir = os.path.join(day_dir, "solutions" if a.solutions else "exercises")
        tests_dir = os.path.join(day_dir, "tests")

    sys.path.insert(0, code_dir)
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for fname in sorted(os.listdir(tests_dir)):
        if not (fname.startswith("test_") and fname.endswith(".py")):
            continue
        if a.pattern and a.pattern not in fname:
            continue
        path = os.path.join(tests_dir, fname)
        spec = importlib.util.spec_from_file_location(fname[:-3], path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:  # e.g. syntax error in your code
            print(f"!! Could not load {fname}: {type(e).__name__}: {e}")
            continue
        suite.addTests(loader.loadTestsFromModule(mod))

    print(f"Running {suite.countTestCases()} tests from {os.path.relpath(tests_dir, ROOT)} "
          f"against {os.path.relpath(code_dir, ROOT)}\n")
    stream = sys.stderr if a.verbose else io.StringIO()   # tracebacks only when asked for
    runner = unittest.TextTestRunner(
        stream=stream, verbosity=2 if a.verbose else 0, failfast=a.failfast,
        resultclass=lambda *args, **kw: ReportResult(*args, code_dir=code_dir, tests_dir=tests_dir, **kw))
    result = runner.run(suite)
    print_report(result.records)
    total = result.testsRun
    # subTest failures are reported individually; count each test method once
    bad = len({getattr(t, "test_case", t).id() for t, _ in result.failures + result.errors})
    print(f"\nSCORE: {total - bad}/{total} passing")
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
