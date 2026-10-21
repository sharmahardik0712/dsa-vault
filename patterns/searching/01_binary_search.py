"""
PATTERN: Binary Search on a Sorted Index Range
USE WHEN: Data is sorted or rotated-sorted and you need a position: exact match, first/last
          occurrence, insertion point, or the rotation pivot.
SIGNALS: "sorted array", "rotated sorted", "first and last position", "search insert position",
         "find minimum in rotated", O(log n) required
TIME: O(log n)   SPACE: O(1)
PITFALLS: - Two templates, don't mix their updates: lower-bound uses [lo, hi) with `lo < hi`, `hi = mid`;
            exact-match uses [lo, hi] with `lo <= hi`, `hi = mid - 1`.
          - Last occurrence of x (ints) = lower_bound(x + 1) - 1.
          - Rotated minimum: compare nums[mid] with nums[hi], not nums[lo].
          - Duplicates in rotated arrays break O(log n) (worst case O(n)).
PROBLEMS: 704 Binary Search, 35 Search Insert Position, 34 First and Last Position,
          33 Search in Rotated Sorted Array, 153 Find Minimum in Rotated Sorted Array
"""


# ---------- Core template: lower bound ----------
def lower_bound(nums: list[int], target: int) -> int:
    """First index with nums[i] >= target (same as bisect_left). LC 35."""
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


# ---------- Worked problems ----------
def search_range(nums: list[int], target: int) -> list[int]:
    # LC 34. Two lower bounds: one for target, one for target + 1.
    start = lower_bound(nums, target)
    if start == len(nums) or nums[start] != target:
        return [-1, -1]
    return [start, lower_bound(nums, target + 1) - 1]


def search_rotated(nums: list[int], target: int) -> int:
    # LC 33. One half is always sorted; check if target lies inside that half.
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                 # left half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                     # right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def find_min_rotated(nums: list[int]) -> int:
    # LC 153. If mid > hi, the drop (minimum) is to the right of mid.
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]


if __name__ == "__main__":
    assert lower_bound([1, 3, 3, 5], 3) == 1
    assert lower_bound([1, 3, 3, 5], 6) == 4
    assert lower_bound([], 1) == 0
    assert lower_bound([-5, -2, 0], -3) == 1

    assert search_range([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert search_range([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
    assert search_range([], 0) == [-1, -1]
    assert search_range([2, 2, 2], 2) == [0, 2]

    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert search_rotated([1], 1) == 0
    assert search_rotated([], 1) == -1
    assert search_rotated([3, 1], 1) == 1

    assert find_min_rotated([3, 4, 5, 1, 2]) == 1
    assert find_min_rotated([4, 5, 6, 7, 0, 1, 2]) == 0
    assert find_min_rotated([11, 13, 15, 17]) == 11
    assert find_min_rotated([1]) == 1 and find_min_rotated([2, 1]) == 1
    print("ok")
