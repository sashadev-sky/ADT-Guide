from dataclasses import dataclass, field
from typing import ClassVar, Self
from collections.abc import Callable

from python.linked_list.linked_list import DoublyLinkedList
from python.linked_list.node import DoublyNode

class LRUDoublyNode(DoublyNode):
    def __repr__(self) -> str:
        return (
            f'Node: key: {self.key}, val: {self.val}, '
            f'has next: {bool(self.next)}, has prev: {bool(self.prev)}'
        )

@dataclass
class LRUDoublyLinkedList(DoublyLinkedList):
    head: LRUDoublyNode = LRUDoublyNode(None, None)
    tail: LRUDoublyNode = LRUDoublyNode(None, None)
    head.next, tail.prev = tail, head

    def append(self, node: LRUDoublyNode) -> None:
        """
        Adds the given node to the end of the list (before tail)
        """

        previous = self.tail.prev

        # All nodes other than self.head are guaranteed to have non-None previous
        assert previous is not None

        previous.next = node
        node.prev = previous
        self.tail.prev = node
        node.next = self.tail

    def remove(self, node: LRUDoublyNode) -> LRUDoublyNode | None:
        """
        Removes and returns the given node from the list

        Returns None if node.prev or node.next is None
        """

        if node.prev is None or node.next is None:
            return None

        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None
        return node

    def __repr__(self) -> str:
        rep = ['LRUDoublyLinkedList']
        node = self.head
        while node.next is not None:
            rep.append(str(node))
            node = node.next
        rep.append(str(self.tail))
        return ',\n    '.join(rep)

@dataclass
class LRUCache:
    """
    LRU Cache to store a given capacity of data. Can be used as a stand-alone object
    or as a function decorator.
    """

    # class variable to map the decorator functions to their respective instance
    decorator_function_to_instance_map: ClassVar[dict[Callable, Self]] = {}

    capacity: int
    list: LRUDoublyLinkedList = field(default_factory=LRUDoublyLinkedList)
    num_keys = 0
    hits = 0
    miss = 0
    cache: dict[str, LRUDoublyNode] = field(default_factory=dict[str, LRUDoublyNode])

    def __repr__(self) -> str:
        """
        Return the details for the cache instance [hits, misses, capacity, current_size]
        """

        return (
            f'CacheInfo(hits={self.hits}, misses={self.miss}, '
            f'capacity={self.capacity}, current size={self.num_keys})'
        )

    def __contains__(self, key) -> bool:
        return key in self.cache

    def get(self, key):
        """
        Returns the value for the input key and updates the Doubly Linked List.
        Returns None if key is not present in cache
        """
        # Note: pythonic interface would throw KeyError rather than return None

        if key in self.cache:
            self.hits += 1
            value_node: LRUDoublyNode = self.cache[key]
            node = self.list.remove(self.cache[key])
            assert node == value_node

            # node is guaranteed not None because it is in self.cache
            assert node is not None
            self.list.append(node)
            return node.val
        self.miss += 1
        return None

    def put(self, key, value) -> None:
        """
        Sets the value for the input key and updates the Doubly Linked List
        """

        if key not in self.cache:
            if self.num_keys >= self.capacity:
                # delete first node (oldest) when over capacity
                first_node = self.list.head.next

                # guaranteed to have a non-None first node when num_keys > 0
                # explain to type checker via assertions
                assert first_node is not None
                assert first_node.key is not None
                assert (
                    self.list.remove(first_node) is not None
                )  # node guaranteed to be in list assert node.key is not None

                del self.cache[first_node.key]
                self.num_keys -= 1
            self.cache[key] = LRUDoublyNode(key, value)
            self.list.append(self.cache[key])
            self.num_keys += 1

        else:
            # bump node to the end of the list, update value
            node = self.list.remove(self.cache[key])
            assert node is not None  # node guaranteed to be in list
            node.val = value
            self.list.append(node)

    @classmethod
    def decorator(cls, size: int = 128) -> Callable[[Callable], Callable]:
        """
        Decorator version of LRU Cache
        """

        def cache_decorator_inner(func: Callable) -> Callable:
            def cache_decorator_wrapper(*args):
                if func not in cls.decorator_function_to_instance_map:
                    cls.decorator_function_to_instance_map[func] = LRUCache(size)

                result = cls.decorator_function_to_instance_map[func].get(args[0])
                if result is None:
                    result = func(*args)
                    cls.decorator_function_to_instance_map[func].put(args[0], result)
                return result

            def cache_info() -> LRUCache:
                return cls.decorator_function_to_instance_map[func]

            setattr(cache_decorator_wrapper, 'cache_info', cache_info)

            return cache_decorator_wrapper

        return cache_decorator_inner


if __name__ == '__main__':
    cache = LRUCache(2)

    print(1 in cache) # False
    cache.put(1, 1)
    print(1 in cache) # True
    cache.put(2, 2)
    print(cache.get(1)) # 1

    print(repr(cache.list))
    # LRUDoublyLinkedList,
    #     None: None,
    #     2: 2,
    #     1: 1,
    #     None: None

    print(cache.cache)
    # {1: Node: key: 1, val: 1, has next: True, has prev: True, 2: Node: key: 2, val: 2, has next: True, has prev: True}

    cache.put(3, 3)

    print(repr(cache.list))
    # {1: Node: key: 1, val: 1, has next: True, has prev: True, 3: Node: key: 3, val: 3, has next: True, has prev: True}

    print(cache.cache)
    # LRUDoublyLinkedList,
    #     None: None,
    #     1: 1,
    #     3: 3,
    #     None: None

    print(cache.get(2)) # None
    cache.put(4, 4)
    print(cache.get(1)) # None
    print(cache.get(3)) # 3
    print(cache.get(4)) # 4
    print(repr(cache)) # CacheInfo(hits=3, misses=2, capacity=2, current size=2)

    @LRUCache.decorator(100)
    def fib(num):
        if num in (1, 2):
            return 1
        return fib(num - 1) + fib(num - 2)

    for i in range(1, 100):
        res = fib(i)

    print(fib.cache_info()) # CacheInfo(hits=194, misses=99, capacity=100, current size=99)
