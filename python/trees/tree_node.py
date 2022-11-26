from dataclasses import dataclass
from typing import Self

@dataclass
class TreeNode:
    val: object
    right: Self | None = None
    left: Self | None = None

    def __repr__(self) -> str:
        from pprint import pformat

        if self.left is None and self.right is None:
            return str(self.val)
        return pformat({f'{self.val}': (self.left, self.right)}, indent=1)

    def __str__(self):
        return f'{self.val}'

    def num_children(self):
        return sum(c is not None for c in [self.left, self.right])

    def height(self) -> int:
        if not self.left or not self.right:
            return 0
        return 1 + max(self.left.height(), self.right.height())

@dataclass
class BSTNode(TreeNode):
    val: int
