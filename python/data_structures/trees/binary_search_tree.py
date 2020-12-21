from tree_traversal import TreeTraversal
from tree_node import TreeNode



class BinarySearchTree(TreeTraversal):
    def __init__(self):
        self.root = None

    @staticmethod
    def find_max(root: TreeNode) -> TreeNode:
        while root.right:
            root = root.right
        return root

    @staticmethod
    def find_min(root: TreeNode) -> TreeNode:
        while root.left:
            root = root.left
        return root

    def height(self, node: TreeNode) -> int:
        """Find the height of the tree by passing root or any other node in the tree."""
        if not node:
            return -1
        return 1 + max(self.height(node.left), self.height(node.right))

    @staticmethod
    def diameter(root: TreeNode) -> int:
        """Find the diameter of the tree.

        The max of 3 scenarios:
          1. The left subtree diameter
          2. The right subtree diameter
          3. The diameter of the path through the root
        """

        def calc_max(node):
            if not node:
                return 0, 0
            l_diameter, l_path = calc_max(node.left)
            r_diameter, r_path = calc_max(node.right)
            diameter = max(l_diameter, r_diameter, l_path + r_path)
            path = 1 + max(l_path, r_path)
            return diameter, path

        return calc_max(root)[0]

    @staticmethod
    def max_width(root: TreeNode) -> int:
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
            if node.left:
                next_level.append(node.left)
            if node.right:
                next_level.append(node.right)
            if not curr:
                if len(next_level) > max_width:
                    max_width = len(next_level)
                curr, next_level = next_level, curr
        return max_width

    @staticmethod
    def is_valid_bst(root: TreeNode) -> bool:
        """Approach 1: Recursive Traversal with Valid Range

        - DFS recursive, top down (preorder).
        - Time complexity: O(N) since we visit each node exactly once.
        - Space complexity: O(N) since we keep up to the entire tree.
        """

        def validate(node, low=-float('inf'), high=float('inf')):
            if not node:
                return True
            if node.val <= low or node.val >= high:
                return False
            return (validate(node.left, low, node.val) and
                    validate(node.right, node.val, high))

        return validate(root)

    @staticmethod
    def is_valid_bst_iter(root: TreeNode) -> bool:
        """Approach 2: Iterative Traversal with Valid Range

        - DFS iterative (in-order traversal result in ordered list, top down)
        (preorder).
        - Time complexity: O(N) since we visit each node exactly once.
        - Space complexity: O(N) since we keep up to the entire tree.
        """

        if not root:
            return True

        stack = [(root, -float("inf"), float("inf"))]
        while stack:
            root, lower, upper = stack.pop()
            if not root:
                continue
            val = root.val
            if val <= lower or val >= upper:
                return False
            # important note - right child is pushed first so that left child is processed first (LIFO order)
            stack.append((root.right, val, upper))
            stack.append((root.left, lower, val))
        return True

    @staticmethod
    def is_valid_bst_iter_inorder(root: TreeNode) -> bool:
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
            # If next element in inorder traversal is smaller than the previous one than not a BST.
            if root.val <= prev:
                return False
            prev = root.val
            root = root.right
        return True

    @staticmethod
    def is_valid_bst_r_inorder(root: TreeNode) -> bool:
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

    def split_bst(self, root, val):
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

    def flatten(self, root) -> None:
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
    def search(root: TreeNode, val: int):
        """Return the data if it was found or None if it wasn't"""
        while root is not None and root.val != val:
            root = root.left if val < root.val else root.right
        return root

    def r_search(self, root, val):
        if root is None or val == root.val:
            return root
        elif val < root.val:
            return self.r_search(root.left, val)
        else:
            return self.r_search(root.right, val)

    def insert(self, val):
        node = TreeNode(val)
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

    def r_insert(self, root, val):
        if not root:
            return TreeNode(val)
        if val <= root.val:
            root.left = self.r_insert(root.left, val)
        else:
            root.right = self.r_insert(root.right, val)
        return root

    def inorder_successor(self, root: TreeNode, p: TreeNode) -> TreeNode:
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

    def inorder_successor2(self, root: TreeNode, p: TreeNode) -> TreeNode:
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

    def inorder_successor3(self, root: TreeNode, p: TreeNode) -> TreeNode:
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
            pre_val = root.val
            root = root.right

        return None

    def inorder_predecessor(self, root: TreeNode, p: TreeNode) -> TreeNode:
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

    def remove(self, root: TreeNode, val: int) -> TreeNode:
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

    print(f'Tree Height: {tree.height(tree.root)}')  # 3
    print(f'Tree Diameter: {tree.diameter(tree.root)}')  # 5

    print()

    found = tree.search(tree.root, 9)
    print(f'Node: {found.val}')  # 9
    print('\t', f'Children: {found.num_children()}')  # 2
    print('\t', f'Height from tree method: {tree.height(found)}')  # 1
    print('\t', f'Height from node method: {found.height()}')  # 1

    print()

    found2 = tree.search(tree.root, 5)
    print(f'Found: {found2.val}')  # 5
    print('\t', f'Children: {found2.num_children()}')  # 2
    print('\t', f'Height from tree method: {tree.height(found2)}')  # 3
    print('\t', f'Height from node method: {found2.height()}')  # 3

    print()

    found2 = tree.search(tree.root, 2)
    print(f'Node: {found2.val}')  # 2
    print('\t', f'Children {found2.num_children()}')  # 2
    print('\t', f'Height from tree method: {tree.height(found2)}')  # 3
    print('\t', f'Height from node method: {found2.height()}')  # 3

    print()

    root_node = tree.root
    print('BFS: ', tree.traversal(root_node, 'bfs', None, None), '\n')
    # [5, 2, 7, 1, 3, 6, 9, 8, 13]

    print('Inorder: ',
          [_ for _ in tree.traversal(root_node, 'dfs', 'inorder')])
    # [1, 2, 3, 5, 6, 7, 8, 9, 13]

    print('\t', 'iterative w/ stack inorder: ',
          [_ for _ in tree.traversal(root_node, 'dfs', 'inorder', 'explicit')])
    # [1, 2, 3, 5, 6, 7, 8, 9, 13]

    print('\t', 'iterative w/ morris inorder: ',
          [_ for _ in tree.traversal(root_node, 'dfs', 'inorder', 'none')])
    # [1, 2, 3, 5, 6, 7, 8, 9, 13]

    print('Preorder: ',
          [_ for _ in tree.traversal(root_node, 'dfs', 'preorder')])
    # [5, 2, 1, 3, 7, 6, 9, 8, 13]

    print('\t', 'iterative w/ stack preorder: ',
          [_ for _ in tree.traversal(root_node, 'dfs', 'preorder', 'explicit')])
    #  [5, 2, 1, 3, 7, 6, 9, 8, 13]

    print('\t', 'iterative w/ morris preorder: ',
          [_ for _ in tree.traversal(root_node, 'dfs', 'preorder', 'none')])
    # [5, 2, 1, 3, 7, 6, 9, 8, 13]

    print('Postorder: ',
          [node for node in tree.traversal(root_node, 'dfs', 'postorder')])
    # [1, 3, 2, 6, 8, 13, 9, 7, 5]

    print('\t', 'iterative w/ stack postorder: ',
          [_ for _ in tree.traversal(root_node, 'dfs', 'postorder', 'explicit')])
    # [1, 3, 2, 6, 8, 13, 9, 7, 5]

    print('\t', 'iterative w/ morris postorder: ',
          [_ for _ in tree.traversal(root_node, 'dfs', 'postorder', 'none')])
    # [1, 3, 2, 6, 8, 13, 9, 7, 5]
    print()

    for i in range(1, 14):
        found = tree.search(root_node, i)
        print(f"{i}: {found}")
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
        print(f"{i}: {found}")
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
    print('\nRecursive DFS: valid BST? ', tree.is_valid_bst(root_node))  # T

    # Traverses DFS preorder iteratively w/ stack
    print('\nIterative Stack DFS: valid BST? ',
          tree.is_valid_bst_iter(root_node))  # T

    # Traverses DFS inorder iteratively w/ stack
    print('\nIterative Stack DFS: valid BST? ',
          tree.is_valid_bst_iter_inorder(root_node))  # T

    # Traverses DFS inorder iteratively w/ stack
    print('\nIterative Stack DFS: valid BST? ',
          tree.is_valid_bst_r_inorder(root_node))  # T

    print(tree.inorder_successor(root_node, tree.search(root_node, 7)))  # 8
    print(tree.inorder_successor(root_node, tree.search(root_node, 13)))  # None

    print(tree.inorder_successor2(root_node, tree.search(root_node, 7)))  # 8
    print(tree.inorder_successor2(root_node, tree.search(root_node, 13)))  # Non
    print(tree.inorder_successor3(root_node, tree.search(root_node, 7)))  # 8
    print(tree.inorder_successor3(root_node, tree.search(root_node, 13)))  # Non
    print(tree.inorder_predecessor(root_node, tree.search(root_node, 3)))  # 2
    print(tree.inorder_predecessor(root_node, tree.search(root_node, 1)))  # Non

    tree.insert(4)
    print([_ for _ in tree.traversal(root_node, 'bfs')])
    # [5, 2, 7, 1, 3, 6, 13, 4, 8]
    s1, s2 = tree.split_bst(root_node, 2)
    print('left split: ',
          [_ for _ in tree.traversal(s1, 'dfs')])  # [2, 1]
    print('right split: ',
          [_ for _ in tree.traversal(s2, 'dfs')])  # [5, 3, 4, 7, 6, 13, 8]

    print([_ for _ in tree.traversal(root_node, 'bfs')])

    print('inorder traversal before flatten: ',
          [_ for _ in tree.traversal(root_node, 'dfs', 'inorder')])
    # [3, 4, 5, 6, 7, 8, 13]

    tree.flatten(root_node)

    print('inorder traversal after flatten: ',
          [_ for _ in tree.traversal(root_node, 'dfs', 'inorder')])
    # [5, 3, 4, 7, 6, 13, 8]
