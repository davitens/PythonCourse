import unittest

from kvstore import KVStore, run_script


class TestBasic(unittest.TestCase):
    def setUp(self):
        self.s = KVStore()

    def test_set_get(self):
        self.s.set("a", "1")
        self.s.set("a", "2")
        self.assertEqual(self.s.get("a"), "2")
        self.assertIsNone(self.s.get("missing"))

    def test_empty_string_value(self):
        self.s.set("a", "")
        self.assertEqual(self.s.get("a"), "")
        self.assertEqual(self.s.keys(), ["a"])

    def test_delete(self):
        self.s.set("a", "1")
        self.assertTrue(self.s.delete("a"))
        self.assertIsNone(self.s.get("a"))
        self.assertFalse(self.s.delete("a"))
        self.assertFalse(self.s.delete("never"))

    def test_count(self):
        for k, v in [("a", "x"), ("b", "y"), ("c", "x")]:
            self.s.set(k, v)
        self.assertEqual(self.s.count("x"), 2)
        self.assertEqual(self.s.count("z"), 0)

    def test_keys(self):
        for k in ["user:2", "user:10", "admin", "user:1"]:
            self.s.set(k, "v")
        self.assertEqual(self.s.keys(), ["admin", "user:1", "user:10", "user:2"])
        self.assertEqual(self.s.keys("user:1"), ["user:1", "user:10"])
        self.assertEqual(self.s.keys("zzz"), [])


class TestTransactions(unittest.TestCase):
    def setUp(self):
        self.s = KVStore()
        self.s.set("a", "10")

    def test_rollback(self):
        self.s.begin()
        self.s.set("a", "20")
        self.s.set("b", "1")
        self.assertEqual(self.s.get("a"), "20")
        self.s.rollback()
        self.assertEqual(self.s.get("a"), "10")
        self.assertIsNone(self.s.get("b"))
        self.assertEqual(self.s.depth, 0)

    def test_nested_visibility(self):
        self.s.begin()
        self.s.set("a", "20")
        self.s.begin()
        self.s.set("a", "30")
        self.assertEqual(self.s.get("a"), "30")
        self.assertEqual(self.s.depth, 2)

    def test_nested_rollback_only_innermost(self):
        self.s.begin()
        self.s.set("a", "20")
        self.s.begin()
        self.s.set("a", "30")
        self.s.rollback()
        self.assertEqual(self.s.get("a"), "20")
        self.s.rollback()
        self.assertEqual(self.s.get("a"), "10")

    def test_delete_in_transaction(self):
        self.s.begin()
        self.assertTrue(self.s.delete("a"))
        self.assertIsNone(self.s.get("a"))
        self.assertFalse(self.s.delete("a"))
        self.assertEqual(self.s.keys(), [])
        self.s.rollback()
        self.assertEqual(self.s.get("a"), "10")

    def test_delete_key_created_in_transaction(self):
        self.s.begin()
        self.s.set("new", "1")
        self.assertTrue(self.s.delete("new"))
        self.assertIsNone(self.s.get("new"))

    def test_spec_example(self):
        self.s.begin()
        self.s.set("a", "20")
        self.s.begin()
        self.s.delete("a")
        self.assertIsNone(self.s.get("a"))
        self.s.rollback()
        self.assertEqual(self.s.get("a"), "20")
        self.s.rollback()
        self.assertEqual(self.s.get("a"), "10")

    def test_commit_all_levels(self):
        self.s.begin()
        self.s.set("b", "1")
        self.s.begin()
        self.s.set("c", "2")
        self.s.delete("a")
        self.s.commit()
        self.assertEqual(self.s.depth, 0)
        self.assertEqual(self.s.keys(), ["b", "c"])
        with self.assertRaises(RuntimeError):
            self.s.rollback()

    def test_commit_with_delete_then_get(self):
        self.s.begin()
        self.s.delete("a")
        self.s.commit()
        self.assertIsNone(self.s.get("a"))
        self.assertEqual(self.s.count("10"), 0)

    def test_no_transaction(self):
        with self.assertRaises(RuntimeError):
            self.s.rollback()
        with self.assertRaises(RuntimeError):
            self.s.commit()

    def test_count_sees_transaction(self):
        self.s.begin()
        self.s.set("b", "10")
        self.assertEqual(self.s.count("10"), 2)
        self.s.delete("a")
        self.assertEqual(self.s.count("10"), 1)


