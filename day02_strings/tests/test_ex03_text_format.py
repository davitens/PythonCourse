import unittest

from ex03_text_format import justify, justify_line, wrap


class TestWrap(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(wrap("the quick brown fox", 10), ["the quick", "brown fox"])

    def test_exact_fit(self):
        self.assertEqual(wrap("aaa bbb", 7), ["aaa bbb"])
        self.assertEqual(wrap("aaa bbb", 6), ["aaa", "bbb"])

    def test_long_word(self):
        self.assertEqual(wrap("a supercalifragilistic word", 6),
                         ["a", "supercalifragilistic", "word"])

    def test_whitespace(self):
        self.assertEqual(wrap("  one\n two\tthree  ", 9), ["one two", "three"])
        self.assertEqual(wrap("   ", 5), [])


class TestJustifyLine(unittest.TestCase):
    def test_uneven(self):
        self.assertEqual(justify_line(["a", "bb", "c"], 9), "a   bb  c")

    def test_even(self):
        self.assertEqual(justify_line(["ab", "cd"], 6), "ab  cd")

    def test_single(self):
        self.assertEqual(justify_line(["hi"], 5), "hi   ")

    def test_exact(self):
        self.assertEqual(justify_line(["a", "b"], 3), "a b")


class TestJustify(unittest.TestCase):
    def test_paragraph(self):
        text = "This is an example of text justification."
        self.assertEqual(justify(text, 16), [
            "This    is    an",
            "example  of text",
            "justification.  ",
        ])

    def test_all_lines_have_width(self):
        text = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do"
        for line in justify(text, 20):
            self.assertEqual(len(line), 20)


if __name__ == "__main__":
    unittest.main()
