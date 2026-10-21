"""
PATTERN: Number Theory (primes, gcd, fast power, nCr mod p)
USE WHEN: The problem involves primes, divisibility, huge powers, or counting answers
          "modulo 10^9 + 7" (combinatorics).
SIGNALS: "count primes", "pow(x, n)", "modulo 1e9+7", "gcd", "lcm", "number of ways" (huge),
         "unique paths" (closed form), "super pow", "simplify fraction"
TIME: sieve O(n log log n); fast pow O(log n); nCr O(1) after O(n) precompute   SPACE: O(n)
PITFALLS: - pow(x, n) with negative n: invert x and negate n.
          - Python ints don't overflow, but still apply % MOD after each multiply (speed, and expected).
          - Modular inverse needs a prime MOD: pow(a, MOD - 2, MOD), or pow(a, -1, MOD) in 3.8+.
          - Sieve: start crossing out at i * i, and only loop i up to sqrt(n).
PROBLEMS: 204 Count Primes, 50 Pow(x, n), 1979 Find GCD of Array, 62 Unique Paths (as nCr),
          372 Super Pow
"""
import math

MOD = 1_000_000_007


# ---------- Core templates ----------
def sieve(n: int) -> list[bool]:
    """is_prime[i] for 0 <= i < n."""
    is_prime = [True] * max(n, 2)
    is_prime[0] = is_prime[1] = False
    i = 2
    while i * i < n:
        if is_prime[i]:
            for j in range(i * i, n, i):
                is_prime[j] = False
        i += 1
    return is_prime[:n]


def fast_pow(x: float, n: int) -> float:
    # LC 50. Square the base, halve the exponent.
    if n < 0:
        x, n = 1 / x, -n
    result = 1.0
    while n:
        if n & 1:
            result *= x
        x *= x
        n >>= 1
    return result


def gcd(a: int, b: int) -> int:
    # Euclid. Same as math.gcd; lcm(a, b) = a // gcd(a, b) * b.
    while b:
        a, b = b, a % b
    return abs(a)


class Combinatorics:
    """nCr mod p with precomputed factorials and Fermat inverses."""

    def __init__(self, n: int) -> None:
        self.fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % MOD
        self.inv = [1] * (n + 1)
        self.inv[n] = pow(self.fact[n], MOD - 2, MOD)
        for i in range(n, 0, -1):
            self.inv[i - 1] = self.inv[i] * i % MOD

    def ncr(self, n: int, r: int) -> int:
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv[r] % MOD * self.inv[n - r] % MOD


# ---------- Worked problems ----------
def count_primes(n: int) -> int:
    # LC 204. Primes strictly less than n.
    return sum(sieve(n))


def find_gcd(nums: list[int]) -> int:
    # LC 1979. gcd of the smallest and largest.
    return gcd(min(nums), max(nums))


def unique_paths(m: int, n: int) -> int:
    # LC 62. Choose which (m - 1) of the (m + n - 2) moves go down.
    return Combinatorics(m + n).ncr(m + n - 2, m - 1)


if __name__ == "__main__":
    assert [i for i, p in enumerate(sieve(20)) if p] == [2, 3, 5, 7, 11, 13, 17, 19]
    assert sieve(0) == [] and sieve(2) == [False, False]

    assert fast_pow(2.0, 10) == 1024.0
    assert abs(fast_pow(2.1, 3) - 9.261) < 1e-9
    assert fast_pow(2.0, -2) == 0.25
    assert fast_pow(5.0, 0) == 1.0 and fast_pow(-2.0, 3) == -8.0
    assert pow(3, 200, MOD) == pow(3, 200) % MOD               # built-in modular pow

    assert gcd(12, 18) == 6 and gcd(7, 0) == 7 and gcd(-4, 6) == 2
    assert 4 // gcd(4, 6) * 6 == 12

    comb = Combinatorics(1000)
    assert comb.ncr(5, 2) == 10 and comb.ncr(10, 3) == 120
    assert comb.ncr(5, 0) == 1 and comb.ncr(3, 5) == 0
    assert comb.ncr(1000, 500) == math.comb(1000, 500) % MOD

    assert count_primes(10) == 4
    assert count_primes(0) == 0 and count_primes(2) == 0 and count_primes(3) == 1

    assert find_gcd([2, 5, 6, 9, 10]) == 2
    assert find_gcd([7, 5, 6, 8, 3]) == 1 and find_gcd([3, 3]) == 3

    assert unique_paths(3, 7) == 28 and unique_paths(3, 2) == 3 and unique_paths(1, 1) == 1
    print("ok")
