"""
PATTERN: Prefix Sum (+ hashmap of seen prefixes)
USE WHEN: Range sums on a static array, or counting/finding subarrays by sum when numbers can be
          negative (so sliding window's "sum only grows" assumption fails).
SIGNALS: "subarray sum equals k", "count subarrays", "equal number of 0s and 1s", "divisible by k",
         "range sum query" (immutable), "product of array except self"
TIME: O(n)   SPACE: O(n)
PITFALLS: - Seed the map with {0: 1} for counts, or {0: -1} for longest length.
          - Look up `prefix - k` BEFORE recording the current prefix.
          - Longest: store only the FIRST index of each prefix. Count: store frequencies.
          - Range sum [l, r] = prefix[r + 1] - prefix[l] with a size n + 1 prefix array.
PROBLEMS: 303 Range Sum Query - Immutable, 560 Subarray Sum Equals K, 525 Contiguous Array,
          974 Subarray Sums Divisible by K, 238 Product of Array Except Self
"""
from collections import defaultdict


# ---------- Core template: prefix array ----------
def build_prefix(nums: list[int]) -> list[int]:
    """prefix[i] = sum(nums[:i]); range sum [l, r] = prefix[r + 1] - prefix[l]."""
    prefix = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] + x
    return prefix


# ---------- Core template: prefix + hashmap ----------
def count_subarrays_with_sum(nums: list[int], k: int) -> int:
    # LC 560. sum(i..j) = prefix[j] - prefix[i-1], so count earlier prefixes equal to prefix - k.
    seen: dict[int, int] = defaultdict(int)
    seen[0] = 1
    prefix = 0
    count = 0
    for x in nums:
        prefix += x
        count += seen[prefix - k]
        seen[prefix] += 1
    return count


# ---------- Worked problems ----------
def find_max_length(nums: list[int]) -> int:
    # LC 525. Treat 0 as -1; equal 0s and 1s <=> same prefix seen before. Keep first index only.
    first_index = {0: -1}
    prefix = 0
    best = 0
    for i, x in enumerate(nums):
        prefix += 1 if x == 1 else -1
        if prefix in first_index:
            best = max(best, i - first_index[prefix])
        else:
            first_index[prefix] = i
    return best


def subarrays_div_by_k(nums: list[int], k: int) -> int:
    # LC 974. Two prefixes with the same remainder -> the subarray between is divisible by k.
    seen: dict[int, int] = defaultdict(int)
    seen[0] = 1
    prefix = 0
    count = 0
    for x in nums:
        prefix = (prefix + x) % k
        count += seen[prefix]
        seen[prefix] += 1
    return count


def product_except_self(nums: list[int]) -> list[int]:
    # LC 238. Prefix products from the left times suffix products from the right, no division.
    res = [1] * len(nums)
    left = 1
    for i in range(len(nums)):
        res[i] = left
        left *= nums[i]
    right = 1
    for i in range(len(nums) - 1, -1, -1):
        res[i] *= right
        right *= nums[i]
    return res


if __name__ == "__main__":
    p = build_prefix([2, -1, 3])
    assert p == [0, 2, 1, 4] and p[3] - p[1] == 2
    assert build_prefix([]) == [0]

    assert count_subarrays_with_sum([1, 1, 1], 2) == 2
    assert count_subarrays_with_sum([1, -1, 0], 0) == 3
    assert count_subarrays_with_sum([], 0) == 0
    assert count_subarrays_with_sum([3], 3) == 1

    assert find_max_length([0, 1]) == 2
    assert find_max_length([0, 1, 0]) == 2
    assert find_max_length([0, 0, 1, 0, 0, 0, 1, 1]) == 6
    assert find_max_length([]) == 0

    assert subarrays_div_by_k([4, 5, 0, -2, -3, 1], 5) == 7
    assert subarrays_div_by_k([5], 9) == 0
    assert subarrays_div_by_k([-1, 2, 9], 2) == 2

    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert product_except_self([5]) == [1] and product_except_self([]) == []
    print("ok")
