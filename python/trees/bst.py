from __future__ import annotations
from dataclasses import dataclass
from python.trees.tree_traversal import TraversalCategory

from python.utils.benchmark import benchmark
from tree_traversal import TreeTraversal
from tree_node import BSTNode


@dataclass
class BinarySearchTree(TreeTraversal):
    root:  BSTNode | None = None

    @staticmethod
    def find_max(root: BSTNode) -> BSTNode:
        while root.right:
            root = root.right
        return root

    @staticmethod
    def find_min(root: BSTNode) -> BSTNode:
        while root.left:
            root = root.left
        return root

    def height(self, node: BSTNode | None) -> int:
        """Find the height of the tree by passing root or any other node in the tree."""
        if not node:
            return -1
        return 1 + max(self.height(node.left), self.height(node.right))

    @staticmethod
    def diameter(root: BSTNode | None) -> int:
        """Find the diameter of the tree.

        The max of 3 scenarios:
          1. The left subtree diameter
          2. The right subtree diameter
          3. The diameter of the path through the root
        """

        def calc_max(node):
            if node is None:
                return 0, 0
            l_diameter, l_path = calc_max(node.left)
            r_diameter, r_path = calc_max(node.right)
            diameter = max(l_diameter, r_diameter, l_path + r_path)
            path = 1 + max(l_path, r_path)
            return diameter, path

        return calc_max(root)[0]

    @staticmethod
    def max_width(root: BSTNode | None):
        """Calculate width of a binary tree.

        This approach uses level order traversal and return maximum length of
        levels in a tree.

        :return: width is the maximum number of nodes at any level in a binary tree.
        """

        curr = [root]
        next_level = []
        max_width = len(curr)
        while curr:
            node = curr.pop()
            assert node is not None
            if node.left:
                next_level.append(node.left)
            if node.right:
                next_level.append(node.right)
            if curr is None:
                if len(next_level) > max_width:
                    max_width = len(next_level)
                curr, next_level = next_level, curr
        return max_width

    @staticmethod
    def is_bst(root:BSTNode | None) -> bool:
        """Approach 1: Recursive Traversal with Valid Range

        - DFS recursive, top down (preorder).
        - Time complexity: O(N) since we visit each node exactly once.
        - Space complexity: O(N) since we keep up to the entire tree.
        """

        def validate(node, low=-float('inf'), high=float('inf')):
            if node is None:
                return True
            if node.val <= low or node.val >= high:
                return False
            return (validate(node.left, low, node.val) and
                    validate(node.right, node.val, high))

        return validate(root)

    @staticmethod
    def is_bst_iter(root: BSTNode | None):
        """Approach 2: Iterative Traversal with Valid Range

        - DFS iterative (in-order traversal result in ordered list, top down)
        (preorder).
        - Time complexity: O(N) since we visit each node exactly once.
        - Space complexity: O(N) since we keep up to the entire tree.
        """

        if root is None:
            return True

        stack: list[tuple[BSTNode | None, float, float]] = [(root, -float('inf'), float('inf'))]
        while stack:
            root, lower, upper = stack.pop()
            if root is None:
                continue
            val = root.val
            if val <= lower or val >= upper:
                return False
            # important note - right child is pushed first so that left child is processed first (LIFO order)
            stack.append((root.right, val, upper))
            stack.append((root.left, lower, val))
        return True

    @staticmethod
    def is_bst_iter_inorder(root: BSTNode | None):
        """Approach 4: Iterative Inorder Traversal

        - Time complexity: O(N) since we visit each node exactly once.
        - Space complexity: O(N) to keep stack.
        """

        stack, prev = [], -float('inf')
        while stack or root:
            while root:
                stack.append(root)
                root = root.left
            root = stack.pop()
            assert root is not None
            # If next element in inorder traversal is smaller than the previous one than not a BST.
            if root.val <= prev:
                return False
            prev = root.val
            root = root.right
        return True

    @staticmethod
    def is_bst_r_inorder(root: BSTNode | None) -> bool:
        """Approach 3: Recursive Inorder Traversal

        - Time complexity: O(N) since we visit each node exactly once.
        - Space complexity: O(N) to keep stack
        """

        def inorder(node):
            nonlocal prev
            if not node:
                return True
            if not inorder(node.left):
                return False
            if node.val <= prev:
                return False
            prev = node.val
            return inorder(node.right)

        prev = -float('inf')
        return inorder(root)

    def split_bst(self, root: BSTNode | None, val: int):
        if root is None:
            return [None, None]

        if root.val > val:
            left, right = self.split_bst(root.left, val)
            root.left = right
            return [left, root]
        else:
            left, right = self.split_bst(root.right, val)
            root.right = left
            return [root, right]

    def flatten(self, root: BSTNode | None):
        """Flatten a binary tree to a linked list.

        The head of the output linked list is the root of the tree node,
        followed by a flattened left subtree, which is followed by a flattened
        right subtree.

        Time: O(n), Space: O(1)
        """

        while root:
            if root.left:
                pre = self.find_max(root.left)
                pre.right = root.right
                root.right = root.left
                root.left = None
            root = root.right

    @staticmethod
    def search(root: BSTNode | None, val: int):
        while root is not None and root.val != val:
            root = root.left if val < root.val else root.right
        return root

    def r_search(self, root: BSTNode | None, val: int) -> BSTNode | None:
        if root is None or val == root.val:
            return root
        elif val < root.val:
            return self.r_search(root.left, val)
        else:
            return self.r_search(root.right, val)

    def insert(self, val: int):
        node = BSTNode(val)
        if self.root is None:
            self.root = node
        else:
            curr, parent = self.root, None
            while curr:
                parent = curr
                if val <= curr.val:
                    curr = curr.left
                    if curr is None:
                        parent.left = node
                else:
                    curr = curr.right
                    if curr is None:
                        parent.right = node

    def r_insert(self, root: BSTNode | None, val: int):
        if not root:
            return BSTNode(val)
        if val <= root.val:
            root.left = self.r_insert(root.left, val)
        else:
            root.right = self.r_insert(root.right, val)
        return root

    def inorder_successor(self, root: BSTNode | None, p: BSTNode):
        """Iterative - no stack"""
        if p.right:
            return self.find_min(p.right)
        succ = None
        while root:
            if p.val < root.val:
                succ = root
                root = root.left
            else:
                root = root.right
        return succ

    def inorder_successor2(self, root: BSTNode | None | None, p: BSTNode):
        """Recursive

        Do a binary search down the tree, and if the current node is greater
        than the target, remember the current node. Binary Search will
        eventually converge to the immediate successor.
        """

        if p.right:
            return self.find_min(p.right)

        def inorder(node):
            if node is None:
                return
            if p.val < node.val:
                succ = node
                inorder(node.left)
            else:
                inorder(node.right)
        succ = None
        inorder(root)
        return succ

    def inorder_successor3(self, root: BSTNode | None, p: BSTNode):
        """Iterative: stack"""

        stack, pre_val = [], None

        if p.right:
            return self.find_min(p.right)

        while stack or root:
            while root:
                stack.append(root)
                if root.val <= p.val:
                    break
                root = root.left

            root = stack.pop()
            if pre_val is not None and pre_val == p.val:
                return root
            if root is not None:
                pre_val = root.val
                root = root.right

        return None

    def inorder_predecessor(self, root: BSTNode | None, p: BSTNode):
        if p.left:
            return self.find_max(p.left)
        pre = None
        while root:
            if p.val <= root.val:
                root = root.left
            else:
                pre = root
                root = root.right
        return pre

    def remove(self, root: BSTNode | None, val: int):
        if not root:
            return None

        if root.val == val:
            if not root.right:
                return root.left

            if not root.left:
                return root.right

            root.val = self.find_min(root.right).val
            root.right = self.remove(root.right, root.val)

        elif root.val > val:
            root.left = self.remove(root.left, val)
        else:
            root.right = self.remove(root.right, val)
        return root


