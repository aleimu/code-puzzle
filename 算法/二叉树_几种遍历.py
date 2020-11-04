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

    def preOrder1(self, node):
        """前序遍历 -递归版"""
        if node == None:
            return
        # 先打印根结点，再打印左结点，后打印右结点
        print("前序遍历-递归版", node.data)
        # fixme 见惯了那种return时进入递归当前函数,这种多递归的还挺好玩,当然还有这种[面试.链表操作_集合2.SingleLinkList.reverse3]在出递归时将进递归的后半部代码继续执行
        self.preOrder1(node.left)  # 会进入递归,至到把左树遍历完
        self.preOrder1(node.right)  # 再进入递归,至到把右树遍历完

    def preOrder2(self, node):
        """前序遍历 -迭代版"""
        stack, res = [], []
        current = node
        while current or stack:
            while current:
                res.append(current.data)
                stack.append(current)
                current = current.left  # 先遍历左节点
            current = stack.pop()
            current = current.right
        print("前序遍历-迭代版", res)
        return res

    def inOrder1(self, node):
        """中序遍历"""
        if node == None:
            return
        # 先打印左结点，再打印根结点，后打印右结点
        self.inOrder1(node.left)
        print("中序遍历-递归版", node.data)
        self.inOrder1(node.right)

    def inOrder2(self, node):
        """中序遍历-迭代版"""
        stack, res = [], []
        current = node
        while current or stack:
            while current:
                stack.append(current)
                current = current.left  # 先遍历左节点
            current = stack.pop()
            res.append(current.data)  # 根节点
            current = current.right  # 右节点
        print("中序遍历-迭代版", res)
        return res

    def postOrder1(self, node):
        """后序遍历-递归版本"""
        if node == None:
            return
        # 先打印左结点，再打印右结点，后打印根结点
        self.postOrder1(node.left)
        self.postOrder1(node.right)
        print("后序遍历-递归版", node.data)

    def postOrder2(self, node):
        """后序遍历-迭代版"""
        stack, res = [], []
        current, last = node, None
        while current or stack:
            while current:
                stack.append(current)
                current = current.left  # 先遍历左节点
            current = stack[-1]
            if not current.right or current.right == last:
                current = stack.pop()
                res.append(current.data)  # 根节点
                last = current
                current = None
            else:
                current = current.right  # 右节点
        print("后序遍历-迭代版", res)
        return res

    def levelOrder1(self, node):
        """层次遍历 -迭代版"""
        if not node:
            return None
        res = {}
        self.dfs(node, 0, res)
        print("层次遍历 -迭代版", res)
        return res

    def dfs(self, node, step, res):
        if node:
            if not res.get(step):
                res[step] = []
            res[step].append(node.data)
            self.dfs(node.left, step + 1, res)
            self.dfs(node.right, step + 1, res)

    def levelOrder2(self, node):
        """层次遍历 -迭代版"""
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

    def depthOrder(self, node):
        """深度遍历"""
        if node == None:
            return 0
        left, right = self.depthOrder(node.left), self.depthOrder(node.right)
        return max(left, right) + 1


n1 = BinaryTreeNode(data="D")
n2 = BinaryTreeNode(data="E")
n3 = BinaryTreeNode(data="F")
n4 = BinaryTreeNode(data="B", left=n1, right=n2)
n5 = BinaryTreeNode(data="C", left=n3, right=None)
root = BinaryTreeNode(data="A", left=n4, right=n5)

bt = BinaryTree(root)

bt.preOrder1(bt.root)
bt.preOrder2(bt.root)
bt.inOrder1(bt.root)
bt.inOrder2(bt.root)
bt.postOrder1(bt.root)
bt.postOrder2(bt.root)
bt.depthOrder(bt.root)
bt.levelOrder1(bt.root)
bt.levelOrder2(bt.root)
