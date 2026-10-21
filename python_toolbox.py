"""
Python toolbox for interviews. Skim the evening before.
Run: python python_toolbox.py  -> prints ok
"""
import bisect
import copy
import heapq
import sys
from collections import Counter, OrderedDict, defaultdict, deque
from functools import lru_cache
from itertools import accumulate, combinations, permutations, product


# ---------------------------------------------------------------- heapq
def heapq_demo() -> None:
    # Min-heap: smallest at index 0.
    h: list[int] = []
    for x in [5, 1, 8, 3]:
        heapq.heappush(h, x)
    assert h[0] == 1
    assert heapq.heappop(h) == 1

    # Max-heap: push negatives, negate on pop.
    mx: list[int] = []
    for x in [5, 1, 8, 3]:
        heapq.heappush(mx, -x)
    assert -heapq.heappop(mx) == 8

    # Heap of tuples: compares first element, then second on ties.
    # Add a counter as tiebreaker if the payload is not comparable.
    tasks: list[tuple[int, str]] = []
    heapq.heappush(tasks, (2, "write"))
    heapq.heappush(tasks, (1, "read"))
    assert heapq.heappop(tasks) == (1, "read")

    nums = [4, 1, 7, 3, 9]
    assert heapq.nlargest(2, nums) == [9, 7]
    assert heapq.nsmallest(2, nums) == [1, 3]

    # heapify is O(n), in place.
    arr = [9, 4, 7, 1]
    heapq.heapify(arr)
    assert arr[0] == 1

    # heapreplace = pop then push (faster); heappushpop = push then pop.
    assert heapq.heappushpop([2, 5], 1) == 1


# ---------------------------------------------------------- collections
def collections_demo() -> None:
    # deque: O(1) at both ends. list.pop(0) is O(n), never use it as a queue.
    q = deque([1, 2, 3])
    q.append(4)
    q.appendleft(0)
    assert q.popleft() == 0 and q.pop() == 4
    window = deque(maxlen=2)
    window.extend([1, 2, 3])
    assert list(window) == [2, 3]

    c = Counter("banana")
    assert c["a"] == 3 and c["z"] == 0          # missing key -> 0, no KeyError
    assert c.most_common(1) == [("a", 3)]
    assert Counter("ab") + Counter("b") == Counter({"b": 2, "a": 1})
    assert Counter("abc") == Counter("cab")      # anagram check

    graph: defaultdict[int, list[int]] = defaultdict(list)
    graph[1].append(2)
    assert graph[1] == [2] and graph[99] == []   # note: graph[99] now exists

    # OrderedDict LRU basics: move_to_end on access, popitem(last=False) evicts oldest.
    lru: OrderedDict[str, int] = OrderedDict()
    cap = 2
    for k, v in [("a", 1), ("b", 2)]:
        lru[k] = v
    lru.move_to_end("a")                         # "a" used -> most recent
    lru["c"] = 3
    if len(lru) > cap:
        lru.popitem(last=False)                  # evicts "b"
    assert list(lru) == ["a", "c"]


# --------------------------------------------------------------- bisect
def bisect_demo() -> None:
    a = [1, 2, 2, 2, 5]
    assert bisect.bisect_left(a, 2) == 1         # first index with a[i] >= x
    assert bisect.bisect_right(a, 2) == 4        # first index with a[i] > x
    assert bisect.bisect_right(a, 2) - bisect.bisect_left(a, 2) == 3  # count of 2s
    assert bisect.bisect_left(a, 3) == 4         # insertion point for missing value
    assert bisect.bisect_left(a, 0) == 0 and bisect.bisect_left(a, 9) == 5

    b = [1, 3]
    bisect.insort(b, 2)                          # keep sorted, O(n) insert
    assert b == [1, 2, 3]

    # Python 3.10+: key= works on bisect.
    pairs = [(1, "a"), (4, "b")]
    assert bisect.bisect_left(pairs, 3, key=lambda p: p[0]) == 1


# ------------------------------------------------------------- memoization
@lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)


def fib_memo(n: int, memo: dict[int, int] | None = None) -> int:
    if memo is None:
        memo = {}
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def memo_demo() -> None:
    assert fib_cached(50) == 12586269025
    assert fib_memo(50) == 12586269025
    fib_cached.cache_clear()                     # reset between test cases
    # lru_cache args must be hashable: pass tuples, not lists.


