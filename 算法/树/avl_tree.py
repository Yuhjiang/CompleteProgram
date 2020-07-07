"""
平衡二叉搜索树
"""
from typing import Optional


class TreeNode:
    def __init__(self, element: int):
        self.element: int = element
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None
        self.height: int = 0


def get_height(node: TreeNode):
    if node:
        return node.height
    else:
        return 0


def single_left_rotation(node: TreeNode) -> TreeNode:
    """
    左单旋: 1.有左节点  2.插入节点在左节点左边
    :param node:
    :return:
    """
    left = node.left
    node.left = left.right
    left.right = node

    node.height = max(get_height(node.left), get_height(node.right))+1
    left.height = max(get_height(node), get_height(left.left)) + 1

    return left


def single_right_rotation(node: TreeNode) -> TreeNode:
    """
    右单旋: 1.有右节点  2.插入节点在右节点右边
    :param node:
    :return:
    """
    right = node.right
    node.right = right.left
    right.left = node

    node.height = max(get_height(node.right), get_height(node.left)) + 1
    right.height = max(get_height(node), get_height(node.right)) + 1

    return right


def double_left_right_rotation(node: TreeNode) -> TreeNode:
    """
    左右双旋: 1.有左节点  2.左节点有右节点  3.插入节点在左节点右边
    :param node:
    :return:
    """
    node.left = single_right_rotation(node.left)

    return single_left_rotation(node)


def double_right_left_rotation(node: TreeNode) -> TreeNode:
    """
    右左双旋: 1.有右节点  2.右节点有左节点  3.插入节点在右节点左边
    :param node:
    :return:
    """
    node.right = single_left_rotation(node.right)

    return single_right_rotation(node)


def insert_tree_node(node: TreeNode, element: int):
    if node is None:
        node = TreeNode(element)
    elif element < node.element:
        node.left = insert_tree_node(node.left, element)

        if get_height(node.left) - get_height(node.right) == 2:
            if element < node.left.element:
                node = single_left_rotation(node)
            else:
                node = double_left_right_rotation(node)
    elif element > node.element:
        node.right = insert_tree_node(node.right, element)

        if get_height(node.right) - get_height(node.left) == 2:
            if element > node.right.element:
                node = single_right_rotation(node)
            else:
                node = double_right_left_rotation(node)
    else:
        pass
    node.height = max(get_height(node.left), get_height(node.right)) + 1

    return node
