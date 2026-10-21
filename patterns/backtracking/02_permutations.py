"""
PATTERN: Backtracking - Permutations and Constrained Sequences
USE WHEN: Generate every ORDERING of items, or build a sequence position by position where a
          running constraint decides what may come next (e.g. balanced parentheses).
SIGNALS: "all permutations", "permutations with duplicates", "generate parentheses",
         "all arrangements", "all valid sequences"
TIME: O(n! * n) permutations; Catalan(n) * n for parentheses   SPACE: O(n)
PITFALLS: - Permutations use a `used` array (any unused item can go next), not a start index.
          - Duplicates: sort, then skip nums[i] == nums[i-1] when the previous copy is NOT used.
          - Undo BOTH the path and `used` after recursing.
          - Prune early: open < n and close < open for parentheses.
PROBLEMS: 46 Permutations, 47 Permutations II, 22 Generate Parentheses, 784 Letter Case Permutation
"""


# ---------- Core template ----------
def permute(nums: list[int]) -> list[list[int]]:
    # LC 46.
    res: list[list[int]] = []
    path: list[int] = []
    used = [False] * len(nums)

    def backtrack() -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return res


# ---------- Worked problems ----------
def permute_unique(nums: list[int]) -> list[list[int]]:
    # LC 47. Use equal values left-to-right only: skip a copy if its earlier twin isn't in the path.
    nums = sorted(nums)
    res: list[list[int]] = []
    path: list[int] = []
    used = [False] * len(nums)

    def backtrack() -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i] or (i > 0 and nums[i] == nums[i - 1] and not used[i - 1]):
                continue
            used[i] = True
            path.append(nums[i])
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return res


def generate_parenthesis(n: int) -> list[str]:
    # LC 22. Add '(' while open < n; add ')' while close < open.
    res: list[str] = []
    path: list[str] = []

    def backtrack(open_count: int, close_count: int) -> None:
        if len(path) == 2 * n:
            res.append("".join(path))
            return
        if open_count < n:
            path.append("(")
            backtrack(open_count + 1, close_count)
            path.pop()
        if close_count < open_count:
            path.append(")")
            backtrack(open_count, close_count + 1)
            path.pop()

    backtrack(0, 0)
    return res


if __name__ == "__main__":
    assert len(permute([1, 2, 3])) == 6
    assert sorted(permute([0, -1])) == [[-1, 0], [0, -1]]
    assert permute([1]) == [[1]] and permute([]) == [[]]

    assert permute_unique([1, 1, 2]) == [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    assert len(permute_unique([1, 2, 3])) == 6
    assert permute_unique([2, 2]) == [[2, 2]]

    assert generate_parenthesis(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert generate_parenthesis(1) == ["()"]
    assert generate_parenthesis(0) == [""]
    print("ok")
