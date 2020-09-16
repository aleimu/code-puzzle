# 一个节点的数据类型，包含左子孩子节点指针 右孩子节点指针 和值
class Node(object):
    def __init__(self, item):
        self.left = None  # 指向左子节点
        self.right = None  # 指向右子节点
        self.item = item  # 保存值


# 树的类
class Tree(object):
    def __init__(self):
        self.root = None  # 保存树根所在位置

    # 添加节点方法，按照层次由低到高，优先靠左的思想添加
    def add(self, item):
        node = Node(item)  # 首先创建一个节点
        # 如果树还没有树根
        if self.root is None:
            self.root = node
        else:
            # 这里需要用到广度优先遍历的思想来找第一个可以添加节点的位置
            # 开一个队列用于广度优先搜索 先把树根放进去
            queue = [self.root]
            # 循环操作：
            # 出队一个节点，如果它没有左海子，为它添加左孩子 退出  否则 左孩子入队列
            #            如果他没有右孩子，为它添加右孩子 退出  否则 右孩子如队列
            # 如果队列里面有元素我们就一直操作。队列空了就退出来（这个只是保险条件，一般队列还没空就找到空位创建节点然后退出了）
            while queue:
                # 取出队节点
                temp = queue.pop(0)
                # 如果没有左孩子 我们 添加左孩子后退出
                if temp.left is None:
                    temp.left = node
                    return
                # 如果有左孩子 我们把左孩子入队列
                else:
                    queue.append(temp.left)

                # 如果没有右孩子 我们添加右孩子 然后退出
                if temp.right is None:
                    temp.right = node
                    return
                # 如果有右孩子 我们把右孩子入队列
                else:
                    queue.append(temp.right)

    # 广度优先遍历
    def breadth_travel(self):
        # 开启一个队列 把树根放进去
        queue = [self.root]
        # 循环操作：从对头取出节点，把值输出后 把他们的左孩子右孩子添加到队列里，一直到队列空了，说明遍历结束
        # 只要队列不是空的 我们就一直遍历
        while queue:
            # 从队列头取出一个元素
            temp = queue.pop(0)
            # 输出节点的值
            print(temp.item, end=" ")
            # 如果节点有左孩子 就把左孩子追加到队列
            if temp.left is not None:
                queue.append(temp.left)
            # 如果节点有右孩子 就把右孩子追加到队列
            if temp.right is not None:
                queue.append(temp.right)
        # 最后来一个换行
        print()

    # 先序遍历  按照 根 左 右 进行遍历
    # 把当前子树的树根传进去做参数
    def preOder(self, node):
        # 如果传进来的十个None，说明上一个节点 没有左孩子或者右孩子 传进来一个None 那就不遍历这个节点
        if not node:
            return
        # 先把根的值输出来
        print(node.item, end=" ")
        # 然后对左孩子进行遍历
        self.preOder(node.left)
        # 然后对右孩子遍历
        self.preOder(node.right)

    # 中序遍历 按照 左 根 右 的顺序进行遍历
    # 传入当前要遍历的子树的根
    def inOrder(self, node):
        # 当传入的子树是None 说明上一个节点没有这个子树 传进来了None 此时不用遍历它了
        if not node:
            return None
        # 先对左子树进行遍历
        self.inOrder(node.left)
        # 再输出自己的数值
        print(node.item, end=" ")
        # 最后对右子树进行遍历
        self.inOrder(node.right)

    # 后序遍历 按照 左 右 根 的顺序进行遍历
    # 把当前子树的树根传进去做参数
    def postOrder(self, node):
        # 如果传进来一个None 说明上一个节点没有这可子树，这时候不用遍历
        if not node:
            return
        # 先对左子树进行遍历
        self.postOrder(node.left)
        # 再对右子树进行遍历
        self.postOrder(node.right)
        # 最后输出自己的值
        print(node.item, end=" ")

    # 我们再封装一下，在外部调用自己的三个深度优先遍历可以不传入自己的根
    def preOrder_travel(self):
        self.preOder(self.root)

    def inOrder_travel(self):
        self.inOrder(self.root)

    def postOrder_travel(self):
        self.postOrder(self.root)


if __name__ == '__main__':
    tree = Tree()
    tree.add(1)
    tree.add(2)
    tree.add(3)
    tree.add(4)
    tree.add(5)
    tree.add(6)
    tree.add(7)
    tree.breadth_travel()  # 1 2 3 4 5 6 7
    tree.preOrder_travel()  # 1 2 4 5 3 6 7
    print()  # 回车换行
    tree.inOrder_travel()  # 4 2 5 1 6 3 7
    print()  # 回车换行
    tree.postOrder_travel()  # 4 5 2 6 7 3 1
