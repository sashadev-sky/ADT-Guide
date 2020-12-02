class HashSet:
    """
    Alternate array-based set implementation that doesn't require the set
    elements to be hashable.
    """
    # ratio of value count to size of array on which it should be upsized
    RESIZE_FACTOR_UP = 2 / 3
    # ratio of value to size of array on which it should be downsized
    RESIZE_FACTOR_DOWN = 1 / 4
    _MIN_SIZE = 8

    def __init__(self, size=10):
        self.n = 0

        if size >= HashSet._MIN_SIZE:
            self.size = size
        else:
            self.size = HashSet._MIN_SIZE

        self.store = [[None] for _ in range(self.size)]

    def _hash_function(self, value):
        return hash(value) % self.size

    def _contains(self, value):
        for idx, e in enumerate(self.store[self._hash_function(value)]):
            if value == e:
                return idx
            # return idx if value == e else -1
        return -1

    def contains(self, value):
        return self._contains(value) >= 0

    def add(self, value):
        if not self.contains(value):
            self.n += 1
        self.store[self._hash_function(value)].append(value)
        self._resize()

    def delete(self, value):
        # decrement amount of elements if you remove element that existed
        index = self._contains(value)
        if index >= 0:
            self.n -= 1
            self.store[self._hash_function(value)].pop(index)
            self._resize()

    def _resize(self):
        capacity_ratio = self._capacity_ratio()
        # shrink array if there is less than SHRINK_FACTOR elements
        if (
                capacity_ratio < HashSet.RESIZE_FACTOR_DOWN
                and self.size / 2 >= HashSet._MIN_SIZE
        ):
            self._create_resized_array(self.size / 2)
        # grow array if there is more than then GROWTH_FACTOR elements
        if capacity_ratio > HashSet.RESIZE_FACTOR_UP:
            self._create_resized_array(self.size * 2)

    def _create_resized_array(self, new_size):
        new_element_array = [[] for _ in range(int(new_size))]
        self.size = len(new_element_array)
        for bucket in self.store:
            for e in bucket:
                # uses new function
                new_element_array[self._hash_function(e)].append(e)
        self.store = new_element_array

    def __iter__(self):
        for bucket in self.store:
            if bucket:
                for e in bucket:
                    yield e
        raise StopIteration()

    def __str__(self):
        return f"size: {self.size} elements: {self.store}"

    def _capacity_ratio(self) -> float:
        return self.n / self.size


if __name__ == '__main__':
    list_set = HashSet()
    for i in range(40):
        list_set.add(i * 4)
        print(list_set)

    print(list_set.contains(4))  # True
    print(list_set.contains(44))  # True
    print(list_set.contains(40))  # True

    print(list_set.contains(41))  # False

    for i in range(40):
        print(list_set.delete(i * 4))
        print(list_set)