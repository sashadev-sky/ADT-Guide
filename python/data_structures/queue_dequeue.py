from python.data_structures.node import DoublyNode


class NaiveArrayQueue:
    def __init__(self):
        self.items = []
        self.size = 0

    def __str__(self):
        return f'[{"->".join(str(item.val) for item in self.items)}]'

    def enqueue(self, key, value):
        node = DoublyNode(key, value)
        self.items.append(node)
        self.size += 1
        return node.val

    def dequeue(self):
        node = self.items.pop(0)
        self.size -= 1
        return node.val

    def peek(self):
        return self.items[0].val if self.items else None

# clever Queue implementation using an array.
# Constant time complexity (amortized)


class StackArrayQueue:
    """
    This implementation of a queue uses two stacks. The stacks in this case are
    simply Python lists that allow us to call `push` and `pop` methods on them.
    """
    def __init__(self):
        """
        inbound_stack: only used to store elements that are added to the queue.
                       No other operation can be performed on this stack.

        outbound_stack: New elements added to our queue end up in the here.
                       Instead of removing elements from the `inbound_stack`,
                       elements only deleted from the queue through this stack.
        """
        self.inbound_stack = []
        self.outbound_stack = []

    def __str__(self):
        inbound_comp = [str(el.val) for el in self.inbound_stack]
        outbound_comp = [str(el.val) for el in self.outbound_stack]
        return f'inbound_stack: [{"->".join(inbound_comp)}] ' \
               f'outbound_stack: [{"->".join(outbound_comp)}]'

    def enqueue(self, key, value):
        """
        `append` is used to mimic the `push` operation, which pushes
        elements to the top of the stack.
        """
        el = DoublyNode(key, value)
        self.inbound_stack.append(el)

    def dequeue(self):
        """"
         first checks whether the `outbound_stack` is empty or not. If it is not
         empty, we proceed to remove the element at the front of the queue.
         If it is empty instead, all the elements in `inbound_stack` are moved
         to `outbound_stack` before the front element in the queue is popped out
        """
        if not self.outbound_stack:
            while self.inbound_stack:
                self.outbound_stack.append(self.inbound_stack.pop())
        return self.outbound_stack.pop()

    def peek(self):
        if self.outbound_stack:
            return self.outbound_stack[-1].val
        elif self.inbound_stack:
            return self.inbound_stack[0].val
        else:
            return None


if __name__ == '__main__':
    naive_queue = NaiveArrayQueue()
    print(naive_queue.peek())  # None
    naive_queue.enqueue("5", 5)
    naive_queue.enqueue("6", 6)
    naive_queue.enqueue("7", 7)
    print(naive_queue)  # [5->6->7]
    print(naive_queue.peek())  # 5
    naive_queue.dequeue()
    print(naive_queue)  # [6->7]
    print(naive_queue.peek())  # 6
    naive_queue.dequeue()
    print(naive_queue)  # [7]

    queue = StackArrayQueue()
    print(queue.peek())  # None
    queue.enqueue("5", 5)
    queue.enqueue("6", 6)
    print(queue.peek())  # 5
    queue.enqueue("7", 7)
    print(queue)  # inbound_stack: [5->6->7] outbound_stack: []
    print(queue.peek())  # 5
    queue.dequeue()
    print(queue)  # inbound_stack: [] outbound_stack: [7->6]
    print(queue.peek())  # 6
    queue.dequeue()
    print(queue)  # inbound_stack: [] outbound_stack: [7]
    print(queue.peek())  # 7


class LinkedListQueue:
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
        if self.head:
            node = self.head
            self.size -= 1

            if self.size == 0:
                self.head = self.tail = None
            else:
                self.head = node.next
                node.prev = None
            return node.val

    def peek(self):
        """
        return the top element from the stack, or return None if the
        stack is empty
        """
        return self.head.val

    def empty(self):
        """return True if stack is empty, else return false"""
        return self.size == 0


if __name__ == '__main__':
    ll_queue = LinkedListQueue()
    print("Checking if queue is empty:", ll_queue.empty())  # True
    ll_queue.enqueue("1", 1)
    ll_queue.enqueue("2", 2)
    print(ll_queue)  # [1->2]
    ll_queue.enqueue("3", 3)
    ll_queue.enqueue("4", 4)
    print("Checking item on top of queue:", ll_queue.peek())  # 1
    ll_queue.enqueue("5", 5)
    print(ll_queue)  # [1->2->3->4->5]
    print(ll_queue.dequeue())  # 1
    print(ll_queue.dequeue())  # 2
    print(ll_queue)  # [3->4->5]
    ll_queue.enqueue("6", 4)
    print(ll_queue)  # [3->4->5->4]
    print(ll_queue.peek())  # 3