# ------------------------------------------------------------ itertools
def itertools_demo() -> None:
    assert list(accumulate([1, 2, 3])) == [1, 3, 6]
    assert list(accumulate([1, 2, 3], initial=0)) == [0, 1, 3, 6]   # prefix sums
    assert list(accumulate([3, 1, 4], max)) == [3, 3, 4]            # running max
    assert list(combinations([1, 2, 3], 2)) == [(1, 2), (1, 3), (2, 3)]
    assert len(list(permutations([1, 2, 3]))) == 6
    assert list(product([0, 1], repeat=2)) == [(0, 0), (0, 1), (1, 0), (1, 1)]


# -------------------------------------------------------------- sorting
def sorting_demo() -> None:
    a = [3, 1, 2]
    b = sorted(a)                                # new list, a unchanged
    assert a == [3, 1, 2] and b == [1, 2, 3]
    a.sort(reverse=True)                         # in place, returns None
    assert a == [3, 2, 1]

    words = ["bb", "a", "ccc", "dd"]
    assert sorted(words, key=len) == ["a", "bb", "dd", "ccc"]   # stable: bb before dd

    people = [("bob", 25), ("amy", 30), ("cat", 25)]
    # Multi-key: age desc, then name asc. Negate numeric keys for mixed order.
    assert sorted(people, key=lambda p: (-p[1], p[0])) == [
        ("amy", 30), ("bob", 25), ("cat", 25)
    ]


# --------------------------------------------------------------- grid
DIRS4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIRS8 = DIRS4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def neighbors(r: int, c: int, rows: int, cols: int) -> list[tuple[int, int]]:
    out = []
    for dr, dc in DIRS4:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            out.append((nr, nc))
    return out


def grid_demo() -> None:
    assert sorted(neighbors(0, 0, 3, 3)) == [(0, 1), (1, 0)]
    assert len(neighbors(1, 1, 3, 3)) == 4
    assert len(DIRS8) == 8


# --------------------------------------------------------------- misc
def misc_demo() -> None:
    inf = float("inf")
    assert 10**18 < inf and -inf < -(10**18)

    assert 7 // 2 == 3 and 7 / 2 == 3.5
    assert -7 // 2 == -4                         # floors toward -inf, not toward 0
    assert int(-7 / 2) == -3                     # truncate toward 0 (C/Java style)
    assert -7 % 3 == 2                           # result has sign of divisor
    assert (-1) % 5 == 4                         # handy for circular indexes

    s = "hello"
    assert s[::-1] == "olleh" and s[1:3] == "el" and s[-1] == "o"
    assert "-".join(["a", "b"]) == "a-b"
    assert "".join(reversed(s)) == "olleh"
    # Strings are immutable: build with a list then join, not += in a loop.

    assert list(zip([1, 2, 3], "ab")) == [(1, "a"), (2, "b")]   # stops at shortest
    assert [i for i, ch in enumerate("abc", start=1) if ch == "b"] == [2]

    x, y = {1, 2, 3}, {2, 3, 4}
    assert x & y == {2, 3} and x | y == {1, 2, 3, 4}
    assert x - y == {1} and x ^ y == {1, 4}

    sys.setrecursionlimit(10**6)                 # default ~1000; deep DFS needs this
    assert ord("c") - ord("a") == 2 and chr(ord("a") + 1) == "b"
    assert divmod(17, 5) == (3, 2)


# -------------------------------------------------------------- traps
def append_bad(x: int, acc: list[int] = []) -> list[int]:  # noqa: B006 (deliberate bug)
    acc.append(x)
    return acc


def append_good(x: int, acc: list[int] | None = None) -> list[int]:
    if acc is None:
        acc = []
    acc.append(x)
    return acc


def traps_demo() -> None:
    # Mutable default arg is shared across calls.
    append_bad(1)
    assert append_bad(2) == [1, 2]
    append_good(1)
    assert append_good(2) == [2]

    # [[0]*n]*m creates m references to ONE row.
    bad = [[0] * 2] * 2
    bad[0][0] = 1
    assert bad == [[1, 0], [1, 0]]
    good = [[0] * 2 for _ in range(2)]
    good[0][0] = 1
    assert good == [[1, 0], [0, 0]]

    # Shallow copy shares inner lists; deepcopy does not.
    orig = [[1], [2]]
    shallow = orig[:]                            # same as list(orig) / orig.copy()
    deep = copy.deepcopy(orig)
    orig[0].append(9)
    assert shallow[0] == [1, 9] and deep[0] == [1]

    # Backtracking: append path[:] not path, or every result aliases one list.
    res, path = [], []
    for v in [1, 2]:
        path.append(v)
        res.append(path[:])
    assert res == [[1], [1, 2]]


if __name__ == "__main__":
    heapq_demo()
    collections_demo()
    bisect_demo()
    memo_demo()
    itertools_demo()
    sorting_demo()
    grid_demo()
    misc_demo()
    traps_demo()
    print("ok")
