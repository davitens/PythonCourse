import itertools
import random
import unittest

from sequences import edit_distance, lcs, lcs_table, longest_common_substring


def is_subsequence(s, t):
    it = iter(t)
    return all(c in it for c in s)


def brute_lcs_len(a, b):
    for r in range(len(a), -1, -1):
        for combo in itertools.combinations(a, r):
            if is_subsequence("".join(combo), b):
                return r


class TestLCS(unittest.TestCase):
    def test_table(self):
        dp = lcs_table("abcde", "ace")
        self.assertEqual(dp[5], [0, 1, 2, 3])
        self.assertEqual([row[0] for row in dp], [0] * 6)

    def test_lengths(self):
        self.assertEqual(lcs_table("abcde", "ace")[-1][-1], 3)
        self.assertEqual(lcs_table("aa", "a")[-1][-1], 1)
        self.assertEqual(lcs_table("abc", "")[-1][-1], 0)

    def test_lcs_string(self):
        self.assertEqual(lcs("abcde", "ace"), "ace")
        self.assertEqual(lcs("abc", "xyz"), "")

    def test_tie_rule(self):
        self.assertEqual(lcs("ab", "ba"), "a")
        self.assertEqual(lcs("abc", "cab"), "ab")

    def test_random_against_brute_force(self):
        rng = random.Random(8)
        for _ in range(150):
            a = "".join(rng.choice("abc") for _ in range(rng.randint(0, 6)))
            b = "".join(rng.choice("abc") for _ in range(rng.randint(0, 6)))
            s = lcs(a, b)
            self.assertEqual(len(s), brute_lcs_len(a, b), (a, b))
            self.assertTrue(is_subsequence(s, a) and is_subsequence(s, b), (a, b, s))


class TestEditDistance(unittest.TestCase):
    def test_classic(self):
        self.assertEqual(edit_distance("kitten", "sitting"), 3)

    def test_substitution_only(self):
        self.assertEqual(edit_distance("cat", "cut"), 1)
        self.assertEqual(edit_distance("abc", "xyz"), 3)

    def test_empty(self):
        self.assertEqual(edit_distance("", "abc"), 3)
        self.assertEqual(edit_distance("abc", ""), 3)
        self.assertEqual(edit_distance("", ""), 0)

    def test_insert_delete(self):
        self.assertEqual(edit_distance("abc", "abxc"), 1)
        self.assertEqual(edit_distance("flaw", "lawn"), 2)

    def test_longer(self):
        self.assertEqual(edit_distance("intention", "execution"), 5)

    def test_symmetric_and_identity(self):
        rng = random.Random(9)
        for _ in range(100):
            a = "".join(rng.choice("ab") for _ in range(rng.randint(0, 6)))
            b = "".join(rng.choice("ab") for _ in range(rng.randint(0, 6)))
            self.assertEqual(edit_distance(a, b), edit_distance(b, a))
            self.assertEqual(edit_distance(a, a), 0)
            self.assertGreaterEqual(edit_distance(a, b), abs(len(a) - len(b)))


class TestSubstring(unittest.TestCase):
    def test_example(self):
        self.assertEqual(longest_common_substring("xabcdy", "zzabcdq"), "abcd")

    def test_contiguous_not_subsequence(self):
        self.assertEqual(longest_common_substring("abcde", "ace"), "a")

    def test_first_of_equal_length(self):
        self.assertEqual(longest_common_substring("abXcd", "cdYab"), "ab")

    def test_none(self):
        self.assertEqual(longest_common_substring("abc", "xyz"), "")
        self.assertEqual(longest_common_substring("", "x"), "")


if __name__ == "__main__":
    unittest.main()
