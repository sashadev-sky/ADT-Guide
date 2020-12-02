import sys

class DynamicArraySet:
    """
    Alternate array-based `Set` implemented with a Python `list`.
    Initially implemented as 1-dimensional list of integers, then augmented
    to a 2-dimensional list of lists containing integers, as described in
    the "Set" section of the `README.md`.

    The list mimics a naive implementation of a dynamic array for educational
    purposes, providing dynamic memory allocation, traversal, insertion and
    removal. In reality a Python list is already a dynamic array, just like
    the Ruby `Array`, as opposed to a static array like in Java.

    This implementation prioritizes space over speed. It limits the valid
    set of contained elements to integers, as the integers are used to
    compute an index into an array of buckets (sub-arrays). Bucket lookup is 0(
    1), then an 0(n) scan finds the correct element in the bucket.

    Lists are equivalent to C or Pascal arrays in their time complexity;
    the primary difference is that a Python list can contain objects of many d
    different types. (lists in C are static) This is thanks to hashing. Update
    this
    class to use
    hashing so that it can store other than integers.


    """
    # What is the ideal growth factor? aka whenever you'd push_back into a
    # vector without there being room, it would multiply the current
    # capacity by growth factor
    # It will entirely depend on the use case. Do you care more about the
    # time wasted copying data around (and reallocating arrays) or the extra
    # memory? How long is the array going to last? If it's not going to be
    # around for long, using a bigger buffer may well be a good idea - the
    # penalty is short-lived. If it's going to hang around that's obviously
    # more of a penalty.

    # There's no such thing as an "ideal growth factor." It's not just
    # theoretically application dependent, it's definitely application
    # dependent.

    # 2 was not a good choice: it can be mathematically proven that a
    # growth factor of 2 is rigorously the worst possible because it never
    # allows the vector to reuse any of its previously-allocated memory.

    # any number smaller than 2 guarantees that you'll at some point be able
    # to reuse the previous chunks. For instance, choosing 1.5 as the factor
    # allows memory reuse after 4 reallocations; 1.45 allows memory reuse
    # after 3 reallocations; and 1.3 allows reuse after only 2 reallocations.
    # We're using 1.5, by the 6th time you will reuse the memory.
    # https://github.com/facebook/folly/blob/master/folly/docs/FBVector.md
    GROWTH_FACTOR = 3 / 2
    SHRINK_FACTOR = 3 / 1

    M_SIZE = 8  # the number of buckets (sub-lists / rows / rank) the list
    # structure will have. This is fixed, which allows us to maintain
    # a contiguous place in memory. This will be the "rows".
    #
    # An example of a contingious memory 2D array structure: an image - its
    # just a 2-D arrays of pixels

    def __init__(self, size=M_SIZE):
        self.n = 0

        if size < 0:
            raise ValueError('size should be a positive integer')

        self.size = int(size)

        # note `[obj] * n` creates a list containing `n` references to the
        # same object, not copies, meaning trying to mutate it at a specific
        # index would update it throughout the entire list instead.
        # To avoid this behavior, only do this if `obj` is immutable.
        # Better yet, use the comprehension.
        # nested: [[None for _ in range(2)] for _ in range(10)]

        # The array is stored in row-column order. That is, the first row is
        # stored sequentially in memory followed by the second row.
        self.store = [[None] for _ in range(self.size)]

    @staticmethod
    def _capacity_ratio(sub_list: list[int], sub_count: int) -> float:
        return sub_count / len(sub_list)

    def capacity_ratio(self) -> float:
        return self.n / self.size

    def contains(self, value: int) -> bool:
        """
        Check if the passed value exists in the underlying array. This will
        become `ResizableArraySet`'s `__contains__` magic method, triggered
        when performing a membership test with thee `in` operator
        """

        if 0 <= value % self.size + 1 <= len(self.store):
            sub_list = self.store[value % self.size]

            for el in sub_list:
                if el == value:
                    return True
        return False

    __contains__ = contains

    def add(self, value: int) -> bool:
        """
        Add the value in the first empty space in the underlying array
        """
        if value not in self:
            self.n += 1
            sub_list = self.store[value % self.size]
            sub_count = 0

            for idx, el in enumerate(sub_list):
                if el is None:
                    sub_list[idx] = value
                    return True

                sub_count += 1
            if sub_count >= len(sub_list):
                self._resize(sub_list, DynamicArraySet.GROWTH_FACTOR)
            sub_list.append(value)
            return True
        return False

    def delete(self, value: int) -> bool:
        """
        Delete the value from the underlying array.
        """
        if value in self:
            self.n -= 1
            sub_list = self.store[value % self.size]
            for idx, el in enumerate(sub_list):
                if el == value:
                    del sub_list[idx]
                    break

            if len(sub_list) > 1:
                capacity_ratio = self.capacity_ratio()

                if (
                        capacity_ratio == 0
                        or 1 / capacity_ratio <= DynamicArraySet.SHRINK_FACTOR
                ):
                    self._resize(sub_list, DynamicArraySet.SHRINK_FACTOR)
            return True
        return False

    def _resize(self, sub_list: list[int], factor: float):
        """
        Resize the underlying array if there is too much or not enough free
        space
        """
        if factor == DynamicArraySet.SHRINK_FACTOR:
            tmp_store = []
            for el in sub_list:
                if el is not None:
                    tmp_store.append(el)
            sub_list = tmp_store

        elif factor == DynamicArraySet.GROWTH_FACTOR:
            num_elements = int((len(sub_list) * DynamicArraySet.GROWTH_FACTOR))
            tmp_store = []
            for el in sub_list:
                if el is not None:
                    tmp_store.append(el)

            tmp_store.extend([None for _ in range(num_elements)])
            sub_list = tmp_store


    # if __repr__ is defined, and __str__ is not, the object will behave as
    # though __str__=__repr__.

    # Container’s __str__ uses contained objects’ __repr__

    #   Implement __repr__ for any class you implement. This should be second
    #   nature.

    #   Implement __str__ if you think it would be useful to have a string
    #   version which errs on the side of readability, i.e if you need a
    #   “pretty print” functionality (for example, used by a report generator).
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(size: {self.size}, count:' \
               f' {self.n}, store: [\n\t{self.ad()}\n ])'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(size: {self.size}, count:' \
                f' {self.n}, store: {self.store}'

    def ad(self):
        return "\n\t".join(["<id=" + str(id(l)) + " bytes=" + str(
            sys.getsizeof(l)) + "> " + str(l) for
                            l in
                            self])

    # maks our class iterable, ie. allows `[sub_list for sub_list in self]`
    def __iter__(self) -> iter:
        return iter(self.store)


if __name__ == '__main__':
    list_set = DynamicArraySet()
    for i in range(40):
        list_set.add(i)
        print(repr(list_set))

        # the printed output makes sense: the minimum size of an empty list in
        # 64-bit Python 3 is 56 bytes (used to be 64, just recently got
        # smaller by 8 bytes) and then another 8 bytes for the contained element

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

    print(list_set.contains(4))  # True
    print(list_set.contains(44))  # True
    print(list_set.contains(40))  # True

    print(list_set.contains(41))  # False

    for i in range(40):
        list_set.delete(i)
        print(repr(list_set))
    print(list_set)
