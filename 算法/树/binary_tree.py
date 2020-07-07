"""
二叉搜索树
"""
from typing import Optional


class TreeNode:
    def __init__(self, element: int):
        self.element: int = element
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None

    def find_min(self):
        temp = self
        while temp.left:
            temp = temp.left

        return temp


def insert_tree_node(node: TreeNode, element: int):
    if node is None:
        return TreeNode(element)

    if element < node.element:
        node.left = insert_tree_node(node.left, element)
    else:
        node.right = insert_tree_node(node.right, element)


def delete_tree_node(node: TreeNode, element: int):
    if node is None:
        return None

    if element < node.element:
        node.left = delete_tree_node(node.left, element)
    elif element > node.element:
        node.right = delete_tree_node(node.right, element)
    else:
        # 被删除节点有左右两个子节点
        if node.left and node.right:
            temp = node.right.find_min()
            node.element = temp.element
            node.right = delete_tree_node(node.right, temp.element)
        elif not node.left:
            node = node.right
        else:
            node = node.left
    return node
