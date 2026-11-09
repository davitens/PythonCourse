import random
import unittest

from bpe import BPETokenizer, get_stats, merge, split_text

A, B, C, D = 97, 98, 99, 100  # byte values of "a", "b", "c", "d"
SPACE = 32

CORPUS = (
    "The quick brown fox jumps over the lazy dog. The dog sleeps; the fox runs!\n"
    "Café, naïve, résumé — 日本語のテキスト. Emoji: 😀😀 👍🏽. Numbers 12345 and 123.\n"
    "the the the then there these those thought through though\n"
) * 3


def trained(text="aaabdaaabac", vocab_size=300):
    tok = BPETokenizer()
    tok.train(text, vocab_size)
    return tok


class TestGetStats(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(get_stats([1, 2, 3, 1, 2]), {(1, 2): 2, (2, 3): 1, (3, 1): 1})

    def test_overlapping(self):
        self.assertEqual(get_stats([1, 1, 1]), {(1, 1): 2})

    def test_short(self):
        self.assertEqual(get_stats([]), {})
        self.assertEqual(get_stats([5]), {})
        self.assertEqual(get_stats([5, 6]), {(5, 6): 1})

    def test_updates_given_dict(self):
        counts = {(1, 2): 5}
        result = get_stats([1, 2, 7], counts)
        self.assertIs(result, counts)
        self.assertEqual(counts, {(1, 2): 6, (2, 7): 1})

    def test_independent_calls(self):
        get_stats([1, 2])
        self.assertEqual(get_stats([3, 4]), {(3, 4): 1})

    def test_first_occurrence_order(self):
        self.assertEqual(list(get_stats([3, 1, 2, 3, 1])), [(3, 1), (1, 2), (2, 3)])


class TestMerge(unittest.TestCase):
    def test_example(self):
        self.assertEqual(merge([1, 1, 1, 2], (1, 1), 9), [9, 1, 2])

    def test_non_overlapping(self):
        self.assertEqual(merge([1, 1, 1, 1], (1, 1), 9), [9, 9])

    def test_pair_at_end(self):
        self.assertEqual(merge([3, 1, 2], (1, 2), 9), [3, 9])

    def test_no_match(self):
        self.assertEqual(merge([1, 2, 3], (3, 1), 9), [1, 2, 3])
        self.assertEqual(merge([], (1, 2), 9), [])

    def test_does_not_mutate(self):
        ids = [1, 2, 1, 2]
        merge(ids, (1, 2), 9)
        self.assertEqual(ids, [1, 2, 1, 2])


class TestSplitText(unittest.TestCase):
    def test_spec_examples(self):
        self.assertEqual(split_text("Hello  world!! 42"), ["Hello", " ", " world", "!", "!", " 42"])
        self.assertEqual(split_text("abc123"), ["abc", "123"])
        self.assertEqual(split_text("\n\nhi there"), ["\n\n", "hi", " there"])
        self.assertEqual(split_text("é😀 x"), ["é", "😀", " x"])

    def test_whitespace_runs(self):
        self.assertEqual(split_text("a   b"), ["a", "  ", " b"])
        self.assertEqual(split_text("a \n b"), ["a", " \n", " b"])
        self.assertEqual(split_text("x  "), ["x", "  "])

    def test_space_before_punctuation(self):
        self.assertEqual(split_text("a !"), ["a", " ", "!"])

    def test_leading_space(self):
        self.assertEqual(split_text(" leading"), [" leading"])

    def test_empty(self):
        self.assertEqual(split_text(""), [])

    def test_concatenation_property(self):
        rng = random.Random(0)
        alphabet = "ab Z9 \n\t.!é😀日 "
        for _ in range(500):
            s = "".join(rng.choice(alphabet) for _ in range(rng.randrange(15)))
            chunks = split_text(s)
            self.assertEqual("".join(chunks), s)
            self.assertTrue(all(chunks), (s, chunks))


class TestTrain(unittest.TestCase):
    def test_vocab_size_too_small(self):
        with self.assertRaises(ValueError):
            BPETokenizer().train("abc", 255)

    def test_vocab_size_256_means_no_merges(self):
        tok = trained("aaaa", 256)
        self.assertEqual(tok.merges, {})
        self.assertEqual(len(tok.vocab), 256)

    def test_classic_example_merges(self):
        tok = trained("aaabdaaabac", 300)
        self.assertEqual(tok.merges, {(A, A): 256, (A, B): 257, (256, 257): 258})

    def test_merge_ids_are_consecutive(self):
        tok = trained(CORPUS, 300)
        self.assertEqual(list(tok.merges.values()), list(range(256, 256 + len(tok.merges))))
        self.assertGreater(len(tok.merges), 20)

    def test_vocab_entries(self):
        tok = trained("aaabdaaabac", 300)
        self.assertEqual(tok.vocab[256], b"aa")
        self.assertEqual(tok.vocab[257], b"ab")
        self.assertEqual(tok.vocab[258], b"aaab")

    def test_vocab_consistent_with_merges(self):
        tok = trained(CORPUS, 320)
        for (a, b), idx in tok.merges.items():
            self.assertEqual(tok.vocab[idx], tok.vocab[a] + tok.vocab[b])

    def test_tie_break_smallest_pair(self):
        # "cdab": every pair occurs twice in "cdab cdab"... chunks are ["cdab", " cdab"].
        # Counts: (c,d)=2, (d,a)=2, (a,b)=2, (space,c)=1 -> smallest pair (a, b) wins.
        tok = trained("cdab cdab", 257)
        self.assertEqual(tok.merges, {(A, B): 256})

    def test_stops_when_no_pair_repeats(self):
        self.assertEqual(trained("abcd", 300).merges, {})

    def test_pairs_do_not_cross_chunks(self):
        # chunks: ["ab", "!", "ab", "!"]; (b, "!") would have count 2 if chunks were joined
        tok = trained("ab!ab!", 300)
        self.assertEqual(tok.merges, {(A, B): 256})

    def test_retrain_replaces(self):
        tok = trained("aaaa", 300)
        tok.train("bbbb", 300)
        self.assertNotIn((A, A), tok.merges)
        self.assertIn((B, B), tok.merges)


class TestEncode(unittest.TestCase):
    def test_untrained_is_raw_bytes(self):
        tok = BPETokenizer()
        self.assertEqual(tok.encode("hé"), [104, 0xC3, 0xA9])

    def test_classic_example(self):
        tok = trained()
        self.assertEqual(tok.encode("aaabdaaabac"), [258, D, 258, A, C])

    def test_lowest_merge_id_first(self):
        tok = trained()  # merges: aa->256, ab->257, (256,257)->258
        self.assertEqual(tok.encode("aab"), [256, B])

    def test_chunks_encoded_separately(self):
        tok = trained()
        self.assertEqual(tok.encode("aa aa"), [256, SPACE, 256])

    def test_roundtrip(self):
        tok = trained(CORPUS, 350)
        for text in [CORPUS, "the fox", "日本", "😀 👍🏽", "", "zzz qqq", "  \n\t x"]:
            with self.subTest(text=text[:20]):
                self.assertEqual(tok.decode(tok.encode(text)), text)

    def test_compresses(self):
        tok = trained(CORPUS, 350)
        self.assertLess(len(tok.encode(CORPUS)), len(CORPUS.encode()) * 0.6)

    def test_encode_ordinary_ignores_specials(self):
        tok = BPETokenizer()
        tok.register_special_tokens({"<|x|>": 999})
        self.assertEqual(tok.encode_ordinary("<|x|>"), list(b"<|x|>"))


class TestDecode(unittest.TestCase):
    def test_bytes(self):
        tok = BPETokenizer()
        self.assertEqual(tok.decode([104, 105]), "hi")

    def test_multibyte_split_over_tokens(self):
        tok = BPETokenizer()
        self.assertEqual(tok.decode(list("é😀".encode())), "é😀")

    def test_invalid_utf8_replaced(self):
        tok = BPETokenizer()
        self.assertEqual(tok.decode([0xFF, 104]), "�h")

    def test_merged_tokens(self):
        tok = trained()
        self.assertEqual(tok.decode([258, D]), "aaabd")

    def test_unknown_id(self):
        with self.assertRaises(ValueError):
            BPETokenizer().decode([256])


class TestSpecialTokens(unittest.TestCase):
    def setUp(self):
        self.tok = trained()
        self.tok.register_special_tokens({"<|end|>": 1001, "<|endoftext|>": 1000, "<|end|>\n": 1002})

    def test_encode_all(self):
        self.assertEqual(self.tok.encode("aa<|end|>b", allowed_special="all"), [256, 1001, B])

    def test_longest_match(self):
        self.assertEqual(self.tok.encode("<|endoftext|>", allowed_special="all"), [1000])
        self.assertEqual(self.tok.encode("<|end|>\n", allowed_special="all"), [1002])
        self.assertEqual(self.tok.encode("<|end|><|endoftext|>", allowed_special="all"),
                         [1001, 1000])

    def test_none_treats_as_text(self):
        self.assertEqual(self.tok.encode("<|end|>"), list(b"<|end|>"))

    def test_bad_allowed_special(self):
        with self.assertRaises(ValueError):
            self.tok.encode("x", allowed_special="some")

    def test_decode_special(self):
        self.assertEqual(self.tok.decode([256, 1000, B]), "aa<|endoftext|>b")

    def test_roundtrip(self):
        text = "x<|endoftext|>aaab<|end|>"
        self.assertEqual(self.tok.decode(self.tok.encode(text, allowed_special="all")), text)

    def test_collisions(self):
        with self.assertRaises(ValueError):
            self.tok.register_special_tokens({"<|bad|>": 100})   # byte token id
        with self.assertRaises(ValueError):
            self.tok.register_special_tokens({"<|bad|>": 258})   # merge id
        with self.assertRaises(ValueError):
            self.tok.register_special_tokens({"<|bad|>": 1000})  # another special
        self.tok.register_special_tokens({"<|end|>": 1001})     # re-registering is fine

    def test_vocab_size(self):
        self.assertEqual(self.tok.vocab_size, 256 + 3 + 3)


class TestSaveLoad(unittest.TestCase):
    def test_save_format(self):
        tok = trained()
        tok.register_special_tokens({"<|a|>": 2000, "<|z|>": 1000})
        self.assertEqual(tok.save(), "\n".join([
            "bpe v1", "3", "97 97", "97 98", "256 257", "2", "1000 <|z|>", "2000 <|a|>"]))

    def test_load_roundtrip(self):
        tok = trained(CORPUS, 330)
        tok.register_special_tokens({"<|my token|>": 5000})
        loaded = BPETokenizer.load(tok.save())
        self.assertEqual(loaded.merges, tok.merges)
        self.assertEqual(loaded.vocab, tok.vocab)
        self.assertEqual(loaded.special_tokens, {"<|my token|>": 5000})
        text = "the fox <|my token|> 日本"
        self.assertEqual(loaded.encode(text, "all"), tok.encode(text, "all"))

    def test_load_untrained(self):
        loaded = BPETokenizer.load(BPETokenizer().save())
        self.assertEqual(loaded.merges, {})
        self.assertEqual(loaded.vocab_size, 256)

    def test_bad_header(self):
        with self.assertRaises(ValueError):
            BPETokenizer.load("bpe v2\n0\n0")


if __name__ == "__main__":
    unittest.main()
