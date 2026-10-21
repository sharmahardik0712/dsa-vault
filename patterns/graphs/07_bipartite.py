"""
PATTERN: Bipartite Check (two-colouring)
USE WHEN: Nodes must be split into two groups so every edge goes between groups: "enemies in
          different teams", "no two adjacent same colour", or detecting an odd cycle.
SIGNALS: "is graph bipartite", "possible bipartition", "two groups", "dislikes",
         "two colours", "odd cycle"
TIME: O(V + E)   SPACE: O(V)
PITFALLS: - The graph may be disconnected: start a BFS from EVERY uncoloured node.
          - Colour on enqueue (like visited), and compare when you see an already coloured neighbour.
          - 1-indexed inputs (people 1..n): size arrays n + 1.
          - Undirected: add both directions when building the adjacency list.
PROBLEMS: 785 Is Graph Bipartite, 886 Possible Bipartition, 1042 Flower Planting With No Adjacent
"""
from collections import deque


# ---------- Core template ----------
def two_colour(adj: list[list[int]]) -> list[int] | None:
    """Returns a 0/1 colour per node, or None if the graph has an odd cycle."""
    colour = [-1] * len(adj)
    for start in range(len(adj)):
        if colour[start] != -1:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in adj[node]:
                if colour[nxt] == -1:
                    colour[nxt] = 1 - colour[node]
                    queue.append(nxt)
                elif colour[nxt] == colour[node]:
                    return None
    return colour


# ---------- Worked problems ----------
def is_bipartite(graph: list[list[int]]) -> bool:
    # LC 785. Input is already an adjacency list.
    return two_colour(graph) is not None


def possible_bipartition(n: int, dislikes: list[list[int]]) -> bool:
    # LC 886. People who dislike each other must be in different groups = bipartite.
    adj: list[list[int]] = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        adj[a].append(b)
        adj[b].append(a)
    return two_colour(adj) is not None


if __name__ == "__main__":
    assert two_colour([[1], [0]]) in ([0, 1], [1, 0])
    assert two_colour([[1, 2], [0, 2], [0, 1]]) is None           # triangle

    assert not is_bipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]])
    assert is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]])
    assert is_bipartite([]) and is_bipartite([[]])
    assert is_bipartite([[1], [0], [4], [4], [2, 3]])            # disconnected components
    assert not is_bipartite([[], [2, 3], [1, 3], [1, 2]])        # odd cycle in 2nd component

    assert possible_bipartition(4, [[1, 2], [1, 3], [2, 4]])
    assert not possible_bipartition(3, [[1, 2], [1, 3], [2, 3]])
    assert not possible_bipartition(5, [[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]])
    assert possible_bipartition(1, [])
    print("ok")
