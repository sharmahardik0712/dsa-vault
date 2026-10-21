"""
PATTERN: Custom Sort Order (key functions and comparators)
USE WHEN: The answer is "sort by a rule you define": multi-key ordering, frequency, a given
          reference order, or a pairwise rule that isn't a simple key (needs a comparator).
SIGNALS: "largest number", "sort by frequency", "relative order", "custom order",
         "reorder log files", "sort by X then by Y", "arrange to form"
TIME: O(n log n) (comparator: O(n log n) comparisons, each maybe O(L))   SPACE: O(n)
PITFALLS: - Prefer key= over a comparator; use functools.cmp_to_key only for pairwise rules.
          - Mixed directions: negate numeric keys (-count) instead of reverse=True on everything.
          - Python sort is stable: sort by the secondary key first, then by the primary (or use a tuple).
          - Largest number: all zeros should return "0", not "000".
PROBLEMS: 179 Largest Number, 1636 Sort Array by Increasing Frequency, 1122 Relative Sort Array,
          791 Custom Sort String, 937 Reorder Data in Log Files
"""
from collections import Counter
from functools import cmp_to_key


# ---------- Core template: comparator when no simple key exists ----------
def largest_number(nums: list[int]) -> str:
    # LC 179. a goes before b if a+b > b+a as strings.
    def compare(a: str, b: str) -> int:
        if a + b > b + a:
            return -1
        if a + b < b + a:
            return 1
        return 0

    parts = sorted((str(x) for x in nums), key=cmp_to_key(compare))
    result = "".join(parts)
    return "0" if result and result[0] == "0" else result


# ---------- Worked problems: tuple keys ----------
def frequency_sort(nums: list[int]) -> list[int]:
    # LC 1636. Increasing frequency; ties by value DEcreasing -> key (count, -value).
    counts = Counter(nums)
    return sorted(nums, key=lambda x: (counts[x], -x))


def relative_sort(arr1: list[int], arr2: list[int]) -> list[int]:
    # LC 1122. Rank by position in arr2; unknown values go last in ascending order.
    rank = {v: i for i, v in enumerate(arr2)}
    return sorted(arr1, key=lambda x: (rank.get(x, len(arr2)), x))


def custom_sort_string(order: str, s: str) -> str:
    # LC 791. Same idea on characters; chars not in `order` keep a fixed rank at the end.
    rank = {ch: i for i, ch in enumerate(order)}
    return "".join(sorted(s, key=lambda ch: rank.get(ch, len(order))))


if __name__ == "__main__":
    assert largest_number([10, 2]) == "210"
    assert largest_number([3, 30, 34, 5, 9]) == "9534330"
    assert largest_number([0, 0]) == "0"
    assert largest_number([]) == ""

    assert frequency_sort([1, 1, 2, 2, 2, 3]) == [3, 1, 1, 2, 2, 2]
    assert frequency_sort([2, 3, 1, 3, 2]) == [1, 3, 3, 2, 2]
    assert frequency_sort([-1, 1, -6, 4, 5, -6, 1, 4, 1]) == [5, -1, 4, 4, -6, -6, 1, 1, 1]
    assert frequency_sort([]) == []

    assert relative_sort([2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], [2, 1, 4, 3, 9, 6]) == \
        [2, 2, 2, 1, 4, 3, 3, 9, 6, 7, 19]
    assert relative_sort([28, 6, 22, 8, 44, 17], [22, 28, 8, 6]) == [22, 28, 8, 6, 17, 44]
    assert relative_sort([], [1]) == []

    assert custom_sort_string("cba", "abcd") == "cbad"
    assert custom_sort_string("bcafg", "abcd") == "bcad"
    assert custom_sort_string("", "ba") == "ba"
    print("ok")
