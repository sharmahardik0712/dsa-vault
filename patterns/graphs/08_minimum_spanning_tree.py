"""
PATTERN: Minimum Spanning Tree (Kruskal and Prim)
USE WHEN: Connect ALL nodes with the minimum total edge cost (no need for paths from a source).
SIGNALS: "minimum cost to connect all", "connecting cities", "min cost to supply water",
         "minimum spanning tree", "cheapest network", "all points connected"
TIME: Kruskal O(E log E); Prim O(E log V) (O(V^2 log V) on a complete graph)   SPACE: O(V + E)
PITFALLS: - Kruskal: the MST exists only if exactly V - 1 edges were added (else disconnected -> -1).
          - Prim: skip nodes already in the tree when popped (stale heap entries).
          - Dense / implicit complete graphs (all point pairs): Prim avoids building all E edges up front.
          - 1-indexed input: size the DSU n + 1.
PROBLEMS: 1584 Min Cost to Connect All Points, 1135 Connecting Cities With Minimum Cost,
          1168 Optimize Water Distribution, 1489 Critical and Pseudo-Critical Edges
"""
import heapq


# ---------- Core template: Kruskal (sort edges + union-find) ----------
def kruskal(n: int, edges: list[tuple[int, int, int]]) -> int:
    """Nodes 0..n-1, edges (w, u, v). Returns MST weight, or -1 if disconnected."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    used = 0
    for w, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += w
            used += 1
    return total if used == max(n - 1, 0) else -1


# ---------- Worked problems ----------
def minimum_cost_cities(n: int, connections: list[list[int]]) -> int:
    # LC 1135. Cities are 1..n; shift to 0-indexed and run Kruskal.
    return kruskal(n, [(w, a - 1, b - 1) for a, b, w in connections])


def min_cost_connect_points(points: list[list[int]]) -> int:
    # LC 1584. Prim: grow the tree from node 0, always add the cheapest edge leaving it.
    n = len(points)
    in_tree = [False] * n
    heap = [(0, 0)]
    total = 0
    added = 0
    while added < n:
        cost, u = heapq.heappop(heap)
        if in_tree[u]:
            continue
        in_tree[u] = True
        total += cost
        added += 1
        for v in range(n):
            if not in_tree[v]:
                d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                heapq.heappush(heap, (d, v))
    return total


if __name__ == "__main__":
    assert kruskal(4, [(1, 0, 1), (2, 1, 2), (3, 0, 2), (4, 2, 3)]) == 7
    assert kruskal(3, [(1, 0, 1)]) == -1
    assert kruskal(1, []) == 0

    assert minimum_cost_cities(3, [[1, 2, 5], [1, 3, 6], [2, 3, 1]]) == 6
    assert minimum_cost_cities(4, [[1, 2, 3], [3, 4, 4]]) == -1

    assert min_cost_connect_points([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20
    assert min_cost_connect_points([[3, 12], [-2, 5], [-4, 1]]) == 18
    assert min_cost_connect_points([[0, 0]]) == 0
    print("ok")
