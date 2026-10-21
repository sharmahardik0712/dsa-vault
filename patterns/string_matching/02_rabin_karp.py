"""
PATTERN: Rabin-Karp Rolling Hash
USE WHEN: You compare MANY substrings of the same length (find repeats, search multiple windows),
          often combined with binary search on the length.
SIGNALS: "repeated DNA sequences", "longest duplicate substring", "longest repeating substring",
         "distinct substrings", "find all occurrences", "substring equality in O(1)"
TIME: O(n + m) expected per pass (O(n log n) with binary search on length)   SPACE: O(n)
PITFALLS: - On a hash match, VERIFY the actual substring (collisions happen).
          - Remove the leading char with base^(m-1) mod p, and keep every step mod a large prime.
          - Python's % is non-negative, so (h - x) % mod is safe (not true in Java/C++).
          - Small alphabets (DNA) can use an exact bit encoding instead of a modded hash.
PROBLEMS: 187 Repeated DNA Sequences, 1044 Longest Duplicate Substring, 28 strStr (alt solution),
          1062 Longest Repeating Substring
"""

BASE = 256
MOD = 1_000_000_007


# ---------- Core template ----------
def rabin_karp(text: str, pattern: str) -> list[int]:
    """All start indexes where pattern occurs."""
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
    high = pow(BASE, m - 1, MOD)
    p_hash = t_hash = 0
    for i in range(m):
        p_hash = (p_hash * BASE + ord(pattern[i])) % MOD
        t_hash = (t_hash * BASE + ord(text[i])) % MOD
    res: list[int] = []
    for i in range(n - m + 1):
        if p_hash == t_hash and text[i:i + m] == pattern:
            res.append(i)
        if i + m < n:
            t_hash = ((t_hash - ord(text[i]) * high) * BASE + ord(text[i + m])) % MOD
    return res


# ---------- Worked problems ----------
def find_repeated_dna(s: str) -> list[str]:
    # LC 187. 2 bits per base, a 10-letter window fits in 20 bits exactly (no collisions).
    code = {"A": 0, "C": 1, "G": 2, "T": 3}
    if len(s) < 10:
        return []
    mask = (1 << 20) - 1
    h = 0
    seen: set[int] = set()
    found: list[str] = []
    added: set[int] = set()
    for i, ch in enumerate(s):
        h = ((h << 2) | code[ch]) & mask
        if i >= 9:
            if h in seen and h not in added:
                found.append(s[i - 9:i + 1])
                added.add(h)
            seen.add(h)
    return found


def longest_dup_substring(s: str) -> str:
    # LC 1044. Binary search the length; check each length with a rolling hash.
    def find_dup(length: int) -> int:
        high = pow(BASE, length - 1, MOD)
        h = 0
        for i in range(length):
            h = (h * BASE + ord(s[i])) % MOD
        seen = {h: [0]}
        for i in range(1, len(s) - length + 1):
            h = ((h - ord(s[i - 1]) * high) * BASE + ord(s[i + length - 1])) % MOD
            for j in seen.get(h, []):
                if s[j:j + length] == s[i:i + length]:
                    return i
            seen.setdefault(h, []).append(i)
        return -1

    lo, hi = 1, len(s) - 1
    best = ""
    while lo <= hi:
        mid = (lo + hi) // 2
        start = find_dup(mid)
        if start != -1:
            best = s[start:start + mid]
            lo = mid + 1
        else:
            hi = mid - 1
    return best


if __name__ == "__main__":
    assert rabin_karp("abababa", "aba") == [0, 2, 4]
    assert rabin_karp("abc", "d") == [] and rabin_karp("a", "ab") == []
    assert rabin_karp("aaaa", "aa") == [0, 1, 2]
    assert rabin_karp("abc", "") == []

    assert sorted(find_repeated_dna("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")) == ["AAAAACCCCC", "CCCCCAAAAA"]
    assert find_repeated_dna("AAAAAAAAAAAAA") == ["AAAAAAAAAA"]
    assert find_repeated_dna("ACGT") == []

    assert longest_dup_substring("banana") == "ana"
    assert longest_dup_substring("abcd") == ""
    assert longest_dup_substring("aa") == "a"
    assert longest_dup_substring("a") == ""
    print("ok")
