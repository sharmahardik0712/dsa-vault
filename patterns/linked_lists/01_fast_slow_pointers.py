"""
PATTERN: Fast and Slow Pointers (Floyd)
USE WHEN: Linked list (or any "next" function) and you need the middle, a cycle, the cycle start,
          or the kth node from the end, in O(1) space.
SIGNALS: "linked list cycle", "middle of the list", "nth node from end", "happy number",
         "find the duplicate" (array as linked list), "palindrome linked list"
TIME: O(n)   SPACE: O(1)
PITFALLS: - Loop condition `while fast and fast.next` (check both before jumping two).
          - Even length: this middle returns the SECOND middle; start fast at head.next for the first.
          - Cycle start: after meeting, reset ONE pointer to head and move both by 1.
          - Nth from end: start both at a dummy and move fast n + 1 steps so slow stops BEFORE the target.
PROBLEMS: 876 Middle of the Linked List, 141 Linked List Cycle, 142 Linked List Cycle II,
          19 Remove Nth Node From End, 202 Happy Number
"""
from _list_node import ListNode, from_list, to_list


# ---------- Core template ----------
def middle(head: ListNode | None) -> ListNode | None:
    # LC 876. Slow moves 1, fast moves 2.
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


# ---------- Worked problems ----------
def detect_cycle(head: ListNode | None) -> ListNode | None:
    # LC 142. Distance head->start equals distance meet->start (mod cycle length).
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            ptr = head
            while ptr is not slow:
                ptr = ptr.next
                slow = slow.next
            return ptr
    return None


def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    # LC 19. Gap of n between fast and slow; slow stops just before the node to delete.
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next


def is_happy(n: int) -> bool:
    # LC 202. The digit-square sequence either reaches 1 or loops: Floyd on numbers.
    def step(x: int) -> int:
        total = 0
        while x:
            x, d = divmod(x, 10)
            total += d * d
        return total

    slow, fast = n, step(n)
    while fast != 1 and slow != fast:
        slow = step(slow)
        fast = step(step(fast))
    return fast == 1


if __name__ == "__main__":
    assert middle(from_list([1, 2, 3, 4, 5])).val == 3
    assert middle(from_list([1, 2, 3, 4])).val == 3
    assert middle(None) is None and middle(from_list([7])).val == 7

    cyc = from_list([3, 2, 0, -4])
    cyc.next.next.next.next = cyc.next
    assert detect_cycle(cyc).val == 2
    assert detect_cycle(from_list([1, 2])) is None
    assert detect_cycle(None) is None
    one = ListNode(1)
    one.next = one
    assert detect_cycle(one) is one

    assert to_list(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    assert to_list(remove_nth_from_end(from_list([1]), 1)) == []
    assert to_list(remove_nth_from_end(from_list([1, 2]), 2)) == [2]     # head removed

    assert is_happy(19) and is_happy(1)
    assert not is_happy(2) and not is_happy(4)
    print("ok")
