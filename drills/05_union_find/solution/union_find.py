"""Union-Find (disjoint sets) and Kruskal's MST. Each docstring is the spec."""


class UnionFind:
    """Disjoint sets over hashable elements.

    UnionFind(elements=()) - every element starts in its own set.
    add(x)            - add x as a new singleton set (no-op if already present)
    find(x)           - root of x's set, with path compression; KeyError if x is unknown
    union(a, b)       - merge the sets; return True if they were different, False otherwise.
                        Union by size: the root of the SMALLER set is attached under the
                        root of the larger one. On equal sizes, b's root goes under a's root.
    connected(a, b)   - same set?
    size_of(x)        - number of elements in x's set
    count             - attribute: number of disjoint sets
    groups()          - list of sets as sorted lists, the list sorted by first element
    """

    def __init__(self, elements=()):
        self.parent = {}
        self.size = {}
        self.count = 0
        for x in elements:
            self.add(x)

    def add(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1
            self.count += 1

    def find(self, x):
        if x not in self.parent:
            raise KeyError(x)
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            nxt = self.parent[x]
            self.parent[x] = root
            x = nxt
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def size_of(self, x):
        return self.size[self.find(x)]

    def groups(self):
        out = {}
        for x in self.parent:
            out.setdefault(self.find(x), []).append(x)
        return sorted(sorted(g) for g in out.values())


def kruskal(n, edges):
    """Minimum spanning tree of nodes 0..n-1. edges: list of (u, v, weight).
    Consider edges by increasing weight (ties: by u, then v). Return (total_weight,
    list of chosen (u, v, weight) in the order chosen). If the graph is disconnected,
    raise ValueError."""
    uf = UnionFind(range(n))
    chosen, total = [], 0
    for u, v, w in sorted(edges, key=lambda e: (e[2], e[0], e[1])):
        if uf.union(u, v):
            chosen.append((u, v, w))
            total += w
    if n > 0 and uf.count != 1:
        raise ValueError("graph is disconnected")
    return total, chosen