if __name__ == '__main__':
    tree = BinarySearchTree()
    tree.insert(5)
    tree.insert(2)
    tree.insert(7)
    tree.insert(9)
    tree.insert(1)
    tree.insert(8)
    tree.insert(3)
    tree.r_insert(tree.root, 13)
    tree.r_insert(tree.root, 6)

    """Creates the tree

         5
       /   \
      2      7
     / \    /  \
    1   3  6    9
              /  \
             8    13
    """

    root_1 = tree.search(tree.root, 1)
    root_2 = tree.search(tree.root, 2)
    root_3 = tree.search(tree.root, 3)
    root_5 = tree.search(tree.root, 5)
    root_9 = tree.search(tree.root, 9)
    root_13 = tree.search(tree.root, 13)
    assert tree.root and root_1 and root_2 and root_3 and root_5 and root_9 and root_13

    assert tree.height(tree.root) == 3
    assert tree.diameter(tree.root) == 5

    assert tree.find_min(tree.root) == root_1
    assert tree.find_max(tree.root) == root_13

    assert root_9.val == 9
    assert root_9.num_children() == 2
    assert tree.height(root_9) == 1
    assert root_9.height() == 1

    assert root_5.val == 5
    assert root_5.num_children() == 2
    assert tree.height(root_5) == 3
    assert root_5.height() == 3

    assert root_2.val == 2
    assert root_2.num_children() == 2
    assert tree.height(root_2) == 1
    assert root_2.height() == 1

    assert tree.traversal(tree.root, TraversalCategory.BFS) == [5, 2, 7, 1, 3, 6, 9, 8, 13] # BFS

    DFS_RESULTS = {
        'inorder': [1, 2, 3, 5, 6, 7, 8, 9, 13],
        'preorder': [5, 2, 1, 3, 7, 6, 9, 8, 13],
        'postorder': [1, 3, 2, 6, 8, 13, 9, 7, 5]
    }

    for traversal, res in DFS_RESULTS.items():
        assert tree.traversal(tree.root, TraversalCategory.DFS, traversal, 'implicit') == res # Recursive
        assert tree.traversal(tree.root, TraversalCategory.DFS, traversal, 'explicit') == res # Iterative with stack
        assert tree.traversal(tree.root, TraversalCategory.DFS, traversal, 'none') == res # Iterative Morris

    for i in range(1, 14):
        found = tree.search(tree.root, i)
        print(f'{i}: {found}')
    # 1: 1
    # 2: 2
    # 3: 3
    # 4: None
    # 5: 5
    # 6: 6
    # 7: 7
    # 8: 8
    # 9: 9
    # 10: None
    # 11: None
    # 12: None
    # 13: 13

    tree.remove(tree.root, 9)
    for i in range(1, 14):
        found = tree.r_search(tree.root, i)
        print(f'{i}: {found}')
    # 1: 1
    # 2: 2
    # 3: 3
    # 4: None
    # 5: 5
    # 6: 6
    # 7: 7
    # 8: 8
    # 9: None
    # 10: None
    # 11: None
    # 12: None
    # 13: 13

    # Traverses DFS preorder recursively
    print('\nRecursive DFS: valid BST? ', tree.is_bst(tree.root))  # True

    # Traverses DFS preorder iteratively w/ stack
    print('\nIterative Stack DFS: valid BST? ', tree.is_bst_iter(tree.root))  # True

    # Traverses DFS inorder iteratively w/ stack
    print('\nIterative Stack DFS: valid BST? ', tree.is_bst_iter_inorder(tree.root))  # True

    # Traverses DFS inorder iteratively w/ stack
    print('\nIterative Stack DFS: valid BST? ', tree.is_bst_r_inorder(tree.root))  # True

    root_7 = tree.search(tree.root, 7)
    root_8 = tree.search(tree.root, 8)
    root_13 = tree.search(tree.root, 13)
    assert root_7 and root_8 and root_13

    assert tree.inorder_successor(tree.root, root_7) == root_8
    assert tree.inorder_successor(tree.root, root_13) == None

    assert tree.inorder_successor2(tree.root, root_7) == root_8
    assert tree.inorder_successor2(tree.root, root_13) == None
    assert tree.inorder_successor3(tree.root, root_7) == root_8
    assert tree.inorder_successor3(tree.root, root_13) == None
    assert tree.inorder_predecessor(tree.root, root_3) == root_2
    assert tree.inorder_predecessor(tree.root, root_1) == None

    benchmark(
        (tree.inorder_successor, tree.inorder_successor2, tree.inorder_successor3),
        ((tree.root, root_7),),
    )

    tree.insert(4)

    assert tree.traversal(tree.root, TraversalCategory.BFS) == [5, 2, 7, 1, 3, 6, 13, 4, 8]

    left_split, right_split = tree.split_bst(tree.root, 2)
    assert left_split and right_split

    assert tree.traversal(left_split, TraversalCategory.DFS) == [2, 1]
    assert tree.traversal(right_split, TraversalCategory.DFS) == [5, 3, 4, 7, 6, 13, 8]

    assert tree.traversal(tree.root, TraversalCategory.BFS) == [5, 3, 7, 4, 6, 13, 8]

    print('inorder traversal before flatten: ',
          [_ for _ in tree.traversal(tree.root, TraversalCategory.DFS, 'inorder')])
    # [3, 4, 5, 6, 7, 8, 13]

    tree.flatten(tree.root)

    print('inorder traversal after flatten: ',
          [_ for _ in tree.traversal(tree.root, TraversalCategory.DFS, 'inorder')])
    # [5, 3, 4, 7, 6, 13, 8]
