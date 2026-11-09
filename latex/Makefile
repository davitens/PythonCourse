# Build the ten course booklets with XeLaTeX + minted.
# Run `make` or `make -B`; see README.md for details.

DAYS := day01_foundations day02_strings day03_dicts_sets \
        day04_classes_objects day05_bytes_utf8 day06_debugging_unittest \
        day07_bug_catalog day08_spec_driven day09_mock_exam_1 \
        day10_mock_exam_2

TEXS := $(addsuffix .tex,$(DAYS))
PDFS := $(addsuffix .pdf,$(DAYS))

LATEXMK ?= latexmk
LATEXMKFLAGS := -xelatex -shell-escape -interaction=nonstopmode -halt-on-error

.PHONY: all clean distclean regenerate tex help

all: $(PDFS)

%.pdf: %.tex python-course.sty
	$(LATEXMK) $(LATEXMKFLAGS) $<

# Regenerate all .tex files from the day READMEs and build the PDFs.
regenerate:
	python3 build_course.py --force

# Regenerate only the LaTeX sources (does not run latexmk).
tex:
	python3 build_course.py --tex-only

clean:
	-@for f in $(TEXS); do $(LATEXMK) -c $$f >/dev/null 2>&1 || true; done
	-@rm -rf _minted-* _minted

distclean: clean
	-@rm -f $(PDFS)

help:
	@echo "make            build PDFs that are out of date"
	@echo "make -B         force all ten PDFs"
	@echo "make regenerate regenerate .tex from README.md and build"
	@echo "make tex        regenerate .tex only"
	@echo "make clean      remove auxiliary files and minted caches"
	@echo "make distclean  also remove the PDFs"
