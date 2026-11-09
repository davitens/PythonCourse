import copy
import unittest

from ex03_nested import deep_merge, flatten_dict, get_path, set_path, unflatten_dict


class TestGetPath(unittest.TestCase):
    def setUp(self):
        self.d = {"a": {"b": {"c": 42}, "x": 0}, "top": "t"}

    def test_found(self):
        self.assertEqual(get_path(self.d, "a.b.c"), 42)
        self.assertEqual(get_path(self.d, "top"), "t")
        self.assertEqual(get_path(self.d, "a.b"), {"c": 42})

    def test_falsy_value_found(self):
        self.assertEqual(get_path(self.d, "a.x", default="nope"), 0)

    def test_missing(self):
        self.assertIsNone(get_path(self.d, "a.zz.c"))
        self.assertEqual(get_path(self.d, "a.b.c.d", default=-1), -1)
        self.assertEqual(get_path(self.d, "top.x", default=-1), -1)


class TestSetPath(unittest.TestCase):
    def test_create(self):
        d = {}
        self.assertIsNone(set_path(d, "a.b.c", 1))
        self.assertEqual(d, {"a": {"b": {"c": 1}}})

    def test_existing(self):
        d = {"a": {"keep": True}}
        set_path(d, "a.new", 2)
        self.assertEqual(d, {"a": {"keep": True, "new": 2}})

    def test_replace_non_dict(self):
        d = {"a": 5}
        set_path(d, "a.b", 1)
        self.assertEqual(d, {"a": {"b": 1}})


class TestFlatten(unittest.TestCase):
    def test_flatten(self):
        d = {"a": {"b": 1, "c": {"d": 2}}, "e": 3, "f": {}}
        self.assertEqual(flatten_dict(d), {"a.b": 1, "a.c.d": 2, "e": 3})
        self.assertEqual(list(flatten_dict(d)), ["a.b", "a.c.d", "e"])

    def test_roundtrip(self):
        d = {"x": {"y": {"z": [1, 2]}, "w": None}, "v": "s"}
        self.assertEqual(unflatten_dict(flatten_dict(d)), d)


class TestDeepMerge(unittest.TestCase):
    def test_merge(self):
        a = {"db": {"host": "a", "port": 1}, "debug": False, "tags": ["x"]}
        b = {"db": {"port": 2, "user": "u"}, "debug": True}
        self.assertEqual(deep_merge(a, b), {
            "db": {"host": "a", "port": 2, "user": "u"}, "debug": True, "tags": ["x"]})

    def test_override_dict_with_value(self):
        self.assertEqual(deep_merge({"a": {"b": 1}}, {"a": 5}), {"a": 5})
        self.assertEqual(deep_merge({"a": 5}, {"a": {"b": 1}}), {"a": {"b": 1}})

    def test_inputs_untouched(self):
        a = {"db": {"host": "a"}}
        b = {"db": {"port": 2}, "new": {"k": 1}}
        a0, b0 = copy.deepcopy(a), copy.deepcopy(b)
        result = deep_merge(a, b)
        result["db"]["host"] = "CHANGED"
        result["new"]["k"] = "CHANGED"
        self.assertEqual(a, a0)
        self.assertEqual(b, b0)


if __name__ == "__main__":
    unittest.main()
