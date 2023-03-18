
from typing import Any, Iterator

from python.linked_list.node import SinglyNode, DoublyNode

class SinglyLinkedList:
    def __init__(self):
        self.head: SinglyNode | None = None
        self.size = 0

    def __contains__(self, value: Any):
        for node in self:
            if node == value:
                return True
        return False

    def __iter__(self) -> Iterator[Any]:
        curr = self.head
        while curr:
            val = curr.val
            curr = curr.next
            yield val

    def __len__(self):
        """return the length of the list, rep'd by number of nodes"""
        return self.size

    def __str__(self):
        return f'[{"->".join([str(node) for node in self])}]'

    def append(self, key: str, value: Any):
        """add value to the end of the list"""
        el = SinglyNode(key, value)
        if self.empty():
            self.head = el
        else:
            curr = self.last()
            assert curr is not None
            curr.next = el
        self.size += 1

    def clear(self) -> None:
        """Clear the entire list."""
        self.head = None
        self.size = 0

    def remove(self, key: str) -> Any:
        prev, curr = None, self.head

        while curr:
            if curr.key == key:
                next_node = curr.next
                assert prev is not None
                prev.next = next_node
                self.size -= 1
                return curr.val

            prev = curr
            curr = curr.next
        return None

    def remove_val_by_index(self, x: int) -> Any:
        """remove and return value at index x provided as parameter"""
        curr = self.head
        i = 0
        while curr and curr.key:
            if i == x:
                return self.remove(curr.key)
            curr = curr.next
            i += 1
        return -1

    def reverse_list_iter(self, head: SinglyNode | None) -> SinglyNode | None:
        """
        # Time complexity : O(n). Assume that n is the list's length,
        # the time complexity is O(n).

        # Space complexity : O(1).

        1. make sure to store its `prev` el beforehand (will be `None` on 1st
           round) bc singly linked list node doesn't have access to that
        2. While you are traversing the list, change the current node's next
           pointer to point to its previous element.

        3. You also need another pointer to store the next node before changing
           the reference. (`curr`)
        4. Do not forget to return the new head reference at the end!
        """
        prev, curr = None, head

        while curr:
            curr.next, prev, curr = prev, curr, curr.next

        self.head = prev
        return prev

    def reverse_list_recur(self, head: SinglyNode | None) -> SinglyNode | None:
        """
        reverse the sequence of node pointers in the linked list

        Given [1->2->3->4->5] reverse pointers [1<-2<-3<-4<-5]
        Turning list to [5->4->3->2->1]

        Time complexity : O(n). Assume that n is the list's length,
                         the time complexity is O(n).

        Space complexity : O(n). The extra space comes from implicit stack space
                           due to recursion. The recursion could go
                           up to n levels deep.

        Be very careful that n1's next must point to Ø. If you forget about this
        ,your linked list has a cycle in it. This bug could be caught if
        you test your code with a linked list of size 2.
        """

        if head is None or head.next is None:
            return head

        new_head = self.reverse_list_iter(head.next)
        head.next.next = head
        head.next = None
        return new_head

    def search_val(self, value: Any) -> int:
        """Return indices where value was found"""
        i = 0
        for node in self:
            if value == node:
                return i
            i += 1
        return -1

    def empty(self) -> bool:
        return self.size == 0

    def first(self) -> SinglyNode | None:
        return self.head

    def last(self) -> SinglyNode | None:
        curr = self.head
        while curr and curr.next:
            curr = curr.next
        return curr

    def prepend(self, key: str, value: Any):
        """Add value to the left of the list making it the head"""
        el = SinglyNode(key, value, self.head)
        self.head = el
        self.size += 1


class DoublyLinkedList(SinglyLinkedList):
    head: DoublyNode | None

    def __init__(self):
        super().__init__()
        self.tail: DoublyNode | None = None

    def append(self, key: str, value: Any):
        if self.empty():
            el = DoublyNode(key, value)
            self.head = self.tail = el
        else:
            el = DoublyNode(key, value, None, self.tail)
            self.tail.next = self.tail = el
        self.size += 1

    def clear(self):
        super().clear()
        self.tail = None

    def prepend(self, key: str, value: Any):
        el = DoublyNode(key, value, self.head)
        self.head.prev = self.head = el
        self.size += 1

    def remove(self, key: str) -> Any:
        curr = self.head

        while curr and curr.key:
            if curr.key == key:
                prev = curr.prev
                next_node = curr.next
                if prev is not None:
                    prev.next = next_node
                if next_node is not None:
                    next_node.prev = prev
                self.size -= 1
                return curr.val

            curr = curr.next
        return None

    def reverse_list_iter(self, head: DoublyNode | None) -> DoublyNode | None:
        prev, curr = None, head

        while curr:
            if prev:
                prev.prev = curr
            curr.next, prev, curr = prev, curr, curr.next

        self.tail = head
        if prev is not None:
            prev.prev = None
        self.head = prev

        return prev

    def reverse_list_recur(self, head: DoublyNode | None) -> DoublyNode | None:
        if head is None or head.next is None:
            return head

        tail = head.next
        new_head = self.reverse_list_iter(head.next)
        tail.next, head.prev, head.next = head, tail, None
        return new_head

    def last(self):
        return self.tail


