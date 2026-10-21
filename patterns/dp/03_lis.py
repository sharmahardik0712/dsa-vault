"""
PATTERN: Longest Increasing Subsequence (O(n^2) DP and O(n log n) patience sorting)
USE WHEN: You need the longest chain where each element "fits after" the previous one
          (increasing values, nesting envelopes, divisible chains, stacking boxes).
SIGNALS: "longest increasing subsequence", "russian doll envelopes", "longest chain",
         "largest divisible subset", "number of LIS", "minimum deletions to make sorted"
TIME: O(n^2) basic, O(n log n) with tails + bisect   SPACE: O(n)
PITFALLS: - `tails` is NOT the actual subsequence, only its length is meaningful.
          - Strictly increasing: bisect_left. Non-decreasing: bisect_right.
          - Envelopes: sort width ASC and height DESC, so equal widths can't chain.
          - O(n^2) version is easier to extend (counts, reconstruction): know both.
PROBLEMS: 300 Longest Increasing Subsequence, 354 Russian Doll Envelopes, 673 Number of LIS,
          368 Largest Divisible Subset, 1671 Minimum Removals to Make Mountain Array
"""
import bisect


# ---------- Core template: O(n^2) ----------
def lis_quadratic(nums: list[int]) -> int:
    # dp[i] = length of the LIS ending exactly at i.
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp, default=0)


# ---------- Worked problems ----------
def length_of_lis(nums: list[int]) -> int:
    # LC 300. tails[k] = smallest tail of an increasing subsequence of length k + 1.
    tails: list[int] = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def max_envelopes(envelopes: list[list[int]]) -> int:
    # LC 354. Sort by (w asc, h desc), then LIS on heights.
    envelopes = sorted(envelopes, key=lambda e: (e[0], -e[1]))
    return length_of_lis([h for _, h in envelopes])


def find_number_of_lis(nums: list[int]) -> int:
    # LC 673. O(n^2) with a parallel count of how many LIS end at i.
    length = [1] * len(nums)
    count = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]
    best = max(length, default=0)
    return sum(c for size, c in zip(length, count) if size == best)


if __name__ == "__main__":
    assert lis_quadratic([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis_quadratic([]) == 0

    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
    assert length_of_lis([7, 7, 7]) == 1          # strictly increasing
    assert length_of_lis([]) == 0 and length_of_lis([-2, -1, 0]) == 3

    assert max_envelopes([[5, 4], [6, 4], [6, 7], [2, 3]]) == 3
    assert max_envelopes([[1, 1], [1, 1], [1, 1]]) == 1
    assert max_envelopes([[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]]) == 4
    assert max_envelopes([]) == 0

    assert find_number_of_lis([1, 3, 5, 4, 7]) == 2
    assert find_number_of_lis([2, 2, 2, 2, 2]) == 5
    assert find_number_of_lis([]) == 0
    print("ok")
