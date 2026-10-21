"""
PATTERN: Binary Search Tree Operations
USE WHEN: The tree is a BST (left < node < right), so you can discard half the tree at each step
          and inorder traversal gives sorted order.
SIGNALS: "BST", "validate BST", "kth smallest", "insert into BST", "search in BST",
         "LCA of a BST", "closest value", "inorder successor", "sorted array to BST"
TIME: O(h) for search/insert/LCA, O(h + k) for kth smallest   SPACE: O(h)
PITFALLS: - Validating by checking only direct children is wrong: pass (low, high) bounds down.
          - Duplicates: decide the rule (usually invalid / go right) and state it.
          - h is O(log n) only if balanced; worst case O(n).
          - Use the BST property before reaching for a generic tree algorithm.
PROBLEMS: 98 Validate BST, 701 Insert into a BST, 230 Kth Smallest Element in a BST,
          235 LCA of a BST, 108 Convert Sorted Array to BST
"""
from _tree import TreeNode, build


# ---------- Core template: walk down by comparison ----------
def bst_insert(root: TreeNode | None, val: int) -> TreeNode:
    # LC 701.
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = bst_insert(root.left, val)
    else:
        root.right = bst_insert(root.right, val)
    return root


def inorder(root: TreeNode | None) -> list[int]:
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)


# ---------- Worked problems ----------
def is_valid_bst(root: TreeNode | None) -> bool:
    # LC 98. Every node must lie inside the open interval inherited from its ancestors.
    def check(node: TreeNode | None, low: float, high: float) -> bool:
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return check(node.left, low, node.val) and check(node.right, node.val, high)

    return check(root, float("-inf"), float("inf"))


def kth_smallest(root: TreeNode | None, k: int) -> int:
    # LC 230. Iterative inorder; stop at the kth visit.
    stack: list[TreeNode] = []
    node = root
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
    return -1


def lca_bst(root: TreeNode | None, p: int, q: int) -> TreeNode | None:
    # LC 235. The LCA is the first node where p and q split to different sides.
    while root:
        if p < root.val and q < root.val:
            root = root.left
        elif p > root.val and q > root.val:
            root = root.right
        else:
            return root
    return None


def sorted_array_to_bst(nums: list[int]) -> TreeNode | None:
    # LC 108. Middle element as root keeps the tree height-balanced.
    if not nums:
        return None
    mid = len(nums) // 2
    return TreeNode(nums[mid], sorted_array_to_bst(nums[:mid]), sorted_array_to_bst(nums[mid + 1:]))


if __name__ == "__main__":
    root = None
    for v in [5, 3, 8, 1, 4]:
        root = bst_insert(root, v)
    assert inorder(root) == [1, 3, 4, 5, 8]

    assert is_valid_bst(build([2, 1, 3]))
    assert not is_valid_bst(build([5, 1, 4, None, None, 3, 6]))
    assert not is_valid_bst(build([5, 4, 6, None, None, 3, 7]))   # 3 is in right subtree of 5
    assert not is_valid_bst(build([1, 1]))
    assert is_valid_bst(None) and is_valid_bst(build([0, -1]))

    assert kth_smallest(root, 1) == 1 and kth_smallest(root, 4) == 5
    assert kth_smallest(build([1]), 1) == 1

    bst = build([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    assert lca_bst(bst, 2, 8).val == 6
    assert lca_bst(bst, 2, 4).val == 2
    assert lca_bst(bst, 3, 5).val == 4

    balanced = sorted_array_to_bst([-10, -3, 0, 5, 9])
    assert inorder(balanced) == [-10, -3, 0, 5, 9] and is_valid_bst(balanced)
    assert sorted_array_to_bst([]) is None
    print("ok")
