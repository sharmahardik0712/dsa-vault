"""
PATTERN: Greedy
USE WHEN: A locally best choice never hurts the global answer (you can argue it with an
          exchange argument: "swapping my choice for any other can't make it better").
SIGNALS: "minimum number of jumps", "can you reach", "gas station", "partition labels",
         "task scheduler", "maximum non-overlapping", "assign cookies", "fewest"
TIME: O(n) or O(n log n) with a sort   SPACE: O(1) to O(n)
PITFALLS: - Greedy without a proof: try a small counterexample first (coin change is NOT greedy).
          - Jump Game II: count a jump when you reach the END of the current range, not every step.
          - Gas station: if total gas < total cost, no answer; otherwise restart after every failure.
          - Task scheduler: answer is max(len(tasks), formula); forgetting the max under-counts.
PROBLEMS: 55 Jump Game, 45 Jump Game II, 134 Gas Station, 763 Partition Labels, 621 Task Scheduler
"""
from collections import Counter


# ---------- Core template: track the farthest reachable point ----------
def can_jump(nums: list[int]) -> bool:
    # LC 55.
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True


# ---------- Worked problems ----------
def jump(nums: list[int]) -> int:
    # LC 45. Implicit BFS: [cur_end] is the current level; farthest is the next level's end.
    jumps = 0
    cur_end = 0
    farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return jumps


def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    # LC 134. If you run dry at i, no start between the old start and i works; restart at i+1.
    if sum(gas) < sum(cost):
        return -1
    start = 0
    tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0
    return start


def partition_labels(s: str) -> list[int]:
    # LC 763. A part must extend to the last occurrence of every char inside it.
    last = {ch: i for i, ch in enumerate(s)}
    sizes: list[int] = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            sizes.append(end - start + 1)
            start = i + 1
    return sizes


def least_interval(tasks: list[str], n: int) -> int:
    # LC 621. The most frequent task forms (max_count - 1) blocks of size n + 1, plus a tail.
    counts = Counter(tasks)
    if not counts:
        return 0
    max_count = max(counts.values())
    num_max = sum(1 for c in counts.values() if c == max_count)
    return max(len(tasks), (max_count - 1) * (n + 1) + num_max)


if __name__ == "__main__":
    assert can_jump([2, 3, 1, 1, 4])
    assert not can_jump([3, 2, 1, 0, 4])
    assert can_jump([0]) and can_jump([])

    assert jump([2, 3, 1, 1, 4]) == 2
    assert jump([2, 3, 0, 1, 4]) == 2
    assert jump([0]) == 0 and jump([1, 1, 1]) == 2

    assert can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert can_complete_circuit([2, 3, 4], [3, 4, 3]) == -1
    assert can_complete_circuit([5], [4]) == 0

    assert partition_labels("ababcbacadefegdehijhklij") == [9, 7, 8]
    assert partition_labels("eccbbbbdec") == [10]
    assert partition_labels("abc") == [1, 1, 1]
    assert partition_labels("") == []

    assert least_interval(["A", "A", "A", "B", "B", "B"], 2) == 8
    assert least_interval(["A", "A", "A", "B", "B", "B"], 0) == 6
    assert least_interval(["A", "C", "A", "B", "D", "B"], 1) == 6
    assert least_interval([], 3) == 0
    print("ok")
