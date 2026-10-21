"""
PATTERN: Monotonic Stack
USE WHEN: For each element you need the nearest greater/smaller element to the left or right,
          or the span/area it controls before something bigger/smaller blocks it.
SIGNALS: "next greater element", "daily temperatures", "stock span", "largest rectangle in histogram",
         "trapping rain water", "remove k digits", "sum of subarray minimums"
TIME: O(n) (each index pushed and popped once)   SPACE: O(n)
PITFALLS: - Store INDEXES, not values, when you need distances or widths.
          - Decreasing stack finds next GREATER; increasing stack finds next SMALLER.
          - Strict vs non-strict comparison changes how equal values are handled.
          - Flush the stack at the end (append a sentinel like height 0).
PROBLEMS: 496 Next Greater Element I, 739 Daily Temperatures, 84 Largest Rectangle in Histogram,
          42 Trapping Rain Water, 901 Online Stock Span
"""


# ---------- Core template: next greater element to the right ----------
def next_greater(nums: list[int]) -> list[int]:
    """res[i] = first value to the right that is > nums[i], else -1."""
    res = [-1] * len(nums)
    stack: list[int] = []                 # indexes; values decreasing from bottom to top
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            res[stack.pop()] = x          # x is the answer for everything it pops
        stack.append(i)
    return res


# ---------- Worked problems ----------
def daily_temperatures(temps: list[int]) -> list[int]:
    # LC 739. Same as next_greater but store the distance in days.
    res = [0] * len(temps)
    stack: list[int] = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            res[j] = i - j
        stack.append(i)
    return res


def largest_rectangle(heights: list[int]) -> int:
    # LC 84. Increasing stack; a popped bar's right boundary is i, left boundary is the new top.
    stack: list[int] = []
    best = 0
    extended = heights + [0]
    for i, h in enumerate(extended):
        while stack and extended[stack[-1]] >= h:
            height = extended[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best


def trap(height: list[int]) -> int:
    # LC 42. Popped bar is a "bottom"; water above it is bounded by the new top and the current bar.
    stack: list[int] = []
    water = 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break
            left = stack[-1]
            width = i - left - 1
            water += width * (min(height[left], h) - height[bottom])
        stack.append(i)
    return water


if __name__ == "__main__":
    assert next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
    assert next_greater([]) == [] and next_greater([5]) == [-1]
    assert next_greater([3, 3]) == [-1, -1]
    assert next_greater([-5, -3, -4]) == [-3, -1, -1]

    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert daily_temperatures([30]) == [0] and daily_temperatures([]) == []

    assert largest_rectangle([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle([2, 4]) == 4
    assert largest_rectangle([]) == 0 and largest_rectangle([3, 3, 3]) == 9

    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([4, 2, 0, 3, 2, 5]) == 9
    assert trap([]) == 0 and trap([5]) == 0 and trap([1, 2, 3]) == 0
    print("ok")
