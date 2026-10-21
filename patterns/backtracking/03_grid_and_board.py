"""
PATTERN: Backtracking on a Grid / Board (place, recurse, remove)
USE WHEN: Search a board for a path or a valid placement where choices block later choices:
          word paths that can't reuse cells, queens that can't attack, sudoku digits.
SIGNALS: "word search", "N-Queens", "sudoku solver", "path that visits", "can't reuse a cell",
         "place pieces so that no two attack"
TIME: Exponential (N-Queens ~O(n!); word search O(cells * 3^L))   SPACE: O(L) or O(n) recursion
PITFALLS: - Mark the cell (e.g. '#') before recursing and RESTORE it after, even on success paths.
          - Prune as early as possible (check the char before recursing, not after).
          - N-Queens: track cols, r - c diagonals, r + c anti-diagonals in sets for O(1) checks.
          - Build board output only at the leaf (copy strings, not the mutable row list).
PROBLEMS: 79 Word Search, 51 N-Queens, 52 N-Queens II, 37 Sudoku Solver, 212 Word Search II (with a trie)
"""


# ---------- Core template ----------
def word_search(board: list[list[str]], word: str) -> bool:
    # LC 79.
    if not board or not board[0]:
        return False
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, k: int) -> bool:
        if k == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[k]:
            return False
        saved = board[r][c]
        board[r][c] = "#"                          # place
        found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1)
                 or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
        board[r][c] = saved                        # remove
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False


# ---------- Worked problems ----------
def solve_n_queens(n: int) -> list[list[str]]:
    # LC 51. One queen per row; sets give O(1) column / diagonal conflict checks.
    res: list[list[str]] = []
    queens: list[int] = []                         # queens[r] = column of the queen in row r
    cols: set[int] = set()
    diag: set[int] = set()                         # r - c
    anti: set[int] = set()                         # r + c

    def backtrack(r: int) -> None:
        if r == n:
            res.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
            return
        for c in range(n):
            if c in cols or r - c in diag or r + c in anti:
                continue
            queens.append(c)
            cols.add(c)
            diag.add(r - c)
            anti.add(r + c)
            backtrack(r + 1)
            queens.pop()
            cols.remove(c)
            diag.remove(r - c)
            anti.remove(r + c)

    backtrack(0)
    return res


def total_n_queens(n: int) -> int:
    # LC 52. Same search, count instead of build.
    return len(solve_n_queens(n))


if __name__ == "__main__":
    b = [list("ABCE"), list("SFCS"), list("ADEE")]
    assert word_search(b, "ABCCED")
    assert word_search(b, "SEE")
    assert not word_search(b, "ABCB")              # can't reuse a cell
    assert b == [list("ABCE"), list("SFCS"), list("ADEE")]   # board restored
    assert not word_search([], "A")
    assert word_search([["a"]], "a")

    assert solve_n_queens(4) == [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]
    assert solve_n_queens(1) == [["Q"]]
    assert solve_n_queens(2) == [] and solve_n_queens(3) == []

    assert total_n_queens(8) == 92 and total_n_queens(4) == 2
    print("ok")
