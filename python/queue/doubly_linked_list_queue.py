from python.linked_list.node import DoublyNode

class DoublyLinkedListQueue:
    def __init__(self):
        """initialize stack with stack pointer"""
        self.head = None
        self.tail = None
        self.size = 0

    def __iter__(self):
        curr = self.head
        while curr:
            val = curr.val
            curr = curr.next
            yield val

    def __str__(self):
        return f'[{"->".join([str(node) for node in self])}]'

    def enqueue(self, key, value):
        """append x to the tail of the queue"""
        el = DoublyNode(key, value)
        if self.empty():
            self.head = self.tail = el
        else:
            el.prev = self.tail
            self.tail.next = self.tail = el
        self.size += 1

    def dequeue(self):
        if not self.head:
            raise IndexError('pop from empty queue')

        node = self.head
        self.size -= 1

        if self.size == 0:
            self.head = self.tail = None
        else:
            self.head = node.next
            node.prev = None
        return node.val

    def first(self):
        return self.head.val

    def empty(self):
        """return True if stack is empty, else return false"""
        return self.size == 0


if __name__ == '__main__':
    ll_queue = DoublyLinkedListQueue()
    print("Checking if queue is empty:", ll_queue.empty())  # True
    ll_queue.enqueue("1", 1)
    ll_queue.enqueue("2", 2)
    print(ll_queue)  # [1->2]
    ll_queue.enqueue("3", 3)
    ll_queue.enqueue("4", 4)
    print("Checking item on top of queue:", ll_queue.first())  # 1
    ll_queue.enqueue("5", 5)
    print(ll_queue)  # [1->2->3->4->5]
    print(ll_queue.dequeue())  # 1
    print(ll_queue.dequeue())  # 2
    print(ll_queue)  # [3->4->5]
    ll_queue.enqueue("6", 4)
    print(ll_queue)  # [3->4->5->4]
    print(ll_queue.first())  # 3
