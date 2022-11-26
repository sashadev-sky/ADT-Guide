from typing import Any, Self

class SinglyNode:
    def __init__(self, key: str | None = None, val: Any = None, next: Self | None = None):
        self.key = key
        self.val = val
        self.next = next

    def __str__(self):
        return f'{self.key}: {self.val}'


class DoublyNode(SinglyNode):
    def __init__(
        self,
        key: str | None = None,
        val: Any = None,
        next: Self | None = None,
        prev: Self | None = None
    ):
        super().__init__(key, val, next)
        self.prev = prev
