"""
PATTERN: Interval DP
USE WHEN: The answer for a range [i, j] is built from smaller ranges inside it, usually by trying
          every split point k, or by shrinking the range from its ends.
SIGNALS: "burst balloons", "minimum cost to cut a stick", "merge stones", "palindromic subsequence",
         "matrix chain multiplication", "remove boxes", "strange printer"
TIME: O(n^3) with a split point, O(n^2) when shrinking from the ends   SPACE: O(n^2)
PITFALLS: - Loop by LENGTH outermost (or i from right to left) so smaller intervals are ready first.
          - Burst balloons: k is the LAST balloon burst in (i, j), so its neighbours are i and j.
          - Pad the input (e.g. [1] + nums + [1], [0] + cuts + [n]) to remove edge cases.
          - Define open vs closed interval clearly: (i, j) exclusive vs [i, j] inclusive.
PROBLEMS: 516 Longest Palindromic Subsequence, 312 Burst Balloons, 1547 Minimum Cost to Cut a Stick,
          1039 Minimum Score Triangulation of Polygon, 664 Strange Printer
"""


# ---------- Core template: shrink from the ends ----------
def longest_palindrome_subseq(s: str) -> int:
    # LC 516. dp[i][j] on s[i..j]: ends match -> 2 + inside, else drop one end.
    n = len(s)
    if n == 0:
        return 0
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]


# ---------- Worked problems: try every split point ----------
def max_coins(nums: list[int]) -> int:
    # LC 312. dp[i][j] = best for balloons strictly between i and j; k = last one burst there.
    vals = [1] + nums + [1]
    n = len(vals)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                dp[i][j] = max(dp[i][j], dp[i][k] + vals[i] * vals[k] * vals[j] + dp[k][j])
    return dp[0][n - 1]


def min_cost_cut_stick(n: int, cuts: list[int]) -> int:
    # LC 1547. dp[i][j] = min cost to make all cuts strictly between c[i] and c[j].
    c = [0] + sorted(cuts) + [n]
    m = len(c)
    dp = [[0] * m for _ in range(m)]
    for length in range(2, m):
        for i in range(m - length):
            j = i + length
            dp[i][j] = min(dp[i][k] + dp[k][j] for k in range(i + 1, j)) + c[j] - c[i]
    return dp[0][m - 1]


if __name__ == "__main__":
    assert longest_palindrome_subseq("bbbab") == 4
    assert longest_palindrome_subseq("cbbd") == 2
    assert longest_palindrome_subseq("") == 0 and longest_palindrome_subseq("a") == 1

    assert max_coins([3, 1, 5, 8]) == 167
    assert max_coins([1, 5]) == 10
    assert max_coins([]) == 0 and max_coins([7]) == 7

    assert min_cost_cut_stick(7, [1, 3, 4, 5]) == 16
    assert min_cost_cut_stick(9, [5, 6, 1, 4, 2]) == 22
    assert min_cost_cut_stick(5, []) == 0
    assert min_cost_cut_stick(4, [2]) == 4
    print("ok")
