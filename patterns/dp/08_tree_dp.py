"""
PATTERN: Tree DP
USE WHEN: An optimisation over a tree where each node's choice (take / skip, camera / covered /
          not covered) constrains its children: return a small TUPLE of options per node.
SIGNALS: "house robber III", "binary tree cameras", "maximum independent set on a tree",
         "minimum vertex cover", "choose nodes with no two adjacent", "distribute coins"
TIME: O(n)   SPACE: O(h) recursion
PITFALLS: - Return all options from the child; let the parent choose. Don't decide greedily at the child.
          - None children need a neutral value (e.g. (0, 0), or "covered" for cameras).
          - Cameras: the root may end up uncovered; check it after the DFS.
          - Unlike tree recursion, the answer is usually max/min of the ROOT's tuple.
PROBLEMS: 337 House Robber III, 968 Binary Tree Cameras, 979 Distribute Coins in Binary Tree,
          2246 Longest Path With Different Adjacent Characters
"""


class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


# ---------- Core template ----------
def rob_tree(root: TreeNode | None) -> int:
    # LC 337. Each node returns (best if robbed, best if skipped).
    def dfs(node: TreeNode | None) -> tuple[int, int]:
        if not node:
            return 0, 0
        left_rob, left_skip = dfs(node.left)
        right_rob, right_skip = dfs(node.right)
        rob = node.val + left_skip + right_skip
        skip = max(left_rob, left_skip) + max(right_rob, right_skip)
        return rob, skip

    return max(dfs(root))


# ---------- Worked problems ----------
def min_camera_cover(root: TreeNode | None) -> int:
    # LC 968. States: 0 = not covered, 1 = has camera, 2 = covered. Place cameras at parents of leaves.
    cameras = 0

    def dfs(node: TreeNode | None) -> int:
        nonlocal cameras
        if not node:
            return 2
        left, right = dfs(node.left), dfs(node.right)
        if left == 0 or right == 0:
            cameras += 1
            return 1
        if left == 1 or right == 1:
            return 2
        return 0

    if root and dfs(root) == 0:
        cameras += 1
    return cameras


def distribute_coins(root: TreeNode | None) -> int:
    # LC 979. Each subtree returns its excess (coins - nodes); every unit of excess crosses one edge.
    moves = 0

    def excess(node: TreeNode | None) -> int:
        nonlocal moves
        if not node:
            return 0
        left, right = excess(node.left), excess(node.right)
        moves += abs(left) + abs(right)
        return node.val + left + right - 1

    excess(root)
    return moves


if __name__ == "__main__":
    t1 = TreeNode(3, TreeNode(2, None, TreeNode(3)), TreeNode(3, None, TreeNode(1)))
    assert rob_tree(t1) == 7
    t2 = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(3)), TreeNode(5, None, TreeNode(1)))
    assert rob_tree(t2) == 9
    assert rob_tree(None) == 0

    assert min_camera_cover(TreeNode(0, TreeNode(0, TreeNode(0), TreeNode(0)))) == 1
    chain = TreeNode(0, TreeNode(0, TreeNode(0, TreeNode(0, None, TreeNode(0)))))
    assert min_camera_cover(chain) == 2
    assert min_camera_cover(TreeNode(0)) == 1 and min_camera_cover(None) == 0

    assert distribute_coins(TreeNode(3, TreeNode(0), TreeNode(0))) == 2
    assert distribute_coins(TreeNode(0, TreeNode(3), TreeNode(0))) == 3
    assert distribute_coins(TreeNode(1)) == 0
    print("ok")
