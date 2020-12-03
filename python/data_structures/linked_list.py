class Node:

    def __init__(self, key=None, val=None, next_node=None, prev_node=None):
        self.key = key
        self.val = val
        self.next = next_node
        self.prev = prev_node

    def __str__(self):
        return f"{self.key}: {self.val}"


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, key, value):
        """add value to the end of the list"""
        if self.empty():
            el = Node(key, value)
            self.head = el
            self.tail = el
        else:
            el = Node(key, value, None, self.tail)
            self.tail.next = el
            self.tail = el

    def empty(self):
        return self.head is None

    def first(self):
        return None if self.empty() else self.head

    def last(self):
        return None if self.empty() else self.tail

    def __str__(self):
        # [5->4->10->1]
        to_print = ""
        curr = self.head
        while curr is not None:
            to_print += str(curr.val) + "->"
            curr = curr.next
        if to_print:
            return "[" + to_print[:-2] + "]"
        return "[]"

    def prepend(self, key, value):
        """add value to the left of the list making it the head"""
        el = Node(key, value, self.head)
        self.head.prev = el
        self.head = el

    def __getitem__(self, key):
        current_node = self.head.next
        while current_node.key != key:
            if current_node == self.tail: return None
            current_node = current_node.next
        return current_node.val

    def search_val(self, value):
        """return indices where value was found"""
        current = self.head
        current_index = 0
        while current is not None:
            if current.val == value: return current_index
            current = current.next
            current_index += 1

        return -1

    def remove(self, key):
        current_node = self.head

        while current_node is not None:
            if current_node.key == key:
                previous_node = current_node.prev
                next_node = current_node.next
                previous_node.next = next_node
                next_node.prev = previous_node
                return current_node.val

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

    def length(self):
        """return the length of the list, rep'd by number of nodes"""
        current = self.head
        current_index = 0
        while current is not None:
            current = current.next
            current_index += 1
        return current_index

    # #1->2->3->4->5->None
    # prev = None
    # current = 1
    #
    # while current != None:
    #     next = current.next #None
    #     current.next = prev #5->4->3-> 2-> 1 -> None
    #     prev = current #5
    #     current = next#None

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

    def reverse_list(self):
        newHead = self.reverse_list_recur(self.head)
        self.tail = self.head
        self.head = newHead

    def reverse_list_recur(self, head):
        """reverse the sequence of node pointers in the linked list"""
        # Given [1->2->3->4->5] reverse pointers [1<-2<-3<-4<-5]
        # Turning list to [5->4->3->2->1]

        if head is None or head.next is None:
            return head

        tail = head.next
        newHead = self.reverse_list_recur(head.next)
        tail.next = head
        head.prev = tail
        head.next = None
        return newHead


if __name__ == '__main__':
    my_list = DoublyLinkedList()
    print(my_list)  # []
    print(my_list.length())  # 0
    print(my_list.empty())  # True
    my_list.append("link1", 3)
    print(my_list)  # [3]
    print(my_list.length())  # 1
    print(my_list.empty())  # False
    print(my_list.first())  # link1: 3
    print(my_list.last())  # link1: 3
    my_list.append("link2", 0)
    my_list.append("link3", 2)
    my_list.append("link4", 5)
    my_list.append("link5", 5)
    print(my_list)  # [3->0->2->5->5]
    my_list.prepend("link0", 0)
    print(my_list)  # [0->3->0->2->5->5]
    print(my_list.length())  # 6
    print(my_list.search_val(3))  # 1
    print(my_list.search_val(6))  # -1
    print(my_list.remove_val_by_index(1))  # 3
    print(my_list)  # [0->0->2->5->5]
    my_list.reverse_list_iter()
    print(my_list)  # [5->5->2->0->0]
    my_list.reverse_list_iter()
    print(my_list)  # [0->0->2->5->5]
    my_list.reverse_list()
    print(my_list)  # [5->5->2->0->0]
