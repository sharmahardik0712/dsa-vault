"""
PATTERN: Quickselect / Partitioning
USE WHEN: You need the kth smallest/largest or the k best items in AVERAGE O(n), or to partition
          an array in place into groups (< pivot, == pivot, > pivot).
SIGNALS: "kth largest" (follow-up: better than O(n log k)), "k closest", "top k" in O(n),
         "sort colors", "partition around pivot", "wiggle sort"
TIME: O(n) average, O(n^2) worst   SPACE: O(1) extra (iterative)
PITFALLS: - Always pick a RANDOM pivot (sorted input makes a fixed pivot O(n^2)).
          - Kth largest = index n - k in ascending order.
          - Lomuto degrades with many duplicates; 3-way partition (Dutch flag) fixes it.
          - Dutch flag: don't advance i after swapping with `high` (the swapped-in value is unchecked).
PROBLEMS: 215 Kth Largest Element (quickselect), 973 K Closest Points (quickselect),
          75 Sort Colors, 324 Wiggle Sort II
"""
import random
from typing import Callable


# ---------- Core template ----------
def partition(arr: list, lo: int, hi: int, key: Callable) -> int:
    """Lomuto around a random pivot. Returns the pivot's final index."""
    pivot_idx = random.randint(lo, hi)
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    pivot = key(arr[hi])
    store = lo
    for i in range(lo, hi):
        if key(arr[i]) < pivot:
            arr[store], arr[i] = arr[i], arr[store]
            store += 1
    arr[store], arr[hi] = arr[hi], arr[store]
    return store


def quickselect(arr: list, target: int, key: Callable = lambda x: x) -> None:
    """Rearranges arr so arr[target] is in sorted position, smaller keys before it."""
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        p = partition(arr, lo, hi, key)
        if p == target:
            return
        if p < target:
            lo = p + 1
        else:
            hi = p - 1


# ---------- Worked problems ----------
def find_kth_largest(nums: list[int], k: int) -> int:
    # LC 215.
    arr = nums[:]
    quickselect(arr, len(arr) - k)
    return arr[len(arr) - k]


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    # LC 973. After selecting index k - 1 by distance, the first k points are the closest.
    arr = [p[:] for p in points]
    quickselect(arr, k - 1, key=lambda p: p[0] * p[0] + p[1] * p[1])
    return arr[:k]


def sort_colors(nums: list[int]) -> None:
    # LC 75. 3-way partition: [0, low) = 0s, [low, i) = 1s, (high, end] = 2s.
    low, i, high = 0, 0, len(nums) - 1
    while i <= high:
        if nums[i] == 0:
            nums[low], nums[i] = nums[i], nums[low]
            low += 1
            i += 1
        elif nums[i] == 2:
            nums[i], nums[high] = nums[high], nums[i]
            high -= 1
        else:
            i += 1


if __name__ == "__main__":
    random.seed(0)
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert find_kth_largest([1], 1) == 1
    assert find_kth_largest([-1, -1, -2], 3) == -2

    assert k_closest([[1, 3], [-2, 2]], 1) == [[-2, 2]]
    assert sorted(k_closest([[3, 3], [5, -1], [-2, 4]], 2)) == [[-2, 4], [3, 3]]
    assert sorted(k_closest([[0, 1], [1, 0]], 2)) == [[0, 1], [1, 0]]

    c = [2, 0, 2, 1, 1, 0]
    sort_colors(c)
    assert c == [0, 0, 1, 1, 2, 2]
    c = [2, 0, 1]
    sort_colors(c)
    assert c == [0, 1, 2]
    c = []
    sort_colors(c)
    assert c == []
    print("ok")
