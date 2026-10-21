"""
PATTERN: Cyclic Sort / Index as Hash
USE WHEN: Values are in a known range like 1..n (or 0..n) and you need missing/duplicate numbers
          in O(n) time and O(1) extra space. The array itself becomes the hash table.
SIGNALS: "numbers in range [1, n]", "find the missing", "find the duplicate", "first missing positive",
         "without extra space", "O(1) space", "array of n integers"
TIME: O(n)   SPACE: O(1)
PITFALLS: - Cyclic sort uses `while`, not `for`: keep swapping at i until nums[i] is placed.
          - Swap condition must check the TARGET slot (nums[j] != nums[i]) or duplicates loop forever.
          - Sign-marking needs abs() when reading values you may already have negated.
          - Values out of range (<= 0 or > n) must be skipped, not swapped.
PROBLEMS: 41 First Missing Positive, 448 Find All Numbers Disappeared, 442 Find All Duplicates,
          287 Find the Duplicate Number, 268 Missing Number
"""


# ---------- Core template: put value v at index v - 1 ----------
def cyclic_sort(nums: list[int]) -> list[int]:
    nums = nums[:]
    i = 0
    while i < len(nums):
        j = nums[i] - 1
        if 0 <= j < len(nums) and nums[j] != nums[i]:
            nums[i], nums[j] = nums[j], nums[i]
        else:
            i += 1
    return nums


# ---------- Worked problems ----------
def first_missing_positive(nums: list[int]) -> int:
    # LC 41. After cyclic sort, the first index i with nums[i] != i + 1 is the answer.
    placed = cyclic_sort(nums)
    for i, x in enumerate(placed):
        if x != i + 1:
            return i + 1
    return len(placed) + 1


def find_disappeared(nums: list[int]) -> list[int]:
    # LC 448.
    placed = cyclic_sort(nums)
    return [i + 1 for i, x in enumerate(placed) if x != i + 1]


def find_duplicates(nums: list[int]) -> list[int]:
    # LC 442. Negate nums[v-1] on first sight of v; already negative means v is a repeat.
    nums = nums[:]
    res: list[int] = []
    for x in nums:
        i = abs(x) - 1
        if nums[i] < 0:
            res.append(abs(x))
        else:
            nums[i] = -nums[i]
    return res


def find_duplicate(nums: list[int]) -> int:
    # LC 287. Read-only: treat i -> nums[i] as a linked list; the duplicate is the cycle start.
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


if __name__ == "__main__":
    assert cyclic_sort([3, 1, 2]) == [1, 2, 3]
    assert cyclic_sort([]) == []

    assert first_missing_positive([1, 2, 0]) == 3
    assert first_missing_positive([3, 4, -1, 1]) == 2
    assert first_missing_positive([7, 8, 9, 11, 12]) == 1
    assert first_missing_positive([1, 1]) == 2
    assert first_missing_positive([]) == 1

    assert find_disappeared([4, 3, 2, 7, 8, 2, 3, 1]) == [5, 6]
    assert find_disappeared([1, 1]) == [2]
    assert find_disappeared([1]) == []

    assert sorted(find_duplicates([4, 3, 2, 7, 8, 2, 3, 1])) == [2, 3]
    assert find_duplicates([1, 1, 2]) == [1]
    assert find_duplicates([1]) == []

    assert find_duplicate([1, 3, 4, 2, 2]) == 2
    assert find_duplicate([3, 1, 3, 4, 2]) == 3
    assert find_duplicate([2, 2, 2, 2]) == 2
    print("ok")
