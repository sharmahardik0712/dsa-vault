"""
PATTERN: Two Heaps
USE WHEN: You need the middle of a changing collection (median), or must repeatedly pick the best
          item from a pool that grows as a threshold moves (e.g. affordable projects by capital).
SIGNALS: "median of data stream", "sliding window median", "IPO", "maximize capital",
         "balance two halves", "smallest of the large half / largest of the small half"
TIME: O(log n) per add/remove, O(1) median   SPACE: O(n)
PITFALLS: - Keep the invariant len(low) == len(high) or len(low) == len(high) + 1.
          - low is a MAX-heap (negate); high is a min-heap.
          - Sliding window removal: heapq can't delete, so use lazy deletion and track VALID sizes.
          - Push to low first, then move low's max to high: keeps every low <= every high.
PROBLEMS: 295 Find Median from Data Stream, 480 Sliding Window Median, 502 IPO,
          1825 Finding MK Average
"""
import heapq
from collections import Counter


# ---------- Core template ----------
class MedianFinder:
    # LC 295. low = smaller half (max-heap via negation), high = larger half.
    def __init__(self) -> None:
        self.low: list[int] = []
        self.high: list[int] = []

    def add(self, num: int) -> None:
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2


# ---------- Worked problems ----------
def find_maximized_capital(k: int, w: int, profits: list[int], capital: list[int]) -> int:
    # LC 502. Min order by capital unlocks projects; max-heap of unlocked profits picks the best.
    projects = sorted(zip(capital, profits))
    available: list[int] = []
    i = 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(available, -projects[i][1])
            i += 1
        if not available:
            break
        w -= heapq.heappop(available)
    return w


def median_sliding_window(nums: list[int], k: int) -> list[float]:
    # LC 480. Two heaps with lazy deletion: `delayed` counts values to drop when they reach a top.
    low: list[int] = []
    high: list[int] = []
    delayed: Counter[int] = Counter()
    sizes = {"low": 0, "high": 0}

    def prune(heap: list[int], sign: int) -> None:
        while heap and delayed[sign * heap[0]]:
            delayed[sign * heap[0]] -= 1
            heapq.heappop(heap)

    def rebalance() -> None:
        if sizes["low"] > sizes["high"] + 1:
            heapq.heappush(high, -heapq.heappop(low))
            sizes["low"] -= 1
            sizes["high"] += 1
            prune(low, -1)
        elif sizes["low"] < sizes["high"]:
            heapq.heappush(low, -heapq.heappop(high))
            sizes["high"] -= 1
            sizes["low"] += 1
            prune(high, 1)

    def add(x: int) -> None:
        if not low or x <= -low[0]:
            heapq.heappush(low, -x)
            sizes["low"] += 1
        else:
            heapq.heappush(high, x)
            sizes["high"] += 1
        rebalance()

    def remove(x: int) -> None:
        delayed[x] += 1
        if x <= -low[0]:
            sizes["low"] -= 1
            if x == -low[0]:
                prune(low, -1)
        else:
            sizes["high"] -= 1
            if high and x == high[0]:
                prune(high, 1)
        rebalance()

    res: list[float] = []
    for i, x in enumerate(nums):
        add(x)
        if i >= k:
            remove(nums[i - k])
        if i >= k - 1:
            res.append(float(-low[0]) if k % 2 else (-low[0] + high[0]) / 2)
    return res


if __name__ == "__main__":
    mf = MedianFinder()
    mf.add(1)
    mf.add(2)
    assert mf.median() == 1.5
    mf.add(3)
    assert mf.median() == 2.0
    mf.add(-10)
    assert mf.median() == 1.5

    assert find_maximized_capital(2, 0, [1, 2, 3], [0, 1, 1]) == 4
    assert find_maximized_capital(3, 0, [1, 2, 3], [0, 1, 2]) == 6
    assert find_maximized_capital(1, 0, [5], [1]) == 0            # nothing affordable
    assert find_maximized_capital(5, 2, [], []) == 2

    assert median_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [1, -1, -1, 3, 5, 6]
    assert median_sliding_window([1, 2, 3, 4, 2, 3, 1, 4, 2], 3) == [2, 3, 3, 3, 2, 3, 2]
    assert median_sliding_window([1, 4, 2, 3], 4) == [2.5]
    assert median_sliding_window([5], 1) == [5.0]
    assert median_sliding_window([2, 2, 2, 2], 2) == [2.0, 2.0, 2.0]
    print("ok")
