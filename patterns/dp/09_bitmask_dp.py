"""
PATTERN: Bitmask DP
USE WHEN: n is small (<= ~16-20) and the state must remember WHICH items are used/visited.
          A bitmask of n bits encodes the subset; combine with "current node" when order matters.
SIGNALS: "visit all nodes", "travelling salesman", "partition into k equal subsets",
         "assign n workers to n jobs", "n <= 16", "minimum incompatibility", "shortest superstring"
TIME: O(2^n * n) or O(2^n * n^2)   SPACE: O(2^n) or O(2^n * n)
PITFALLS: - Parenthesise: `mask & (1 << i)`, `mask | (1 << i)` (shift binds tighter, but be explicit).
          - There are `1 << n` states, not n.
          - Shortest path visiting all nodes: BFS over (node, mask), start from EVERY node.
          - Partition-k: dp[mask] stores the current bucket fill (sum % target), not a boolean.
PROBLEMS: 847 Shortest Path Visiting All Nodes, 698 Partition to K Equal Sum Subsets,
          1986 Minimum Number of Work Sessions, 943 Find the Shortest Superstring, TSP (classic)
"""
from collections import deque


# ---------- Core template: TSP ----------
def tsp(dist: list[list[int]]) -> int:
    """Min cost tour from node 0 visiting every node once and returning to 0."""
    n = len(dist)
    inf = float("inf")
    dp = [[inf] * n for _ in range(1 << n)]       # dp[mask][last]
    dp[1][0] = 0
    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == inf or not mask & (1 << last):
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                new_mask = mask | (1 << nxt)
                cost = dp[mask][last] + dist[last][nxt]
                if cost < dp[new_mask][nxt]:
                    dp[new_mask][nxt] = cost
    full = (1 << n) - 1
    return int(min(dp[full][i] + dist[i][0] for i in range(n)))


# ---------- Worked problems ----------
def shortest_path_length(graph: list[list[int]]) -> int:
    # LC 847. BFS over (node, visited mask) from every start node simultaneously.
    n = len(graph)
    full = (1 << n) - 1
    queue = deque((i, 1 << i, 0) for i in range(n))
    seen = {(i, 1 << i) for i in range(n)}
    while queue:
        node, mask, steps = queue.popleft()
        if mask == full:
            return steps
        for nxt in graph[node]:
            state = (nxt, mask | (1 << nxt))
            if state not in seen:
                seen.add(state)
                queue.append((nxt, state[1], steps + 1))
    return 0


def can_partition_k(nums: list[int], k: int) -> bool:
    # LC 698. dp[mask] = fill of the current bucket using items in mask (-1 = unreachable).
    total = sum(nums)
    if not nums or total % k:
        return False
    target = total // k
    if max(nums) > target:
        return False
    n = len(nums)
    dp = [-1] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] == -1:
            continue
        for i in range(n):
            nxt = mask | (1 << i)
            if not mask & (1 << i) and dp[nxt] == -1 and dp[mask] + nums[i] <= target:
                dp[nxt] = (dp[mask] + nums[i]) % target
    return dp[-1] == 0


if __name__ == "__main__":
    d = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
    assert tsp(d) == 80
    assert tsp([[0]]) == 0
    assert tsp([[0, 3], [4, 0]]) == 7

    assert shortest_path_length([[1, 2, 3], [0], [0], [0]]) == 4
    assert shortest_path_length([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]]) == 4
    assert shortest_path_length([[]]) == 0

    assert can_partition_k([4, 3, 2, 3, 5, 2, 1], 4)
    assert not can_partition_k([1, 2, 3, 4], 3)
    assert can_partition_k([5], 1)
    assert not can_partition_k([2, 2, 2, 2, 3, 4, 5], 4)
    assert not can_partition_k([], 2)
    print("ok")
