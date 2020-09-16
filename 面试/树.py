__doc__ = """
树的构造
递归实现先序遍历、中序遍历、后序遍历
堆栈实现先序遍历、中序遍历、后序遍历
队列实现层次遍历


二叉树的遍历通常有前序，中序和后续三种。遍历算法通常使用递归实现:
先序遍历就是先访问树的根节点，再访问树的左子节点，再访问右子节点。
中序遍历就是先访问树的左子节点，再访问树的根节点，再访问右子节点。
先序遍历就是先访问树的左子节点，再访问树的右子节点，再访问根节点。
"""


class Node(object):
    """节点类"""

    def __init__(self, elem=-1, lchild=None, rchild=None):
        self.elem = elem
        self.lchild = lchild
        self.rchild = rchild


class Tree(object):
    """树类"""

    def __init__(self):
        self.root = Node()

    def add(self, elem):
        """为树加入节点"""
        node = Node(elem)
        if self.root.elem == -1:  # 假设树是空的。则对根节点赋值
            self.root = node
        else:
            myQueue = []
            treeNode = self.root
            myQueue.append(treeNode)
            while myQueue:  # 对已有的节点进行层次遍历
                treeNode = myQueue.pop(0)
                if treeNode.lchild == None:
                    treeNode.lchild = node
                    return
                elif treeNode.rchild == None:
                    treeNode.rchild = node
                    return
                else:
                    myQueue.append(treeNode.lchild)
                    myQueue.append(treeNode.rchild)

    def front_digui(self, root):
        """利用递归实现树的先序遍历"""
        if root == None:
            return
        print(root.elem, end=' ')
        self.front_digui(root.lchild)
        self.front_digui(root.rchild)

    def middle_digui(self, root):
        """利用递归实现树的中序遍历"""
        if root == None:
            return
        self.middle_digui(root.lchild)
        print(root.elem, end=' ')
        self.middle_digui(root.rchild)

    def later_digui(self, root):
        """利用递归实现树的后序遍历"""
        if root == None:
            return
        self.later_digui(root.lchild)
        self.later_digui(root.rchild)
        print(root.elem, end=' ')

    def front_stack(self, root):
        """利用堆栈实现树的先序遍历"""
        if root == None:
            return
        myStack = []
        node = root
        while node or myStack:
            while node:  # 从根节点開始，一直找它的左子树
                print(node.elem, end=' ')
                myStack.append(node)
                node = node.lchild
            node = myStack.pop()  # while结束表示当前节点node为空，即前一个节点没有左子树了
            node = node.rchild  # 開始查看它的右子树

    def middle_stack(self, root):
        """利用堆栈实现树的中序遍历"""
        if root == None:
            return
        myStack = []
        node = root
        while node or myStack:
            while node:  # 从根节点開始。一直找它的左子树
                myStack.append(node)
                node = node.lchild
            node = myStack.pop()  # while结束表示当前节点node为空。即前一个节点没有左子树了
            print(node.elem, end=' ')
            node = node.rchild  # 開始查看它的右子树

    def later_stack(self, root):
        """利用堆栈实现树的后序遍历"""
        if root == None:
            return
        myStack1 = []
        myStack2 = []
        node = root
        myStack1.append(node)
        while myStack1:  # 这个while循环的功能是找出后序遍历的逆序，存在myStack2里面
            node = myStack1.pop()
            if node.lchild:
                myStack1.append(node.lchild)
            if node.rchild:
                myStack1.append(node.rchild)
            myStack2.append(node)
        while myStack2:  # 将myStack2中的元素出栈，即为后序遍历次序
            print(myStack2.pop().elem, end=' ')

    def level_queue(self, root):
        """利用队列实现树的层次遍历"""
        if root == None:
            return
        myQueue = []
        node = root
        myQueue.append(node)
        while myQueue:
            node = myQueue.pop(0)
            print(node.elem, end=' ')
            if node.lchild != None:
                myQueue.append(node.lchild)
            if node.rchild != None:
                myQueue.append(node.rchild)


if __name__ == '__main__':
    """主函数"""
    elems = list(range(10))  # 生成十个数据作为树节点
    tree = Tree()  # 新建一个树对象
    for elem in elems:
        tree.add(elem)  # 逐个加入树的节点

    print('队列实现层次遍历:')
    tree.level_queue(tree.root)

    print('\n\n递归实现先序遍历:')
    tree.front_digui(tree.root)
    print('\n递归实现中序遍历:')
    tree.middle_digui(tree.root)
    print('\n递归实现后序遍历:')
    tree.later_digui(tree.root)

    print('\n\n堆栈实现先序遍历:')
    tree.front_stack(tree.root)
    print('\n堆栈实现中序遍历:')
    tree.middle_stack(tree.root)
    print('\n堆栈实现后序遍历:')
    tree.later_stack(tree.root)