class TestSerialize(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(KVStore().serialize(), b"KV1\x00\x00\x00\x00")

    def test_exact_bytes(self):
        s = KVStore()
        s.set("b", "2")
        s.set("é", "x y")
        s.set("a", "")
        self.assertEqual(s.serialize(),
                         b"KV1" + b"\x00\x00\x00\x03"
                         + b"\x00\x01a" + b"\x00\x00\x00\x00"
                         + b"\x00\x01b" + b"\x00\x00\x00\x012"
                         + b"\x00\x02\xc3\xa9" + b"\x00\x00\x00\x03x y")

    def test_visible_state(self):
        s = KVStore()
        s.set("a", "1")
        s.begin()
        s.set("b", "2")
        s.delete("a")
        restored = KVStore.deserialize(s.serialize())
        self.assertEqual(restored.keys(), ["b"])

    def test_roundtrip_unicode(self):
        s = KVStore()
        data = {"日本": "語", "emoji😀": "👍🏽 ok", "plain": "text with  spaces", "z": ""}
        for k, v in data.items():
            s.set(k, v)
        restored = KVStore.deserialize(s.serialize())
        self.assertEqual({k: restored.get(k) for k in restored.keys()}, data)
        self.assertEqual(restored.depth, 0)

    def test_long_value(self):
        s = KVStore()
        s.set("k", "v" * 70000)
        self.assertEqual(KVStore.deserialize(s.serialize()).get("k"), "v" * 70000)

    def test_bad_magic(self):
        with self.assertRaises(ValueError):
            KVStore.deserialize(b"KV2\x00\x00\x00\x00")

    def test_truncated(self):
        s = KVStore()
        s.set("key", "value")
        blob = s.serialize()
        for cut in range(len(blob)):
            with self.subTest(cut=cut):
                with self.assertRaises(ValueError):
                    KVStore.deserialize(blob[:cut])

    def test_trailing_bytes(self):
        with self.assertRaises(ValueError):
            KVStore.deserialize(KVStore().serialize() + b"\x00")

    def test_invalid_utf8(self):
        blob = b"KV1\x00\x00\x00\x01\x00\x01\xff\x00\x00\x00\x00"
        with self.assertRaises(ValueError):
            KVStore.deserialize(blob)

    def test_unsorted_or_duplicate(self):
        entry_b = b"\x00\x01b\x00\x00\x00\x00"
        entry_a = b"\x00\x01a\x00\x00\x00\x00"
        for blob in (b"KV1\x00\x00\x00\x02" + entry_b + entry_a,
                     b"KV1\x00\x00\x00\x02" + entry_a + entry_a):
            with self.assertRaises(ValueError):
                KVStore.deserialize(blob)


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.s = KVStore()

    def test_set_get(self):
        self.assertEqual(self.s.execute("SET name Ada"), "")
        self.assertEqual(self.s.execute("GET name"), "Ada")
        self.assertEqual(self.s.execute("GET nobody"), "NULL")

    def test_value_with_spaces(self):
        self.s.execute("SET greeting   hello   big world  ")
        self.assertEqual(self.s.execute("GET greeting"), "hello   big world")

    def test_case_insensitive_command(self):
        self.s.execute("set K v")
        self.assertEqual(self.s.execute("Get K"), "v")
        self.assertEqual(self.s.execute("get k"), "NULL")

    def test_delete_count_keys(self):
        self.s.execute("SET a x")
        self.s.execute("SET b x")
        self.s.execute("SET ab y")
        self.assertEqual(self.s.execute("COUNT x"), "2")
        self.assertEqual(self.s.execute("KEYS a"), "a,ab")
        self.assertEqual(self.s.execute("KEYS"), "a,ab,b")
        self.assertEqual(self.s.execute("DELETE a"), "1")
        self.assertEqual(self.s.execute("DELETE a"), "0")
        self.assertEqual(self.s.execute("KEYS zz"), "")

    def test_count_value_with_spaces(self):
        self.s.execute("SET a two words")
        self.assertEqual(self.s.execute("COUNT two words"), "1")

    def test_transactions(self):
        self.assertEqual(self.s.execute("ROLLBACK"), "NO TRANSACTION")
        self.assertEqual(self.s.execute("COMMIT"), "NO TRANSACTION")
        self.assertEqual(self.s.execute("BEGIN"), "")
        self.assertEqual(self.s.execute("ROLLBACK"), "")

    def test_errors(self):
        for bad in ["FLY away", "SET onlykey", "GET", "GET a b", "DELETE", "BEGIN now", "KEYS a b"]:
            with self.subTest(bad=bad):
                self.assertEqual(self.s.execute(bad), "ERROR")

    def test_blank(self):
        self.assertEqual(self.s.execute("   "), "")


class TestRunScript(unittest.TestCase):
    def test_script(self):
        script = [
            "SET a 10",
            "BEGIN",
            "SET a 20",
            "GET a",
            "BEGIN",
            "DELETE a",
            "GET a",
            "ROLLBACK",
            "GET a",
            "COMMIT",
            "GET a",
            "ROLLBACK",
            "",
            "COUNT 20",
        ]
        self.assertEqual(run_script(script), ["20", "1", "NULL", "20", "20", "NO TRANSACTION", "1"])

    def test_fresh_store_each_time(self):
        run_script(["SET a 1"])
        self.assertEqual(run_script(["GET a"]), ["NULL"])


if __name__ == "__main__":
    unittest.main()
