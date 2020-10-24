# -*- coding:utf-8 -*-
__doc__ = "反转链表"


class Node(object):
    """单链表的结点"""

    def __init__(self, item):
        # item存放数据元素
        self.item = item
        # next是下一个节点的标识
        self.next = None

    def __repr__(self):  # 递归打印链表串
        return "{} -> ".format(self.item)


class SingleLinkList(object):
    """单链表"""

    def __init__(self):
        self._head = None
        self._end = None

    def is_empty(self):
        """判断链表是否为空"""
        return self._head is None

    def length(self):
        """链表长度"""
        # 初始指针指向head
        cur = self._head
        count = 0
        # 指针指向None 表示到达尾部
        while cur is not None:
            count += 1
            # 指针下移
            cur = cur.next
        return count

    # 创建单链表
    def create(self, node_list):
        for k, v in enumerate(node_list):
            if k == 0:
                self._head = Node(v)
                self._end = self._head
            else:
                p = self._end
                p.next = Node(v)
                self._end = p.next

    def items(self):
        """遍历链表"""
        # 获取head指针
        cur = self._head
        # 循环遍历
        while cur is not None:
            # 返回生成器
            yield cur.item
            # 指针下移
            cur = cur.next

    def print(self):
        """遍历打印链表"""
        # 获取head指针
        cur = self._head
        # 循环遍历
        while cur is not None:
            # 返回生成器
            print(cur.item, end=',')
            # 指针下移
            cur = cur.next
        print("\n--------------")

    def add(self, item):
        """向链表头部添加元素"""
        node = Node(item)
        # 新结点指针指向原头部结点
        node.next = self._head
        # 头部结点指针修改为新结点
        self._head = node

    def append(self, item):
        """尾部添加元素"""
        node = Node(item)
        # 先判断是否为空链表
        if self.is_empty():
            # 空链表，_head 指向新结点
            self._head = node
            self._end = node
        else:
            # 不是空链表，则找到尾部，将尾部next结点指向新结点
            cur = self._head
            while cur.next is not None:
                cur = cur.next
            cur.next = node
            self._end = node

    def insert(self, index, item):
        """指定位置插入元素"""
        # 指定位置在第一个元素之前，在头部插入
        if index <= 0:
            self.add(item)
        # 指定位置超过尾部，在尾部插入
        elif index > (self.length() - 1):
            self.append(item)
        else:
            # 创建元素结点
            node = Node(item)
            cur = self._head
            # 循环到需要插入的位置
            for i in range(index - 1):
                cur = cur.next
            node.next = cur.next
            cur.next = node

    def remove(self, item):
        """删除节点"""
        cur = self._head
        pre = None
        while cur is not None:
            # 找到指定元素
            if cur.item == item:
                # 如果第一个就是删除的节点
                if not pre:
                    # 将头指针指向头节点的后一个节点
                    self._head = cur.next
                else:
                    # 将删除位置前一个节点的next指向删除位置的后一个节点
                    pre.next = cur.next
                return True
            else:
                # 继续按链表后移节点
                pre = cur
                cur = cur.next

    def find(self, item):
        """查找元素是否存在"""
        return item in self.items()

    # def reverse(self):  # FIXME 想办法通过翻转单个note节点达到链表翻转
    #     """翻转链表"""
    #     pre, cur = None, self._head
    #     # pre, cur = self._head.next, self._head
    #     pre, cur = self._head, self._head.next
    #     # print(pre, cur)
    #     while cur:
    #         cur.next, pre, cur = pre, cur, cur.next  # 无中间变量交换
    #     return pre

    def reverse(self):
        """翻转链表"""
        # 非递归实现
        if self._head is None:
            return self._head
        last = None  # 指向上一个节点
        while self._head:
            # 先用tmp保存head的下一个节点的信息，保证单链表不会因为失去head节点的next而就此断裂
            tmp = self._head.next
            # 保存完next，就可以让head的next指向last了
            self._head.next = last
            # 让last，head依次向后移动一个节点，继续下一次的指针反转
            last = self._head
            self._head = tmp
        return last

    # def __repr__(self):  # 递归打印链表串
    #     return "{}".format(self._head)


line = SingleLinkList()
# for x in range(1, 10):
#     line.append(x)
line.create(range(10))

print(line._head, line._end)
print("原始链表:", type(line))  # before: f next:->e next:->d next:->c next:->b next:->a next:->None
line.print()
line.reverse()
print("翻转链表:", type(line))  # before: f next:->e next:->d next:->c next:->b next:->a next:->None
line.print()

# def reverseList(head: Node) -> Node:
#     pre, cur = None, head
#     while cur:
#         cur.next, pre, cur = pre, cur, cur.next  # 无中间变量交换
#     return pre
#
#
# reverseList(line._head)
# print("翻转后:", line, type(line))  # after: a next:->b next:->c next:->d next:->e next:->f next:->None
#
#
# def reverseListNoRec(line):
#     head = line._head
#     # 非递归实现
#     if head is None:
#         return head
#     last = None  # 指向上一个节点
#     while head:
#         # 先用tmp保存head的下一个节点的信息，保证单链表不会因为失去head节点的next而就此断裂
#         tmp = head.next
#         # 保存完next，就可以让head的next指向last了
#         head.next = last
#         # 让last，head依次向后移动一个节点，继续下一次的指针反转
#         last = head
#         head = tmp
#     # return last
#
#
# reverseListNoRec(line)
# print("翻转后:", line, type(line))  # after: a next:->b next:->c next:->d next:->e next:->f next:->None
#
#
# def ReverseListRec(head):
#     # 递归实现
#     if not head or not head.next:
#         return head
#     else:
#         newHead = ReverseListRec(head.next)
#         head.next.next = head
#         head.next = None
#         return newHead
#
#
# line = ReverseListRec(line._head)
# print("再翻转还原:", line, type(line))
# # after and after: f next:->e next:->d next:->c next:->b next:->a next:->None
