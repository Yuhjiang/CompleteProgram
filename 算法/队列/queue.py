class ListNode:
    def __init__(self, value: int):
        self.val = value
        self.next = None


class Queue(object):
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def enqueue(self, value: int):
        new_node = ListNode(value)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def dequeue(self):
        deleted_node = self.front

        if self.is_empty():
            return None
        elif self._size == 1:
            self.front = self.rear = None
        else:
            self.front = deleted_node.next
        self._size -= 1

        return deleted_node
