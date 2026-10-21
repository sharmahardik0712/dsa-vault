"""
PATTERN: Topological Sort (Kahn's BFS and DFS)
USE WHEN: Directed graph of dependencies; you need a valid order, or to detect whether a cycle
          makes ordering impossible.
SIGNALS: "prerequisites", "course schedule", "build order", "dependencies", "tasks before",
         "alien dictionary", "DAG", "can all be finished"
TIME: O(V + E)   SPACE: O(V + E)
PITFALLS: - Edge direction: [course, prereq] means prereq -> course. Draw it before coding.
          - Cycle detection: Kahn's -> processed count < V. DFS -> need 3 colours, not a bool visited.
          - Nodes with no edges still belong in the result (initialise indegree for ALL nodes).
          - Alien dictionary: prefix case ("abc" before "ab") is invalid.
PROBLEMS: 207 Course Schedule, 210 Course Schedule II, 269 Alien Dictionary,
          1136 Parallel Courses, 310 Minimum Height Trees
"""
from collections import deque


# ---------- Core template: Kahn's algorithm ----------
def topo_sort(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """edges are (u, v) meaning u must come before v. Returns [] if there is a cycle."""
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    queue = deque(i for i in range(n) if indegree[i] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == n else []


# ---------- Worked problems ----------
def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    # LC 210. [a, b] means b -> a; then it's plain Kahn's.
    return topo_sort(num_courses, [(b, a) for a, b in prerequisites])


def can_finish_dfs(num_courses: int, prerequisites: list[list[int]]) -> bool:
    # LC 207 via DFS. Colours: 0 = unvisited, 1 = on current path, 2 = done. Hitting 1 = cycle.
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    for a, b in prerequisites:
        graph[b].append(a)
    state = [0] * num_courses

    def has_cycle(node: int) -> bool:
        if state[node] == 1:
            return True
        if state[node] == 2:
            return False
        state[node] = 1
        for nxt in graph[node]:
            if has_cycle(nxt):
                return True
        state[node] = 2
        return False

    return not any(has_cycle(i) for i in range(num_courses))


def alien_order(words: list[str]) -> str:
    # LC 269. First differing char of adjacent words gives one edge.
    chars = {ch for w in words for ch in w}
    graph: dict[str, set[str]] = {ch: set() for ch in chars}
    indegree = {ch: 0 for ch in chars}
    for w1, w2 in zip(words, words[1:]):
        for a, b in zip(w1, w2):
            if a != b:
                if b not in graph[a]:
                    graph[a].add(b)
                    indegree[b] += 1
                break
        else:
            if len(w1) > len(w2):
                return ""
    queue = deque(sorted(ch for ch in chars if indegree[ch] == 0))
    order: list[str] = []
    while queue:
        ch = queue.popleft()
        order.append(ch)
        for nxt in sorted(graph[ch]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return "".join(order) if len(order) == len(chars) else ""


if __name__ == "__main__":
    assert topo_sort(4, [(0, 1), (0, 2), (1, 3), (2, 3)]) == [0, 1, 2, 3]
    assert topo_sort(2, [(0, 1), (1, 0)]) == []
    assert topo_sort(0, []) == []
    assert topo_sort(3, []) == [0, 1, 2]

    assert find_order(2, [[1, 0]]) == [0, 1]
    assert find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) == [0, 1, 2, 3]
    assert find_order(2, [[1, 0], [0, 1]]) == []
    assert find_order(1, []) == [0]

    assert can_finish_dfs(2, [[1, 0]])
    assert not can_finish_dfs(2, [[1, 0], [0, 1]])
    assert not can_finish_dfs(1, [[0, 0]])               # self loop
    assert can_finish_dfs(3, [[1, 0], [2, 0]])           # diamond-ish, no cycle

    assert alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
    assert alien_order(["z", "x", "z"]) == ""
    assert alien_order(["abc", "ab"]) == ""
    assert alien_order(["z"]) == "z"
    print("ok")
