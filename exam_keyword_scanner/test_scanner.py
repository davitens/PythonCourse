import random
import unittest

from scanner import KeywordScanner, Match, utf8_offsets


def brute_force(keywords, text):
    """Every occurrence of every keyword, found the slow and obvious way, as a set of tuples."""
    found = set()
    for keyword in keywords:
        for start in range(len(text) - len(keyword) + 1):
            if text[start:start + len(keyword)] == keyword:
                found.add((keyword, start, start + len(keyword)))
    return found


def as_set(matches):
    return {(m.keyword, m.start, m.end) for m in matches}


class TestUtf8Offsets(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(utf8_offsets(b""), [0])

    def test_ascii(self):
        self.assertEqual(utf8_offsets(b"abc"), [0, 1, 2, 3])

    def test_two_byte(self):
        self.assertEqual(utf8_offsets("aé".encode()), [0, 1, 1, 2])

    def test_three_byte(self):
        self.assertEqual(utf8_offsets("€a".encode()), [0, 0, 0, 1, 2])

    def test_four_byte(self):
        self.assertEqual(utf8_offsets("😀a".encode()), [0, 0, 0, 0, 1, 2])

    def test_invalid_lead(self):
        for data in (b"\x80", b"\xff", b"a\xf8"):
            with self.assertRaises(ValueError):
                utf8_offsets(data)

    def test_truncated(self):
        with self.assertRaises(ValueError):
            utf8_offsets("€".encode()[:2])


class TestMatch(unittest.TestCase):
    def test_attributes(self):
        m = Match("he", 2, 4)
        self.assertEqual((m.keyword, m.start, m.end, m.length), ("he", 2, 4, 2))

    def test_equality(self):
        self.assertEqual(Match("he", 2, 4), Match("he", 2, 4))
        self.assertNotEqual(Match("he", 2, 4), Match("he", 3, 5))
        self.assertNotEqual(Match("he", 2, 4), ("he", 2, 4))

    def test_hashable(self):
        self.assertEqual(len({Match("he", 2, 4), Match("he", 2, 4), Match("he", 3, 5)}), 2)

    def test_repr(self):
        self.assertEqual(repr(Match("he", 2, 4)), "Match('he', 2, 4)")


class TestAdd(unittest.TestCase):
    def test_keywords_in_insertion_order(self):
        self.assertEqual(KeywordScanner(["b", "a", "c"]).keywords(), ["b", "a", "c"])

    def test_keywords_returns_a_copy(self):
        s = KeywordScanner(["a"])
        s.keywords().append("zzz")
        self.assertEqual(s.keywords(), ["a"])

    def test_duplicates_ignored(self):
        s = KeywordScanner(["a", "b", "a"])
        self.assertEqual(s.keywords(), ["a", "b"])

    def test_duplicates_ignored_when_folded(self):
        s = KeywordScanner(["He", "he"], ignore_case=True)
        self.assertEqual(s.keywords(), ["He"])

    def test_empty_keyword(self):
        with self.assertRaises(ValueError):
            KeywordScanner().add("")

    def test_non_string_keyword(self):
        with self.assertRaises(TypeError):
            KeywordScanner().add(b"bytes")

    def test_add_after_searching(self):
        s = KeywordScanner(["cat"])
        self.assertEqual(s.find_all("cat dog"), [Match("cat", 0, 3)])
        s.add("dog")
        self.assertEqual(s.find_all("cat dog"), [Match("cat", 0, 3), Match("dog", 4, 7)])


class TestFindAll(unittest.TestCase):
    def test_no_keywords(self):
        self.assertEqual(KeywordScanner().find_all("anything"), [])

    def test_empty_text(self):
        self.assertEqual(KeywordScanner(["a"]).find_all(""), [])

    def test_single(self):
        self.assertEqual(KeywordScanner(["cat"]).find_all("a cat sat"), [Match("cat", 2, 5)])

    def test_classic_example(self):
        s = KeywordScanner(["he", "she", "his", "hers"])
        self.assertEqual(s.find_all("ushers"),
                         [Match("she", 1, 4), Match("he", 2, 4), Match("hers", 2, 6)])

    def test_keyword_inside_keyword(self):
        s = KeywordScanner(["abcd", "bc"])
        self.assertEqual(s.find_all("abcd"), [Match("bc", 1, 3), Match("abcd", 0, 4)])

    def test_self_overlapping(self):
        self.assertEqual(KeywordScanner(["aa"]).find_all("aaaa"),
                         [Match("aa", 0, 2), Match("aa", 1, 3), Match("aa", 2, 4)])

    def test_longer_first_at_same_end(self):
        s = KeywordScanner(["c", "bc", "abc"])
        self.assertEqual(s.find_all("abc"),
                         [Match("abc", 0, 3), Match("bc", 1, 3), Match("c", 2, 3)])

    def test_following_several_fallbacks(self):
        s = KeywordScanner(["abcd", "bcde", "cx"])
        self.assertEqual(s.find_all("abcx"), [Match("cx", 2, 4)])

    def test_deep_fallback_links(self):
        # Needs the links of shallow nodes to exist before deeper ones are worked out.
        s = KeywordScanner(["xyza", "yzb", "zc", "ad"])
        self.assertEqual(s.find_all("xyzc"), [Match("zc", 2, 4)])
        self.assertEqual(s.find_all("xyzad"), [Match("xyza", 0, 4), Match("ad", 3, 5)])

    def test_non_ascii_offsets_are_characters(self):
        s = KeywordScanner(["€", "日本"])
        self.assertEqual(s.find_all("a€日本b"), [Match("€", 1, 2), Match("日本", 2, 4)])

    def test_match_at_end_of_text(self):
        self.assertEqual(KeywordScanner(["é"]).find_all("café"), [Match("é", 3, 4)])

    def test_emoji(self):
        self.assertEqual(KeywordScanner(["😀"]).find_all("a😀b😀"),
                         [Match("😀", 1, 2), Match("😀", 3, 4)])

    def test_same_lead_byte_is_not_a_match(self):
        # é and è share their first UTF-8 byte.
        self.assertEqual(KeywordScanner(["é"]).find_all("è"), [])

    def test_against_brute_force(self):
        rng = random.Random(11)
        alphabet = "abé€"
        for _ in range(200):
            keywords = {"".join(rng.choice(alphabet) for _ in range(rng.randint(1, 4)))
                        for _ in range(rng.randint(1, 6))}
            text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            self.assertEqual(as_set(KeywordScanner(keywords).find_all(text)), brute_force(keywords, text),
                             f"keywords={keywords} text={text!r}")


class TestIgnoreCase(unittest.TestCase):
    def test_text_case(self):
        self.assertEqual(KeywordScanner(["cat"], ignore_case=True).find_all("a CAT"), [Match("cat", 2, 5)])

    def test_keyword_case(self):
        self.assertEqual(KeywordScanner(["CAT"], ignore_case=True).find_all("a cat"), [Match("CAT", 2, 5)])

    def test_off_by_default(self):
        self.assertEqual(KeywordScanner(["cat"]).find_all("CAT"), [])

    def test_only_ascii_is_folded(self):
        self.assertEqual(KeywordScanner(["é"], ignore_case=True).find_all("É"), [])


class TestContainsAny(unittest.TestCase):
    def test_found(self):
        self.assertTrue(KeywordScanner(["cat"]).contains_any("a cat"))

    def test_not_found(self):
        self.assertFalse(KeywordScanner(["cat"]).contains_any("a dog"))

    def test_keyword_ending_inside_a_longer_path(self):
        self.assertTrue(KeywordScanner(["he", "shex"]).contains_any("she"))

    def test_no_keywords(self):
        self.assertFalse(KeywordScanner().contains_any("x"))


class TestNonOverlapping(unittest.TestCase):
    def test_leftmost_wins(self):
        s = KeywordScanner(["abc", "cde"])
        self.assertEqual(s.find_non_overlapping("abcde"), [Match("abc", 0, 3)])

    def test_longest_wins_at_same_start(self):
        s = KeywordScanner(["ab", "abcd"])
        self.assertEqual(s.find_non_overlapping("abcd"), [Match("abcd", 0, 4)])

    def test_adjacent_matches_are_kept(self):
        s = KeywordScanner(["ab", "cd"])
        self.assertEqual(s.find_non_overlapping("abcd"), [Match("ab", 0, 2), Match("cd", 2, 4)])

    def test_repeats(self):
        self.assertEqual(KeywordScanner(["aa"]).find_non_overlapping("aaaaa"),
                         [Match("aa", 0, 2), Match("aa", 2, 4)])

    def test_first(self):
        s = KeywordScanner(["b", "ab"])
        self.assertEqual(s.first("xab b"), Match("ab", 1, 3))

    def test_first_none(self):
        self.assertIsNone(KeywordScanner(["b"]).first("xyz"))


class TestCount(unittest.TestCase):
    def test_counts_overlaps_and_zeros(self):
        s = KeywordScanner(["aa", "b", "zzz"])
        self.assertEqual(s.count("aaab"), {"aa": 2, "b": 1, "zzz": 0})

    def test_key_order(self):
        s = KeywordScanner(["b", "a"])
        self.assertEqual(list(s.count("")), ["b", "a"])


class TestRewriting(unittest.TestCase):
    def test_replace(self):
        s = KeywordScanner(["cat", "dog"])
        self.assertEqual(s.replace("a cat and a dog!", {"cat": "lion", "dog": "wolf"}), "a lion and a wolf!")

    def test_replace_keeps_the_tail(self):
        self.assertEqual(KeywordScanner(["a"]).replace("xay", {"a": "-"}), "x-y")

    def test_replace_without_entry_leaves_text(self):
        s = KeywordScanner(["cat", "dog"])
        self.assertEqual(s.replace("cat dog", {"dog": "wolf"}), "cat wolf")

    def test_replace_non_ascii(self):
        self.assertEqual(KeywordScanner(["€"]).replace("5€ é", {"€": "EUR"}), "5EUR é")

    def test_replace_nothing_found(self):
        self.assertEqual(KeywordScanner(["z"]).replace("abc", {"z": "y"}), "abc")

    def test_highlight(self):
        self.assertEqual(KeywordScanner(["cat"]).highlight("a cat sat"), "a [cat] sat")

    def test_highlight_custom_markers(self):
        self.assertEqual(KeywordScanner(["é"]).highlight("café!", "<b>", "</b>"), "caf<b>é</b>!")

    def test_highlight_keeps_original_case(self):
        self.assertEqual(KeywordScanner(["cat"], ignore_case=True).highlight("CAT"), "[CAT]")

    def test_summary(self):
        s = KeywordScanner(["b", "a", "c", "zzz"])
        self.assertEqual(s.summary("c a b a b c c"), "c: 3\na: 2\nb: 2")

    def test_summary_nothing_found(self):
        self.assertEqual(KeywordScanner(["z"]).summary("abc"), "")


class TestStream(unittest.TestCase):
    def test_one_chunk(self):
        st = KeywordScanner(["cat"]).stream()
        self.assertEqual(st.feed(b"a cat"), [("cat", 2, 5)])

    def test_match_split_across_chunks(self):
        st = KeywordScanner(["cat"]).stream()
        self.assertEqual(st.feed(b"a c"), [])
        self.assertEqual(st.feed(b"at"), [("cat", 2, 5)])

    def test_offsets_keep_counting(self):
        st = KeywordScanner(["ab"]).stream()
        st.feed(b"ab")
        self.assertEqual(st.feed(b"xab"), [("ab", 3, 5)])

    def test_character_split_across_chunks(self):
        data = "x日本".encode()
        st = KeywordScanner(["日本"]).stream()
        self.assertEqual(st.feed(data[:2]) + st.feed(data[2:5]) + st.feed(data[5:]), [("日本", 1, 7)])

    def test_position(self):
        st = KeywordScanner(["a"]).stream()
        self.assertEqual(st.position, 0)
        st.feed(b"xyz")
        st.feed(b"w")
        self.assertEqual(st.position, 4)

    def test_reset(self):
        st = KeywordScanner(["cat"]).stream()
        st.feed(b"ca")
        st.reset()
        self.assertEqual(st.position, 0)
        self.assertEqual(st.feed(b"t"), [])

    def test_streams_are_independent(self):
        s = KeywordScanner(["cat"])
        a, b = s.stream(), s.stream()
        a.feed(b"ca")
        self.assertEqual(b.feed(b"t"), [])
        self.assertEqual(a.feed(b"t"), [("cat", 0, 3)])

    def test_uses_keywords_added_before_streaming(self):
        s = KeywordScanner(["cat"])
        s.find_all("x")
        s.add("dog")
        self.assertEqual(s.stream().feed(b"dog"), [("dog", 0, 3)])


if __name__ == "__main__":
    unittest.main()
