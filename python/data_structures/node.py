class SinglyNode:
    def __init__(self, key=None, val=None, next_node=None):
        self.key = key
        self.val = val
        self.next = next_node

    def __str__(self):
        return f"{self.key}: {self.val}"


class DoublyNode(SinglyNode):
    def __init__(self, key=None, val=None, next_node=None, prev_node=None):
        super().__init__(key=key, val=val, next_node=next_node)
        self.prev = prev_node
