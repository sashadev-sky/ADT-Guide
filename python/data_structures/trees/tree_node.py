class TreeNode:
    def __init__(self, val):
        self.val = val
        self.right = None
        self.left = None

    def __str__(self):
        return f'{self.val}'

    def num_children(self):
        return sum(c is not None for c in [self.left, self.right])

    def height(self):
        if not self.left or not self.right:
            return 0
        return 1 + max(self.left.height(), self.right.height())
