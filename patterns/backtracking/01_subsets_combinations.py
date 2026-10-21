"""
PATTERN: Backtracking - Subsets and Combinations
USE WHEN: Generate every SELECTION of items where order doesn't matter (subsets, combinations,
          combination sums), or pick one option per position (phone letters). Small n (<= ~20).
SIGNALS: "all subsets", "power set", "combinations of k", "combination sum", "letter combinations",
         "all possible", "generate all"
TIME: O(2^n * n) subsets; O(C(n, k) * k) combinations   SPACE: O(n) recursion depth
PITFALLS: - Pass a `start` index so you never pick an earlier item again (avoids [1,2] and [2,1]).
          - Append `path[:]`, not `path` (all results would alias one list).
          - Duplicates: sort, then skip nums[i] == nums[i-1] when i > start (same depth only).
          - Reuse allowed (combination sum): recurse with i, not i + 1.
PROBLEMS: 78 Subsets, 90 Subsets II, 77 Combinations, 39 Combination Sum, 40 Combination Sum II,
          17 Letter Combinations of a Phone Number
"""


# ---------- Core template: choose / explore / un-choose ----------
def subsets(nums: list[int]) -> list[list[int]]:
    # LC 78.
    res: list[list[int]] = []
    path: list[int] = []

    def backtrack(start: int) -> None:
        res.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])         # choose
            backtrack(i + 1)             # explore
            path.pop()                   # un-choose

    backtrack(0)
    return res


# ---------- Worked problems ----------
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    # LC 90. Sorted; at the same depth, skip a value equal to the previous sibling.
    nums = sorted(nums)
    res: list[list[int]] = []
    path: list[int] = []

    def backtrack(start: int) -> None:
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return res


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    # LC 39. Reuse allowed -> recurse with i; sorted so we can break once too big.
    candidates = sorted(candidates)
    res: list[list[int]] = []
    path: list[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(i, remaining - candidates[i])
            path.pop()

    backtrack(0, target)
    return res


def letter_combinations(digits: str) -> list[str]:
    # LC 17. One choice per position: depth = index into digits.
    if not digits:
        return []
    letters = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
               "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    res: list[str] = []
    path: list[str] = []

    def backtrack(i: int) -> None:
        if i == len(digits):
            res.append("".join(path))
            return
        for ch in letters[digits[i]]:
            path.append(ch)
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return res


if __name__ == "__main__":
    assert sorted(subsets([1, 2, 3])) == sorted([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]])
    assert subsets([]) == [[]]

    assert sorted(subsets_with_dup([1, 2, 2])) == sorted([[], [1], [1, 2], [1, 2, 2], [2], [2, 2]])
    assert subsets_with_dup([0]) == [[], [0]]

    assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
    assert combination_sum([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert combination_sum([2], 1) == []

    assert letter_combinations("23") == ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    assert letter_combinations("") == []
    assert letter_combinations("7") == ["p", "q", "r", "s"]
    print("ok")
