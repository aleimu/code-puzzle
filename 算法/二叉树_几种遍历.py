__doc__ = """二叉树的基础遍历方式"""


class BinaryTreeNode(object):
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class BinaryTree(object):
    """
    tips:前,中,后遍历的命名意思是将处理逻辑代码写在遍历左右子节点的代码的位置.
    """

    def __init__(self, root=None):
        self.root = root

    def is_empty(self):
        return self.root == None

    def preOrder(self, node):
        """前序遍历"""
        if node == None:
            return
        # 先打印根结点，再打印左结点，后打印右结点
        print(node.data)
        # fixme 见惯了那种return时进入递归当前函数,这种多递归的还挺好玩,当然还有这种[面试.链表操作_集合2.SingleLinkList.reverse3]在出递归时将进递归的后半部代码继续执行
        self.preOrder(node.left)  # 会进入递归,至到把左树遍历完
        self.preOrder(node.right)  # 再进入递归,至到把右树遍历完

    def inOrder(self, node):
        """中序遍历"""
        if node == None:
            return
        # 先打印左结点，再打印根结点，后打印右结点
        self.inOrder(node.left)
        print(node.data)
        self.inOrder(node.right)

    def postOrder(self, node):
        """后序遍历"""
        if node == None:
            return
        # 先打印左结点，再打印右结点，后打印根结点
        self.postOrder(node.left)
        self.postOrder(node.right)
        print(node.data)

    def depthOrder(self, node):
        """深度遍历"""
        if node == None:
            return 0
        left, right = self.depthOrder(node.left), self.depthOrder(node.right)
        return max(left, right) + 1

    def levelOrder(self, node):
        """层次遍历"""
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
