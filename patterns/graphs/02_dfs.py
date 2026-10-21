"""
PATTERN: Depth-First Search (connected regions, flood fill, reachability)
USE WHEN: You need to explore everything reachable from a cell/node: count components, measure
          region size, flood fill, or find cells reachable from a border. Path length doesn't matter.
SIGNALS: "number of islands", "max area of island", "flood fill", "connected components",
         "surrounded regions", "pacific atlantic", "clone graph", "can reach"
TIME: O(V + E), grids O(rows * cols)   SPACE: O(V) for visited + stack
PITFALLS: - Recursive DFS on large grids hits Python's recursion limit: use an explicit stack.
          - Mark visited when PUSHING to avoid duplicate work.
          - "Reachable from border" problems: start DFS from the border inward (reverse the condition).
          - Bounds check before indexing grid[r][c].
PROBLEMS: 200 Number of Islands, 695 Max Area of Island, 417 Pacific Atlantic Water Flow,
          130 Surrounded Regions, 133 Clone Graph
"""

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


# ---------- Core template: iterative DFS returning region size ----------
def flood(grid: list[list[int]], r: int, c: int) -> int:
    """Sink every 1 connected to (r, c); return how many were sunk."""
    rows, cols = len(grid), len(grid[0])
    stack = [(r, c)]
    grid[r][c] = 0
    size = 0
    while stack:
        cr, cc = stack.pop()
        size += 1
        for dr, dc in DIRS:
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 0
                stack.append((nr, nc))
    return size


# ---------- Worked problems ----------
def num_islands(grid: list[list[int]]) -> int:
    # LC 200. Each unvisited land cell starts a new component.
    if not grid or not grid[0]:
        return 0
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 1:
                count += 1
                flood(grid, r, c)
    return count


def max_area_of_island(grid: list[list[int]]) -> int:
    # LC 695. Same scan, keep the biggest flood size.
    best = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 1:
                best = max(best, flood(grid, r, c))
    return best


def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    # LC 417. Reverse flow: DFS uphill from each ocean's border; answer is the intersection.
    if not heights:
        return []
    rows, cols = len(heights), len(heights[0])

    def reach(starts: list[tuple[int, int]]) -> set[tuple[int, int]]:
        seen = set(starts)
        stack = list(starts)
        while stack:
            r, c = stack.pop()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen
                        and heights[nr][nc] >= heights[r][c]):
                    seen.add((nr, nc))
                    stack.append((nr, nc))
        return seen

    pacific = reach([(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)])
    atlantic = reach([(rows - 1, c) for c in range(cols)] + [(r, cols - 1) for r in range(rows)])
    return sorted([r, c] for r, c in pacific & atlantic)


if __name__ == "__main__":
    g = [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1]]
    assert num_islands(g) == 3
    assert num_islands([]) == 0 and num_islands([[0]]) == 0 and num_islands([[1]]) == 1

    assert max_area_of_island([[1, 1, 0], [1, 0, 0], [0, 0, 1]]) == 3
    assert max_area_of_island([[0, 0]]) == 0
    assert max_area_of_island([[1, 0, 1], [1, 0, 1], [0, 0, 1]]) == 3

    h = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
    assert pacific_atlantic(h) == [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
    assert pacific_atlantic([[1]]) == [[0, 0]]
    assert pacific_atlantic([]) == []
    print("ok")
