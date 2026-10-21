"""
PATTERN: Tree Traversals (iterative DFS orders and BFS level order)
USE WHEN: You need nodes in a specific order: inorder (sorted for BST), preorder (copy/serialize),
          postorder (children before parent), or level by level (BFS).
SIGNALS: "inorder/preorder/postorder traversal", "level order", "zigzag", "right side view",
         "average of levels", "serialize", "iterative" (no recursion allowed)
TIME: O(n)   SPACE: O(h) for DFS stack, O(w) for BFS queue (w = max width)
PITFALLS: - Iterative preorder: push RIGHT before LEFT so left is popped first.
          - Iterative postorder trick: do root-right-left preorder, then reverse.
          - BFS levels: snapshot `len(queue)` before the inner loop.
          - Recursive versions can hit Python's recursion limit on skewed trees (~1000 deep).
PROBLEMS: 94 Inorder Traversal, 144 Preorder Traversal, 145 Postorder Traversal,
          102 Level Order Traversal, 199 Right Side View, 103 Zigzag Level Order
"""
from collections import deque

from _tree import TreeNode, build


# ---------- Core templates ----------
def inorder(root: TreeNode | None) -> list[int]:
    # LC 94. Go left as far as possible, visit, then go right.
    res: list[int] = []
    stack: list[TreeNode] = []
    node = root
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        res.append(node.val)
        node = node.right
    return res


def preorder(root: TreeNode | None) -> list[int]:
    # LC 144.
    res: list[int] = []
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return res


def postorder(root: TreeNode | None) -> list[int]:
    # LC 145. Root-right-left preorder, reversed = left-right-root.
    res: list[int] = []
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return res[::-1]


def level_order(root: TreeNode | None) -> list[list[int]]:
    # LC 102.
    if not root:
        return []
    res: list[list[int]] = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(level)
    return res


# ---------- Worked problems ----------
def right_side_view(root: TreeNode | None) -> list[int]:
    # LC 199. Last node of each BFS level.
    return [level[-1] for level in level_order(root)]


def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    # LC 103. Plain level order, reverse every other level.
    levels = level_order(root)
    return [lvl if i % 2 == 0 else lvl[::-1] for i, lvl in enumerate(levels)]


if __name__ == "__main__":
    t = build([1, 2, 3, 4, 5, None, 6])
    assert inorder(t) == [4, 2, 5, 1, 3, 6]
    assert preorder(t) == [1, 2, 4, 5, 3, 6]
    assert postorder(t) == [4, 5, 2, 6, 3, 1]
    assert level_order(t) == [[1], [2, 3], [4, 5, 6]]
    assert inorder(None) == preorder(None) == postorder(None) == level_order(None) == []
    assert inorder(build([1])) == [1]

    assert right_side_view(build([1, 2, 3, None, 5, None, 4])) == [1, 3, 4]
    assert right_side_view(build([1, 2])) == [1, 2]
    assert right_side_view(None) == []

    assert zigzag_level_order(build([3, 9, 20, None, None, 15, 7])) == [[3], [20, 9], [15, 7]]
    assert zigzag_level_order(build([-1])) == [[-1]]
    print("ok")
