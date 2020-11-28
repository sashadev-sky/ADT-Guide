class ResizableArray:
    """
    Alternate array-based set implementation favoring space over speed
    and not requiring the set elements to be hashable.
    """
    # ratio of element count to size of array on which it should be upsized
    RESIZE_FACTOR_UP = 2 / 3
    # ratio of element to size of array on which it should be downsized
    RESIZE_FACTOR_DOWN = 1 / 4
    # minimal size of the array (the size is not shrunk below this size)
    _MIN_SIZE = 10

    def __init__(self):
        self.n = 0  # current actual size (number of elements)
        self.size = ResizableArray._MIN_SIZE  # maximum memory size
        # allocate array
        self.store = [None for _ in range(ResizableArray._MIN_SIZE)]

    def contains(self, element):
        """
        Check if the passed element exists in the underlying array
        """
        for el in self.store:
            if el == element:
                return True
        return False

    __contains__ = contains

    def add(self, element):
        """
        Add the element in the first empty space in the underlying array
        """
        if element not in self.store:
            self.n += 1
            if self.n == self.size:
                self._resize(1.0)

            for idx, el in enumerate(self.store):
                if el is None:
                    self.store[idx] = element
                    break

            return True
        return False

    def delete(self, element):
        """
        Delete the element from the underlying array
        """
        if element in self.store:
            self.n -= 1
            capacity_ratio = self._capacity_ratio()
            # if 1 - capacity_ratio >= ResizableArray.RESIZE_FACTOR_UP:
            if capacity_ratio <= ResizableArray.RESIZE_FACTOR_DOWN:
                self._resize(capacity_ratio)

            for idx, el in enumerate(self.store):
                if el == element:
                    self.store[idx] = None
                    break

            return True
        return False

    def _resize(self, capacity_ratio):
        """
        Resize the underlying array if there is too much or not enough free
        space
        """
        if (
            0 <= capacity_ratio < 1
            and self.size / 1.5 >= ResizableArray._MIN_SIZE
        ):
            new_element_array = [None for _ in range(int(self.size / 1.5))]
            idx = 0
            for el in self.store:
                if el is not None:
                    new_element_array[idx] = el
                    idx += 1
                # else:
                #     new_element_array.append(None)
            self.store = new_element_array
            self.size = len(new_element_array)
        # grow array if there is more than then RESIZE_FACTOR_UP elements
        elif capacity_ratio >= ResizableArray.RESIZE_FACTOR_UP:
            for times in range(int(self.size * 1.5)):
                self.store.append(None)
            # self.store.extend([None] * int(self.size / 2))
            self.size = int(self.size * 1.5)

    def __str__(self):
        return f'[{", ".join(map(str, self.store))}]'

    def __iter__(self):
        return iter(self.store)

    def _capacity_ratio(self):
        print(f'{self.n=}')
        print(f'{self.size=}')
        return self.n / self.size


if __name__ == '__main__':
    list_set = ResizableArray()
    for i in range(40):
        list_set.add(i * 4)
        print(list_set)

    print(type(list_set))

    print(list_set.contains(4))  # True
    print(list_set.contains(44))  # True
    print(list_set.contains(40))  # True

    print(list_set.contains(41))  # False
    # for e in list_set:
    #     print(e)

    for i in range(40):
        print(list_set.delete(i * 4))
        print(list_set)
