from python.linked_list.node import DoublyNode
from python.queue.doubly_linked_list_queue import DoublyLinkedListQueue

class Deque(DoublyLinkedListQueue):
    def add_first(self, key, value):
        """prepend x to the head of the queue"""
        el = DoublyNode(key, value)
        if self.empty():
            self.head = self.tail = el
        else:
            el.next = self.head
            self.head.prev = self.head = el
        self.size += 1

    def add_last(self, key, value):
        super().enqueue(key, value)

    def delete_first(self):
        return super().dequeue()

    def delete_last(self):
        if self.tail:
            node = self.tail
            self.size -= 1

            if self.size == 0:
                self.head = self.tail = None
            else:
                self.tail = node.prev
                assert self.tail is not None
                self.tail.next = None
            return node.val

    def dequeue(self):
        pass

    def enqueue(self):
        pass

    def last(self):
        if self.tail:
            return self.tail.val


if __name__ == '__main__':
    ll_queue = Deque()
    print("Checking if queue is empty:", ll_queue.empty())  # True
    ll_queue.add_last("1", 1)
    ll_queue.add_last("2", 2)
    print(ll_queue)  # [1->2]
    ll_queue.add_first("3", 3)
    ll_queue.add_first("4", 4)
    print(ll_queue.first())  # 4
    print(ll_queue.last())  # 2
    ll_queue.add_last("5", 5)
    print(ll_queue)  # [4->3->1->2->5]
    print(ll_queue.delete_first())  # 4
    print(ll_queue.delete_first())  # 3
    print(ll_queue)  # [1->2->5]
    ll_queue.add_last("6", 4)
    print(ll_queue)  # [1->2->5->4]
    print(ll_queue.first()) # 1
    print(ll_queue.last())  # 4
    print(ll_queue.delete_last())  # 4
    print(ll_queue.last())  # 5
    print(ll_queue.delete_last())  # 5
    print(ll_queue.last())  # 2
    print(ll_queue)  # [1->2]
