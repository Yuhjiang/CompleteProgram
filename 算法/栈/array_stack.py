from array import array
from typing import Optional


class ArrayStack(object):
    def __init__(self, capacity=10):
        self._items = array('i', [0 for _ in range(capacity)])
        self._capacity = capacity
        self._size = 0

    def __iter__(self):
        cursor = 0
        while cursor < self._size:
            yield self._items[cursor]
            cursor += 1

    def peek(self):
        return self._items[self._size-1]

    def clear(self):
        self._size = 0
        self._items = array('i', [0 for _ in range(self._capacity)])

    def push(self, item):
        self._items[self._size] = item
        self._size += 1

    def pop(self):
        item = self._items[self._size - 1]
        self._size -= 1
        return item


class StackNode:
    def __init__(self, val):
        self.val = val
        self.next = None


class LinkedStack(object):
    def __init__(self):
        self._items: Optional[StackNode] = None
        self._size = 0

    def __iter__(self):
        tmp_list = []

        def visit_nodes(node: StackNode):
            if node:
                visit_nodes(node)
                tmp_list.append(node)
        visit_nodes(self._items)
        return iter(tmp_list)

    def peek(self):
        if self._size:
            return self._items.val
        else:
            raise KeyError('The stack is empty')

    def clear(self):
        self._size = 0
        self._items = 0

    def push(self, item: int):
        tmp = StackNode(item)
        tmp.next = self._items
        self._items = tmp
        self._size += 1

    def pop(self):
        if not self._size:
            raise KeyError('The stack is empty')
        tmp = self._items
        self._items = tmp.next
        self._size -= 1

        return tmp
