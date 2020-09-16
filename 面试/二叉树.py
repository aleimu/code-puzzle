class BinaryTreeNode(object):
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class BinaryTree(object):
    def __init__(self, root=None):
        self.root = root

    def is_empty(self):
        return self.root == None

    def preOrder(self, node):
        if node == None:
            return
        # 先打印根结点，再打印左结点，后打印右结点
        print(node.data)
        self.preOrder(node.left)
        self.preOrder(node.right)

    def inOrder(self, node):
        if node == None:
            return
        # 先打印左结点，再打印根结点，后打印右结点
        self.inOrder(node.left)
        print(node.data)
        self.inOrder(node.right)

    def postOrder(self, node):
        if node == None:
            return
        # 先打印左结点，再打印右结点，后打印根结点
        self.postOrder(node.left)
        self.postOrder(node.right)
        print(node.data)

    # 深度
    def depthOrder(self, node):
        if node == None:
            return 0
        left, right = self.depthOrder(node.left), self.depthOrder(node.right)
        return max(left, right) + 1

    # 层次遍历
    def levelOrder(self, node):
        if node == None:
            return
        q = []
        q.append(node)
        while q:
            current = q.pop(0)
            print(current.data)
            if current.left != None:
                q.append(current.left)
            if current.right != None:
                q.append(current.right)


n1 = BinaryTreeNode(data="D")
n2 = BinaryTreeNode(data="E")
n3 = BinaryTreeNode(data="F")
n4 = BinaryTreeNode(data="B", left=n1, right=n2)
n5 = BinaryTreeNode(data="C", left=n3, right=None)
root = BinaryTreeNode(data="A", left=n4, right=n5)

bt = BinaryTree(root)
print('先序遍历')
bt.preOrder(bt.root)
print('中序遍历')
bt.inOrder(bt.root)
print('后序遍历')
bt.postOrder(bt.root)
print('深度遍历')
bt.depthOrder(bt.root)
print('层次遍历')
bt.levelOrder(bt.root)