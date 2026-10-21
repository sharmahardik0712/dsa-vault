"""
PATTERN: Knapsack DP (0/1 and unbounded)
USE WHEN: Choose items (each once = 0/1, or unlimited = unbounded) to hit / not exceed a capacity
          or target sum, and count ways or optimise.
SIGNALS: "partition equal subset sum", "target sum", "coin change", "number of combinations",
         "subset sum", "ones and zeroes", "last stone weight II", "can you make amount"
TIME: O(n * capacity)   SPACE: O(capacity) with a 1D array
PITFALLS: - 0/1: iterate capacity BACKWARDS (each item used once). Unbounded: FORWARDS.
          - Counting combinations: items in the OUTER loop (else you count permutations).
          - Min-count DP starts at inf except dp[0] = 0; count DP starts at dp[0] = 1.
          - Target sum: transform to subset sum p = (total + target) / 2; check parity and |target| <= total.
PROBLEMS: 416 Partition Equal Subset Sum, 494 Target Sum, 322 Coin Change, 518 Coin Change II,
          474 Ones and Zeroes, 1049 Last Stone Weight II
"""


# ---------- Core template: 0/1 knapsack (reachability) ----------
def can_partition(nums: list[int]) -> bool:
    # LC 416. Can a subset reach total / 2? Loop capacity backwards so each item is used once.
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [True] + [False] * target
    for x in nums:
        for cap in range(target, x - 1, -1):
            dp[cap] = dp[cap] or dp[cap - x]
    return dp[target]


# ---------- Worked problems ----------
def find_target_sum_ways(nums: list[int], target: int) -> int:
    # LC 494. Plus-set P and minus-set N: P - N = target, P + N = total -> P = (total + target) / 2.
    total = sum(nums)
    if abs(target) > total or (total + target) % 2:
        return 0
    p = (total + target) // 2
    dp = [1] + [0] * p
    for x in nums:
        for cap in range(p, x - 1, -1):
            dp[cap] += dp[cap - x]
    return dp[p]


def coin_change(coins: list[int], amount: int) -> int:
    # LC 322. Unbounded, minimise count: dp[a] = min coins to make a.
    inf = float("inf")
    dp = [0] + [inf] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == inf else int(dp[amount])


def coin_change_ways(amount: int, coins: list[int]) -> int:
    # LC 518. Unbounded, count combinations: coins OUTER, amount forwards.
    dp = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]


if __name__ == "__main__":
    assert can_partition([1, 5, 11, 5])
    assert not can_partition([1, 2, 3, 5])
    assert can_partition([]) and not can_partition([1])
    assert not can_partition([2, 2, 3])          # using 2 twice would wrongly say True

    assert find_target_sum_ways([1, 1, 1, 1, 1], 3) == 5
    assert find_target_sum_ways([1], 1) == 1
    assert find_target_sum_ways([1], 2) == 0
    assert find_target_sum_ways([0, 0, 0], 0) == 8
    assert find_target_sum_ways([1, 2], -1) == 1

    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0 and coin_change([], 3) == -1

    assert coin_change_ways(5, [1, 2, 5]) == 4
    assert coin_change_ways(3, [2]) == 0
    assert coin_change_ways(0, [7]) == 1
    print("ok")
