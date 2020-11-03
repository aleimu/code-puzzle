__doc__ = """
判断二叉树是否镜像对称
"""


class Node(object):
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


tree1 = Node('D',
             Node('B',
                  left=Node('G',
                            left=None,
                            right=None),
                  right=None),
             Node('B',
                  left=None,
                  right=Node('S',
                             left=None,
                             right=Node('F'))))

tree = Node('D',
            Node('B',
                 left=Node('G',
                           left=Node('F'),
                           right=None),
                 right=None),
            Node('B',
                 left=None,
                 right=Node('G',
                            left=None,
                            right=Node('F'))))


def mirror_tree(node: Node):
    """
    迭代方式判断,层次遍历
    """
    if not node:
        return False
    stack = []
    stack.append(node.left)
    stack.append(node.right)
    while stack:
        right = stack.pop()
        left = stack.pop()
        if right == None and left == None:  # 很重要的前置判断
            continue
        if left == None or right == None:  # 很重要的前置判断
            return False
        if right.data != left.data:
            return False
        stack.append(right.right)  # 注意加入的次序
        stack.append(left.left)
        stack.append(right.left)
        stack.append(left.right)
    return True


print(mirror_tree(tree))
print(mirror_tree(tree1))


def mirror_tree(node: Node):
    """递归版本"""
    if not node:
        return True
    return check_same(node.left, node.right)


def check_same(left: Node, right: Node):
    if left == None and right == None:
        return True
    if left == None or right == None:
        return False
    return left.data == right.data and check_same(left.left, right.right) and check_same(right.left, left.right)


print(mirror_tree(tree))
print(mirror_tree(tree1))
