"""
PATTERN: Randomized Algorithms (reservoir sampling, shuffle, weighted pick, rejection sampling)
USE WHEN: You must pick uniformly at random from a stream of unknown length, shuffle fairly,
          sample by weight, or build one random generator from another.
SIGNALS: "linked list random node", "random pick index", "shuffle an array",
         "random pick with weight", "implement rand10 using rand7", "uniformly at random"
TIME: reservoir O(n); shuffle O(n); weighted pick O(log n) after O(n) prefix sums   SPACE: O(1) / O(n)
PITFALLS: - Reservoir: keep item i (1-indexed) with probability 1/i, not 1/n.
          - Fisher-Yates: swap i with random index in [i, n-1]; [0, n-1] gives a biased shuffle.
          - Weighted pick: random integer in [1, total], then bisect_left on prefix sums.
          - Rejection sampling: discard values outside the largest multiple of the target range.
PROBLEMS: 382 Linked List Random Node, 384 Shuffle an Array, 528 Random Pick with Weight,
          470 Implement Rand10() Using Rand7(), 398 Random Pick Index
"""
import bisect
import random
from itertools import accumulate


# ---------- Core template: reservoir sampling ----------
def reservoir_sample(stream: list[int]) -> int:
    # LC 382. Every item ends up chosen with probability 1/n without knowing n in advance.
    chosen = stream[0]
    for i, x in enumerate(stream[1:], start=2):
        if random.randint(1, i) == 1:
            chosen = x
    return chosen


# ---------- Worked problems ----------
def shuffle(nums: list[int]) -> list[int]:
    # LC 384. Fisher-Yates.
    arr = nums[:]
    for i in range(len(arr)):
        j = random.randint(i, len(arr) - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


class WeightedPicker:
    # LC 528. Prefix sums split [1, total] into slices proportional to weight.
    def __init__(self, weights: list[int]) -> None:
        self.prefix = list(accumulate(weights))

    def pick_index(self) -> int:
        target = random.randint(1, self.prefix[-1])
        return bisect.bisect_left(self.prefix, target)


def rand7() -> int:
    return random.randint(1, 7)


def rand10() -> int:
    # LC 470. Two rand7 calls give a uniform 1..49; keep 1..40 (4 full copies of 1..10).
    while True:
        idx = (rand7() - 1) * 7 + rand7()
        if idx <= 40:
            return 1 + (idx - 1) % 10


if __name__ == "__main__":
    random.seed(42)
    stream = [10, 20, 30, 40]
    assert reservoir_sample(stream) in stream and reservoir_sample([7]) == 7
    counts = {x: 0 for x in stream}
    for _ in range(4000):
        counts[reservoir_sample(stream)] += 1
    assert all(800 < c < 1200 for c in counts.values())      # roughly uniform

    assert sorted(shuffle([1, 2, 3, 4, 5])) == [1, 2, 3, 4, 5]
    assert shuffle([]) == [] and shuffle([-1]) == [-1]

    wp = WeightedPicker([1, 3])
    picks = [wp.pick_index() for _ in range(4000)]
    assert 2700 < picks.count(1) < 3300                       # ~75%
    assert WeightedPicker([5]).pick_index() == 0

    rolls = [rand10() for _ in range(5000)]
    assert set(rolls) == set(range(1, 11))
    assert all(400 < rolls.count(v) < 600 for v in range(1, 11))
    print("ok")
