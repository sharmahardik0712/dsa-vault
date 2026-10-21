"""
PATTERN: KMP (prefix function / LPS array)
USE WHEN: Substring search must be O(n + m), or the problem is about a string's borders
          (prefixes that are also suffixes): repetition, shortest palindrome by prepending.
SIGNALS: "find the index of the first occurrence", "strStr", "repeated substring pattern",
         "shortest palindrome", "longest happy prefix", "prefix that is also a suffix"
TIME: O(n + m)   SPACE: O(m)
PITFALLS: - On mismatch fall back with `length = lps[length - 1]` and DON'T advance i.
          - lps[0] is always 0 (a proper prefix can't be the whole string).
          - Shortest palindrome: build lps on s + "#" + reversed(s); the separator stops overlap.
          - Empty pattern matches at index 0.
PROBLEMS: 28 Find the Index of the First Occurrence, 459 Repeated Substring Pattern,
          214 Shortest Palindrome, 1392 Longest Happy Prefix
"""


# ---------- Core template ----------
def build_lps(pattern: str) -> list[int]:
    """lps[i] = length of the longest proper prefix of pattern[:i+1] that is also its suffix."""
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            i += 1
    return lps


def kmp_search(text: str, pattern: str) -> int:
    # LC 28.
    if not pattern:
        return 0
    lps = build_lps(pattern)
    j = 0
    for i, ch in enumerate(text):
        while j and ch != pattern[j]:
            j = lps[j - 1]
        if ch == pattern[j]:
            j += 1
            if j == len(pattern):
                return i - j + 1
    return -1


# ---------- Worked problems ----------
def repeated_substring_pattern(s: str) -> bool:
    # LC 459. s repeats iff its longest border leaves a period that divides n.
    if not s:
        return False
    border = build_lps(s)[-1]
    return border > 0 and len(s) % (len(s) - border) == 0


def shortest_palindrome(s: str) -> str:
    # LC 214. Longest palindromic PREFIX = longest border of s + "#" + reverse(s).
    k = build_lps(s + "#" + s[::-1])[-1]
    return s[k:][::-1] + s


def longest_prefix(s: str) -> str:
    # LC 1392. The answer is exactly the last lps value.
    if not s:
        return ""
    return s[:build_lps(s)[-1]]


if __name__ == "__main__":
    assert build_lps("aabaaab") == [0, 1, 0, 1, 2, 2, 3]
    assert kmp_search("sadbutsad", "sad") == 0
    assert kmp_search("leetcode", "leeto") == -1
    assert kmp_search("aaaab", "aab") == 2
    assert kmp_search("a", "") == 0 and kmp_search("", "a") == -1

    assert repeated_substring_pattern("abab")
    assert not repeated_substring_pattern("aba")
    assert repeated_substring_pattern("abcabcabcabc")
    assert not repeated_substring_pattern("a") and not repeated_substring_pattern("")

    assert shortest_palindrome("aacecaaa") == "aaacecaaa"
    assert shortest_palindrome("abcd") == "dcbabcd"
    assert shortest_palindrome("") == "" and shortest_palindrome("aba") == "aba"

    assert longest_prefix("level") == "l"
    assert longest_prefix("ababab") == "abab"
    assert longest_prefix("a") == ""
    print("ok")
