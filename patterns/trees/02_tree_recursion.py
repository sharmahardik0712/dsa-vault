"""
PATTERN: Tree Recursion (bottom-up return values, global best)
USE WHEN: The answer for a node depends on answers from its subtrees. Decide what each call
          RETURNS to its parent, and separately what it records in a global best.
SIGNALS: "maximum depth", "diameter", "balanced", "lowest common ancestor", "maximum path sum",
         "path sum", "invert", "same tree", "subtree"
TIME: O(n)   SPACE: O(h) recursion stack
PITFALLS: - The return value (e.g. height, best single branch) is often NOT the answer (e.g. diameter).
          - Max path sum: clip negative child gains to 0; return only ONE branch upward.
          - Always handle the None base case first.
          - LCA assumes both nodes exist; if not guaranteed, count matches explicitly.
PROBLEMS: 104 Maximum Depth, 543 Diameter of Binary Tree, 236 LCA of a Binary Tree,
          124 Binary Tree Maximum Path Sum, 110 Balanced Binary Tree
"""
from _tree import TreeNode, build


# ---------- Core template ----------
def max_depth(root: TreeNode | None) -> int:
    # LC 104. Combine children's results, add this node.
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


# ---------- Worked problems ----------
def diameter(root: TreeNode | None) -> int:
    # LC 543. Return height to the parent; update the global best with left + right.
    best = 0

    def height(node: TreeNode | None) -> int:
        nonlocal best
        if not node:
            return 0
        left, right = height(node.left), height(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    height(root)
    return best


def lca(root: TreeNode | None, p: int, q: int) -> TreeNode | None:
    # LC 236. If p and q come back from different subtrees, this node is the LCA.
    if not root or root.val == p or root.val == q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root
    return left or right


def max_path_sum(root: TreeNode | None) -> int:
    # LC 124. Path through node = val + both gains; return val + the better single gain.
    best = float("-inf")

    def gain(node: TreeNode | None) -> int:
        nonlocal best
        if not node:
            return 0
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)
        return node.val + max(left, right)

    gain(root)
    return int(best)


def is_balanced(root: TreeNode | None) -> bool:
    # LC 110. Return -1 as a "not balanced" signal so the check stays O(n).
    def height(node: TreeNode | None) -> int:
        if not node:
            return 0
        left, right = height(node.left), height(node.right)
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return height(root) != -1


if __name__ == "__main__":
    assert max_depth(build([3, 9, 20, None, None, 15, 7])) == 3
    assert max_depth(None) == 0 and max_depth(build([1, None, 2])) == 2

    assert diameter(build([1, 2, 3, 4, 5])) == 3
    assert diameter(build([1])) == 0 and diameter(None) == 0

    tree = build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    assert lca(tree, 5, 1).val == 3
    assert lca(tree, 5, 4).val == 5
    assert lca(build([1, 2]), 1, 2).val == 1

    assert max_path_sum(build([1, 2, 3])) == 6
    assert max_path_sum(build([-10, 9, 20, None, None, 15, 7])) == 42
    assert max_path_sum(build([-3])) == -3
    assert max_path_sum(build([2, -1])) == 2

    assert is_balanced(build([3, 9, 20, None, None, 15, 7]))
    assert not is_balanced(build([1, 2, 2, 3, 3, None, None, 4, 4]))
    assert is_balanced(None)
    print("ok")
