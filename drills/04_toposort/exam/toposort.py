"""Topological sorting. An edge (a, b) means "a must come before b".
`nodes` may omit nodes that appear in edges; those are included too. Duplicate edges are
ignored. Each docstring is the spec."""
import heapq


def _graph(nodes, edges):
    succ = {n: set() for n in nodes}
    for a, b in edges:
        succ.setdefault(a, set()).add(b)
        succ.setdefault(b, set())
    indeg = {n: 0 for n in succ}
    for a, b in edges:
        indeg[b] += 1
    return succ, indeg


def topo_sort(nodes, edges):
    """Kahn's algorithm. Whenever several nodes are available, take the SMALLEST.
    Raise ValueError("cycle") if the graph has a cycle."""
    succ, indeg = _graph(nodes, edges)
    heap = [n for n in succ if indeg[n] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        n = heap.pop()
        order.append(n)
        for m in succ[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                heapq.heappush(heap, m)
    if len(order) != len(nodes):
        raise ValueError("cycle")
    return order


def build_order(depends_on):
    """depends_on: {task: [tasks it depends on]}. Return an order in which every task comes
    after all its dependencies (smallest-available rule, as topo_sort)."""
    edges = [(task, dep) for task, deps in depends_on.items() for dep in deps]
    return topo_sort(list(depends_on), edges)


def levels(nodes, edges):
    """Group nodes into levels: level 0 = nodes without predecessors; level k+1 = nodes
    whose predecessors are all in levels <= k. Each level sorted. ValueError on a cycle."""
    succ, indeg = _graph(nodes, edges)
    current = sorted(n for n in succ if indeg[n] == 0)
    out, seen = [], 0
    while current:
        out.append(current)
        seen += len(current)
        nxt = []
        for n in current:
            for m in succ[n]:
                indeg[m] -= 1
                if indeg[m] == 0:
                    nxt.append(m)
        current = sorted(nxt)
    if seen != len(succ):
        raise ValueError("cycle")
    return out


def longest_chain(nodes, edges):
    """Number of nodes on the longest path in the DAG (a single node is a chain of 1;
    an empty graph -> 0). ValueError on a cycle."""
    succ, _ = _graph(nodes, edges)
    longest = {n: 0 for n in succ}
    for n in topo_sort(nodes, edges):
        for m in succ[n]:
            longest[m] = max(longest[m], longest[n] + 1)
    return max(longest.values(), default=0)
