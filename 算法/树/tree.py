class TreeNode(object):
    def __init__(self, element):
        self.element = element
        self.left = None
        self.right = None


def preorder_traversal(node: TreeNode):
    """
    先序遍历
    """
    if node:
        print(node.element)
        preorder_traversal(node.left)
        preorder_traversal(node.right)


def postorder_traversal(node: TreeNode):
    """
    后序遍历
    """
    if node:
        postorder_traversal(node.left)
        postorder_traversal(node.right)
        print(node.element)


def inorder_traversal(node: TreeNode):
    """
    中序遍历
    """
    if node:
        inorder_traversal(node.left)
        print(node.element)
        inorder_traversal(node.right)


def level_traversal(node: TreeNode):
    """
    层序遍历
    """
    queue = []
    if node:
        queue.append(node)

    while queue:
        tmp = queue.pop(0)
        print(tmp.element)
        if tmp.left:
            queue.append(tmp.left)
        if tmp.right:
            queue.append(tmp.right)


def invert(node: TreeNode):
    """
    左右节点翻转
    """
    if not node:
        return None
    node.left, node.right = node.right, node.left
    invert(node.left)
    invert(node.right)


def tree_search(node: TreeNode, element: int):
    """
    二叉树搜索
    """
    if node.element == element:
        return node
    if node.left:
        return tree_search(node.left, element)
    if node.right:
        return tree_search(node.right, element)
