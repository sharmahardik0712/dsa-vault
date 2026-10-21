"""
PATTERN: Dijkstra (single-source shortest path, non-negative weights)
USE WHEN: Weighted graph/grid with NON-NEGATIVE costs and you need the cheapest path from a source.
          Also works for "bottleneck" costs (max edge on path) and max-probability paths.
SIGNALS: "network delay time", "cheapest path", "minimum cost", "weighted graph",
         "path with minimum effort", "path with maximum probability", "swim in rising water"
TIME: O((V + E) log V) with a binary heap   SPACE: O(V + E)
PITFALLS: - Skip stale heap entries: `if d > dist[node]: continue`.
          - Negative edges silently give wrong answers: use Bellman-Ford.
          - Unweighted graphs don't need Dijkstra: plain BFS is simpler and O(V + E).
          - Max probability: maximise with a max-heap (negate), multiply instead of add.
PROBLEMS: 743 Network Delay Time, 1631 Path With Minimum Effort, 1514 Path with Maximum Probability,
          778 Swim in Rising Water, 1976 Number of Ways to Arrive at Destination
"""
import heapq


# ---------- Core template ----------
def dijkstra(n: int, edges: list[tuple[int, int, int]], src: int) -> list[float]:
    """Directed edges (u, v, w). Returns dist list, inf where unreachable."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [float("inf")] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for nxt, w in graph[node]:
            nd = d + w
            if nd < dist[nxt]:
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return dist


# ---------- Worked problems ----------
def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    # LC 743. Nodes are 1..n; answer is the max of shortest distances.
    dist = dijkstra(n + 1, [(u, v, w) for u, v, w in times], k)
    worst = max(dist[1:])
    return -1 if worst == float("inf") else int(worst)


def minimum_effort_path(heights: list[list[int]]) -> int:
    # LC 1631. Path cost = max edge on the path instead of the sum; Dijkstra still works.
    rows, cols = len(heights), len(heights[0])
    effort = [[float("inf")] * cols for _ in range(rows)]
    effort[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        e, r, c = heapq.heappop(heap)
        if (r, c) == (rows - 1, cols - 1):
            return e
        if e > effort[r][c]:
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                ne = max(e, abs(heights[nr][nc] - heights[r][c]))
                if ne < effort[nr][nc]:
                    effort[nr][nc] = ne
                    heapq.heappush(heap, (ne, nr, nc))
    return 0


def max_probability(n: int, edges: list[list[int]], probs: list[float], start: int, end: int) -> float:
    # LC 1514. Max-heap on probability; multiplying by p <= 1 never increases it (like non-negative weights).
    graph: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for (u, v), p in zip(edges, probs):
        graph[u].append((v, p))
        graph[v].append((u, p))
    best = [0.0] * n
    best[start] = 1.0
    heap = [(-1.0, start)]
    while heap:
        neg_p, node = heapq.heappop(heap)
        p = -neg_p
        if node == end:
            return p
        if p < best[node]:
            continue
        for nxt, edge_p in graph[node]:
            if p * edge_p > best[nxt]:
                best[nxt] = p * edge_p
                heapq.heappush(heap, (-best[nxt], nxt))
    return 0.0


if __name__ == "__main__":
    assert dijkstra(4, [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1)], 0) == [0, 3, 1, 4]
    assert dijkstra(2, [], 0) == [0, float("inf")]
    assert dijkstra(1, [], 0) == [0]

    assert network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert network_delay_time([[1, 2, 1]], 2, 2) == -1
    assert network_delay_time([], 1, 1) == 0

    assert minimum_effort_path([[1, 2, 2], [3, 8, 2], [5, 3, 5]]) == 2
    assert minimum_effort_path([[1, 2, 3], [3, 8, 4], [5, 3, 5]]) == 1
    assert minimum_effort_path([[7]]) == 0

    assert max_probability(3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.2], 0, 2) == 0.25
    assert max_probability(3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.3], 0, 2) == 0.3
    assert max_probability(3, [[0, 1]], [0.5], 0, 2) == 0.0
    print("ok")
