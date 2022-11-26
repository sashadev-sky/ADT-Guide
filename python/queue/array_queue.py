from python.linked_list.node import SinglyNode

class NaiveArrayQueue:
    def __init__(self):
        self.items = []
        self.size = 0

    def __str__(self):
        return f'[{"->".join(str(item.val) for item in self.items)}]'

    def __len__(self):
        """Return the number of elements in the queue."""
        return self.size

    def enqueue(self, key, value):
        node = SinglyNode(key, value)
        self.items.append(node)
        self.size += 1
        return node.val

    def dequeue(self):
        node = self.items.pop(0)
        self.size -= 1
        return node.val

    def is_empty(self):
        return False if self.items else True

    def first(self):
        return self.items[0].val if self.items else None

# clever Queue implementation using an array.
# Constant time complexity (amortized)

class StackQueue:
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
        el = SinglyNode(key, value)
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

    def is_empty(self):
        return False if self.outbound_stack or self.inbound_stack else True

    def first(self):
        if self.outbound_stack:
            return self.outbound_stack[-1].val
        elif self.inbound_stack:
            return self.inbound_stack[0].val
        else:
            return None


if __name__ == '__main__':
    naive_queue = NaiveArrayQueue()
    print(naive_queue.first())  # None
    print(naive_queue.is_empty())  # True
    naive_queue.enqueue("5", 5)
    naive_queue.enqueue("6", 6)
    naive_queue.enqueue("7", 7)
    print(naive_queue.is_empty())  # False
    print(naive_queue)  # [5->6->7]
    print(naive_queue.first())  # 5
    naive_queue.dequeue()
    print(naive_queue)  # [6->7]
    print(naive_queue.first())  # 6
    naive_queue.dequeue()
    print(naive_queue)  # [7]

    queue = StackQueue()
    print(queue.first())  # None
    print(queue.is_empty()) # True
    queue.enqueue("5", 5)
    queue.enqueue("6", 6)
    print(queue.is_empty()) # False
    print(queue.first())  # 5
    queue.enqueue("7", 7)
    print(queue)  # inbound_stack: [5->6->7] outbound_stack: []
    print(queue.first())  # 5
    queue.dequeue()
    print(queue)  # inbound_stack: [] outbound_stack: [7->6]
    print(queue.first())  # 6
    queue.dequeue()
    print(queue)  # inbound_stack: [] outbound_stack: [7]
    print(queue.first())  # 7
