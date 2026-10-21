"""
PATTERN: Hashmap / Hashset Lookup
USE WHEN: You need O(1) "have I seen X?" or "what is stored for X?", turning an O(n^2) pair search
          into one pass, or grouping items by a canonical key.
SIGNALS: "two sum", "pair with", "complement", "group anagrams", "frequency", "first unique",
         "longest consecutive sequence", "isomorphic", O(n) required on unsorted input
TIME: O(n) average   SPACE: O(n)
PITFALLS: - Check for the complement BEFORE inserting the current item (avoids using it twice).
          - Lists are unhashable as keys: use tuple(...) or a sorted string.
          - defaultdict creates keys on read: use `in` to test membership without inserting.
          - Longest consecutive: only start counting at x where x - 1 is NOT in the set (keeps it O(n)).
PROBLEMS: 1 Two Sum, 49 Group Anagrams, 128 Longest Consecutive Sequence, 387 First Unique Character,
          205 Isomorphic Strings
"""
from collections import defaultdict


# ---------- Core template: one-pass complement lookup ----------
def two_sum(nums: list[int], target: int) -> list[int]:
    # LC 1.
    index_of: dict[int, int] = {}
    for i, x in enumerate(nums):
        if target - x in index_of:
            return [index_of[target - x], i]
        index_of[x] = i
    return []


# ---------- Worked problems ----------
def group_anagrams(words: list[str]) -> list[list[str]]:
    # LC 49. Sorted word (or 26-count tuple) is the canonical key.
    groups: dict[str, list[str]] = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())


def longest_consecutive(nums: list[int]) -> int:
    # LC 128. Only walk forward from sequence starts, so each number is visited at most twice.
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 not in values:
            length = 1
            while x + length in values:
                length += 1
            best = max(best, length)
    return best


def is_isomorphic(s: str, t: str) -> bool:
    # LC 205. Mapping must be one-to-one in BOTH directions.
    s_to_t: dict[str, str] = {}
    t_to_s: dict[str, str] = {}
    for a, b in zip(s, t):
        if s_to_t.get(a, b) != b or t_to_s.get(b, a) != a:
            return False
        s_to_t[a] = b
        t_to_s[b] = a
    return len(s) == len(t)


if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 3], 6) == [0, 1]
    assert two_sum([-3, 4, 3, 90], 0) == [0, 2]
    assert two_sum([1], 2) == []

    groups = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert sorted(sorted(g) for g in groups) == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
    assert group_anagrams([""]) == [[""]]
    assert group_anagrams([]) == []

    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0
    assert longest_consecutive([-1, -2, 5]) == 2

    assert is_isomorphic("egg", "add")
    assert not is_isomorphic("foo", "bar")
    assert not is_isomorphic("badc", "baba")     # b->b and d->b: reverse map catches it
    assert is_isomorphic("", "")
    print("ok")
