class DynamicArraySet:
    """
    Alternate array-based set implementation that doesn't require the set
    elements to be hashable.
    """
    # ratio of value count to size of array on which it should be upsized
    RESIZE_FACTOR_UP = 2 / 3
    # ratio of value to size of array on which it should be downsized
    RESIZE_FACTOR_DOWN = 1 / 4
    _MIN_SIZE = 4

    def __init__(self, size=10):
        self.n = 0

        # minimum size in memory
        if size >= DynamicArraySet._MIN_SIZE:
            self.size = size
        else:
            self.size = DynamicArraySet._MIN_SIZE

        # allocate array
        self.store = [None for _ in range(self.size)]

    def contains(self, value: int) -> bool:
        """
        Check if the passed value exists in the underlying array
        """
        for el in self.store:
            if el == value:
                return True
        return False

    def add(self, value: int) -> bool:
        """
        Add the value in the first empty space in the underlying array
        """
        if value not in self.store:
            self.n += 1
            if self.n >= self.size:
                self._resize(1.0)

            for idx, el in enumerate(self.store):
                if el is None:
                    self.store[idx] = value
                    break

            return True
        return False

    def delete(self, value: int) -> bool:
        """
        Delete the value from the underlying array.
        """
        if value in self.store:
            self.n -= 1
            capacity_ratio = self._capacity_ratio()
            if capacity_ratio <= DynamicArraySet.RESIZE_FACTOR_DOWN:
                self._resize(capacity_ratio)

            for idx, el in enumerate(self.store):
                if el == value:
                    self.store[idx] = None
                    break

            return True
        return False

    def _resize(self, capacity_ratio: float):
        """
        Resize the underlying array if there is too much or not enough free
        space
        """
        if (
            0 <= capacity_ratio < 1
            and self.size / 1.5 >= DynamicArraySet._MIN_SIZE
        ):
            tmp_store = [None for _ in range(int(self.size / 1.5))]
            idx = 0
            for el in self.store:
                if el is not None:
                    tmp_store[idx] = el
                    idx += 1

            self.store = tmp_store
            self.size = len(tmp_store)

        elif capacity_ratio >= DynamicArraySet.RESIZE_FACTOR_UP:
            self.store.extend([None for _ in range(int(self.size * 1.5))])
            self.size = int(self.size * 1.5)

    def __str__(self) -> str:
        return f'{{{", ".join(map(str, self.store))}}}'

    def __iter__(self) -> iter:
        return iter(self.store)

    def __len__(self) -> int:
        return len(self.store)

    def _capacity_ratio(self) -> float:
        return self.n / self.size


if __name__ == '__main__':
    list_set = DynamicArraySet()
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
