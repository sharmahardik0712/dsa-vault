"""
PATTERN: Bit Manipulation
USE WHEN: Pairs cancel out (XOR), you need O(1) space tricks on integers, subset enumeration
          with bitmasks (n <= 20), or counting/setting individual bits.
SIGNALS: "single number", "appears twice except one", "without extra space", "power of two",
         "count set bits", "missing number", "all subsets" (small n), "XOR", "bitmask DP"
TIME: O(n) or O(bits)   SPACE: O(1)
PITFALLS: - Python ints are unbounded: emulate 32-bit with `& 0xFFFFFFFF` and convert sign back.
          - Operator precedence: `x & 1 == 0` is `x & (1 == 0)`. Always parenthesise.
          - `~x` in Python is `-x - 1`, not a 32-bit flip.
          - `x & (x - 1)` clears the lowest set bit; `x & -x` isolates it.
PROBLEMS: 136 Single Number, 191 Number of 1 Bits, 338 Counting Bits, 268 Missing Number,
          371 Sum of Two Integers, 78 Subsets (bitmask)
"""


# ---------- Core template: common bit ops ----------
def get_bit(x: int, i: int) -> int:
    return (x >> i) & 1


def set_bit(x: int, i: int) -> int:
    return x | (1 << i)


def clear_bit(x: int, i: int) -> int:
    return x & ~(1 << i)


def toggle_bit(x: int, i: int) -> int:
    return x ^ (1 << i)


def is_power_of_two(x: int) -> bool:
    # A power of two has exactly one set bit.
    return x > 0 and (x & (x - 1)) == 0


# ---------- Worked problems ----------
def single_number(nums: list[int]) -> int:
    # LC 136. a ^ a = 0 and a ^ 0 = a, so all pairs cancel.
    res = 0
    for x in nums:
        res ^= x
    return res


def hamming_weight(n: int) -> int:
    # LC 191. Brian Kernighan: each `n &= n - 1` removes one set bit.
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def count_bits(n: int) -> list[int]:
    # LC 338. bits(i) = bits(i >> 1) + lowest bit.
    res = [0] * (n + 1)
    for i in range(1, n + 1):
        res[i] = res[i >> 1] + (i & 1)
    return res


def missing_number(nums: list[int]) -> int:
    # LC 268. XOR every index 0..n with every value; the missing one is left.
    res = len(nums)
    for i, x in enumerate(nums):
        res ^= i ^ x
    return res


def get_sum(a: int, b: int) -> int:
    # LC 371. XOR = sum without carry, AND << 1 = carry. Mask to 32 bits for Python.
    mask = 0xFFFFFFFF
    while b & mask:
        a, b = a ^ b, (a & b) << 1
    a &= mask
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)


def subsets_bitmask(nums: list[int]) -> list[list[int]]:
    # Bit i of mask says whether nums[i] is in the subset.
    n = len(nums)
    res = []
    for mask in range(1 << n):
        res.append([nums[i] for i in range(n) if (mask >> i) & 1])
    return res


if __name__ == "__main__":
    assert get_bit(5, 0) == 1 and get_bit(5, 1) == 0
    assert set_bit(5, 1) == 7 and clear_bit(7, 1) == 5 and toggle_bit(5, 2) == 1
    assert is_power_of_two(1) and is_power_of_two(16)
    assert not is_power_of_two(0) and not is_power_of_two(-8) and not is_power_of_two(6)

    assert single_number([4, 1, 2, 1, 2]) == 4
    assert single_number([1]) == 1
    assert single_number([-1, 3, 3]) == -1

    assert hamming_weight(11) == 3 and hamming_weight(0) == 0 and hamming_weight(2**31) == 1

    assert count_bits(5) == [0, 1, 1, 2, 1, 2]
    assert count_bits(0) == [0]

    assert missing_number([3, 0, 1]) == 2
    assert missing_number([0, 1]) == 2
    assert missing_number([1]) == 0
    assert missing_number([]) == 0

    assert get_sum(1, 2) == 3 and get_sum(-2, 3) == 1
    assert get_sum(-5, -7) == -12 and get_sum(0, 0) == 0

    assert sorted(subsets_bitmask([1, 2])) == [[], [1], [1, 2], [2]]
    assert subsets_bitmask([]) == [[]]
    print("ok")
