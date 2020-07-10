class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


def swap_pairs(node: Node):
    """
    两两翻转链表
    """

    def swap(n: Node):
        if not n or not n.next:
            return n
        tmp = n.next
        n.next = swap(tmp.next)
        tmp.next = n
        return tmp

    return swap(node)


def swap_paris2(node: Node):
    """
    两两翻转链表，迭代版
    """
    dummy = Node(-1)
    prev_node = dummy

    while node and node.next:
        first = node
        second = node.next

        prev_node.next = second
        node = second.next
        second.next = first

        prev_node = first

    prev_node.next = node

    return dummy.next


def cross_list(list1: Node, list2: Node):
    """
    分叉链表求交点
    """
    p1, p2 = list1, list2

    while p1 != p2:
        p1 = p1.next
        p2 = p2.next
        if p1 is None:
            p1 = list2
        if p2 is None:
            p2 = list1
    return p1


def reverse_recursion(node: Node):
    """
    迭代翻转链表
    """

    def reverse(n: Node):
        if not n or not n.next:
            return n
        tmp = reverse(n.next)
        n.next.next = n
        n.next = None

        return tmp
    return reverse(node)


def reverse_loop(node: Node):
    prev = None

    while node:
        tmp = node
        node = node.next
        tmp.next = prev
        prev = tmp

    return prev


def has_cycle(node: Node):
    if not node:
        return False
    slow, fast = node, node

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True
    return False


def cross_point(node: Node):
    if not node:
        return None
    slow, fast = node, node

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow2 = node
            while slow2 != slow:
                slow = slow.next
                slow2 = slow2.next
            return slow
    return None


def print_list(list_node):
    while list_node:
        print(list_node.val, end=' -> ')
        list_node = list_node.next
    print('None')


def create_list(nodes):
    if not nodes:
        return None
    t = Node(nodes[0])
    temp = t
    for i in nodes:
        temp.next = Node(i)
        temp = temp.next
    return t.next


if __name__ == '__main__':
    # print_list(reverse_loop(create_list([1, 2, 3, 4, 5])))
    t = create_list([1, 2, 3, 4, 5])
    t.next.next.next.next.next = t.next.next.next
    print(cross_point(t))
