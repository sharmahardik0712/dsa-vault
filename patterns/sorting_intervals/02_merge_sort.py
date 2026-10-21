"""
PATTERN: Merge Sort / Divide and Conquer Counting
USE WHEN: You need a stable O(n log n) sort, or to COUNT pairs (i < j) with a condition across
          the array: count during the merge step, when both halves are sorted.
SIGNALS: "count inversions", "reverse pairs", "count of smaller numbers after self",
         "sort an array" (implement), "stable sort", "sort a linked list"
TIME: O(n log n)   SPACE: O(n)
PITFALLS: - Use `<=` when merging to keep the sort stable.
          - Inversions: when taking from the RIGHT half, add len(left) - i (all remaining left are bigger).
          - Reverse pairs: count with a separate pointer BEFORE merging (condition differs from order).
          - Slicing copies: fine in interviews, but say it costs O(n) per level.
PROBLEMS: 912 Sort an Array, 493 Reverse Pairs, 315 Count of Smaller Numbers After Self,
          148 Sort List, "count inversions" (classic)
"""


# ---------- Core template ----------
def merge(left: list[int], right: list[int]) -> list[int]:
    merged: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(nums: list[int]) -> list[int]:
    # LC 912.
    if len(nums) <= 1:
        return nums[:]
    mid = len(nums) // 2
    return merge(merge_sort(nums[:mid]), merge_sort(nums[mid:]))


# ---------- Worked problems ----------
def count_inversions(nums: list[int]) -> int:
    # Pairs i < j with nums[i] > nums[j]. Taking right[j] means every remaining left item beats it.
    def sort_count(arr: list[int]) -> tuple[list[int], int]:
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, a = sort_count(arr[:mid])
        right, b = sort_count(arr[mid:])
        merged: list[int] = []
        count = a + b
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                count += len(left) - i
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, count

    return sort_count(nums)[1]


def reverse_pairs(nums: list[int]) -> int:
    # LC 493. Pairs i < j with nums[i] > 2 * nums[j]: count with a moving pointer, then merge.
    def sort_count(arr: list[int]) -> tuple[list[int], int]:
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, a = sort_count(arr[:mid])
        right, b = sort_count(arr[mid:])
        count = a + b
        j = 0
        for x in left:
            while j < len(right) and x > 2 * right[j]:
                j += 1
            count += j
        return merge(left, right), count

    return sort_count(nums)[1]


if __name__ == "__main__":
    assert merge_sort([5, 2, 3, 1]) == [1, 2, 3, 5]
    assert merge_sort([]) == [] and merge_sort([1]) == [1]
    assert merge_sort([3, -1, 3, 0]) == [-1, 0, 3, 3]

    assert count_inversions([2, 4, 1, 3, 5]) == 3
    assert count_inversions([5, 4, 3, 2, 1]) == 10
    assert count_inversions([]) == 0 and count_inversions([1, 1, 1]) == 0

    assert reverse_pairs([1, 3, 2, 3, 1]) == 2
    assert reverse_pairs([2, 4, 3, 5, 1]) == 3
    assert reverse_pairs([-5, -5]) == 1                # -5 > -10
    assert reverse_pairs([]) == 0
    print("ok")
