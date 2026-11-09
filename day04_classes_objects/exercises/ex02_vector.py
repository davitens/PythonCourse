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
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __mul__(self, k):
        raise NotImplementedError

    def __rmul__(self, k):
        raise NotImplementedError

    def __abs__(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def dot(self, other):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError
