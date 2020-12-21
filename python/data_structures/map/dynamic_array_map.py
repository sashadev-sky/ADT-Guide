class DynamicArrayMap:
    def __init__(self):
        self.store = []

    def __getitem__(self, key):
        for pair in self.store:
            if pair[0] == key:
                return pair[1]

    def __setitem__(self, key, value):
        for i, pair in enumerate(self.store):
            if pair[0] == key:
                self.store[i][1] = value
                return
        self.store.append([key, value])

    def __delitem__(self, key):
        for pair in self.store:
            if pair[0] == key:
                self.store.remove(pair)
