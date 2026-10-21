"""
PATTERN: In-place Linked List Reversal
USE WHEN: You must reverse a whole list, a sub-range, or groups of k nodes, or compare/weave the
          two halves of a list, without extra space.
SIGNALS: "reverse linked list", "reverse between left and right", "reverse nodes in k-group",
         "reorder list", "palindrome linked list", "swap nodes in pairs"
TIME: O(n)   SPACE: O(1)
PITFALLS: - Save `nxt = cur.next` BEFORE rewiring, or you lose the rest of the list.
          - Use a dummy head when the head itself may change.
          - k-group: check that k nodes exist BEFORE reversing (leftover group stays as is).
          - Cut the list (`slow.next = None`) before reversing the second half, or you create a cycle.
PROBLEMS: 206 Reverse Linked List, 92 Reverse Linked List II, 25 Reverse Nodes in k-Group,
          143 Reorder List, 234 Palindrome Linked List
"""
from _list_node import ListNode, from_list, to_list


# ---------- Core template ----------
def reverse(head: ListNode | None) -> ListNode | None:
    # LC 206.
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


# ---------- Worked problems ----------
def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    # LC 92. Walk to the node before `left`, then repeatedly move the next node to the front.
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next
    cur = prev.next
    for _ in range(right - left):
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = prev.next
        prev.next = nxt
    return dummy.next


def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    # LC 25. Find the kth node; reverse the group onto group_next; reconnect; advance.
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next
        group_next = kth.next
        prev, cur = group_next, group_prev.next
        while cur is not group_next:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        first = group_prev.next
        group_prev.next = kth
        group_prev = first


def reorder_list(head: ListNode | None) -> None:
    # LC 143. Find the middle, reverse the second half, weave the two halves.
    if not head or not head.next:
        return
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    second = reverse(slow.next)
    slow.next = None
    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2


if __name__ == "__main__":
    assert to_list(reverse(from_list([1, 2, 3]))) == [3, 2, 1]
    assert to_list(reverse(None)) == [] and to_list(reverse(from_list([1]))) == [1]

    assert to_list(reverse_between(from_list([1, 2, 3, 4, 5]), 2, 4)) == [1, 4, 3, 2, 5]
    assert to_list(reverse_between(from_list([5]), 1, 1)) == [5]
    assert to_list(reverse_between(from_list([3, 5]), 1, 2)) == [5, 3]

    assert to_list(reverse_k_group(from_list([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
    assert to_list(reverse_k_group(from_list([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]
    assert to_list(reverse_k_group(from_list([1, 2]), 1)) == [1, 2]
    assert to_list(reverse_k_group(None, 2)) == []

    h = from_list([1, 2, 3, 4, 5])
    reorder_list(h)
    assert to_list(h) == [1, 5, 2, 4, 3]
    h = from_list([1, 2, 3, 4])
    reorder_list(h)
    assert to_list(h) == [1, 4, 2, 3]
    reorder_list(None)
    print("ok")
