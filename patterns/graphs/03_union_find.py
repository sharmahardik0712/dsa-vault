"""
PATTERN: Union-Find (Disjoint Set Union)
USE WHEN: You need to dynamically group items into connected sets and answer "are a and b
          connected?" or "how many groups?" as edges arrive. Also cycle detection in undirected graphs.
SIGNALS: "connected components", "number of provinces", "redundant connection", "accounts merge",
         "union", "group", "equivalence", "Kruskal / minimum spanning tree"
TIME: ~O(alpha(n)) per op with path compression + union by rank (effectively O(1))   SPACE: O(n)
PITFALLS: - Comparing parent[a] == parent[b] instead of find(a) == find(b).
          - Forgetting path compression (degrades to O(n) chains).
          - Decrementing the component count when a and b were already in the same set.
          - Mapping non-integer keys (emails, strings) to ids first, or use a dict-based parent.
PROBLEMS: 547 Number of Provinces, 684 Redundant Connection, 721 Accounts Merge,
          323 Number of Connected Components, 1584 Min Cost to Connect All Points
"""


# ---------- Core template ----------
class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path halving
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        """Returns False if a and b were already connected."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1
        return True


# ---------- Worked problems ----------
def find_circle_num(is_connected: list[list[int]]) -> int:
    # LC 547. Union every connected pair; remaining set count is the answer.
    n = len(is_connected)
    dsu = DSU(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                dsu.union(i, j)
    return dsu.count


def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    # LC 684. The first edge whose endpoints are already connected closes a cycle.
    dsu = DSU(len(edges) + 1)
    for a, b in edges:
        if not dsu.union(a, b):
            return [a, b]
    return []


def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    # LC 721. Union all emails within an account (map email -> id); group by root.
    email_id: dict[str, int] = {}
    email_name: dict[str, str] = {}
    for acc in accounts:
        for email in acc[1:]:
            if email not in email_id:
                email_id[email] = len(email_id)
            email_name[email] = acc[0]
    dsu = DSU(len(email_id))
    for acc in accounts:
        for email in acc[2:]:
            dsu.union(email_id[acc[1]], email_id[email])
    groups: dict[int, list[str]] = {}
    for email, i in email_id.items():
        groups.setdefault(dsu.find(i), []).append(email)
    return [[email_name[emails[0]]] + sorted(emails) for emails in groups.values()]


if __name__ == "__main__":
    d = DSU(5)
    assert d.union(0, 1) and d.union(1, 2)
    assert not d.union(0, 2)
    assert d.find(0) == d.find(2) and d.find(3) != d.find(0)
    assert d.count == 3

    assert find_circle_num([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert find_circle_num([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
    assert find_circle_num([[1]]) == 1
    assert find_circle_num([]) == 0

    assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
    assert find_redundant_connection([]) == []

    merged = accounts_merge([
        ["John", "a@x", "b@x"],
        ["John", "c@x"],
        ["John", "b@x", "d@x"],
        ["Mary", "m@x"],
    ])
    assert sorted(merged) == [["John", "a@x", "b@x", "d@x"], ["John", "c@x"], ["Mary", "m@x"]]
    assert accounts_merge([]) == []
    print("ok")
