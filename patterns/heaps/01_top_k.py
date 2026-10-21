"""
PATTERN: Top K with a Heap
USE WHEN: You need the K largest / smallest / most frequent / closest items, or the kth one,
          without fully sorting.
SIGNALS: "k largest", "kth largest", "k most frequent", "k closest points", "top k",
         "k smallest pairs", "sort characters by frequency"
TIME: O(n log k)   SPACE: O(k)
PITFALLS: - K LARGEST uses a MIN-heap of size k (evict the smallest); K smallest uses a max-heap.
          - Python heapq is min-only: push negated keys for a max-heap.
          - Ties in tuples compare the next field: add an index if payloads aren't comparable.
          - O(n) alternatives worth mentioning: quickselect, bucket sort by frequency.
PROBLEMS: 215 Kth Largest Element, 347 Top K Frequent Elements, 973 K Closest Points to Origin,
          692 Top K Frequent Words, 451 Sort Characters By Frequency
"""
import heapq
from collections import Counter


# ---------- Core template: keep the k largest in a min-heap ----------
def k_largest(nums: list[int], k: int) -> list[int]:
    heap: list[int] = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted(heap, reverse=True)


# ---------- Worked problems ----------
def find_kth_largest(nums: list[int], k: int) -> int:
    # LC 215. Root of a size-k min-heap is the kth largest.
    heap = nums[:k]
    heapq.heapify(heap)
    for x in nums[k:]:
        if x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap[0]


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    # LC 347. Count, then take the k entries with the largest counts.
    counts = Counter(nums)
    return [x for x, _ in heapq.nlargest(k, counts.items(), key=lambda kv: kv[1])]


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    # LC 973. Max-heap of size k on distance (negated); evict the farthest.
    heap: list[tuple[int, int, int]] = []
    for x, y in points:
        heapq.heappush(heap, (-(x * x + y * y), x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]


if __name__ == "__main__":
    assert k_largest([3, 1, 5, 12, 2, 11], 3) == [12, 11, 5]
    assert k_largest([], 2) == [] and k_largest([4], 3) == [4]

    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert find_kth_largest([1], 1) == 1
    assert find_kth_largest([-1, -5, -3], 1) == -1

    assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert top_k_frequent([1], 1) == [1] and top_k_frequent([], 1) == []

    assert k_closest([[1, 3], [-2, 2]], 1) == [[-2, 2]]
    assert sorted(k_closest([[3, 3], [5, -1], [-2, 4]], 2)) == [[-2, 4], [3, 3]]
    assert k_closest([], 1) == []
    print("ok")
