"""
PATTERN: State Machine DP
USE WHEN: At each step you are in one of a few modes (holding / not holding a stock, in cooldown,
          transactions used), and transitions between modes have a cost or gain.
SIGNALS: "best time to buy and sell stock" with cooldown / fee / at most k transactions,
         "paint house", "states per day", "can't do X two days in a row"
TIME: O(n * states)   SPACE: O(states)
PITFALLS: - Draw the states and arrows first; each arrow is one line of code.
          - Compute new states from OLD values (save temporaries) when transitions depend on each other.
          - "hold" starts at -inf (can't hold before buying), cash states start at 0.
          - Fee: charge it once per transaction (on sell OR buy, not both).
PROBLEMS: 309 Stock with Cooldown, 714 Stock with Transaction Fee, 123 Stock III (2 transactions),
          188 Stock IV (k transactions), 256 Paint House
"""


# ---------- Core template ----------
def max_profit_cooldown(prices: list[int]) -> int:
    # LC 309. hold -> sold -> rest (cooldown) -> hold.
    hold, sold, rest = float("-inf"), 0, 0
    for p in prices:
        prev_sold = sold
        sold = hold + p
        hold = max(hold, rest - p)
        rest = max(rest, prev_sold)
    return int(max(sold, rest))


# ---------- Worked problems ----------
def max_profit_fee(prices: list[int], fee: int) -> int:
    # LC 714. Two states; buying right after selling on the same day never helps, so no temp needed.
    cash, hold = 0, float("-inf")
    for p in prices:
        cash = max(cash, hold + p - fee)
        hold = max(hold, cash - p)
    return int(cash)


def max_profit_two_transactions(prices: list[int]) -> int:
    # LC 123. Four states in order: buy1 -> sell1 -> buy2 -> sell2.
    buy1 = buy2 = float("-inf")
    sell1 = sell2 = 0
    for p in prices:
        buy1 = max(buy1, -p)
        sell1 = max(sell1, buy1 + p)
        buy2 = max(buy2, sell1 - p)
        sell2 = max(sell2, buy2 + p)
    return int(sell2)


def min_cost_paint_houses(costs: list[list[int]]) -> int:
    # LC 256. State = colour of the previous house; can't repeat it.
    red = blue = green = 0
    for r, b, g in costs:
        red, blue, green = r + min(blue, green), b + min(red, green), g + min(red, blue)
    return min(red, blue, green)


if __name__ == "__main__":
    assert max_profit_cooldown([1, 2, 3, 0, 2]) == 3
    assert max_profit_cooldown([1]) == 0 and max_profit_cooldown([]) == 0
    assert max_profit_cooldown([5, 4, 3]) == 0

    assert max_profit_fee([1, 3, 2, 8, 4, 9], 2) == 8
    assert max_profit_fee([1, 3, 7, 5, 10, 3], 3) == 6
    assert max_profit_fee([], 1) == 0

    assert max_profit_two_transactions([3, 3, 5, 0, 0, 3, 1, 4]) == 6
    assert max_profit_two_transactions([1, 2, 3, 4, 5]) == 4
    assert max_profit_two_transactions([7, 6, 4, 3, 1]) == 0
    assert max_profit_two_transactions([]) == 0

    assert min_cost_paint_houses([[17, 2, 17], [16, 16, 5], [14, 3, 19]]) == 10
    assert min_cost_paint_houses([[7, 6, 2]]) == 2
    assert min_cost_paint_houses([]) == 0
    print("ok")
