class Node:

    def __init__(self, key=None, val=None, next_node=None, prev_node=None):
        self.key = key
        self.val = val
        self.next = next_node
        self.prev = prev_node

    def __str__(self):
        return f"{self.key}: {self.val}"


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __contains__(self, value) -> bool:
        for node in self:
            if node == value:
                return True
        return False

    def __iter__(self):
        current = self.head
        while current:
            val = current.val
            current = current.next
            yield val

    def __len__(self):
        """return the length of the list, rep'd by number of nodes"""
        return self.size

    def __str__(self):
        to_print = ""
        for node in self:
            to_print += str(node) + "->"
        if to_print:
            return "[" + to_print[:-2] + "]"
        return "[]"

    def append(self, key, value):
        """add value to the end of the list"""
        if self.empty():
            el = Node(key, value)
            self.head = el
            self.tail = el
        else:
            el = Node(key, value)
            self.tail.next = el
            self.tail = el
        self.size += 1

    def clear(self):
        """ Clear the entire list. """
        self.tail = None
        self.head = None

    def remove(self, key):
        current_node = self.head
        prev = None

        while current_node is not None:
            if current_node.key == key:
                next_node = current_node.next
                prev.next = next_node
                self.size -= 1
                return current_node.val

            prev = current_node
            current_node = current_node.next
        return None

    def remove_val_by_index(self, x):
        """remove and return value at index x provided as parameter"""
        current = self.head
        current_index = 0
        while current is not None:
            if current_index == x: return self.remove(current.key)
            current = current.next
            current_index += 1
        return -1

    def reverse_list_iter(self):
        prev_node = None
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = prev_node
            prev_node = current
            current = next_node

        self.tail = self.head
        self.head = prev_node

    def reverse_list_recur(self):
        new_head = self.reverse_list(self.head)
        self.tail = self.head
        self.head = new_head

    def reverse_list(self, head):
        """
        reverse the sequence of node pointers in the linked list

        Given [1->2->3->4->5] reverse pointers [1<-2<-3<-4<-5]
        Turning list to [5->4->3->2->1]
        """

        if head is None or head.next is None:
            return head

        tail = head.next
        new_head = self.reverse_list(head.next)
        tail.next = head
        head.next = None
        return new_head

    def search_val(self, value):
        """return indices where value was found"""
        current_index = 0
        for node in self:
            if value == node:
                return current_index
            current_index += 1

        return -1

    def empty(self):
        return self.size == 0

    def first(self):
        return None if self.empty() else self.head

    def last(self):
        return None if self.empty() else self.tail

    def prepend(self, key, value):
        """add value to the left of the list making it the head"""
        el = Node(key, value, self.head)
        self.head = el
        self.size += 1


class DoublyLinkedList(SinglyLinkedList):
    def append(self, key, value):
        if self.empty():
            el = Node(key, value)
            self.head = el
            self.tail = el
        else:
            el = Node(key, value, None, self.tail)
            self.tail.next = el
            self.tail = el
        self.size += 1

    def prepend(self, key, value):
        el = Node(key, value, self.head)
        self.head.prev = el
        self.head = el
        self.size += 1

    def remove(self, key):
        current_node = self.head

        while current_node is not None:
            if current_node.key == key:
                previous_node = current_node.prev
                next_node = current_node.next
                previous_node.next = next_node
                next_node.prev = previous_node
                self.size -= 1
                return current_node.val

            current_node = current_node.next
        return None

    def reverse_list_iter(self):
        prev_node = None
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = prev_node
            if prev_node is not None:
                prev_node.prev = current
            prev_node = current
            current = next_node

        prev_node.prev = None
        self.tail = self.head
        self.head = prev_node

    def reverse_list(self, head):
        if head is None or head.next is None:
            return head

        tail = head.next
        new_head = self.reverse_list(head.next)
        tail.next = head
        head.prev = tail
        head.next = None
        return new_head


class CircularlyLinkedList(DoublyLinkedList):

    def __iter__(self):
        current = self.head
        counter = 0

        while current:
            val = current.val
            if counter > 0 and current == self.tail.next:
                yield val
                break
            current = current.next
            counter += 1
            yield val

    def append(self, key, value):
        if self.empty():
            el = Node(key, value)
            self.head = el
            self.tail = el
        else:
            el = Node(key, value, None, self.tail)
            self.tail.next = el
            self.tail = el
            el.next = self.head
            self.head.prev = el
        self.size += 1

    def remove(self, key):
        current = self.head
        prev = self.tail

        while current is not None:
            if current.key == key:
                if current == self.tail:
                    self.tail = current.next
                    self.head.next = self.tail
                else:
                    prev.next = current.next

                next_node = current.next
                next_node.prev = prev
                self.size -= 1
                return current.val
            prev == current
            current = current.next
        return None


if __name__ == '__main__':
    my_singly_list = SinglyLinkedList()
    my_singly_list.append("link2", 0)
    my_singly_list.append("link3", 2)
    my_singly_list.append("link4", 5)
    my_singly_list.append("link5", 5)
    print(my_singly_list)  # [0->2->5->5]
    my_singly_list.reverse_list_iter()
    print(my_singly_list)  # [5->5->2->0]
    my_singly_list.reverse_list_iter()
    print(my_singly_list)  # [0->2->5->5]
    my_singly_list.reverse_list_recur()
    print(my_singly_list)  # [5->5->2->0]
    my_singly_list.prepend("link1", 10)
    print(my_singly_list)  # [10->5->5->2->0]

    print("----------------")

    my_doubly_list = DoublyLinkedList()
    print(my_doubly_list)  # []
    print(len(my_doubly_list))  # 0
    print(my_doubly_list.empty())  # True
    my_doubly_list.append("link1", 3)
    print(my_doubly_list)  # [3]
    print(len(my_doubly_list))  # 1
    print(my_doubly_list.empty())  # False
    print(my_doubly_list.first())  # link1: 3
    print(my_doubly_list.last())  # link1: 3
    my_doubly_list.append("link2", 0)
    my_doubly_list.append("link3", 2)
    my_doubly_list.append("link4", 5)
    my_doubly_list.append("link5", 5)
    print(my_doubly_list)  # [3->0->2->5->5]
    my_doubly_list.prepend("link0", 0)
    print(my_doubly_list)  # [0->3->0->2->5->5]
    print(len(my_doubly_list))  # 6
    print(my_doubly_list.search_val(3))  # 1
    print(my_doubly_list.search_val(6))  # -1
    print(my_doubly_list.remove_val_by_index(1))  # 3
    print(my_doubly_list)  # [0->0->2->5->5]
    my_doubly_list.reverse_list_iter()
    print(my_doubly_list)  # [5->5->2->0->0]
    my_doubly_list.reverse_list_iter()
    print(my_doubly_list)  # [0->0->2->5->5]
    my_doubly_list.reverse_list_recur()
    print(my_doubly_list)  # [5->5->2->0->0]
    my_doubly_list.clear()  # [5->5->2->0->0]
    print(my_doubly_list)  # []

    print("----------------")

    my_circularly_list = CircularlyLinkedList()
    my_circularly_list.append("link2", 0)
    my_circularly_list.append("link3", 2)
    my_circularly_list.append("link4", 5)
    my_circularly_list.append("link5", 5)
    print(my_circularly_list)  # [0->2->5->5->0]

