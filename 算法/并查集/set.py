class Set(object):
    def __init__(self, size):
        self.data = [-1] * size

    def find(self, element):
        if self.data[element] < 0:
            return element
        else:
            return self.find(self.data[element])

    def union(self, set1, set2):
        set1 = self.find(set1)
        set2 = self.find(set2)
        if self.data[set1] < self.data[set2]:
            self.data[set1] += self.data[set2]
            self.data[set2] = set1
        else:
            self.data[set2] += self.data[set1]
            self.data[set1] = set2


if __name__ == '__main__':
    s = Set(10)
    s.union(2, 3)
    print(s.data)
    s.union(1, 2)
    print(s.data)
