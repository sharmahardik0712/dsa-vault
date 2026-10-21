"""
PATTERN: K-way Merge
USE WHEN: You have K sorted lists/rows/streams and need a merged order, the kth smallest overall,
          or a range that touches every list. Keep one "frontier" element per list in a min-heap.
SIGNALS: "merge k sorted lists", "kth smallest in sorted matrix", "smallest range covering k lists",
         "k pairs with smallest sums", "sorted rows", "ugly number"
TIME: O(N log K), N = total elements popped   SPACE: O(K)
PITFALLS: - Heap entries need (value, list_index, element_index) so ties don't compare payloads.
          - Push the NEXT element from the same list after each pop.
          - Skip empty lists when seeding the heap.
          - Smallest range: track the current max separately; stop when any list runs out.
PROBLEMS: 23 Merge k Sorted Lists, 378 Kth Smallest Element in a Sorted Matrix,
          632 Smallest Range Covering Elements from K Lists, 373 Find K Pairs with Smallest Sums
"""
import heapq


# ---------- Core template ----------
def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    # LC 23 (arrays instead of linked lists; same idea).
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    res: list[int] = []
    while heap:
        val, i, j = heapq.heappop(heap)
        res.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return res


# ---------- Worked problems ----------
def kth_smallest_matrix(matrix: list[list[int]], k: int) -> int:
    # LC 378. Each row is a sorted list; pop k - 1 times, the top is the kth smallest.
    heap = [(row[0], r, 0) for r, row in enumerate(matrix) if row]
    heapq.heapify(heap)
    for _ in range(k - 1):
        _, r, c = heapq.heappop(heap)
        if c + 1 < len(matrix[r]):
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
    return heap[0][0]


def smallest_range(lists: list[list[int]]) -> list[int]:
    # LC 632. Heap holds one value per list; [heap min, current max] always covers every list.
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists)]
    heapq.heapify(heap)
    cur_max = max(lst[0] for lst in lists)
    best = [heap[0][0], cur_max]
    while True:
        val, i, j = heapq.heappop(heap)
        if cur_max - val < best[1] - best[0]:
            best = [val, cur_max]
        if j + 1 == len(lists[i]):
            return best
        nxt = lists[i][j + 1]
        heapq.heappush(heap, (nxt, i, j + 1))
        cur_max = max(cur_max, nxt)


if __name__ == "__main__":
    assert merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert merge_k_sorted([]) == [] and merge_k_sorted([[]]) == []
    assert merge_k_sorted([[-2, 0], [-3]]) == [-3, -2, 0]

    m = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
    assert kth_smallest_matrix(m, 8) == 13
    assert kth_smallest_matrix(m, 1) == 1
    assert kth_smallest_matrix([[-5]], 1) == -5

    assert smallest_range([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]) == [20, 24]
    assert smallest_range([[1, 2, 3], [1, 2, 3], [1, 2, 3]]) == [1, 1]
    assert smallest_range([[7]]) == [7, 7]
    print("ok")