class CircularlyLinkedList(DoublyLinkedList):

    def __iter__(self) -> Iterator[Any]:
        curr = self.head
        counter = 0

        while curr:
            val = curr.val
            assert self.tail is not None
            if counter > 0 and curr == self.tail.next:
                yield val
                break
            curr = curr.next
            counter += 1
            yield val

    def append(self, key: str, value: Any):
        if self.empty():
            el = DoublyNode(key, value)
            self.head = self.tail = el
        else:
            el = DoublyNode(key, value, None, self.tail)
            self.tail.next = self.tail = el
            el.next = self.head
            assert self.head is not None
            self.head.prev = el
        self.size += 1

    def remove(self, key: str) -> Any:
        curr, prev = self.head, self.tail

        while curr:
            if curr.key == key:
                assert isinstance(curr.next, DoublyNode) and isinstance(self.head, DoublyNode) and isinstance(prev, DoublyNode)
                if curr == self.tail:
                    self.tail = curr.next
                    self.head.next = self.tail
                else:
                    prev.next = curr.next

                next_node = curr.next
                next_node.prev = prev
                self.size -= 1
                return curr.val
            prev = curr
            curr = curr.next
        return None


if __name__ == '__main__':
    singly_list = SinglyLinkedList()
    print(singly_list)  # []
    print(singly_list.first())  # None
    print(singly_list.last())  # None
    singly_list.append('link2', 0)
    singly_list.append('link3', 2)
    singly_list.append('link4', 5)
    singly_list.append('link5', 5)
    print(singly_list.first())  # link2: 0
    print(singly_list.last())  # link5: 5
    print(singly_list)  # [0->2->5->5]
    singly_list.reverse_list_iter(singly_list.head)
    print(singly_list)  # [5->5->2->0]
    singly_list.reverse_list_iter(singly_list.head)
    print(singly_list)  # [0->2->5->5]
    singly_list.reverse_list_recur(singly_list.head)
    print(singly_list)  # [5->5->2->0]
    singly_list.prepend('link1', 10)
    print(singly_list)  # [10->5->5->2->0]
    singly_list.clear()
    print(singly_list)  # []

    print('----------------')

    doubly_list = DoublyLinkedList()
    print(doubly_list)  # []
    print(len(doubly_list))  # 0
    print(doubly_list.empty())  # True
    doubly_list.append('link1', 3)
    print(doubly_list)  # [3]
    print(len(doubly_list))  # 1
    print(doubly_list.empty())  # False
    print(doubly_list.first())  # link1: 3
    print(doubly_list.last())  # link1: 3
    doubly_list.append('link2', 0)
    doubly_list.append('link3', 2)
    doubly_list.append('link4', 5)
    doubly_list.append('link5', 5)
    print(doubly_list)  # [3->0->2->5->5]
    doubly_list.prepend('link0', 0)
    print(doubly_list)  # [0->3->0->2->5->5]
    print(len(doubly_list))  # 6
    print(doubly_list.search_val(3))  # 1
    print(doubly_list.search_val(6))  # -1
    print(doubly_list.remove_val_by_index(1))  # 3
    print(doubly_list)  # [0->0->2->5->5]
    doubly_list.reverse_list_iter(doubly_list.head)
    print(doubly_list)  # [5->5->2->0->0]
    doubly_list.reverse_list_iter(doubly_list.head)
    print(doubly_list)  # [0->0->2->5->5]
    doubly_list.reverse_list_recur(doubly_list.head)
    print(doubly_list)  # [5->5->2->0->0]
    doubly_list.clear()
    print(doubly_list)  # []

    print('----------------')

    my_circularly_list = CircularlyLinkedList()
    my_circularly_list.append('link2', 0)
    my_circularly_list.append('link3', 2)
    my_circularly_list.append('link4', 5)
    my_circularly_list.append('link5', 5)
    print(my_circularly_list)  # [0->2->5->5->0]
    my_circularly_list.remove('link3')
    print(my_circularly_list)  # [0->5->5->0]
