from typing import Hashable


class DynamicArraySet:
    def __init__(self, size: int = 4) -> None:
        self.n = 0

        if size < 0:
            raise ValueError('size should be a positive integer')

        self.store = [[] for _ in range(size if size else 1)]

    def contains(self, value: int) -> bool:
        if self.n == 0 or not 0 <= value % self.size <= self.size - 1:
            return False
        return value in self.store[value % self.size]

    __contains__ = contains

    def __iter__(self) -> iter:
        return iter(self.store)

    def __len__(self) -> int:
        return len(self.store)

    def __repr__(self) -> str:
        comp = [str(e) for _ in self for e in _ if e is not None]
        return f'{{{", ".join(comp)}}}'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(size: {self.size}, count: {self.n}' \
               f', store: {self.store})'

    @property
    def size(self) -> int:
        return len(self)

    def add(self, value: int) -> bool:
        if value not in self:
            sub_list = self.store[value % self.size]
            for idx, el in enumerate(sub_list):
                if el is None:
                    sub_list[idx] = value
                    self.n += 1
                    return True

            sub_list.append(value)
            self.n += 1

            if self.size < self.n:
                self._resize()

            return True
        return False

    def discard(self, value: int) -> bool:
        if value in self:
            sub_list = self.store[value % self.size]
            for idx, el in enumerate(sub_list):
                if el == value:
                    del sub_list[idx]
                    self.n -= 1
                    return True
        return False

    def _resize(self):
        flat_list = [e for sl in self for e in sl if e is not None]
        alloc_memory = int((self.n >> 3) + (3 if self.n < 9 else 6))
        self.store = [[] for _ in range(self.size + alloc_memory + 1)]
        self.n = 0
        for el in flat_list:
            self.add(el)

    def difference(self, s: iter) -> list:
        """
        The set of all elements of A that are not elements of B
        Different result if swap A and B
        """
        return [e for _ in self for e in _ if e is not None and e not in s]

    def intersection(self, s: iter) -> list:
        """
        The intersection of two sets includes members that are present in both
        sets.
        Accepts any iterable.
        """
        return [e for _ in self for e in _ if e is not None and e in s]

    __and__ = intersection

    def union(self, s: iter) -> list:
        """
        The union of two sets A and B is the set of elements which are in A,
        in B, or in both A and B.
        Accepts any iterable.
        """
        flat_l = [e for _ in self for e in _ if e is not None]
        other_list = [e for e in s if e not in flat_l]
        flat_l.extend(other_list)
        return flat_l

    __or__ = union


class DynamicHashSet(DynamicArraySet):
    def contains(self, value: Hashable) -> bool:
        if self.n == 0 or not 0 <= hash(value) % self.size <= self.size - 1:
            return False
        return value in self.store[hash(value) % self.size]

    __contains__ = contains

    def add(self, value: Hashable) -> bool:
        if value not in self:
            sub_list = self.store[hash(value) % self.size]
            for idx, el in enumerate(sub_list):
                if el is None:
                    sub_list[idx] = value
                    self.n += 1
                    return True

            sub_list.append(value)
            self.n += 1

            if self.size < self.n:
                self._resize()

            return True
        return False

    def discard(self, value: Hashable) -> bool:
        if value in self:
            sub_list = self.store[hash(value) % self.size]
            for idx, el in enumerate(sub_list):
                if el == value:
                    del sub_list[idx]
                    self.n -= 1
                    return True
        return False


if __name__ == '__main__':
    s1 = DynamicArraySet()
    s2 = set()
    for i in range(40):
        s1.add(i * 4)
        print(s1)
        s2.add(i * 2)

    print(repr(s1))
    print(s2)

    # the printed output from playing around with sys.`getsizeof` makes sense:
    #   - the size of an empty list in 64-bit Python 3 is 56 bytes. For
    #     each element added, another 8 bytes is allocated
    #       - 8 bytes = 64 bits
    #
    # DynamicArraySet(size: 8, count: 1, store: [
    # 	<id=4515156736 bytes=64> [0]
    # 	<id=4515241088 bytes=64> [None]
    # 	<id=4515241024 bytes=64> [None]
    # 	<id=4515240832 bytes=64> [None]
    # 	<id=4515240768 bytes=64> [None]
    # 	<id=4515240640 bytes=64> [None]
    # 	<id=4515240576 bytes=64> [None]
    # 	<id=4515240512 bytes=64> [None]
    #  ])
    #
    #   - allocated size was then increased by 12.5%.
    #   - 56 + 56 * .125 = 88
    #
    # DynamicArraySet(size: 8, count: 9, store: [
    # 	<id=4563446400 bytes=88> [0, 8]
    # 	<id=4563447040 bytes=64> [1]
    # 	<id=4563446976 bytes=64> [2]
    # 	<id=4563446848 bytes=64> [3]
    # 	<id=4563446784 bytes=64> [4]
    # 	<id=4563446720 bytes=64> [5]
    # 	<id=4563446656 bytes=64> [6]
    # 	<id=4563446464 bytes=64> [7]
    #  ])

    z = s1.intersection(s2)
    u = s1.union(s2)
    d = s1.difference(s2)
    print(z)
    print(s1 & s2)
    print(u)
    print(s1 | s2)
    print(d)

    print(len(z))
    print(len(u))

    for i in range(40):
        s1.discard(i * 4)
        print(s1)

    hs1 = DynamicHashSet()
    for i in "hellohey":
        hs1.add(i)
        print(hs1)
