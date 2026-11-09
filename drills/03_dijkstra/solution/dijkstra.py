"""Dijkstra's algorithm. A graph is a dict {u: [(v, weight), ...]} (directed edges).
A node may appear only as an edge target. Each docstring is the spec."""
import heapq


def validate(graph):
    """Raise ValueError if any edge weight is negative."""
    for u, edges in graph.items():
        for v, w in edges:
            if w < 0:
                raise ValueError(f"negative weight on {u}->{v}")


def dijkstra(graph, source):
    """Return (dist, prev): dist[node] = cost of the cheapest path from source, for every
    REACHABLE node (dist[source] == 0); prev[node] = previous node on that path (source has
    no entry). When two paths have the same cost, keep the one found FIRST (only a strictly
    cheaper path replaces a known one). Raises ValueError for negative weights."""
    validate(graph)
    dist, prev = {source: 0}, {}
    heap = [(0, source)]
    done = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, w in graph.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def shortest_path(graph, source, target):
    """(cost, [source, ..., target]) for the cheapest path, or None if unreachable.
    source == target -> (0, [source])."""
    dist, prev = dijkstra(graph, source)
    if target not in dist:
        return None
    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    path.reverse()
    return dist[target], path


def within(graph, source, max_cost):
    """List of (cost, node) for every node whose distance from source is <= max_cost,
    sorted by cost, then node. Includes the source itself."""
    dist, _ = dijkstra(graph, source)
    return sorted((d, node) for node, d in dist.items() if d <= max_cost)
