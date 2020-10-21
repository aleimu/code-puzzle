# -*- coding: utf-8 -*-

class node(object):
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


# 深度
def depth(tree):
    if tree == None:
        return 0
    left, right = depth(tree.left), depth(tree.right)
    return max(left, right) + 1


# 层次遍历
def level_order(tree):
    if tree == None:
        return
    q = []
    q.append(tree)
    while q:
        current = q.pop(0)

        if current.left != None:
            print(current.data)
            q.append(current.left)
        if current.right != None:
            q.append(current.right)


tree = node('D', node('B', node('A'), node('C')), node('E', right=node('G', node('F'))))
level_order(tree)

print(depth(tree))


class Solution:

    def TreeDeep(self, root):  # 获取树高度
        if not root:
            return 0
        left = self.TreeDeep(root.left) + 1
        right = self.TreeDeep(root.right) + 1
        return left if left > right else right

    def LevelLeft(self, node, i):
        reString = ""
        if not node or i < 1:
            return reString
        if i == 1:
            return str(node.data)
        reString = self.LevelLeft(node.left, i - 1)  # 先遍历左树
        if reString == "":
            reString = self.LevelLeft(node.right, i - 1)  # 再遍历右树
        return reString

    def levelOrderBottom(self, root):
        if not root:
            return
        depth = self.TreeDeep(root)
        for i in range(1, 1 + depth):
            re = self.LevelLeft(root, i)  # 依据层次重新遍历树
            print(re)


a = Solution()
a.levelOrderBottom(tree)


class Solution:
    def printRightNode(self, root):
        q1, q2 = [], []
        tmp = node(0)
        if not root:
            return
        q1.append(root)
        while len(q1) != 0 or len(q2) != 0:
            count1 = 0
            while len(q1) != 0:
                tmp = q1[0]
                q1.pop(0)
                if count1 == 0:
                    print(tmp.val)
                count1 += 1
                if (tmp.left):
                    q2.append(tmp.left)
                if (tmp.right):
                    q2.append(tmp.right)
            count2 = 0
            while len(q2) != 0:
                tmp = q2[0]
                q2.pop(0)
                if count2 == 0:
                    print(tmp.val)
                count2 += 1
                if (tmp.left):
                    q1.append(tmp.left)
                if (tmp.right):
                    q1.append(tmp.right)

    def levelOrderBottom(self, root):
        if not root:
            return
        self.printRightNode(root)
