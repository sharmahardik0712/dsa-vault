"""
PATTERN: Floyd-Warshall (all-pairs shortest paths / transitive closure)
USE WHEN: You need distances or reachability between EVERY pair of nodes and n is small (<= ~400).
          Also for ratio/closure problems where "i -> k -> j" combines two known facts.
SIGNALS: "all pairs", "city with the smallest number of neighbours within threshold",
         "course schedule IV" (is a a prerequisite of b?), "evaluate division", "transitive"
TIME: O(n^3)   SPACE: O(n^2)
PITFALLS: - The intermediate node k MUST be the outermost loop.
          - Initialise dist[i][i] = 0 and use min() for parallel edges.
          - Undirected input: set both dist[u][v] and dist[v][u].
          - Negative cycle exists if any dist[i][i] < 0 afterwards.
PROBLEMS: 1334 Find the City With the Smallest Number of Neighbors, 1462 Course Schedule IV,
          399 Evaluate Division, 2976 Minimum Cost to Convert String I
"""


# ---------- Core template ----------
def floyd_warshall(n: int, edges: list[tuple[int, int, int]]) -> list[list[float]]:
    """Directed edges (u, v, w). Returns the n x n shortest distance matrix."""
    dist = [[float("inf")] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


# ---------- Worked problems ----------
def find_the_city(n: int, edges: list[list[int]], threshold: int) -> int:
    # LC 1334. Count reachable cities per node; ties go to the larger index (hence <=).
    both_ways = [(u, v, w) for u, v, w in edges] + [(v, u, w) for u, v, w in edges]
    dist = floyd_warshall(n, both_ways)
    best_city, best_count = -1, float("inf")
    for i in range(n):
        count = sum(1 for j in range(n) if j != i and dist[i][j] <= threshold)
        if count <= best_count:
            best_city, best_count = i, count
    return best_city


def check_if_prerequisite(n: int, prereqs: list[list[int]], queries: list[list[int]]) -> list[bool]:
    # LC 1462. Boolean closure: i reaches j if i reaches k and k reaches j.
    reach = [[False] * n for _ in range(n)]
    for a, b in prereqs:
        reach[a][b] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return [reach[a][b] for a, b in queries]


def calc_equation(equations: list[list[str]], values: list[float],
                  queries: list[list[str]]) -> list[float]:
    # LC 399. ratio[a][c] = ratio[a][b] * ratio[b][c]; None means unknown.
    names = {v for pair in equations for v in pair}
    idx = {name: i for i, name in enumerate(names)}
    n = len(idx)
    ratio: list[list[float | None]] = [[None] * n for _ in range(n)]
    for i in range(n):
        ratio[i][i] = 1.0
    for (a, b), v in zip(equations, values):
        ratio[idx[a]][idx[b]] = v
        ratio[idx[b]][idx[a]] = 1 / v
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if ratio[i][j] is None and ratio[i][k] is not None and ratio[k][j] is not None:
                    ratio[i][j] = ratio[i][k] * ratio[k][j]
    res = []
    for a, b in queries:
        if a not in idx or b not in idx or ratio[idx[a]][idx[b]] is None:
            res.append(-1.0)
        else:
            res.append(ratio[idx[a]][idx[b]])
    return res


if __name__ == "__main__":
    d = floyd_warshall(3, [(0, 1, 4), (1, 2, 1), (0, 2, 7)])
    assert d[0][2] == 5 and d[2][0] == float("inf") and d[1][1] == 0

    assert find_the_city(4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4) == 3
    assert find_the_city(5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2) == 0
    assert find_the_city(2, [], 1) == 1

    assert check_if_prerequisite(3, [[1, 2], [1, 0], [2, 0]], [[1, 0], [1, 2]]) == [True, True]
    assert check_if_prerequisite(2, [[1, 0]], [[0, 1], [1, 0]]) == [False, True]
    assert check_if_prerequisite(2, [], [[1, 0], [0, 1]]) == [False, False]

    eq = [["a", "b"], ["b", "c"]]
    q = [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]
    assert calc_equation(eq, [2.0, 3.0], q) == [6.0, 0.5, -1.0, 1.0, -1.0]
    assert calc_equation([["a", "b"]], [0.5], [["b", "a"]]) == [2.0]
    print("ok")
