"""Day 4 - Exercise 2: an immutable-ish 2D vector."""


class Vector2D:
    """Vector2D(x, y).

    - v + w, v - w -> new Vector2D; adding a non-vector must raise TypeError
      (hint: return NotImplemented from the dunder method).
    - v * k and k * v (k a number) -> scaled vector.
    - abs(v) -> Euclidean length (float).
    - v == w compares coordinates; a vector is never equal to a non-vector.
    - Vectors are hashable (usable in sets / as dict keys), consistent with ==.
    - x, y = v works (iteration).
    - v.dot(w) -> dot product.
    - repr(Vector2D(1, 2)) == "Vector2D(1, 2)"
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        if not isinstance(k, (int, float)):
            return NotImplemented
        return Vector2D(self.x * k, self.y * k)

    def __rmul__(self, k):
        return self.__mul__(k)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        yield self.x
        yield self.y

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __repr__(self):
        return f"Vector2D({self.x!r}, {self.y!r})"
