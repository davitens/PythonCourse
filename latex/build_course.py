#!/usr/bin/env python3
"""Build the 10 course booklets: Markdown -> LaTeX -> PDF.

Usage:
    python3 build_course.py            # all ten, then PDFs
    python3 build_course.py --day 1    # one booklet
    python3 build_course.py --tex-only # regenerate .tex, do not run latexmk
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Metadata and editorial additions
# ---------------------------------------------------------------------------

DAYS = {
    1: {
        "folder": "day01_foundations",
        "short": "FOUNDATIONS",
        "title": r"Python Foundations\\+ Running Tests",
        "subtitle": "Types, control flow, functions, lists, and the edit-test-fix loop.",
        "time": "2–3 hours",
        "focus": "Core Python",
        "topics": ["Types", "Control flow", "Functions", "Lists", "unittest"],
        "next": "Turn the page to Day 2.",
        "practice": "Work in `exercises/`. Read each docstring as the spec. Run `python run.py {day}` after every change; peek at `solutions/` only after 15 minutes stuck.",
        "boxes": [
            {"prefix": "Get into the habit:", "type": "tip", "title": "REPL habit"},
            {"prefix": "**Truthiness trap:**", "type": "trap", "title": "Truthiness trap"},
            {"prefix": "**Classic bug — missing `return`:**", "type": "trap", "title": "Missing return"},
            {"prefix": "**Classic bug — `return` inside the loop:**", "type": "trap", "title": "Return inside the loop"},
        ],
        "exam": [
            "Read the failing assertion first; reproduce its input in the REPL, then fix the smallest line that explains it.",
            "`return` and mutability bugs are common. Check them before digging into deeper logic.",
            "The tests are the spec: exact types, formats, and boundary behaviour all score points.",
        ],
    },
    2: {
        "folder": "day02_strings",
        "short": "STRINGS",
        "title": r"Strings",
        "subtitle": "Slicing, methods, formatting, and the text algorithms the exam loves.",
        "time": "2–3 hours",
        "focus": "Text processing",
        "topics": ["Slicing", "Methods", "f-strings", "Scanning"],
        "next": "Turn the page to Day 3.",
        "practice": "Work in `exercises/`. Read each docstring as the spec. Run `python run.py {day}` after every change; peek at `solutions/` only after 15 minutes stuck.",
        "boxes": [
            {"prefix": "**Methods never modify the string, they return a new one:**", "type": "key", "title": "Strings are immutable"},
            {"prefix": "A line like `name.strip()` on its own does nothing.", "type": "trap", "title": "No-op method calls", "strip": False},
            {"prefix": r'''`"apostrophe's".title()`''', "type": "tip", "title": "title() gotcha", "strip": False},
            {"prefix": "When debugging whitespace issues,", "type": "tip", "title": "See the invisible"},
        ],
        "exam": [
            "Expect edge cases: empty strings, repeated separators, mixed case, and multi-digit run lengths.",
            "`split()` versus `split(\" \")`, `strip` as a character set, and off-by-one slices are planted often.",
            "When the spec says bytes, compare `len(s)` with `len(s.encode())`; they are not the same.",
        ],
    },
    3: {
        "folder": "day03_dicts_sets",
        "short": "DICTS \\& SETS",
        "title": r"Dictionaries \& Sets",
        "subtitle": "Counting, grouping, sorting by value, and the traps hiding in mutable keys.",
        "time": "2–3 hours",
        "focus": "Maps and sets",
        "topics": ["Counting", "Grouping", "Sorting", "Sets"],
        "next": "Turn the page to Day 4.",
        "practice": "Work in `exercises/`. Read each docstring as the spec. Run `python run.py {day}` after every change; peek at `solutions/` only after 15 minutes stuck.",
        "boxes": [
            {"prefix": "Since Python 3.7, dicts", "type": "key", "title": "Insertion order is guaranteed", "strip": False},
            {"prefix": "**Don't add/remove keys while iterating**", "type": "trap", "title": "Don't mutate while iterating"},
            {"prefix": "Trap: `defaultdict` creates the key", "type": "trap", "title": "defaultdict inserts on read"},
            {"prefix": "Trap: `dict.fromkeys(keys, [])`", "type": "trap", "title": "Shared list from fromkeys"},
            {"prefix": 'When a spec says "ties are broken by X"', "type": "key", "title": "Tie-break in the key tuple", "strip": False},
            {"prefix": 'A function that "returns a new dict"', "type": "trap", "title": "Aliasing instead of copying", "strip": False},
        ],
        "exam": [
            "Counting and grouping are the backbone of tokenizers, caches, and parsers; know the idioms cold.",
            "Write tie-breaks into the sort key. `reverse=True` reverses every component, not just the count.",
            "Keys must be hashable. Convert lists to tuples before counting pairs.",
        ],
    },
    4: {
        "folder": "day04_classes_objects",
        "short": "OBJECTS",
        "title": r"Classes, Objects\\\& Exceptions",
        "subtitle": "Classes, dunder methods, exceptions, and the object-model traps.",
        "time": "2–3 hours",
        "focus": "Objects and errors",
        "topics": ["Classes", "Dunders", "Exceptions", "Mutability"],
        "next": "Turn the page to Day 5.",
        "practice": "Work in `exercises/`. Read each docstring as the spec. Run `python run.py {day}` after every change; peek at `solutions/` only after 15 minutes stuck.",
        "boxes": [
            {"prefix": "Forgetting `self.` is a classic bug", "type": "trap", "title": "Missing self", "strip": False},
            {"prefix": "Also note `self.lines = lines`", "type": "note", "title": "Aliasing the input", "strip": False},
            {"prefix": "A generator is exhausted after one pass", "type": "trap", "title": "One-shot generators", "strip": False},
        ],
        "exam": [
            "The broken implementation is often a class: inspect `__init__`, shared state, and dunders first.",
            "A missing `super().__init__` or a property setter that assigns to itself is a quick win.",
            "Match the exact exception type the tests expect; a subclass also satisfies `assertRaises`.",
        ],
    },
    5: {
        "folder": "day05_bytes_utf8",
        "short": "BYTES \\& UTF-8",
        "title": r"Bytes, Bits\\\& UTF-8",
        "subtitle": "Bits, masks, and UTF-8 encoding and decoding by hand.",
        "time": "3 hours",
        "focus": "Bytes and UTF-8",
        "topics": ["Bits", "Masks", "UTF-8", "Error handling"],
        "next": "Turn the page to Day 6.",
        "practice": "Work in `exercises/`. Read each docstring as the spec. Run `python run.py {day}` after every change; do `ex05` with a 20-minute timer.",
        "boxes": [
            {"prefix": "**Multi-byte chars split across chunks**", "type": "trap", "title": "Never decode per chunk", "strip": False},
            {"prefix": "When in doubt, add parentheses.", "type": "tip", "title": "Parenthesise bit code", "strip": False},
            {"prefix": "**Order of the lead-byte checks matters.**", "type": "trap", "title": "Check lead bytes in the right order"},
            {"prefix": "The bits of `cp` are written", "type": "key", "title": "Most-significant bits first", "strip": False},
            {"prefix": "`UnicodeDecodeError`", "type": "note", "title": "Decode errors are ValueErrors", "strip": False},
        ],
        "exam": [
            "Decode the lead byte, validate each continuation, then reject overlong, surrogate, and out-of-range values.",
            "Never decode per chunk; concatenate the bytes first and decode once.",
            "Hand-compute `C3 A9`, `E2 82 AC`, and `F0 9F 98 80` until the masks are automatic.",
        ],
    },
    6: {
        "folder": "day06_debugging_unittest",
        "short": "DEBUGGING",
        "title": r"unittest, pdb\\\& Debugging",
        "subtitle": "unittest, pdb, and a repeatable method for maximizing passing tests.",
        "time": "2–3 hours",
        "focus": "Debug method",
        "topics": ["unittest", "pdb", "Triage", "Workflow"],
        "next": "Turn the page to Day 7.",
        "practice": "Work in `exercises/`. Read each docstring as the spec. Run `python run.py {day}` after every change; time `ex03` at 45 minutes.",
        "boxes": [
            {"prefix": "**The last line of the traceback inside YOUR file is where to look**", "type": "key", "title": "Read the last frame in your file", "strip": False},
            {"prefix": "unittest **shows** prints", "type": "tip", "title": "Print debugging, done well", "strip": False},
            {"prefix": "The first assertion that fires gives you a minimal failing input.", "type": "key", "title": "Minimal failing input", "strip": False},
            {"prefix": "Note: unittest catches exceptions", "type": "note", "title": "Post-mortem inside unittest", "strip": False},
            {"prefix": "**Differential testing:**", "type": "tip", "title": "Differential testing"},
        ],
        "exam": [
            "Run all tests, triage by helper, and fix the lowest-level bug first.",
            "Re-run the full suite after every fix; a score drop is information, not failure.",
            "Time-box: 10--15 minutes without progress, write it down and move on.",
        ],
    },
    7: {
        "folder": "day07_bug_catalog",
        "short": "BUG CATALOG",
        "title": r"The Bug\\Catalog",
        "subtitle": "The planted bugs you must recognize on sight.",
        "time": "2–3 hours",
        "focus": "Bug recognition",
        "topics": ["Boundaries", "Logic", "Objects", "Bytes"],
        "next": "Turn the page to Day 8.",
        "practice": "Target: under 2 minutes per bug. Write the catalog code (for example `A4`) in a comment next to each fix.",
        "boxes": [
            {"prefix": "Read the catalog, then do the bug hunts.", "type": "tip", "title": "How to use this catalog", "strip": False},
        ],
        "exam": [
            "Planted bugs are one-token changes: `<` versus `<=`, `i` versus `i+1`, `+` versus `-`, a mask, `is` versus `==`.",
            "Check loop bounds, post-loop handling, and the indentation of every `return`.",
            "Name the catalog code in your journal; recognition is the skill being tested.",
        ],
        "checklist": [
            "I can name the catalog code (A4, B3, C10, ...) for each bug I fixed.",
            "I ran `python run.py 7` and the full suite passes.",
            "I added tonight's bugs to `bug_journal.md`.",
        ],
        "unnumbered_all": True,
    },
    8: {
        "folder": "day08_spec_driven",
        "short": "SPEC-DRIVEN",
        "title": r"Code from\\a Spec",
        "subtitle": "Turning a written spec into correct encoders and parsers.",
        "time": "3 hours",
        "focus": "Spec implementation",
        "topics": ["Specs", "Parsers", "Encodings", "Round-trips"],
        "next": "Turn the page to Day 9.",
        "practice": "Implement each function from the spec in its docstring. Work one file at a time; the tests are the final word.",
        "boxes": [
            {"prefix": "**Cursor-based parsing**", "type": "key", "title": "Cursor-based parsing", "strip": False},
            {"prefix": "**Recursive descent**", "type": "key", "title": "Recursive descent", "strip": False},
            {"prefix": "**Round-trip property:**", "type": "key", "title": "Round-trip property"},
            {"prefix": "Each is ~30–60 lines.", "type": "tip", "title": "Time-box each exercise", "strip": False},
        ],
        "section_overrides": {
            "Exercises (implement from the spec in each file's docstring)": "Exercises",
        },
        "exam": [
            "Turn every spec sentence into a checklist item; the tests win where the spec is vague.",
            "Cursor-based parsing: always advance, validate lengths, and return the new position.",
            "Round-trip tests catch encoder/decoder mismatches faster than reading the code.",
        ],
        "checklist": [
            "I can turn a spec sentence into a checklist item.",
            "My encoder/decoder passes the round-trip property: `decode(encode(x)) == x`.",
            "I can parse a length-prefixed format without losing the cursor.",
            "All day-8 tests pass.",
        ],
    },
    9: {
        "folder": "day09_mock_exam_1",
        "short": "MOCK EXAM 1",
        "title": r"Mock Exam\\\#1",
        "subtitle": "A full timed rehearsal: broken BPE tokenizer, 51 tests.",
        "time": "120 min + review",
        "focus": "Timed exam",
        "topics": ["BPE", "Timed run", "Debrief", "Bug journal"],
        "next": "Turn the page to Day 10.",
        "goal": "A 120-minute dress rehearsal of the real assessment: fix a broken BPE tokenizer and maximize the 51 passing tests. No AI, no web, no solutions.",
        "goal_title": "The brief",
        "drop_first_para": True,
        "test_count": 51,
        "boxes": [
            {"prefix": "Read `exam/SPEC.md` first.", "type": "tip", "title": "Read before you fix", "strip": False},
            {"prefix": "Before you start, keep a pristine copy", "type": "tip", "title": "Keep a pristine copy", "strip": False},
        ],
        "exam": [
            "Read the spec before touching code, and baseline the score before your first edit.",
            "Fix high-leverage helpers; one correct fix can turn many tests green.",
            "Debrief every missed bug: the pattern matters more than the score.",
        ],
        "checklist": [
            "I completed the 120-minute run with no AI, web search, or solutions.",
            "I recorded my score and the order in which I found the bugs.",
            "I read `solution/BUGS.md` and logged every bug I missed.",
        ],
    },
    10: {
        "folder": "day10_mock_exam_2",
        "short": "MOCK EXAM 2",
        "title": r"Mock Exam\\\#2",
        "subtitle": "A second timed rehearsal, then the exam-day playbook.",
        "time": "120 min + strategy",
        "focus": "Exam strategy",
        "topics": ["Key-value store", "Strategy", "Cheat sheet"],
        "next": "You are ready. Good luck.",
        "goal": "A second 120-minute rehearsal -- a transactional key-value store -- followed by the exam-day playbook.",
        "goal_title": "The brief",
        "test_count": 35,
        "boxes": [
            {"prefix": "Compare your Day 9 and Day 10 results:", "type": "key", "title": "Compare the two runs", "strip": False},
        ],
        "exam": [
            "Protect the score: minimal diffs, no refactors, no style points.",
            "Keep a 10-minute buffer to remove debug code and run the full suite.",
            "Use the cheat sheet for formats, not for logic you can derive.",
        ],
        "checklist": [
            "I completed the second 120-minute run and recorded my score.",
            "I compared Day 9 and Day 10: time per bug, missed patterns, score.",
            "I read the exam-day strategy and the last-minute cheat sheet.",
        ],
        "unnumbered_all": True,
    },
}

# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------

SPECIAL_RE = re.compile(r"^(#{1,4})\s+(.*)$")
UL_RE = re.compile(r"^(\s*)[-*]\s+(.*)$")
OL_RE = re.compile(r"^(\s*)(\d+)\.\s+(.*)$")
CHECK_RE = re.compile(r"^(\s*)- \[ \]\s+(.*)$")
SEP_CELL_RE = re.compile(r"^:?-{3,}:?$")


def split_table_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells: list[str] = []
    buf: list[str] = []
    in_code = False
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            buf.append("|")
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
            buf.append(ch)
        elif ch == "|" and not in_code:
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
        i += 1
    cells.append("".join(buf).strip())
    return cells


def is_separator_row(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(SEP_CELL_RE.match(c.replace(" ", "")) for c in cells)


def parse_list(lines: list[str], start: int):
    first = CHECK_RE.match(lines[start])
    if first:
        kind = "check"
    else:
        first = UL_RE.match(lines[start])
        if first:
            kind = "ul"
        else:
            first = OL_RE.match(lines[start])
            kind = "ol" if first else None
    if not first or kind is None:
        raise ValueError("not a list")

    base_indent = len(first.group(1))
    root: list[dict] = []
    stack = [{"indent": base_indent, "nodes": root, "kind": kind}]
    last_node = None
    i = start

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            break
        m_check = CHECK_RE.match(line)
        m_ul = UL_RE.match(line)
        m_ol = OL_RE.match(line)
        m = None
        item_kind = None
        if m_check:
            m, item_kind = m_check, "check"
        elif m_ul:
            m, item_kind = m_ul, "ul"
        elif m_ol:
            m, item_kind = m_ol, "ol"
        if m:
            indent = len(m.group(1))
            text = m.group(2) if item_kind == "check" else (m.group(2) if item_kind == "ul" else m.group(3))
            if indent < base_indent:
                break
            if indent > stack[-1]["indent"]:
                if last_node is None:
                    break
                child_nodes: list[dict] = []
                last_node["children"].append({"kind": item_kind, "nodes": child_nodes})
                stack.append({"indent": indent, "nodes": child_nodes, "kind": item_kind})
            else:
                while len(stack) > 1 and indent < stack[-1]["indent"]:
                    stack.pop()
            node = {"text": text.strip(), "children": []}
            stack[-1]["nodes"].append(node)
            last_node = node
            i += 1
            continue
        # an indented fenced code block ends the list and is parsed by the
        # main loop as a standalone block (minted will autogobble it)
        if line.strip().startswith("```"):
            break
        # continuation line of the previous item
        if line[:1].isspace() and last_node is not None:
            last_node["text"] += " " + line.strip()
            i += 1
            continue
        break
    return ("list", kind, root), i


def parse_blocks(text: str):
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks = []
    title = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        m = SPECIAL_RE.match(line)
        if m:
            level = len(m.group(1))
            heading = m.group(2).strip()
            if level == 1:
                title = heading
            elif level == 2:
                blocks.append(("h2", heading))
            elif level == 3:
                blocks.append(("h3", heading))
            else:
                blocks.append(("h4", heading))
            i += 1
            continue
        if stripped.startswith("```"):
            lang = stripped[3:].strip().lower()
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            blocks.append(("code", lang, "\n".join(code)))
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and is_separator_row(lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            header = split_table_row(rows[0])
            data = [split_table_row(r) for r in rows[2:]]
            width = len(header)
            data = [(r + [""] * width)[:width] for r in data]
            blocks.append(("table", header, data))
            continue
        if stripped == "---":
            i += 1
            continue
        if CHECK_RE.match(line) or UL_RE.match(line) or OL_RE.match(line):
            block, i = parse_list(lines, i)
            blocks.append(block)
            continue
        # paragraph
        para = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            ns = nxt.strip()
            if not ns or ns == "---" or SPECIAL_RE.match(nxt) or ns.startswith("```"):
                break
            if ns.startswith("|") and i + 1 < len(lines) and is_separator_row(lines[i + 1]):
                break
            if CHECK_RE.match(nxt) or UL_RE.match(nxt) or OL_RE.match(nxt):
                break
            para.append(ns)
            i += 1
        blocks.append(("p", " ".join(para)))
    return title, blocks


# ---------------------------------------------------------------------------
# Inline Markdown -> LaTeX
# ---------------------------------------------------------------------------

TEXT_ESCAPE = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "&": r"\&",
    "%": r"\%",
    "#": r"\#",
    "_": r"\_",
    "$": r"\$",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "|": r"\textbar{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
}

CODE_ESCAPE = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "&": r"\&",
    "%": r"\%",
    "#": r"\#",
    "_": r"\_",
    "$": r"\$",
    "^": r"\textasciicircum{}",
    "~": r"\textasciitilde{}",
    '"': r"\textquotedbl{}",
    "|": r"\textbar{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
}


def escape_text(s: str) -> str:
    return "".join(TEXT_ESCAPE.get(ch, ch) for ch in s)


def escape_code(s: str, breakable=False) -> str:
    s = s.replace("👍🏽", "\x03T")
    s = s.replace("👍", "\x03T")
    s = s.replace("😀", "\x03S")
    break_chars = ".,:;/_=()[]<>|&" if breakable == "table" else ":;/,()=<>|&"
    out: list[str] = []
    for ch in s:
        if ch == " ":
            out.append(r"\ ")
        elif ch in break_chars:
            out.append(CODE_ESCAPE.get(ch, ch) + r"\allowbreak{}")
        else:
            out.append(CODE_ESCAPE.get(ch, ch))
    return "".join(out).replace("\x03T", r"\thumbsup{}").replace("\x03S", r"\smiley{}")


def smart_quotes(s: str) -> str:
    s = re.sub(r'(^|[\s(\[{])"', r"\1“", s)
    s = s.replace('"', "”")
    s = re.sub(r"(^|[\s(\[{])'(?=\S)", r"\1‘", s)
    s = s.replace("'", "’")
    return s


def inline(text: str, breakable: bool = False) -> str:
    code_spans: list[str] = []

    def protect(m):
        code_spans.append(m.group(1))
        return f"\x00{len(code_spans) - 1}\x00"

    text = re.sub(r"`([^`]*)`", protect, text)
    text = escape_text(text)
    text = text.replace("👍🏽", r"\thumbsup{}")
    text = text.replace("👍", r"\thumbsup{}")
    text = text.replace("😀", r"\smiley{}")
    # links (none in the day files, but harmless to support)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\\href{\2}{\1}", text)
    # bold before italic; italic may then operate inside bold
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\\emph{\1}", text)
    text = smart_quotes(text)

    def restore(m):
        raw = code_spans[int(m.group(1))]
        return r"\code{" + escape_code(raw, breakable=breakable) + "}"

    text = re.sub("\x00(\\d+)\x00", restore, text)
    return text


def strip_md(s: str) -> str:
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", s)
    return s


def cap_first(s: str) -> str:
    if s and s[0].islower():
        return s[0].upper() + s[1:]
    return s


def cap_first_md(s: str) -> str:
    m = re.match(r"^(\*\*|`|\*)([a-z])", s)
    if m:
        pos = m.start(2)
        return s[:pos] + s[pos].upper() + s[pos + 1:]
    return cap_first(s)


# ---------------------------------------------------------------------------
# LaTeX rendering
# ---------------------------------------------------------------------------

BOX_ENV = {
    "tip": "tipbox",
    "trap": "trapbox",
    "key": "keybox",
    "note": "notebox",
    "repl": "replbox",
}


def col_weight(cells: list[str]) -> float:
    plain = [strip_md(c) for c in cells]
    lens = [len(x) for x in plain if x]
    if not lens:
        return 5.0
    return max(5.0, 0.55 * max(lens) + 0.45 * (sum(lens) / len(lens)))


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    n = len(headers)
    weights = []
    for j in range(n):
        cells = [headers[j]] + [r[j] for r in rows]
        weights.append(col_weight(cells))
    total = sum(weights)
    scaled = [max(0.45, w / total * n) for w in weights]
    if n == 3 and headers and headers[0].strip().lower() == "file":
        if len(headers) > 1 and headers[1].strip().lower() == "type":
            scaled = [1.60, 0.70, 1.30]
        else:
            scaled = [1.60, 1.20, 1.00]
        total = sum(scaled)
        scaled = [w / total * n for w in scaled]
    scale = n / sum(scaled)
    scaled = [round(w * scale, 2) for w in scaled]
    # adjust the last weight so the total is exactly n
    scaled[-1] = round(n - sum(scaled[:-1]), 2)
    spec = "@{}" + "".join(f"Y{{{w:.2f}}}" for w in scaled) + "@{}"
    has_long_path = any("/" in c and len(strip_md(c)) > 18 for row in rows for c in row)
    size = r"\footnotesize" if n >= 6 or has_long_path else r"\small"
    out = [rf"\begin{{datatable}}{{}}{{{size}}}", rf"\begin{{xltabular}}{{\linewidth}}{{{spec}}}"]
    out.append(r"\rowcolor{primary}")
    out.append(" & ".join(rf"\thd{{{inline(h, breakable='table')}}}" for h in headers) + r" \\ \hline")
    out.append(r"\endhead")
    for row in rows:
        out.append(" & ".join(inline(c, breakable='table') if c else "" for c in row) + r" \\")
    out.append(r"\hline")
    out.append(r"\end{xltabular}")
    out.append(r"\end{datatable}")
    return "\n".join(out)


def render_list(kind: str, nodes: list[dict]) -> str:
    if kind == "check":
        env = "checklist"
    elif kind == "ol":
        env = "enumerate"
    else:
        env = "itemize"
    out = [rf"\begin{{{env}}}"]
    for node in nodes:
        out.append(r"\item " + inline(node["text"]))
        for child in node["children"]:
            out.append(render_list(child["kind"], child["nodes"]))
    out.append(rf"\end{{{env}}}")
    return "\n".join(out)


def render_code(lang: str, code: str) -> str:
    if "�" in code:
        env = "utfcode"
    elif lang == "bash" and any(l.strip().startswith(">>>") for l in code.splitlines()):
        env = "replcode"
    elif lang == "bash":
        env = "shcode"
    elif lang == "python":
        env = "pycode"
    else:
        env = "txtcode"
    nlines = code.count("\n") + 1
    if nlines <= 4:
        need = 2
    else:
        need = min(17, int(nlines * 0.8) + 3)
    return rf"\Needspace{{{need}\baselineskip}}" + f"\n\\begin{{{env}}}\n{code}\n\\end{{{env}}}"


def render_paragraph(text: str, rules: list[dict]) -> str:
    for rule in rules:
        if text.startswith(rule["prefix"]):
            body = text
            if rule.get("strip", True):
                body = text[len(rule["prefix"]):].lstrip()
                if body.startswith("— "):
                    body = body[2:].lstrip()
                if body and not (body[0].isalnum() or body[0] in "`*_\\"):
                    body = text
            if not body.strip():
                body = text
            if body.strip():
                env = BOX_ENV[rule["type"]]
                title = rule["title"]
                return rf"\begin{{{env}}}[{title}]" + "\n" + inline(cap_first_md(body)) + "\n" + rf"\end{{{env}}}"
    return inline(text)


def extract_goal(blocks: list[tuple]):
    for idx, block in enumerate(blocks):
        if block[0] == "p":
            raw = block[1]
            m = re.match(r"^\*\*(Goal[^*]*?):\*\*\s*(.*)$", raw)
            if not m:
                m = re.match(r"^\*\*(Goal[^*]*?)\*\*\s*(.*)$", raw)
            if m:
                return m.group(2).strip(), blocks[:idx] + blocks[idx + 1:]
        if block[0] == "h2":
            break
    return None, blocks


def latex_metadata(day: dict, num: int, goal: str) -> list[str]:
    d = f"{num:02d}"
    eyebrow = r"DAY %s\enspace\textcolor{rule}{\textperiodcentered}\enspace %s" % (d, day["short"])
    topics = "".join(r"\topic{%s}" % t for t in day["topics"])
    return [
        rf"\renewcommand{{\courseDay}}{{{d}}}",
        rf"\renewcommand{{\courseDayInt}}{{{num}}}",
        rf"\renewcommand{{\courseShort}}{{{day['short']}}}",
        rf"\renewcommand{{\courseTitle}}{{{day['title']}}}",
        rf"\renewcommand{{\courseSubtitle}}{{{day['subtitle']}}}",
        rf"\renewcommand{{\courseTime}}{{{day['time']}}}",
        rf"\renewcommand{{\courseFocus}}{{{day['focus']}}}",
        rf"\renewcommand{{\courseFolder}}{{{day['folder'].replace('_', r'\_')}}}",
        rf"\renewcommand{{\courseEyebrow}}{{{eyebrow}}}",
        rf"\renewcommand{{\courseTopics}}{{{topics}}}",
        rf"\renewcommand{{\courseNext}}{{{day['next']}}}",
        rf"\renewcommand{{\courseTestCount}}{{{day.get('test_count', 0)}}}",
        rf"\renewcommand{{\courseGoal}}{{{goal}}}",
    ]


def build_tex(num: int, day: dict) -> tuple[str, str]:
    src = ROOT / day["folder"] / "README.md"
    title, blocks = parse_blocks(src.read_text(encoding="utf-8"))

    # Pull the goal out of the body (it is shown in a box at the top).
    goal_raw, blocks = extract_goal(blocks)
    if day.get("goal"):
        goal_raw = day["goal"]
    if goal_raw is None:
        goal_raw = day["subtitle"]
    goal = inline(cap_first(goal_raw))
    if day.get("drop_first_para") and blocks and blocks[0][0] == "p":
        blocks = blocks[1:]

    # Pull the source checklist out of the body.
    checklist_items = []
    body_blocks = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if block[0] == "h2" and block[1].strip().lower() == "end-of-day checklist":
            i += 1
            if i < len(blocks) and blocks[i][0] == "list" and blocks[i][1] == "check":
                checklist_items = [n["text"] for n in blocks[i][2]]
                i += 1
            continue
        body_blocks.append(block)
        i += 1
    if not checklist_items:
        checklist_items = day.get("checklist", [])

    boxes = day.get("boxes", [])
    overrides = day.get("section_overrides", {})
    unnumbered_all = day.get("unnumbered_all", False)

    out: list[str] = []
    out.append(r"\documentclass[10pt,a4paper]{article}")
    out.append(r"\usepackage{python-course}")
    out.extend(latex_metadata(day, num, goal))
    out.append(r"\begin{document}")
    out.append(r"\makecover")
    out.append(r"\setcounter{page}{2}")
    out.append(r"\makefrontmatter")
    out.append(r"\begin{goalbox}[%s]" % day.get("goal_title", "Today's goal"))
    out.append(goal)
    out.append(r"\end{goalbox}")
    out.append(r"\vspace{2pt}")

    for idx, block in enumerate(body_blocks):
        kind = block[0]
        if kind == "h2":
            raw = block[1].strip()
            heading = overrides.get(raw, raw)
            is_exercises = raw.lower().startswith("exercises")
            if is_exercises:
                heading = "Exercises"
            numbered = re.match(r"^(\d+)\.\s+", heading)
            text = re.sub(r"^\d+\.\s+", "", heading)
            letter = re.match(r"^([A-Z])\.\s+(.*)$", text)
            part = re.match(r"^(Part\s+\d+\s*[—–-]\s*.*)$", text)
            next_kind = body_blocks[idx + 1][0] if idx + 1 < len(body_blocks) else "p"
            if is_exercises:
                section_need = 22
            elif next_kind == "table":
                section_need = 8
            elif next_kind == "code":
                code_lines = len(body_blocks[idx + 1][2].splitlines())
                section_need = min(18, code_lines + 5)
            else:
                section_need = 10
            out.append(rf"\Needspace{{{section_need}\baselineskip}}")
            if letter:
                sec_title = f"{letter.group(1)}. {inline(letter.group(2))}"
                out.append(rf"\unnumberedsection{{{sec_title}}}")
            elif part:
                out.append(rf"\unnumberedsection{{{inline(part.group(1))}}}")
            elif unnumbered_all:
                out.append(rf"\unnumberedsection{{{inline(text)}}}")
            elif numbered:
                # Keep the README's own numbering so "see section N" references match the booklet.
                out.append(rf"\setcounter{{section}}{{{int(numbered.group(1)) - 1}}}")
                out.append(rf"\section{{{inline(text)}}}")
            else:
                out.append(rf"\unnumberedsection{{{inline(text)}}}")
            if is_exercises:
                practice = day.get("practice", "Work in `exercises/`. Run `python run.py {day}` after every change.")
                practice_tex = inline(practice.format(day=num))
                out.append(r"\begin{practicebox}")
                out.append(practice_tex)
                out.append(r"\end{practicebox}")
        elif kind == "h3":
            text = re.sub(r"^\d+\.\s+", "", block[1].strip())
            out.append(r"\Needspace{10\baselineskip}")
            if unnumbered_all:
                out.append(rf"\unnumberedsubsection{{{inline(text)}}}")
            else:
                out.append(rf"\subsection{{{inline(text)}}}")
        elif kind == "h4":
            out.append(rf"\subsubsection{{{inline(block[1])}}}")
        elif kind == "p":
            out.append(render_paragraph(block[1], boxes))
        elif kind == "code":
            out.append(render_code(block[1], block[2]))
        elif kind == "table":
            out.append(render_table(block[1], block[2]))
        elif kind == "list":
            out.append(render_list(block[1], block[2]))
        else:
            raise ValueError(f"unknown block {kind}")

    # Review section: keep it together when possible, but let it flow rather
    # than leaving a near-empty page after short days.
    out.append(r"\Needspace{22\baselineskip}")
    out.append(r"\unnumberedsection{End-of-day checklist}")
    out.append(r"\begin{checklistbox}[Tick every box]")
    out.append(r"\begin{checklist}")
    for item in checklist_items:
        out.append(r"\item " + inline(item))
    out.append(r"\end{checklist}")
    out.append(r"\scoreline")
    out.append(r"\end{checklistbox}")
    out.append(r"\begin{examlensbox}")
    out.append(r"\begin{itemize}")
    for item in day.get("exam", []):
        out.append(r"\item " + inline(item))
    out.append(r"\end{itemize}")
    out.append(r"\end{examlensbox}")
    out.append(r"\bugjournalifspace")
    out.append(r"\end{document}")

    filename = f"day{num:02d}_{day['folder'].split('_', 1)[1]}"
    return filename, "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build_pdf(tex_path: Path) -> bool:
    name = tex_path.name
    cmd = [
        "latexmk", "-xelatex", "-shell-escape",
        "-interaction=nonstopmode", "-halt-on-error", name,
    ]
    result = subprocess.run(cmd, cwd=tex_path.parent, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout[-2500:])
        print(result.stderr[-2500:])
        log = tex_path.with_suffix(".log")
        if log.exists():
            lines = log.read_text(errors="replace").splitlines()
            errors = [l for l in lines if l.startswith("!") or "Overfull" in l or "Missing character" in l]
            print("\n".join(errors[-30:]))
        return False
    return True


def clean_aux(tex_path: Path):
    subprocess.run(["latexmk", "-c", tex_path.name], cwd=tex_path.parent,
                   capture_output=True, text=True)
    for minted in (tex_path.parent / f"_minted-{tex_path.stem}",
                   tex_path.parent / "_minted"):
        if minted.exists():
            shutil.rmtree(minted, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, default=None, help="build only this day")
    parser.add_argument("--tex-only", action="store_true", help="do not run latexmk")
    parser.add_argument("--keep-aux", action="store_true")
    parser.add_argument("--force", action="store_true", help="rebuild even if PDF is newer")
    args = parser.parse_args()

    nums = [args.day] if args.day else sorted(DAYS)
    failures = []
    for num in nums:
        day = DAYS[num]
        filename, tex = build_tex(num, day)
        tex_path = OUT / f"{filename}.tex"
        tex_path.write_text(tex, encoding="utf-8")
        print(f"[{num:02d}] wrote {tex_path.name} ({len(tex.splitlines())} lines)")
        if args.tex_only:
            continue
        pdf = tex_path.with_suffix(".pdf")
        if pdf.exists() and not args.force and pdf.stat().st_mtime > tex_path.stat().st_mtime:
            print(f"[{num:02d}] PDF is up to date")
            continue
        ok = build_pdf(tex_path)
        if ok:
            print(f"[{num:02d}] built {pdf.name}")
            if not args.keep_aux:
                clean_aux(tex_path)
        else:
            failures.append(num)
            print(f"[{num:02d}] FAILED")
    if failures:
        print("\nFailed: " + ", ".join(f"day{n:02d}" for n in failures))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
