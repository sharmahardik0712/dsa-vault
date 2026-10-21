"""
PATTERN: Matrix Traversal and Manipulation
USE WHEN: 2D array problems that are about index bookkeeping rather than graph search:
          spiral/diagonal order, in-place rotation, marking rows/cols, sorted-matrix search.
SIGNALS: "spiral order", "rotate image 90 degrees", "in place", "set matrix zeroes",
         "rows and columns sorted", "diagonal", "transpose", "game of life"
TIME: O(m * n), O(m + n) for staircase search   SPACE: O(1) extra when done in place
PITFALLS: - Spiral: re-check `top <= bottom` / `left <= right` before the 3rd and 4th edges.
          - Rotate 90 clockwise = transpose then reverse each row (counter-clockwise: reverse rows first).
          - In-place marking: use first row/col as markers, but save their own zero-state first.
          - Diagonals: r - c is constant on "\\" diagonals, r + c on "/" anti-diagonals.
PROBLEMS: 54 Spiral Matrix, 48 Rotate Image, 73 Set Matrix Zeroes, 240 Search a 2D Matrix II,
          289 Game of Life
"""


# ---------- Core template: shrinking boundaries ----------
def spiral_order(matrix: list[list[int]]) -> list[int]:
    # LC 54.
    if not matrix or not matrix[0]:
        return []
    res: list[int] = []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            res.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            res.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                res.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                res.append(matrix[r][left])
            left += 1
    return res


# ---------- Worked problems ----------
def rotate(matrix: list[list[int]]) -> None:
    # LC 48. Transpose (swap across main diagonal), then reverse every row.
    n = len(matrix)
    for r in range(n):
        for c in range(r + 1, n):
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
    for row in matrix:
        row.reverse()


def set_zeroes(matrix: list[list[int]]) -> None:
    # LC 73. O(1) space: first row/col store the markers for the rest of the matrix.
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(cols))
    first_col_zero = any(matrix[r][0] == 0 for r in range(rows))
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    if first_row_zero:
        for c in range(cols):
            matrix[0][c] = 0
    if first_col_zero:
        for r in range(rows):
            matrix[r][0] = 0


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    # LC 240. Start top-right: left makes it smaller, down makes it bigger. One cell per step.
    if not matrix or not matrix[0]:
        return False
    r, c = 0, len(matrix[0]) - 1
    while r < len(matrix) and c >= 0:
        if matrix[r][c] == target:
            return True
        if matrix[r][c] > target:
            c -= 1
        else:
            r += 1
    return False


def game_of_life(board: list[list[int]]) -> None:
    # LC 289. In place with 2-bit state: bit 0 = current, bit 1 = next.
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            live = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if (dr or dc) and 0 <= nr < rows and 0 <= nc < cols:
                        live += board[nr][nc] & 1
            if live == 3 or (board[r][c] & 1 and live == 2):
                board[r][c] |= 2
    for r in range(rows):
        for c in range(cols):
            board[r][c] >>= 1


if __name__ == "__main__":
    assert spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == \
        [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    assert spiral_order([[1], [2], [3]]) == [1, 2, 3]
    assert spiral_order([]) == [] and spiral_order([[7]]) == [7]

    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate(m)
    assert m == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    m = [[1]]
    rotate(m)
    assert m == [[1]]

    m = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    set_zeroes(m)
    assert m == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    m = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
    set_zeroes(m)
    assert m == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]

    grid = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
    assert search_matrix(grid, 5) and not search_matrix(grid, 20)
    assert not search_matrix([], 1) and search_matrix([[-1]], -1)

    b = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    game_of_life(b)
    assert b == [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
    print("ok")
