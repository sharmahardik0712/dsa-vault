"""
PATTERN: Binary Search on the Answer Space
USE WHEN: You're asked for the min (or max) value X that satisfies a condition, and feasibility is
          monotonic: if X works, every bigger X works too (or every smaller one, for maximising).
SIGNALS: "minimum speed/capacity/time such that", "within D days", "minimize the maximum",
         "maximize the minimum", "at least m groups", answer range is huge but checking one X is O(n)
TIME: O(n log R), R = size of the answer range   SPACE: O(1)
PITFALLS: - lo must be a lower bound on the answer, hi must be feasible (or hi + 1 used as "not found").
          - Maximising: find the first X that FAILS, answer is X - 1 (or flip the predicate).
          - Ceil division without floats: (a + b - 1) // b.
          - The feasibility check is the real problem: write and test it first.
PROBLEMS: 875 Koko Eating Bananas, 1011 Capacity To Ship Packages, 410 Split Array Largest Sum,
          1552 Magnetic Force Between Two Balls, 1482 Minimum Number of Days to Make m Bouquets
"""
from typing import Callable


# ---------- Core template: first value where predicate is True ----------
def first_true(lo: int, hi: int, pred: Callable[[int], bool]) -> int:
    """Search [lo, hi). pred is False...False True...True. Returns hi if never True."""
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


# ---------- Worked problems ----------
def min_eating_speed(piles: list[int], h: int) -> int:
    # LC 875. Answer space [1, max(piles)]; "speed k finishes in h hours" is monotonic.
    def can_finish(k: int) -> bool:
        hours = 0
        for p in piles:
            hours += (p + k - 1) // k
        return hours <= h

    return first_true(1, max(piles) + 1, can_finish)


def ship_within_days(weights: list[int], days: int) -> int:
    # LC 1011 (same check solves LC 410). lo = heaviest item (must fit), hi = total (one day).
    def feasible(cap: int) -> bool:
        used_days, load = 1, 0
        for w in weights:
            if load + w > cap:
                used_days += 1
                load = 0
            load += w
        return used_days <= days

    return first_true(max(weights), sum(weights) + 1, feasible)


def max_distance(position: list[int], m: int) -> int:
    # LC 1552. Maximise the minimum gap: find the first gap that does NOT fit m balls, minus 1.
    position = sorted(position)

    def can_place(gap: int) -> bool:
        count, last = 1, position[0]
        for p in position[1:]:
            if p - last >= gap:
                count += 1
                last = p
        return count >= m

    hi = position[-1] - position[0] + 1
    return first_true(1, hi + 1, lambda gap: not can_place(gap)) - 1


if __name__ == "__main__":
    assert first_true(0, 10, lambda x: x * x >= 20) == 5
    assert first_true(0, 3, lambda x: False) == 3

    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
    assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23
    assert min_eating_speed([1], 1) == 1

    assert ship_within_days([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
    assert ship_within_days([1, 2, 3, 1, 1], 4) == 3
    assert ship_within_days([7, 2, 5, 10, 8], 2) == 18        # LC 410 example
    assert ship_within_days([7], 1) == 7

    assert max_distance([1, 2, 3, 4, 7], 3) == 3
    assert max_distance([5, 4, 3, 2, 1, 1000000000], 2) == 999999999
    assert max_distance([1, 2], 2) == 1
    print("ok")
