"""
PATTERN: Bridges and Articulation Points (Tarjan's low-link)
USE WHEN: You need edges (bridges) or nodes (articulation points) whose removal disconnects an
          undirected graph: single points of failure in a network.
SIGNALS: "critical connections", "critical edges", "cut vertex", "single point of failure",
         "minimum days to disconnect island", "which server removal splits the network"
TIME: O(V + E)   SPACE: O(V + E)
PITFALLS: - disc[u] = discovery time; low[u] = earliest disc reachable from u's subtree using ONE back edge.
          - Bridge: low[v] > disc[u]. Articulation point: low[v] >= disc[u] (non-root),
            or the DFS root with 2+ children.
          - Skip the parent when looking at back edges (skip the parent EDGE id if parallel edges exist).
          - Deep graphs hit the recursion limit: raise it or convert to iterative.
PROBLEMS: 1192 Critical Connections in a Network, 1568 Minimum Number of Days to Disconnect Island,
          "articulation points" (classic)
"""
import sys


def build_graph(n: int, edges: list[list[int]]) -> list[list[int]]:
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph


# ---------- Core template: bridges ----------
def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:
    # LC 1192.
    sys.setrecursionlimit(max(1000, 2 * n + 10))
    graph = build_graph(n, connections)
    disc = [-1] * n
    low = [0] * n
    timer = 0
    bridges: list[list[int]] = []

    def dfs(u: int, parent: int) -> None:
        nonlocal timer
        disc[u] = low[u] = timer
        timer += 1
        for v in graph[u]:
            if v == parent:
                continue
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append([u, v])
            else:
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)
    return bridges


# ---------- Worked problem: articulation points ----------
def articulation_points(n: int, edges: list[list[int]]) -> list[int]:
    # Same DFS; condition becomes low[v] >= disc[u], and the root needs 2+ DFS children.
    sys.setrecursionlimit(max(1000, 2 * n + 10))
    graph = build_graph(n, edges)
    disc = [-1] * n
    low = [0] * n
    timer = 0
    points: set[int] = set()

    def dfs(u: int, parent: int) -> None:
        nonlocal timer
        disc[u] = low[u] = timer
        timer += 1
        children = 0
        for v in graph[u]:
            if v == parent:
                continue
            if disc[v] == -1:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if parent != -1 and low[v] >= disc[u]:
                    points.add(u)
            else:
                low[u] = min(low[u], disc[v])
        if parent == -1 and children > 1:
            points.add(u)

    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)
    return sorted(points)


if __name__ == "__main__":
    assert sorted(map(sorted, critical_connections(4, [[0, 1], [1, 2], [2, 0], [1, 3]]))) == [[1, 3]]
    assert critical_connections(2, [[0, 1]]) == [[0, 1]]
    assert critical_connections(3, [[0, 1], [1, 2], [2, 0]]) == []
    assert sorted(map(sorted, critical_connections(3, [[0, 1], [1, 2]]))) == [[0, 1], [1, 2]]

    assert articulation_points(5, [[1, 0], [0, 2], [2, 1], [0, 3], [3, 4]]) == [0, 3]
    assert articulation_points(3, [[0, 1], [1, 2], [2, 0]]) == []
    assert articulation_points(3, [[0, 1], [1, 2]]) == [1]
    assert articulation_points(1, []) == []
    print("ok")
