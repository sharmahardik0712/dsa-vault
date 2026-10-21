"""
PATTERN: Bellman-Ford (negative weights, at most K edges, negative-cycle detection)
USE WHEN: Edges can be negative, you must detect a negative cycle, or the path is limited to
          at most K edges/stops (which breaks Dijkstra's greedy choice).
SIGNALS: "negative weights", "at most k stops", "cheapest flights within k stops",
         "detect negative cycle", "arbitrage", "limited number of edges"
TIME: O(V * E) (O(K * E) for the K-edge version)   SPACE: O(V)
PITFALLS: - Shortest path uses at most V - 1 edges, so V - 1 rounds; one more successful relax = negative cycle.
          - K stops = K + 1 edges = K + 1 rounds.
          - For the K-edge limit, relax from a SNAPSHOT of the previous round, or one round chains many edges.
          - Skip relaxing from nodes still at inf (inf + negative is still inf in Python, but be explicit).
PROBLEMS: 787 Cheapest Flights Within K Stops, 743 Network Delay Time (alt solution),
          "negative cycle detection" (classic), 1514 Path with Maximum Probability (alt solution)
"""


# ---------- Core template ----------
def bellman_ford(n: int, edges: list[tuple[int, int, int]], src: int) -> list[float] | None:
    """Directed edges (u, v, w). Returns dist list, or None if a negative cycle is reachable."""
    dist = [float("inf")] * n
    dist[src] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            return None
    return dist


# ---------- Worked problems ----------
def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    # LC 787. k + 1 rounds; relax from a snapshot so each round adds exactly one more edge.
    cost = [float("inf")] * n
    cost[src] = 0
    for _ in range(k + 1):
        snapshot = cost[:]
        for u, v, w in flights:
            if snapshot[u] != float("inf") and snapshot[u] + w < cost[v]:
                cost[v] = snapshot[u] + w
    return -1 if cost[dst] == float("inf") else int(cost[dst])


def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    # LC 743 again: Bellman-Ford is slower than Dijkstra here but works unchanged.
    dist = bellman_ford(n + 1, [(u, v, w) for u, v, w in times], k)
    worst = max(dist[1:])
    return -1 if worst == float("inf") else int(worst)


if __name__ == "__main__":
    assert bellman_ford(4, [(0, 1, 4), (0, 2, 5), (1, 2, -3), (2, 3, 2)], 0) == [0, 4, 1, 3]
    assert bellman_ford(3, [(0, 1, 1), (1, 2, -1), (2, 0, -1)], 0) is None
    assert bellman_ford(2, [], 0) == [0, float("inf")]

    flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
    assert find_cheapest_price(4, flights, 0, 3, 1) == 700
    tri = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    assert find_cheapest_price(3, tri, 0, 2, 1) == 200
    assert find_cheapest_price(3, tri, 0, 2, 0) == 500
    assert find_cheapest_price(2, [], 0, 1, 1) == -1

    assert network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert network_delay_time([[1, 2, 1]], 2, 2) == -1
    print("ok")
