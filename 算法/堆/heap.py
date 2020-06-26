class Heap(object):
    def __init__(self):
        self.data = []
        self._size = 0

    @staticmethod
    def _parent(i):
        return (i - 1) // 2

    @staticmethod
    def _left(i):
        return i * 2 + 1

    @staticmethod
    def _right(i):
        return i * 2 + 2

    def _has_left(self, i):
        return self._left(i) < self._size

    def _has_right(self, i):
        return self._right(i) < self._size

    def _upheap(self, i):
        """
        从i位置开始上滤
        """
        new_item = self.data[i]

        parent = self._parent(i)
        while parent >= 0:
            if new_item < self.data[parent]:
                self.data[i] = self.data[parent]
                i = parent
                parent = self._parent(parent)
            else:
                break
        self.data[i] = new_item

    def add(self, other):
        self._size += 1
        self.data.append(other)
        self._upheap(self._size-1)

    def _downheap(self, i):
        """
        从i位置开始下滤
        """
        if not self.size:
            return None
        x = self.data[i]
        while self._has_left(i):
            child = self._left(i)
            if self._has_right(i) and \
                    self.data[child] > self.data[self._right(i)]:
                child = self._right(i)

            if self.data[child] < x:
                self.data[i] = self.data[child]
                i = child
            else:
                break
        self.data[i] = x

    @property
    def size(self):
        return self._size

    def heapify(self):
        for i in range(self._size // 2)[::-1]:
            self._downheap(i)

    def is_empty(self):
        return self._size == 0

    def remove_min(self):
        if self.is_empty():
            return None
        result = self.data.pop(0)
        self._size -= 1

        self._downheap(0)

        return result


if __name__ == '__main__':
    heap = Heap()
    for j in range(10, 0, -1):
        heap.add(j)

    print(heap.data)
    heap.data = heap.data[::-1]
    heap.heapify()
    print(heap.data)

    for j in range(heap.size):
        print(heap.remove_min(), heap.data)
