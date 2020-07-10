class HashTable(object):
    def __init__(self):
        self.table_size = 17
        self.table = []
        for i in range(self.table_size):
            self.table.append([])

    def __contains__(self, item):
        return self._has(item)

    def _hash(self, s):
        total = 0
        factor = 1
        for c in s:
            asc = ord(c)
            total += asc * factor
            factor *= 10
        return total

    def _index(self, key):
        index = self._hash(key) % self.table_size
        return index

    def _has(self, key):
        index = self._index(key)
        v = self.table[index]
        for data in v:
            if data[0] == key:
                return True

    def __len__(self):
        length = 0
        for v in self.table:
            length = length + len(v)
        return length

    def __setitem__(self, key, value):
        return self.add(key, value)

    def add(self, key, value):
        index = self._index(key)
        self._insert_or_update(index, key, value)

    def _insert_or_update(self, index, key, value):
        v = self.table[index]
        found = False

        for data in v:
            if data[0] == key:
                data[1] = value
                return True
        if not found:
            data = [key, value]
            v.append(data)

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, default_value=None):
        index = self._index(key)
        v = self.table[index]
        for data in v:
            if data[0] == key:
                return data[1]
        return default_value


if __name__ == '__main__':
    memo = HashTable()
    memo['a'] = 1
    memo['b'] = 2
    print(memo['a'])
