"""
PATTERN: Fenwick Tree (Binary Indexed Tree)
USE WHEN: Point updates mixed with prefix/range SUM queries, or counting "how many values smaller
          than x have I seen so far" while scanning (with values compressed to ranks).
SIGNALS: "range sum query - mutable", "count of smaller numbers after self", "count inversions",
         "number of elements less than", "online frequency counts"
TIME: O(log n) per update/query   SPACE: O(n)
PITFALLS: - Internally 1-indexed: shift i by +1 at the API boundary.
          - update() takes a DELTA; to set a value pass (new - old) and keep the old values.
          - Only invertible ops (sum, xor): range min/max need a segment tree.
          - Big or negative values: coordinate-compress to ranks 0..m-1 first.
PROBLEMS: 307 Range Sum Query - Mutable, 315 Count of Smaller Numbers After Self,
          493 Reverse Pairs, 1649 Create Sorted Array through Instructions
"""


# ---------- Core template ----------
class Fenwick:
    def __init__(self, n: int) -> None:
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i: int, delta: int) -> None:
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i                       # next node responsible for i

    def prefix(self, i: int) -> int:
        """Sum of [0..i]. prefix(-1) == 0."""
        i += 1
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i                       # strip lowest set bit
        return total

    def range_sum(self, left: int, right: int) -> int:
        return self.prefix(right) - self.prefix(left - 1)


# ---------- Worked problems ----------
class NumArray:
    # LC 307. Fenwick stores values; update passes the difference.
    def __init__(self, nums: list[int]) -> None:
        self.nums = nums[:]
        self.fw = Fenwick(len(nums))
        for i, x in enumerate(nums):
            self.fw.update(i, x)

    def update(self, i: int, val: int) -> None:
        self.fw.update(i, val - self.nums[i])
        self.nums[i] = val

    def sum_range(self, left: int, right: int) -> int:
        return self.fw.range_sum(left, right)


def count_smaller(nums: list[int]) -> list[int]:
    # LC 315. Scan right to left; Fenwick over value ranks counts smaller values already seen.
    ranks = {v: i for i, v in enumerate(sorted(set(nums)))}
    fw = Fenwick(len(ranks))
    res = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):
        r = ranks[nums[i]]
        res[i] = fw.prefix(r - 1)
        fw.update(r, 1)
    return res


if __name__ == "__main__":
    fw = Fenwick(5)
    for i, x in enumerate([1, 2, 3, 4, 5]):
        fw.update(i, x)
    assert fw.prefix(4) == 15 and fw.range_sum(1, 3) == 9 and fw.prefix(-1) == 0
    fw.update(2, -3)
    assert fw.range_sum(0, 2) == 3

    na = NumArray([1, 3, 5])
    assert na.sum_range(0, 2) == 9
    na.update(1, 2)
    assert na.sum_range(0, 2) == 8 and na.sum_range(1, 1) == 2
    neg = NumArray([-2, 0, 3, -5, 2, -1])
    assert neg.sum_range(0, 2) == 1 and neg.sum_range(2, 5) == -1

    assert count_smaller([5, 2, 6, 1]) == [2, 1, 1, 0]
    assert count_smaller([-1]) == [0] and count_smaller([-1, -1]) == [0, 0]
    assert count_smaller([]) == []
    print("ok")
