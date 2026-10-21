"""
PATTERN: 1D Dynamic Programming (linear sequence DP)
USE WHEN: The answer at position i depends on a few earlier positions (i - 1, i - 2, or any j < i
          via a dictionary/word check). Count ways, min/max over choices at each step.
SIGNALS: "climbing stairs", "number of ways", "house robber", "decode ways", "word break",
         "minimum cost to reach", "jump", "can you segment"
TIME: O(n) (O(n * L) for word break)   SPACE: O(1) with rolling variables, else O(n)
PITFALLS: - Define dp[i] in one sentence first ("dp[i] = ways to decode s[:i]").
          - Size n + 1 when dp[0] means "empty prefix", and seed it (often 1 or True).
          - Decode ways: '0' can't stand alone; "10".."26" are the only valid pairs.
          - Top-down with @lru_cache is fine to start; say you'd convert to bottom-up for space.
PROBLEMS: 70 Climbing Stairs, 198 House Robber, 213 House Robber II, 91 Decode Ways, 139 Word Break,
          746 Min Cost Climbing Stairs
"""
from functools import lru_cache


# ---------- Core template: top-down, then bottom-up with rolling variables ----------
def climb_stairs_memo(n: int) -> int:
    @lru_cache(maxsize=None)
    def ways(i: int) -> int:
        if i <= 1:
            return 1
        return ways(i - 1) + ways(i - 2)

    return ways(n)


def climb_stairs(n: int) -> int:
    # LC 70. dp[i] = dp[i-1] + dp[i-2].
    prev, cur = 1, 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
    return cur


# ---------- Worked problems ----------
def rob(nums: list[int]) -> int:
    # LC 198. Skip this house (prev best) or rob it (best two back + this).
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1


def num_decodings(s: str) -> int:
    # LC 91. dp[i] = dp[i-1] if s[i-1] is 1-9, plus dp[i-2] if s[i-2:i] is 10-26.
    if not s:
        return 0
    prev2, prev1 = 1, 1                      # dp[i-2], dp[i-1]; dp[0] = 1 (empty prefix)
    for i in range(len(s)):
        cur = 0
        if s[i] != "0":
            cur += prev1
        if i > 0 and 10 <= int(s[i - 1:i + 1]) <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1


def word_break(s: str, words: list[str]) -> bool:
    # LC 139. dp[i] = s[:i] can be segmented; try every word ending at i.
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for w in words:
            if len(w) <= i and dp[i - len(w)] and s[i - len(w):i] == w:
                dp[i] = True
                break
    return dp[len(s)]


if __name__ == "__main__":
    assert climb_stairs(1) == 1 and climb_stairs(2) == 2 and climb_stairs(5) == 8
    assert climb_stairs_memo(5) == 8 and climb_stairs(0) == 1

    assert rob([1, 2, 3, 1]) == 4
    assert rob([2, 7, 9, 3, 1]) == 12
    assert rob([]) == 0 and rob([5]) == 5

    assert num_decodings("12") == 2
    assert num_decodings("226") == 3
    assert num_decodings("06") == 0
    assert num_decodings("10") == 1 and num_decodings("0") == 0 and num_decodings("") == 0

    assert word_break("leetcode", ["leet", "code"])
    assert word_break("applepenapple", ["apple", "pen"])
    assert not word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])
    assert word_break("", ["a"])
    print("ok")
