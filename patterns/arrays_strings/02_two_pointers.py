"""
PATTERN: Two Pointers (opposite ends, same direction / read-write)
USE WHEN: Input is sorted (or can be sorted) and you look for pairs/triplets with a target,
          or you need in-place filtering/partitioning, or comparing from both ends.
SIGNALS: "sorted array", "pair with sum", "3sum", "in place", "remove duplicates",
         "palindrome", "container", "move zeroes"
TIME: O(n) per pass (O(n^2) for 3sum, O(n log n) if you sort first)   SPACE: O(1)
PITFALLS: - Forgetting to skip duplicates in 3sum (both for i and after a match).
          - `left < right` vs `left <= right`: pairs need two distinct indexes -> `<`.
          - Sorting destroys original indexes (LC 1 Two Sum needs a hashmap instead).
          - Off-by-one in the write pointer for in-place removal.
PROBLEMS: 167 Two Sum II, 15 3Sum, 11 Container With Most Water, 26 Remove Duplicates
          from Sorted Array, 125 Valid Palindrome
"""


# ---------- Core template (opposite ends) ----------
def pair_with_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """nums sorted. Returns indexes of a pair summing to target."""
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return left, right
        if s < target:
            left += 1
        else:
            right -= 1
    return None


# ---------- Core template (read/write, same direction) ----------
def remove_duplicates(nums: list[int]) -> int:
    """LC 26. In place on sorted nums; returns new length."""
    write = 0
    for read in range(len(nums)):
        if read == 0 or nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write


# ---------- Worked problems ----------
def three_sum(nums: list[int]) -> list[list[int]]:
    # LC 15. Sort, fix i, two-pointer the rest; skip duplicates at every level.
    nums = sorted(nums)
    res: list[list[int]] = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        if nums[i] > 0:
            break
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s < 0:
                left += 1
            elif s > 0:
                right -= 1
            else:
                res.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
    return res


def max_area(height: list[int]) -> int:
    # LC 11. Move the shorter side: the taller one can never be the bottleneck of a better answer.
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        best = max(best, (right - left) * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best


def is_palindrome(s: str) -> bool:
    # LC 125. Skip non-alphanumerics on both sides before comparing.
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        else:
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
    return True


if __name__ == "__main__":
    assert pair_with_sum([1, 2, 4, 7, 11], 15) == (2, 4)
    assert pair_with_sum([-3, -1, 0, 2], -4) == (0, 1)
    assert pair_with_sum([], 1) is None
    assert pair_with_sum([5], 10) is None                 # same element twice not allowed

    arr = [1, 1, 2, 3, 3, 3]
    n = remove_duplicates(arr)
    assert n == 3 and arr[:n] == [1, 2, 3]
    assert remove_duplicates([]) == 0

    assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
    assert three_sum([0, 0, 0, 0]) == [[0, 0, 0]]
    assert three_sum([]) == []
    assert three_sum([1, 2]) == []

    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert max_area([1, 1]) == 1
    assert max_area([5]) == 0

    assert is_palindrome("A man, a plan, a canal: Panama")
    assert not is_palindrome("race a car")
    assert is_palindrome("")
    assert is_palindrome(".,")
    print("ok")
