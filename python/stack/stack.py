from typing import Any, Generic, TypeVar

from python.linked_list.node import SinglyNode
from python.utils.errors import StackUnderflowError

T = TypeVar('T')

class ArrayStack(Generic[T]):
    def __init__(self):
        self.stack: list[T] = []

    def push(self, el: T):
        self.stack.append(el)

    def pop(self):
        if not self.stack:
            raise StackUnderflowError()
        return self.stack.pop()

    def peek(self):
        if not self.stack:
            raise StackUnderflowError()
        return self.stack[-1]

    def empty(self):
        """Check if the stack is empty.

        :return: True if stack is empty, else False
        """

        return not self.stack


class LinkedListStack:
    def __init__(self):
        """Initialize stack with stack pointer"""
        self.top = None
        self.size = 0

    def __iter__(self):
        curr = self.top
        while curr:
            val = curr.val
            curr = curr.next
            yield val

    def __str__(self) -> str:
        return '[]' if self.empty() else f'[{"->".join([str(node) for node in self])}]'

    def push(self, key, value: Any) -> None:
        """Add node to the top of the stack"""
        node = SinglyNode(key, value)
        if self.top:
            node.next = self.top
        self.top = node
        self.size += 1

    def pop(self):
        """
        Remove the top element from the stack and return it, or return
        None if the stack is empty
        """

        if not self.top:
            raise StackUnderflowError()
        node = self.top.val
        self.size -= 1
        self.top = self.top.next if self.top.next else None
        return node

    def peek(self):
        """Get the value of the top element from the stack.

        :return: the top element from the stack, or None if the stack is empty
        """

        if not self.top:
            raise StackUnderflowError()
        return self.top.val

    def empty(self) -> bool:
        """Check if the stack is empty.

        :return: True if stack is empty, else False
        """

        return self.size == 0


if __name__ == '__main__':
    arr_stack: ArrayStack[Any] = ArrayStack()
    print(arr_stack.empty())  # True

    ll_stack = LinkedListStack()
    print('Checking if stack is empty:', ll_stack.empty())  # True
    ll_stack.push('1', 1)
    ll_stack.push('2', 2)
    print(ll_stack)  # [2->1]
    ll_stack.push('3', 3)
    ll_stack.push('4', 4)
    print('Checking item on top of stack:', ll_stack.peek())  # 4
    ll_stack.push('5', 5)
    print(ll_stack)  # [5->4->3->2->1]
    print(ll_stack.pop())  # 5
    print(ll_stack.pop())  # 4
    print(ll_stack)  # [3->2->1]
    ll_stack.push('6', 4)
    print(ll_stack)  # [4->3->2->1]
    print(ll_stack.peek())  # 4
