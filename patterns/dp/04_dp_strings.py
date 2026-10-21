"""
PATTERN: Two-String DP (LCS, edit distance, subsequence counting)
USE WHEN: Two sequences are compared/aligned and the state is (i, j) = "first i chars of a,
          first j chars of b". Match moves diagonally; mismatch takes the best of neighbours.
SIGNALS: "longest common subsequence", "edit distance", "minimum insertions/deletions",
         "distinct subsequences", "interleaving string", "shortest common supersequence",
         "wildcard / regex matching"
TIME: O(m * n)   SPACE: O(m * n), reducible to O(n) with one row
PITFALLS: - Use size (m + 1) x (n + 1); dp[0][*] and dp[*][0] are the empty-prefix base cases.
          - Index the strings with i - 1 and j - 1 inside the loops.
          - Edit distance base: dp[i][0] = i, dp[0][j] = j (all deletes / inserts).
          - 1D compression: iterate j backwards when you need the old diagonal value.
PROBLEMS: 1143 Longest Common Subsequence, 72 Edit Distance, 115 Distinct Subsequences,
          583 Delete Operation for Two Strings, 97 Interleaving String
"""


# ---------- Core template ----------
def lcs(a: str, b: str) -> int:
    # LC 1143. Match -> diagonal + 1, else max(up, left).
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


# ---------- Worked problems ----------
def edit_distance(a: str, b: str) -> int:
    # LC 72. Insert / delete / replace = left / up / diagonal + 1.
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]


def min_delete_distance(a: str, b: str) -> int:
    # LC 583. Keep the LCS, delete everything else from both strings.
    return len(a) + len(b) - 2 * lcs(a, b)


def num_distinct(s: str, t: str) -> int:
    # LC 115. dp[j] = ways to form t[:j]; j backwards so dp[j - 1] is still the previous row.
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):
            if t[j - 1] == ch:
                dp[j] += dp[j - 1]
    return dp[len(t)]


if __name__ == "__main__":
    assert lcs("abcde", "ace") == 3
    assert lcs("abc", "def") == 0
    assert lcs("", "abc") == 0 and lcs("aaa", "aa") == 2

    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5
    assert edit_distance("", "ab") == 2 and edit_distance("a", "a") == 0

    assert min_delete_distance("sea", "eat") == 2
    assert min_delete_distance("leetcode", "etco") == 4
    assert min_delete_distance("", "") == 0

    assert num_distinct("rabbbit", "rabbit") == 3
    assert num_distinct("babgbag", "bag") == 5
    assert num_distinct("abc", "") == 1 and num_distinct("", "a") == 0
    print("ok")
