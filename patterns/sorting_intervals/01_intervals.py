"""
PATTERN: Intervals and Sorting
USE WHEN: Input is a list of ranges/meetings/events, or ordering the input makes a greedy choice
          obviously correct (sort by start to merge, by end to pick max non-overlapping).
SIGNALS: "intervals", "meetings", "overlapping", "merge", "insert interval", "minimum rooms",
         "non-overlapping", "schedule", "start/end times"
TIME: O(n log n) for the sort   SPACE: O(n) for output (O(1) extra otherwise)
PITFALLS: - Touching intervals: is [1,2],[2,3] overlapping? Read the problem (`<` vs `<=`).
          - Merging: update end with max(end, cur_end), not cur_end (containment case).
          - Max non-overlapping: sort by END, not start.
          - Meeting rooms: sweep line with starts/ends sorted separately, or a min-heap of end times.
PROBLEMS: 56 Merge Intervals, 57 Insert Interval, 435 Non-overlapping Intervals,
          253 Meeting Rooms II, 252 Meeting Rooms
"""
import heapq


# ---------- Core template: sort by start, merge ----------
def merge(intervals: list[list[int]]) -> list[list[int]]:
    # LC 56.
    res: list[list[int]] = []
    for start, end in sorted(intervals, key=lambda iv: iv[0]):
        if res and start <= res[-1][1]:
            res[-1][1] = max(res[-1][1], end)
        else:
            res.append([start, end])
    return res


# ---------- Worked problems ----------
def insert(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    # LC 57. Three phases: before (ends before new starts), overlap (absorb), after.
    res: list[list[int]] = []
    i, n = 0, len(intervals)
    start, end = new
    while i < n and intervals[i][1] < start:
        res.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    res.append([start, end])
    res.extend(intervals[i:])
    return res


def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    # LC 435. Greedy: keep the interval that ends earliest; it leaves the most room.
    removed = 0
    prev_end = float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if start >= prev_end:
            prev_end = end
        else:
            removed += 1
    return removed


def min_meeting_rooms(intervals: list[list[int]]) -> int:
    # LC 253. Min-heap of end times = rooms in use; reuse a room if its meeting already ended.
    ends: list[int] = []
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)
        else:
            heapq.heappush(ends, end)
    return len(ends)


if __name__ == "__main__":
    assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge([[1, 10], [2, 3]]) == [[1, 10]]            # containment
    assert merge([]) == [] and merge([[1, 1]]) == [[1, 1]]
    assert merge([[-5, -1], [-3, 2]]) == [[-5, 2]]

    assert insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
    assert insert([], [5, 7]) == [[5, 7]]
    assert insert([[1, 5]], [6, 8]) == [[1, 5], [6, 8]]

    assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]) == 2
    assert erase_overlap_intervals([]) == 0

    assert min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2
    assert min_meeting_rooms([[7, 10], [2, 4]]) == 1
    assert min_meeting_rooms([[1, 5], [5, 10]]) == 1        # back-to-back reuses the room
    assert min_meeting_rooms([]) == 0
    print("ok")
