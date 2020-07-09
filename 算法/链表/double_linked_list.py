from typing import Optional


class ListNode:
    def __init__(self, val: int):
        self.val = val
        self.next = None
        self.previous = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    @property
    def length(self):
        _len = 0
        tmp = self.head
        while tmp:
            _len += 1
            tmp = tmp.next
        return _len

    def insert_at_head(self, value: int):
        # 头部插入数据
        new_node = ListNode(value)
        if not self.head:
            self.tail = new_node
        else:
            self.head.previous = new_node
        new_node.next = self.head
        self.head = new_node

    def delete_at_head(self):
        # 头部删除数据
        tmp = self.head
        self.head = tmp.next
        if not self.head:
            self.tail = None
        else:
            self.head.previous = None

        return tmp

    def insert_at_tail(self, value):
        # 尾部插入数据
        new_node = ListNode(value)
        if not self.tail:
            self.head = new_node
        else:
            self.tail.next = new_node
        new_node.previous = self.tail
        self.tail = new_node

    def delete_at_tail(self):
        tmp = self.tail
        self.tail = tmp.previous
        if not self.tail:
            self.head = None
        else:
            self.tail.next = None

        return tmp

    def insert_at_index(self, value: int, index: int):
        if index == 1:
            self.insert_at_head(value)
        elif index == self.length + 1:
            self.insert_at_tail(value)
        else:
            new_node = ListNode(value)
            tmp = self.head
            for _ in range(index-1):
                tmp = tmp.next
            new_node.next = tmp.next
            tmp.next.previous = new_node
            tmp.next = new_node
            new_node.previous = tmp

    def delete_at_index(self, index):
        if index == 1:
            return self.delete_at_head()
        elif index == self.length:
            return self.delete_at_tail()
        else:
            tmp = self.head
            for _ in range(index-1):
                tpm = tmp.next
            tmp.previous.next = tmp.next
            tmp.next.previous = tmp.previous


if __name__ == '__main__':
    pass
