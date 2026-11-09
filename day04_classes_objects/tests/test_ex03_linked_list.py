import unittest

from ex03_linked_list import LinkedList


class TestLinkedList(unittest.TestCase):
    def test_empty(self):
        ll = LinkedList()
        self.assertEqual(len(ll), 0)
        self.assertEqual(ll.to_list(), [])
        with self.assertRaises(IndexError):
            ll.pop_left()

    def test_init_append_prepend(self):
        ll = LinkedList([2, 3])
        ll.append(4)
        ll.prepend(1)
        self.assertEqual(ll.to_list(), [1, 2, 3, 4])
        self.assertEqual(len(ll), 4)

    def test_prepend_then_append_on_empty(self):
        ll = LinkedList()
        ll.prepend("a")
        ll.append("b")
        self.assertEqual(ll.to_list(), ["a", "b"])

    def test_pop_left(self):
        ll = LinkedList([1, 2])
        self.assertEqual(ll.pop_left(), 1)
        self.assertEqual(ll.pop_left(), 2)
        self.assertEqual(len(ll), 0)
        ll.append(9)  # tail must have been reset
        self.assertEqual(ll.to_list(), [9])

    def test_remove(self):
        ll = LinkedList([1, 2, 3, 2])
        ll.remove(2)
        self.assertEqual(ll.to_list(), [1, 3, 2])
        ll.remove(2)  # removing the tail
        ll.append(5)
        self.assertEqual(ll.to_list(), [1, 3, 5])
        ll.remove(1)  # removing the head
        self.assertEqual(ll.to_list(), [3, 5])
        self.assertEqual(len(ll), 2)
        with self.assertRaises(ValueError):
            ll.remove(42)

    def test_contains_and_iter(self):
        ll = LinkedList("abc")
        self.assertIn("b", ll)
        self.assertNotIn("z", ll)
        self.assertEqual([x for x in ll], ["a", "b", "c"])
        self.assertEqual(list(ll), list(ll))  # iterable more than once

    def test_getitem(self):
        ll = LinkedList([10, 20, 30])
        self.assertEqual(ll[0], 10)
        self.assertEqual(ll[2], 30)
        self.assertEqual(ll[-1], 30)
        self.assertEqual(ll[-3], 10)
        for bad in (3, -4):
            with self.assertRaises(IndexError):
                ll[bad]

    def test_reverse(self):
        ll = LinkedList([1, 2, 3])
        ll.reverse()
        self.assertEqual(ll.to_list(), [3, 2, 1])
        ll.append(0)  # tail updated correctly
        self.assertEqual(ll.to_list(), [3, 2, 1, 0])

    def test_reverse_empty(self):
        ll = LinkedList()
        ll.reverse()
        self.assertEqual(ll.to_list(), [])


if __name__ == "__main__":
    unittest.main()
