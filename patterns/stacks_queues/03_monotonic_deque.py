"""
PATTERN: Monotonic Deque
USE WHEN: Sliding window where you need the window's max or min at every step in O(1),
          or "shortest subarray with sum >= K" when numbers can be negative.
SIGNALS: "sliding window maximum/minimum", "max - min <= limit", "shortest subarray sum at least K"
         (with negatives), "jump game VI", "constrained subsequence sum"
TIME: O(n) (each index enters and leaves the deque once)   SPACE: O(k)
PITFALLS: - Store indexes, so you can pop the front when it falls out of the window.
          - Pop the front for "out of window" BEFORE reading the answer.
          - Decreasing deque for max, increasing deque for min. Mixing them up is the #1 bug.
          - Plain sliding window fails with negatives: that's why 862 needs prefix sums + deque.
PROBLEMS: 239 Sliding Window Maximum, 1438 Longest Subarray With Abs Diff <= Limit,
          862 Shortest Subarray with Sum at Least K, 1696 Jump Game VI
"""
from collections import deque


# ---------- Core template: window maximum ----------
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    # LC 239. Deque holds indexes with decreasing values; front is the window max.
    dq: deque[int] = deque()
    res: list[int] = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()                         # smaller items can never be a max again
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()                     # front fell out of the window
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res


# ---------- Worked problems ----------
def longest_subarray(nums: list[int], limit: int) -> int:
    # LC 1438. Two deques give window max and min; shrink while max - min > limit.
    max_q: deque[int] = deque()
    min_q: deque[int] = deque()
    left = 0
    best = 0
    for right, x in enumerate(nums):
        while max_q and max_q[-1] < x:
            max_q.pop()
        max_q.append(x)
        while min_q and min_q[-1] > x:
            min_q.pop()
        min_q.append(x)
        while max_q[0] - min_q[0] > limit:
            if nums[left] == max_q[0]:
                max_q.popleft()
            if nums[left] == min_q[0]:
                min_q.popleft()
            left += 1
        best = max(best, right - left + 1)
    return best


def shortest_subarray(nums: list[int], k: int) -> int:
    # LC 862. Increasing deque of prefix indexes: front is the best (smallest) start candidate.
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    dq: deque[int] = deque()
    best = float("inf")
    for i, p in enumerate(prefix):
        while dq and p - prefix[dq[0]] >= k:
            best = min(best, i - dq.popleft())
        while dq and prefix[dq[-1]] >= p:
            dq.pop()                         # a later, smaller prefix is a strictly better start
        dq.append(i)
    return -1 if best == float("inf") else int(best)


def max_result(nums: list[int], k: int) -> int:
    # LC 1696. dp[i] = nums[i] + max(dp[i-k..i-1]); deque gives that window max in O(1).
    dp = [0] * len(nums)
    dq: deque[int] = deque()
    for i, x in enumerate(nums):
        if dq and dq[0] < i - k:
            dq.popleft()
        dp[i] = x + (dp[dq[0]] if dq else 0)
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)
    return dp[-1] if nums else 0


if __name__ == "__main__":
    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert max_sliding_window([1], 1) == [1]
    assert max_sliding_window([], 2) == []
    assert max_sliding_window([4, 4, 4], 2) == [4, 4]
    assert max_sliding_window([-7, -8, 7, 5, 7, 1, 6, 0], 4) == [7, 7, 7, 7, 7]

    assert longest_subarray([8, 2, 4, 7], 4) == 2
    assert longest_subarray([10, 1, 2, 4, 7, 2], 5) == 4
    assert longest_subarray([4, 2, 2, 2, 4, 4, 2, 2], 0) == 3
    assert longest_subarray([], 1) == 0

    assert shortest_subarray([1], 1) == 1
    assert shortest_subarray([1, 2], 4) == -1
    assert shortest_subarray([2, -1, 2], 3) == 3
    assert shortest_subarray([84, -37, 32, 40, 95], 167) == 3
    assert shortest_subarray([], 1) == -1

    assert max_result([1, -1, -2, 4, -7, 3], 2) == 7
    assert max_result([10, -5, -2, 4, 0, 3], 3) == 17
    assert max_result([1, -5, -20, 4, -1, 3, -6, -3], 2) == 0
    assert max_result([5], 1) == 5
    print("ok")
