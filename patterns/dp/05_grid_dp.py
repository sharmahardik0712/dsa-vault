"""
PATTERN: Grid DP
USE WHEN: Moving through a grid only right/down (or similar fixed directions), counting paths or
          optimising a cost, or when a cell's value builds on its top/left/diagonal neighbours.
SIGNALS: "unique paths", "minimum path sum", "obstacles", "maximal square", "dungeon game",
         "triangle", "cherry pickup", "only move right or down"
TIME: O(rows * cols)   SPACE: O(cols) with one rolling row
PITFALLS: - First row and first column have only one way in: handle them (or pad with a border).
          - Obstacles: set dp to 0 at the obstacle, don't skip the cell.
          - Maximal square returns SIDE length in dp; the answer is side^2.
          - Bottom-up direction matters for problems like Dungeon Game (fill from the target backwards).
PROBLEMS: 62 Unique Paths, 63 Unique Paths II, 64 Minimum Path Sum, 221 Maximal Square,
          120 Triangle, 174 Dungeon Game
"""


# ---------- Core template: one rolling row ----------
def unique_paths(rows: int, cols: int) -> int:
    # LC 62. dp[c] (from above) += dp[c - 1] (from the left).
    dp = [1] * cols
    for _ in range(1, rows):
        for c in range(1, cols):
            dp[c] += dp[c - 1]
    return dp[-1]


# ---------- Worked problems ----------
def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    # LC 63. Same recurrence; an obstacle resets the cell to 0.
    if not grid or grid[0][0] == 1:
        return 0
    cols = len(grid[0])
    dp = [0] * cols
    dp[0] = 1
    for row in grid:
        for c in range(cols):
            if row[c] == 1:
                dp[c] = 0
            elif c > 0:
                dp[c] += dp[c - 1]
    return dp[-1]


def min_path_sum(grid: list[list[int]]) -> int:
    # LC 64. dp[c] = grid value + min(from above, from left).
    cols = len(grid[0])
    dp = [float("inf")] * cols
    dp[0] = 0
    for row in grid:
        for c in range(cols):
            best_in = dp[c] if c == 0 else min(dp[c], dp[c - 1])
            dp[c] = row[c] + best_in
    return int(dp[-1])


def maximal_square(matrix: list[list[str]]) -> int:
    # LC 221. dp[r][c] = side of the largest square ending at (r, c) = 1 + min(up, left, diag).
    if not matrix:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    dp = [[0] * (cols + 1) for _ in range(rows + 1)]
    best = 0
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            if matrix[r - 1][c - 1] == "1":
                dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])
                best = max(best, dp[r][c])
    return best * best


if __name__ == "__main__":
    assert unique_paths(3, 7) == 28 and unique_paths(3, 2) == 3 and unique_paths(1, 1) == 1

    assert unique_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
    assert unique_paths_with_obstacles([[0, 1], [0, 0]]) == 1
    assert unique_paths_with_obstacles([[1]]) == 0 and unique_paths_with_obstacles([[0]]) == 1

    assert min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    assert min_path_sum([[1, 2, 3], [4, 5, 6]]) == 12
    assert min_path_sum([[5]]) == 5

    m = [list("10100"), list("10111"), list("11111"), list("10010")]
    assert maximal_square(m) == 4
    assert maximal_square([list("01"), list("10")]) == 1
    assert maximal_square([["0"]]) == 0 and maximal_square([]) == 0
    print("ok")
