# 10-Day Python Debugging Course — Typeset Booklets

One standalone booklet per day, generated from the day's `README.md`:

| Day | Booklet | Pages | Focus |
|----:|---------|------:|-------|
| 1 | [`day01_foundations`](day01_foundations.pdf) | 26 | Core Python and unittest |
| 2 | [`day02_strings`](day02_strings.pdf) | 18 | Strings and text algorithms |
| 3 | [`day03_dicts_sets`](day03_dicts_sets.pdf) | 16 | Dictionaries, sets, counting |
| 4 | [`day04_classes_objects`](day04_classes_objects.pdf) | 18 | Classes, dunders, exceptions |
| 5 | [`day05_bytes_utf8`](day05_bytes_utf8.pdf) | 17 | Bits and UTF-8 by hand |
| 6 | [`day06_debugging_unittest`](day06_debugging_unittest.pdf) | 17 | unittest, pdb, debug method |
| 7 | [`day07_bug_catalog`](day07_bug_catalog.pdf) | 13 | The planted-bug catalog |
| 8 | [`day08_spec_driven`](day08_spec_driven.pdf) | 12 | Specs, parsers, encoders |
| 9 | [`day09_mock_exam_1`](day09_mock_exam_1.pdf) | 7 | Timed BPE mock exam |
| 10 | [`day10_mock_exam_2`](day10_mock_exam_2.pdf) | 7 | Timed KV-store exam + strategy |

Each PDF has the same structure:

1. A cover with the day number, title, session time, folder, focus, and progress through the course.
2. A short "How to use this booklet" page with the study loop and a linked table of contents.
3. The day's theory, typeset with syntax-highlighted code, styled reference tables, and callout boxes for key ideas and exam traps.
4. The exercises section, with file table and runner command.
5. An end-of-day review: checklist, exam lens, and—when space allows—a bug-journal table.

## Build

Requirements: XeLaTeX, `latexmk`, TeX Live, `minted`, and Pygments. The shared style uses the TeX Live fonts **Source Serif Pro**, **Inter**, and **Source Code Pro**.

```bash
make                 # build every PDF that is out of date
make -B              # force all ten
make clean           # remove .aux/.log/.toc/.xdv and minted caches
make distclean       # also remove the PDFs
```

The `.tex` files are standalone but share [`python-course.sty`](python-course.sty), so keep it in the same folder.

## Regenerate from Markdown

[`build_course.py`](build_course.py) reads `../dayXX_*/README.md`, converts the Markdown, and writes both the `.tex` and the `.pdf`:

```bash
python3 build_course.py            # all ten, build PDFs
python3 build_course.py --day 5    # one day
python3 build_course.py --tex-only # regenerate .tex, do not run LaTeX
python3 build_course.py --force    # rebuild even if the PDF is newer
```

> Rerunning the generator **overwrites** the `.tex` files. If you edit a `.tex` by hand, rebuild it with `make`; do not rerun `build_course.py`.

## Design notes

- **Paper and typography:** A4, 10pt Source Serif Pro body, Inter headings, Source Code Pro code, generous margins, and a 16 cm text block for comfortable line length.
- **Colour system:** deep navy for structure, amber for key ideas, terracotta for traps, teal for practice and review.
- **Code:** `minted` + Pygments via XeLaTeX shell escape. A DejaVu Sans Mono fallback handles the one code block containing U+FFFD; all other blocks use Source Code Pro.
- **Tables:** page-breaking `xltabular` with weighted `X` columns, a navy header, zebra rows, and no decorative vertical rules.
- **Review material:** the `Exam lens` bullets and the `bug journal` are editorial study aids added to the original README content. The review section is allowed to flow onto the exercises page when it fits, or start a fresh page when it does not.

## Source fidelity

The theory, examples, tables, command lines, exercise descriptions, and checklists come from the corresponding `../dayXX_*/README.md`. The typesetting adds a cover, study guidance, callouts, the exam lens, the review checklist, and the optional bug journal. Day 9's one-paragraph dress-rehearsal intro is folded into its "brief" box rather than repeated.

## Troubleshooting

- **`minted` errors / missing Pygments:** confirm `python3 -c "import pygments"` works, and compile with `-shell-escape`.
- **Missing font:** check that the TeX Live `sourceserifpro`, `inter`, and `sourcecodepro` packages are installed.
- **Stale cross-references:** delete the auxiliary files with `make clean` and rebuild. `latexmk` normally handles this automatically.
