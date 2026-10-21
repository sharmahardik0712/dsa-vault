"""
PATTERN: Segment Tree (point update, range query for any associative op)
USE WHEN: Point updates mixed with range MIN / MAX / GCD / sum queries, or a DP where dp[x] needs
          the best value over a range of earlier keys (range-max over values).
SIGNALS: "range minimum query", "range max with updates", "longest increasing subsequence II",
         "falling squares", "count of range sum", "online queries on intervals"
TIME: O(n) build, O(log n) update/query   SPACE: O(n)
PITFALLS: - The identity must not affect results: inf for min, -inf/0 for max, 0 for sum.
          - Iterative tree uses half-open [l, r); convert from inclusive at the API boundary.
          - DP over VALUES: tree size is max value + 1 (compress if values are huge).
          - Range UPDATES need lazy propagation (rare in interviews; mention, don't build).
PROBLEMS: 307 Range Sum Query - Mutable, 2407 Longest Increasing Subsequence II, 699 Falling Squares,
          327 Count of Range Sum, 1157 Online Majority Element In Subarray
"""
from typing import Callable


# ---------- Core template: iterative segment tree ----------
class SegmentTree:
    def __init__(self, nums: list[int], func: Callable[[int, int], int], identity: int) -> None:
        self.n = len(nums)
        self.func = func
        self.identity = identity
        self.tree = [identity] * (2 * self.n)
        for i, x in enumerate(nums):
            self.tree[self.n + i] = x
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = func(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i: int, val: int) -> None:
        i += self.n
        self.tree[i] = val
        while i > 1:
            i //= 2
            self.tree[i] = self.func(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, left: int, right: int) -> int:
        """Inclusive [left, right]."""
        res = self.identity
        left += self.n
        right += self.n + 1
        while left < right:
            if left & 1:
                res = self.func(res, self.tree[left])
                left += 1
            if right & 1:
                right -= 1
                res = self.func(res, self.tree[right])
            left //= 2
            right //= 2
        return res


# ---------- Worked problems ----------
class RangeMin:
    # Classic RMQ with point updates (min isn't invertible, so Fenwick can't do this).
    def __init__(self, nums: list[int]) -> None:
        self.st = SegmentTree(nums, min, float("inf"))

    def update(self, i: int, val: int) -> None:
        self.st.update(i, val)

    def query(self, left: int, right: int) -> int:
        return self.st.query(left, right)


def length_of_lis_k(nums: list[int], k: int) -> int:
    # LC 2407. dp[v] = longest valid subsequence ending with value v; extend from max over [v-k, v-1].
    if not nums:
        return 0
    st = SegmentTree([0] * (max(nums) + 1), max, 0)
    best = 0
    for x in nums:
        lo = max(0, x - k)
        prev = st.query(lo, x - 1) if x - 1 >= lo else 0
        cur = prev + 1
        if cur > st.query(x, x):
            st.update(x, cur)
        best = max(best, cur)
    return best


if __name__ == "__main__":
    sm = SegmentTree([1, 3, 5], lambda a, b: a + b, 0)
    assert sm.query(0, 2) == 9
    sm.update(1, -2)
    assert sm.query(0, 2) == 4 and sm.query(1, 1) == -2

    rmq = RangeMin([2, 5, 1, 4, 9, 3])
    assert rmq.query(1, 3) == 1 and rmq.query(0, 5) == 1 and rmq.query(4, 4) == 9
    rmq.update(2, 6)
    assert rmq.query(1, 3) == 4 and rmq.query(0, 5) == 2
    assert RangeMin([-7]).query(0, 0) == -7

    assert length_of_lis_k([4, 2, 1, 4, 3, 4, 5, 8, 15], 3) == 5
    assert length_of_lis_k([7, 4, 5, 1, 8, 12, 4, 7], 5) == 4
    assert length_of_lis_k([1, 5], 1) == 1
    assert length_of_lis_k([], 3) == 0
    print("ok")
