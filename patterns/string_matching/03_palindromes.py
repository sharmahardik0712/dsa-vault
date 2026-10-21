"""
PATTERN: Palindromes (expand around center, two-pointer check)
USE WHEN: Find or count palindromic substrings, or check if a string is (almost) a palindrome.
SIGNALS: "longest palindromic substring", "count palindromic substrings", "valid palindrome II"
         (delete at most one char), "palindrome check", "palindromic partitions"
TIME: O(n^2) expand-around-center, O(n) for a two-pointer check   SPACE: O(1)
PITFALLS: - Expand from BOTH odd (i, i) and even (i, i + 1) centers; there are 2n - 1 centers.
          - Return boundaries from expand() as (left + 1, right) after the loop overshoots.
          - Valid palindrome II: on the first mismatch try skipping EITHER side, then stop.
          - Subsequence (not substring) palindromes need DP (see dp/07_interval_dp.py).
PROBLEMS: 5 Longest Palindromic Substring, 647 Palindromic Substrings, 680 Valid Palindrome II,
          125 Valid Palindrome, 131 Palindrome Partitioning
"""


# ---------- Core template ----------
def expand(s: str, left: int, right: int) -> tuple[int, int]:
    """Grow while s[left] == s[right]; returns the palindrome as a half-open (start, end)."""
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return left + 1, right


# ---------- Worked problems ----------
def longest_palindrome(s: str) -> str:
    # LC 5. Try every center, keep the widest.
    best_start, best_end = 0, 0
    for i in range(len(s)):
        for start, end in (expand(s, i, i), expand(s, i, i + 1)):
            if end - start > best_end - best_start:
                best_start, best_end = start, end
    return s[best_start:best_end]


def count_substrings(s: str) -> int:
    # LC 647. Each successful expansion step is one more palindrome.
    count = 0
    for center in range(2 * len(s) - 1):
        left = center // 2
        right = left + center % 2
        while left >= 0 and right < len(s) and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    return count


def valid_palindrome_ii(s: str) -> bool:
    # LC 680. At the first mismatch, the rest must be a palindrome after skipping one side.
    def is_pal(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_pal(left + 1, right) or is_pal(left, right - 1)
        left += 1
        right -= 1
    return True


if __name__ == "__main__":
    assert expand("abba", 1, 2) == (0, 4) and expand("abc", 1, 1) == (1, 2)

    assert longest_palindrome("babad") in ("bab", "aba")
    assert longest_palindrome("cbbd") == "bb"
    assert longest_palindrome("a") == "a" and longest_palindrome("") == ""

    assert count_substrings("abc") == 3
    assert count_substrings("aaa") == 6
    assert count_substrings("") == 0

    assert valid_palindrome_ii("aba")
    assert valid_palindrome_ii("abca")
    assert not valid_palindrome_ii("abc")
    assert valid_palindrome_ii("") and valid_palindrome_ii("deeee")
    print("ok")
