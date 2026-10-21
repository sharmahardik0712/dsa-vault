"""
PATTERN: Breadth-First Search (shortest path in unweighted graphs, multi-source BFS)
USE WHEN: Shortest path / minimum number of steps where every move costs the same, or spreading
          from many sources at once ("distance to nearest X", "minutes until all rot").
SIGNALS: "shortest path" (unweighted), "minimum steps/moves", "word ladder", "rotting oranges",
         "nearest", "level by level", "open the lock", "knight moves"
TIME: O(V + E), grids O(rows * cols)   SPACE: O(V)
PITFALLS: - Mark visited when you ENQUEUE, not when you dequeue (or nodes get queued many times).
          - Multi-source: put ALL sources in the queue at distance 0 before the loop.
          - Counting levels: process `len(queue)` items per round.
          - Use collections.deque; list.pop(0) is O(n).
PROBLEMS: 994 Rotting Oranges, 127 Word Ladder, 542 01 Matrix, 1091 Shortest Path in Binary Matrix,
          752 Open the Lock
"""
from collections import defaultdict, deque

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


# ---------- Core template ----------
def bfs_distance(n: int, edges: list[tuple[int, int]], src: int, dst: int) -> int:
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    queue = deque([src])
    dist = {src: 0}                         # doubles as visited
    while queue:
        node = queue.popleft()
        if node == dst:
            return dist[node]
        for nxt in graph[node]:
            if nxt not in dist:
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return -1


# ---------- Worked problems ----------
def oranges_rotting(grid: list[list[int]]) -> int:
    # LC 994. Multi-source BFS: every rotten orange starts in the queue at minute 0.
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    queue: deque[tuple[int, int]] = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1


def ladder_length(begin: str, end: str, words: list[str]) -> int:
    # LC 127. BFS over words; neighbours via wildcard buckets "h*t" -> [hot, hit].
    if end not in words:
        return 0
    buckets: dict[str, list[str]] = defaultdict(list)
    for w in words + [begin]:
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)
    queue = deque([(begin, 1)])
    seen = {begin}
    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps
        for i in range(len(word)):
            key = word[:i] + "*" + word[i + 1:]
            for nxt in buckets[key]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps + 1))
            buckets[key] = []               # bucket fully explored, never scan again
    return 0


def update_matrix(mat: list[list[int]]) -> list[list[int]]:
    # LC 542. Multi-source BFS from every 0 gives distance to the nearest 0.
    rows, cols = len(mat), len(mat[0])
    dist = [[-1] * cols for _ in range(rows)]
    queue: deque[tuple[int, int]] = deque()
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist


if __name__ == "__main__":
    assert bfs_distance(5, [(0, 1), (1, 2), (0, 3), (3, 2), (2, 4)], 0, 4) == 3
    assert bfs_distance(3, [(0, 1)], 0, 2) == -1
    assert bfs_distance(1, [], 0, 0) == 0

    assert oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    assert oranges_rotting([[0, 2]]) == 0 and oranges_rotting([[0]]) == 0

    assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
    assert ladder_length("a", "c", ["a", "b", "c"]) == 2

    assert update_matrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]]) == [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
    assert update_matrix([[0]]) == [[0]]
    assert update_matrix([[1, 0, 1]]) == [[1, 0, 1]]
    print("ok")
