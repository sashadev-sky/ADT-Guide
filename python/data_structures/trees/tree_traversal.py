from tree_node import TreeNode


class IterativeDFS:
    """Iterative Depth-First Traversals w/ Stack"""

    @staticmethod
    def inorder(root, res):
        stack = []
        while stack or root:
            if root:
                stack.append(root)
                root = root.left
            else:
                node = stack.pop()
                res.append(node.val)
                root = node.right
        return res

    @staticmethod
    def preorder(root, res):
        stack = [root]
        while stack:
            root = stack.pop()
            if root:
                res.append(root.val)
                if root.right:
                    stack.append(root.right)
                if root.left:
                    stack.append(root.left)
        return res

    @staticmethod
    # Post Order :children before node( L ,R , N)
    def postorder(root, res):
        stack = [root]
        while stack:
            root = stack.pop()
            if root:
                # res.append(root.val)
                res.insert(0, root.val)
                if root.left:
                    stack.append(root.left)
                if root.right:
                    stack.append(root.right)
        # res.reverse()
        return res

    @staticmethod
    def morris_inorder(root, res):
        while root is not None:
            if root.left is None:
                res.append(root.val)
                root = root.right

            # find the inorder predecessor of the root (right most
            # node on the left side of root)
            else:
                node = root.left
                while node.right is not None and node.right is not root:
                    node = node.right

                # Make root as right child of its inorder predecessor
                if node.right is None:
                    node.right = root
                    root = root.left
                # Revert the changes made in the 'if' part to restore the
                # original tree. i.e., fix the right child of predecessor
                else:
                    node.right = None
                    res.append(root.val)
                    root = root.right
        return res

    @staticmethod
    def morris_preorder(root, res):
        while root is not None:
            if root.left is None:
                res.append(root.val)
                root = root.right

            # find the inorder predecessor of the root (right most
            # node on the left side of root)
            else:
                node = root.left
                while node.right is not None and node.right is not root:
                    node = node.right

                # Make root as right child of its inorder predecessor
                if node.right is None:
                    res.append(root.val)   # hi
                    node.right = root
                    root = root.left
                # Revert the changes made in the 'if' part to restore the
                # original tree. i.e., fix the right child of predecessor
                else:
                    node.right = None
                    # res.append(root.val)  # bye
                    root = root.right
        return res

    @staticmethod
    def morris_postorder(root, res):
        def reverse_order(left, right):
            while left < right:
                res[left], res[right] = res[right], res[left]
                left += 1
                right -= 1
        dummy_node = TreeNode(None)
        node = dummy_node
        node.left = root
        while node is not None:
            if node.left is None:
                node = node.right
            else:
                pre = node.left
                while pre.right is not None and pre.right is not node:
                    pre = pre.right
                if pre.right is None:
                    pre.right = node
                    node = node.left
                else:
                    pre = node.left
                    count = 1
                    while pre.right is not None and pre.right is not node:
                        res.append(pre.val)
                        pre = pre.right
                        count += 1
                    res.append(pre.val)
                    pre.right = None
                    reverse_order(len(res)-count, len(res)-1)
                    node = node.right

        return res


class DFS:
    """Recursive Depth-First Traversals"""

    def __init__(self, root, res, alg, stack):
        if stack == 'implicit':
            if alg == 'inorder':
                self.inorder(root, res)
            elif alg == 'preorder':
                self.preorder(root, res)
            else:
                self.postorder(root, res)
        else:
            self._stack = IterativeDFS()
            if alg == 'inorder':
                if stack == 'none':
                    self._stack.morris_inorder(root, res)
                else:
                    self._stack.inorder(root, res)
            if alg == 'preorder':
                if stack == 'none':
                    self._stack.morris_preorder(root, res)
                else:
                    self._stack.preorder(root, res)
            if alg == 'postorder':
                if stack == 'none':
                    self._stack.morris_postorder(root, res)
                else:
                    self._stack.postorder(root, res)

    def inorder(self, root, res):
        if root is None:
            return
        self.inorder(root.left, res)
        res.append(root.val)
        self.inorder(root.right, res)

    def preorder(self, root, res):
        if root is None:
            return
        res.append(root.val)
        self.preorder(root.left, res)
        self.preorder(root.right, res)

    def postorder(self, root, res):
        if root is None:
            return
        self.postorder(root.left, res)
        self.postorder(root.right, res)
        res.append(root.val)

    def verticalorder(self, root):
        if root is None:
            return []

        node_map = {}
        min_column = max_column = 0

        def DFS(node, row, column):
            if node is not None:
                nonlocal min_column, max_column

                if node_map.get(column):
                    node_map[column].append((row, node.val))
                else:
                    node_map[column] = [(row, node.val)]
                min_column = min(min_column, column)
                max_column = max(max_column, column)

                # preorder DFS
                DFS(node.left, row + 1, column - 1)
                DFS(node.right, row + 1, column + 1)

        DFS(root, 0, 0)

        # order by column and sort by row
        ret = []
        for col in range(min_column, max_column + 1):
            node_map[col].sort(key=lambda x:x[0])
            col_vals = [val for row, val in node_map[col]]
            ret.append(col_vals)
        return ret


class BFS:
    @staticmethod
    def bfs(root):
        list_of_nodes, traversal_queue = [], [root]
        while traversal_queue:
            node = traversal_queue.pop(0)
            list_of_nodes.append(node.val)
            if node.left:
                traversal_queue.append(node.left)
            if node.right:
                traversal_queue.append(node.right)
        return list_of_nodes


class TreeTraversal:
    @staticmethod
    def traversal(root, category='dfs', alg='preorder', stack='implicit'):
        if category == 'dfs':
            res = []
            DFS(root, res, alg, stack)
            return res
        elif category == 'bfs':
            bfs = BFS()
            return bfs.bfs(root)
