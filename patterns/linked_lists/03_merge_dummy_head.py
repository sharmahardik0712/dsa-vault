"""
PATTERN: Dummy Head + Merge / Build a New List
USE WHEN: You build an output list node by node (merging, partitioning, adding digits, sorting),
          and the head of the result isn't known up front.
SIGNALS: "merge two sorted lists", "sort list", "partition list", "add two numbers",
         "remove elements", "odd even linked list"
TIME: O(n) (O(n log n) for sort list)   SPACE: O(1) extra (O(log n) recursion for sort list)
PITFALLS: - Return `dummy.next`, not `dummy`.
          - Terminate the tail (`tail.next = None`) when reusing nodes, or old links create cycles.
          - Add two numbers: keep looping while `carry` is non-zero, not just while nodes remain.
          - Sort list: split with slow/fast starting at (head, head.next) so 2-node lists split.
PROBLEMS: 21 Merge Two Sorted Lists, 148 Sort List, 86 Partition List, 2 Add Two Numbers,
          328 Odd Even Linked List
"""
from _list_node import ListNode, from_list, to_list


# ---------- Core template ----------
def merge_two(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    # LC 21.
    dummy = ListNode()
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


# ---------- Worked problems ----------
def sort_list(head: ListNode | None) -> ListNode | None:
    # LC 148. Merge sort: split at the middle, sort halves, merge.
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None
    return merge_two(sort_list(head), sort_list(mid))


def partition(head: ListNode | None, x: int) -> ListNode | None:
    # LC 86. Two dummy lists (< x and >= x), then join.
    before, after = ListNode(), ListNode()
    b_tail, a_tail = before, after
    while head:
        if head.val < x:
            b_tail.next = head
            b_tail = head
        else:
            a_tail.next = head
            a_tail = head
        head = head.next
    a_tail.next = None
    b_tail.next = after.next
    return before.next


def add_two_numbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    # LC 2. Digits are stored in reverse, so add from the head with a carry.
    dummy = ListNode()
    tail = dummy
    carry = 0
    while l1 or l2 or carry:
        total = carry + (l1.val if l1 else 0) + (l2.val if l2 else 0)
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next


if __name__ == "__main__":
    assert to_list(merge_two(from_list([1, 2, 4]), from_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
    assert to_list(merge_two(None, from_list([0]))) == [0]
    assert to_list(merge_two(None, None)) == []
    assert to_list(merge_two(from_list([-3, 5]), from_list([-4]))) == [-4, -3, 5]

    assert to_list(sort_list(from_list([4, 2, 1, 3]))) == [1, 2, 3, 4]
    assert to_list(sort_list(from_list([-1, 5, 3, 4, 0]))) == [-1, 0, 3, 4, 5]
    assert to_list(sort_list(None)) == [] and to_list(sort_list(from_list([2, 2]))) == [2, 2]

    assert to_list(partition(from_list([1, 4, 3, 2, 5, 2]), 3)) == [1, 2, 2, 4, 3, 5]
    assert to_list(partition(from_list([2, 1]), 2)) == [1, 2]
    assert to_list(partition(None, 0)) == []

    assert to_list(add_two_numbers(from_list([2, 4, 3]), from_list([5, 6, 4]))) == [7, 0, 8]
    assert to_list(add_two_numbers(from_list([0]), from_list([0]))) == [0]
    assert to_list(add_two_numbers(from_list([9, 9, 9, 9, 9, 9, 9]), from_list([9, 9, 9, 9]))) == \
        [8, 9, 9, 9, 0, 0, 0, 1]
    print("ok")
