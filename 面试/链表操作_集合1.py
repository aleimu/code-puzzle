'''
    Python版单向链表-单向链表简称单链表
    单链表中所包含的基本操作：
    初始化
    创建
    链表生成器
    打印
    显示调用过程
    计算长度
    判空
    获取
    删除
    插入
    修改
    追加
    逆转单向链表
'''


class Node(object):
    # 节点初始化
    def __init__(self, value, p=None):
        self.value = value
        self.next = p


class LinkList(object):
    # 初始化单链表
    def __init__(self):
        self.head = None

    # 创建单链表
    def create(self, node_value_list):
        self.head = Node(node_value_list[0])
        p = self.head
        for i in node_value_list[1:]:
            p.next = Node(i)
            p = p.next

    # 生成单链表
    def generate(self):
        p = self.head
        while p:
            yield p.value
            p = p.next

    # 打印单链表
    def print(self):
        print([i for i in self.generate()])

    # 显示方法调用前后的单链表
    def show(func):
        def wrapper(self, *args):
            print("方法{func_name}执行前".format(func_name=func.__name__))
            self.print()
            print("方法{func_name}执行中".format(func_name=func.__name__))
            func(self, *args)
            print("方法{func_name}执行后".format(func_name=func.__name__))
            self.print()

        return wrapper

    # 获取单链表的长度
    def length(self):
        p = self.head
        length = 0
        while p:
            length += 1
            p = p.next
        return length

    # 判断单链表是否为空
    def is_null(self):
        return self.length() == 0

    # 获取单链表偏移位元素返回并打印其节点值
    # 支持顺序索引和逆序索引：0代表索引0位，-1代表倒数第一位，-2代表倒数第二位
    # 获取不存在的位返回None
    def get(self, offset):
        p = self.head
        index = 0
        length = self.length()
        if offset > length - 1:
            print(None)
            return None
        if offset < 0 and offset + length < 0:
            print(None)
            return None
        if offset < 0 and offset + length >= 0:
            offset = length + offset
        while index < length - 1 and index < offset:
            p = p.next
            index += 1
        print("获取索引{index}位节点-值为{value}".format(index=index, value=p.value))
        return p

    # 删除单链表偏移位元素并打印
    # 支持顺序索引和逆序索引：0代表索引0位，-1代表倒数第一位，-2代表倒数第二位
    # 删除不存在的位返回None
    @show
    def remove(self, offset):
        p = self.head
        length = self.length()
        index = 0
        if offset > length - 1:
            print(None)
            return None
        if offset == 0 or offset + length == 0:
            print("删除索引{index}位节点-值为{value}".format(index=index, value=self.head.value))
            self.head = p.next
            return None
        if offset < 0 and length + offset > 0:
            offset = length + offset
        while index < length - 1 and index < offset - 1:
            p = p.next
            index += 1
        print("删除索引{index}位节点-值为{value}".format(index=index + 1, value=p.next.value))
        p.next = p.next.next

    # 在指定index位插入节点-值为value
    # 什么是插入——在两个节点之间加入才叫插入
    # 所以在末尾插入的意思就是在索引倒数第二位和倒数第一位之间插入
    @show
    def insert(self, offset, value):
        length = self.length()
        # 如果偏移量对应的索引位不在链表对应索引位范围内-返回None
        if offset > length - 1 or offset + length < 0:
            return None
        if offset < 0:
            offset = offset + length
        node = Node(value)
        if offset == 0 or offset + length == 0:
            p = self.head
            self.head = node
            node.next = p
        else:
            previous_node = self.get(offset - 1)
            current_node = self.get(offset)
            previous_node.next = node
            node.next = current_node
        print("在索引{index}位插入节点-值为{value}".format(index=offset, value=value))

    # 在链表索引末位追加一个节点-值为value
    @show
    def append(self, value):
        last_node = self.get(self.length() - 1)
        last_node.next = Node(value)

    # 修改链表索引位节点值
    @show
    def modify(self, offset, value):
        self.get(offset).value = value

    # 逆向生成单向链表
    @show
    def reverse(self):
        # 将节点生成器转变为列表并逆序
        reverse_list = [i for i in self.generate()][::-1]
        self.create(reverse_list)
        # self.head = Node(reverse_list[0])
        # p = self.head
        # for i in reverse_list[1:]:
        #     p.next = Node(i)
        #     p = p.next


if __name__ == '__main__':
    list = [1, 2, 33, 4, 55, 6, 76, 78]
    # 初始化链表
    link_list = LinkList()
    # 创建链表
    link_list.create(list)
    # 获取节点
    link_list.get(-1)
    # 删除节点
    link_list.remove(0)
    # 插入节点
    link_list.insert(-2, 0.2)
    # 末位追加节点
    link_list.append(3)
    # 修改节点值
    link_list.modify(-1, 666)
    # 逆转
    link_list.reverse()
