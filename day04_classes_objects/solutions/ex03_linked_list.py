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
        self.head = None
        self.tail = None
        self._size = 0
        if iterable is not None:
            for v in iterable:
                self.append(v)

    def append(self, value):
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def prepend(self, value):
        self.head = Node(value, self.head)
        if self.tail is None:
            self.tail = self.head
        self._size += 1

    def pop_left(self):
        if self.head is None:
            raise IndexError("pop from empty list")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return node.value

    def remove(self, value):
        prev, cur = None, self.head
        while cur is not None:
            if cur.value == value:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                if cur is self.tail:
                    self.tail = prev
                self._size -= 1
                return
            prev, cur = cur, cur.next
        raise ValueError(f"{value!r} not in list")

    def reverse(self):
        prev, cur = None, self.head
        self.tail = self.head
        while cur is not None:
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        self.head = prev

    def __len__(self):
        return self._size

    def __iter__(self):
        cur = self.head
        while cur is not None:
            yield cur.value
            cur = cur.next

    def __contains__(self, value):
        return any(v == value for v in self)

    def __getitem__(self, index):
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("index out of range")
        for i, v in enumerate(self):
            if i == index:
                return v

    def to_list(self):
        return list(self)
