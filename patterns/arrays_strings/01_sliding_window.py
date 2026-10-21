"""
PATTERN: Sliding Window (fixed and variable size)
USE WHEN: You need the best/count of contiguous subarrays or substrings, and growing
          the window only makes a constraint "worse" (monotonic), so you can shrink from the left.
SIGNALS: "contiguous subarray", "substring", "longest/shortest", "at most K", "window of size k",
         "without repeating", "minimum window containing"
TIME: O(n)   SPACE: O(k) for the window state (hashmap/counter)
PITFALLS: - Using `if` instead of `while` when shrinking (one shrink may not be enough).
          - Updating the answer before vs after shrinking (longest: after; shortest: inside while).
          - Negative numbers break the "sum only grows" assumption -> use prefix sum + hashmap instead.
          - "Exactly K" = atMost(K) - atMost(K-1).
PROBLEMS: 3 Longest Substring Without Repeating Characters, 76 Minimum Window Substring,
          424 Longest Repeating Character Replacement, 209 Minimum Size Subarray Sum,
          992 Subarrays with K Different Integers
"""
from collections import defaultdict


# ---------- Core template (variable window) ----------
def longest_valid_window(nums: list[int], k: int) -> int:
    """Longest window whose sum is <= k (non-negative nums)."""
    left = 0
    window_sum = 0
    best = 0
    for right, x in enumerate(nums):
        window_sum += x                      # 1. expand
        while window_sum > k:                # 2. shrink while invalid
            window_sum -= nums[left]
            left += 1
        best = max(best, right - left + 1)   # 3. window is valid, record
    return best


# ---------- Core template (fixed window) ----------
def max_sum_fixed(nums: list[int], k: int) -> int:
    if k <= 0 or k > len(nums):
        return 0
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]
        best = max(best, window)
    return best


# ---------- Worked problems ----------
def length_of_longest_substring(s: str) -> int:
    # LC 3. Jump left past the last occurrence of the repeated char.
    last_seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


def min_window(s: str, t: str) -> str:
    # LC 76. Track how many chars of t are still "missing"; shrink while missing == 0.
    if not t or not s:
        return ""
    need: dict[str, int] = defaultdict(int)
    for ch in t:
        need[ch] += 1
    missing = len(t)
    left = 0
    best_start, best_len = 0, float("inf")
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left + 1 < best_len:
                best_start, best_len = left, right - left + 1
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if best_len == float("inf") else s[best_start:best_start + int(best_len)]


def subarrays_with_k_distinct(nums: list[int], k: int) -> int:
    # LC 992. exactly(K) = atMost(K) - atMost(K-1); each atMost counts windows ending at right.
    def at_most(k: int) -> int:
        count: dict[int, int] = defaultdict(int)
        left = 0
        total = 0
        for right, x in enumerate(nums):
            count[x] += 1
            while len(count) > k:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            total += right - left + 1
        return total

    return at_most(k) - at_most(k - 1) if k > 0 else 0


if __name__ == "__main__":
    assert longest_valid_window([1, 2, 1, 0, 1, 1, 0], 4) == 5
    assert longest_valid_window([], 3) == 0
    assert longest_valid_window([5], 3) == 0
    assert longest_valid_window([3], 3) == 1

    assert max_sum_fixed([1, 4, 2, 10, 2, 3, 1, 0, 20], 4) == 24
    assert max_sum_fixed([-1, -2, -3], 2) == -3
    assert max_sum_fixed([], 1) == 0

    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
    assert length_of_longest_substring("") == 0
    assert length_of_longest_substring("abba") == 2       # stale index trap

    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""
    assert min_window("", "a") == ""

    assert subarrays_with_k_distinct([1, 2, 1, 2, 3], 2) == 7
    assert subarrays_with_k_distinct([1, 2, 1, 3, 4], 3) == 3
    assert subarrays_with_k_distinct([], 1) == 0
    print("ok")
