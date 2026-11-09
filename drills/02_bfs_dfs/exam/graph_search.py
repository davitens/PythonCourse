"""Graph traversal. A graph is a dict {node: sorted list of neighbours}. Each docstring is the spec."""
from collections import deque


def build_graph(edges, directed=False):
    """Adjacency dict from (u, v) edges. Every node that appears in an edge is a key,
    even if it has no outgoing edges. Undirected graphs get both directions.
    Neighbour lists are sorted and contain no duplicates."""
    graph = {}
    for u, v in edges:
        graph.setdefault(u, set()).add(v)
        if not directed:
            graph.setdefault(v, set()).add(u)
    return {node: sorted(nbs) for node, nbs in graph.items()}


def bfs_order(graph, start):
    """Nodes in breadth-first order from start (neighbours in list order)."""
    seen = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.pop()
        order.append(node)
        for nb in graph[node]:
            if nb not in seen:
                seen.add(nb)
                queue.append(nb)
    return order


def dfs_order(graph, start):
    """Nodes in recursive depth-first PREORDER from start (neighbours in list order)."""
    order, seen = [], set()

    def visit(node):
        seen.add(node)
        order.append(node)
        for nb in graph[node]:
            if nb not in seen:
                visit(nb)

    visit(start)
    return order


def shortest_path(graph, start, goal):
    """A path with the fewest edges from start to goal, as a list of nodes from start to
    goal (found by BFS, neighbours in list order). [start] if start == goal; None if
    goal is unreachable."""
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path
        for nb in graph[node]:
            if nb not in parent:
                parent[nb] = node
                queue.append(nb)
    return None


def grid_distance(grid, start, goal):
    """grid: list of equal-length strings, '#' = wall, anything else = open.
    start/goal: (row, col). Moves: up/down/left/right. Return the minimum number of
    moves, or -1 if unreachable (or if start or goal is a wall)."""
    rows, cols = len(grid), len(grid[0])
    if grid[start[0]][start[1]] == "#" or grid[goal[0]][goal[1]] == "#":
        return -1
    dist = {start: 0}
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            return dist[(r, c)]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and nc < cols and grid[nr][nc] != "#" and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                queue.append((nr, nc))
    return -1


def has_cycle(graph):
    """True if the DIRECTED graph contains a cycle (a self-loop counts)."""
    state = {}  # node -> "grey" (on the current path) or "black" (finished)

    def visit(u):
        state[u] = "grey"
        for v in graph[u]:
            if state.get(v) == "grey":
                return True
            if v not in state and visit(v):
                return True
        return False

    return any(visit(u) for u in graph if u not in state)
