"""Day 4 - Exercise 3: singly linked list."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    """A singly linked list.

    LinkedList(iterable=None) - optional initial values, in order.
    append(v), prepend(v)
    pop_left() -> removes and returns the first value; IndexError if empty
    remove(v)  -> removes the FIRST node with value v; ValueError if absent
    reverse()  -> reverses in place
    len(ll), iter(ll), v in ll, ll[i] (negative indices allowed; IndexError if out of range)
    to_list()  -> list of values
    """

    def __init__(self, iterable=None):
        raise NotImplementedError

    def append(self, value):
        raise NotImplementedError

    def prepend(self, value):
        raise NotImplementedError

    def pop_left(self):
        raise NotImplementedError

    def remove(self, value):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __contains__(self, value):
        raise NotImplementedError

    def __getitem__(self, index):
        raise NotImplementedError

    def to_list(self):
        raise NotImplementedError
