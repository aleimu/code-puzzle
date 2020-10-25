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
        last = None  # 上一个节点
        while cur is not None:
            # 找到指定元素
            if cur.item == item:
                # 如果第一个就是删除的节点
                if not last:
                    # 将头指针指向头节点的后一个节点
                    self._head = cur.next
                else:
                    # 将删除位置前一个节点的next指向删除位置的后一个节点
                    last.next = cur.next
                return True
            else:
                # 继续按链表后移节点
                last = cur
                cur = cur.next

    def find(self, item):
        """查找元素是否存在"""
        return item in self.items()

    def reverse1(self):  # 通过翻转单个note节点达到链表翻转
        """翻转链表"""
        # 非递归实现
        if not self._head or not self._head.next:
            return self._head
        last = None  # 指向上一个节点,以备后用
        cur = self._head  # 当前节点,也可以不定义变量直接参与循环,此处为了方便理解,单独定义变量
        while cur:
            # 先用next_tmp保存head的下一个节点的信息，保证单链表不会因为失去head节点的next而就此断裂(内部循环使用)
            next_tmp = cur.next
            # 下一跳已经保存好,可以开始修改当前节点的下一跳了,也就是上一个节点last,初始头的上一个是没有的即None
            cur.next = last
            # 记录下修改后的当前节点,并保存跟新'上一个节点'给下次用.
            last = cur
            # 当前节点处理完毕,更新为备份好的原先的下一个节点
            cur = next_tmp
        # 最后一个节点变成了头节点
        self._head = last

    def reverse2(self):
        last, cur = None, self._head
        while cur:
            # cur.next, last, cur = last, cur, cur.next  # 无中间变量交换,链式赋值生效顺序从左到右.
            print(cur, cur.next, last)
            # last, cur, cur.next = cur, cur.next, last  # 异常   (详见 交换变量.py)
            cur, cur.next, last = cur.next, last, cur  # 异常
            break
        self._head = last

    """Python 的链式赋值顺序是 自左往右
    x = [1, 2, 3, 4, 5]
    i = 0
    i = x[i] = 3
    正确的答案却是：变量 i 首先被赋值为 3，然后 x[3] 再被赋值为3，所以最终变量 x 的值为 [1, 2, 3, 3, 5]。
    """

    def reverse3(self, cur):
        # 递归实现
        if not cur or not cur.next:
            return cur
        else:
            newHead = self.reverse3(cur.next)
            cur.next.next = cur
            cur.next = None
            self._head = newHead
            return newHead

    # def __repr__(self):  # 递归打印链表串
    #     return "{}".format(self._head)


line = SingleLinkList()
# for x in range(1, 10):
#     line.append(x)
line.create(range(10))
print(line._head, line._end)
print("原始链表:", type(line))
line.print()
# print("翻转链表:", type(line))
# line.print()
# line.reverse1()
# print("翻转链表:", type(line))
# line.print()
line.reverse2()
print("翻转链表:", type(line))
line.print()
# line.reverse3(line._head)
# print("翻转链表:", type(line))
line.print()