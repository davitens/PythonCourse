"""Day 4 - Exercise 4: FIX ME (reference solution). One bug per class; fixes marked # FIX."""


class Team:
    """A team with its own member list."""

    def __init__(self, name):
        self.name = name
        self.members = []  # FIX: was a class attribute `members = []` shared by all teams

    def add(self, member):
        self.members.append(member)


class Basket:
    """Basket(items=None). Must copy the given items (never alias the caller's list)
    and never share state between baskets."""

    def __init__(self, items=None):  # FIX: was items=[] and self.items = items
        self.items = list(items) if items is not None else []

    def add(self, item):
        self.items.append(item)


class Point:
    """Points are equal when their coordinates are equal, and usable in sets."""

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):  # FIX: missing (defining __eq__ removes the default __hash__)
        return hash((self.x, self.y))


class Shape:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"{self.name} with area {self.area()}"


class Rectangle(Shape):
    def __init__(self, w, h):
        super().__init__("rectangle")  # FIX: super().__init__ was not called
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h


class Temperature:
    """Temperature(celsius); celsius below -273.15 raises ValueError."""

    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value  # FIX: was self.celsius = value (infinite recursion)

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32


class Playlist:
    """A playlist of song titles; iterating yields titles in order, len = number of songs."""

    def __init__(self):
        self.songs = []

    def add(self, title):
        self.songs.append(title)
        return self

    def __len__(self):
        return len(self.songs)

    def __iter__(self):
        return iter(self.songs)  # FIX: was `yield self.songs` (yielded the whole list once)
