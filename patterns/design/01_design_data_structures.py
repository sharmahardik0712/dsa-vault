"""
PATTERN: Design Data Structures (LRU, LFU, O(1) set, time-based store)
USE WHEN: The problem says "design a class" with required time complexities per operation.
          Combine a hashmap (O(1) lookup) with a second structure that keeps the order you need.
SIGNALS: "design", "implement class", "O(1) get and put", "least recently used",
         "least frequently used", "getRandom", "timestamp", "snapshot"
TIME: O(1) per op (LRU/LFU/RandomizedSet), O(log n) get for TimeMap   SPACE: O(capacity)
PITFALLS: - LRU: on put of an EXISTING key, update and move to front (don't evict).
          - Doubly linked list: sentinel head/tail nodes remove every None check.
          - LFU tie-break is LRU within the same frequency; reset min_freq to 1 on a new insert.
          - RandomizedSet remove: swap with last element and UPDATE the moved element's index.
PROBLEMS: 146 LRU Cache, 460 LFU Cache, 380 Insert Delete GetRandom O(1),
          981 Time Based Key-Value Store, 155 Min Stack
"""
import bisect
import random
from collections import OrderedDict, defaultdict


# ---------- Core template: hashmap + doubly linked list (LRU, LC 146) ----------
class Node:
    def __init__(self, key: int = 0, val: int = 0) -> None:
        self.key = key
        self.val = val
        self.prev: "Node | None" = None
        self.next: "Node | None" = None


class LRUCache:
    # Most recent right after head, least recent right before tail.
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.map: dict[int, Node] = {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node: Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_front(self, node: Node) -> None:
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_front(node)
        return node.val

    def put(self, key: int, val: int) -> None:
        if key in self.map:
            self._remove(self.map[key])
        node = Node(key, val)
        self.map[key] = node
        self._add_front(node)
        if len(self.map) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]


# ---------- Worked problems ----------
class LFUCache:
    # LC 460. freq -> OrderedDict of keys (insertion order = recency within that freq).
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.vals: dict[int, int] = {}
        self.freq: dict[int, int] = {}
        self.buckets: defaultdict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)
        self.min_freq = 0

    def _touch(self, key: int) -> None:
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq += 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key: int, val: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.vals:
            self.vals[key] = val
            self._touch(key)
            return
        if len(self.vals) >= self.capacity:
            evict, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[evict], self.freq[evict]
        self.vals[key] = val
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1


class RandomizedSet:
    # LC 380. List for O(1) random choice, dict value -> index for O(1) remove via swap-with-last.
    def __init__(self) -> None:
        self.items: list[int] = []
        self.index: dict[int, int] = {}

    def insert(self, val: int) -> bool:
        if val in self.index:
            return False
        self.index[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.index:
            return False
        i = self.index.pop(val)
        last = self.items.pop()
        if i < len(self.items):
            self.items[i] = last
            self.index[last] = i
        return True

    def get_random(self) -> int:
        return random.choice(self.items)


class TimeMap:
    # LC 981. Timestamps arrive increasing, so each key's list is sorted: binary search on get.
    def __init__(self) -> None:
        self.times: defaultdict[str, list[int]] = defaultdict(list)
        self.values: defaultdict[str, list[str]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times[key].append(timestamp)
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        i = bisect.bisect_right(self.times[key], timestamp)
        return self.values[key][i - 1] if i else ""


if __name__ == "__main__":
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1
    lru.put(3, 3)                       # evicts 2
    assert lru.get(2) == -1
    lru.put(4, 4)                       # evicts 1
    assert lru.get(1) == -1 and lru.get(3) == 3 and lru.get(4) == 4
    lru.put(3, 30)                      # update existing, no eviction
    assert lru.get(3) == 30 and lru.get(4) == 4
    one = LRUCache(1)
    one.put(1, 1)
    one.put(2, 2)
    assert one.get(1) == -1 and one.get(2) == 2

    lfu = LFUCache(2)
    lfu.put(1, 1)
    lfu.put(2, 2)
    assert lfu.get(1) == 1
    lfu.put(3, 3)                       # evicts 2 (lowest freq)
    assert lfu.get(2) == -1 and lfu.get(3) == 3
    lfu.put(4, 4)                       # 1 and 3 both freq 2 -> evict 1 (least recent)
    assert lfu.get(1) == -1 and lfu.get(3) == 3 and lfu.get(4) == 4
    zero = LFUCache(0)
    zero.put(1, 1)
    assert zero.get(1) == -1

    rs = RandomizedSet()
    assert rs.insert(1) and not rs.remove(2) and rs.insert(2)
    assert rs.get_random() in (1, 2)
    assert rs.remove(1) and not rs.insert(2)
    assert rs.get_random() == 2
    assert rs.remove(2) and rs.items == [] and rs.insert(-5)

    tm = TimeMap()
    tm.set("foo", "bar", 1)
    assert tm.get("foo", 1) == "bar" and tm.get("foo", 3) == "bar"
    tm.set("foo", "bar2", 4)
    assert tm.get("foo", 4) == "bar2" and tm.get("foo", 5) == "bar2"
    assert tm.get("foo", 0) == "" and tm.get("missing", 10) == ""
    print("ok")
