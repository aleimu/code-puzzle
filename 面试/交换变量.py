__doc__ = """
Python的变量并不直接存储值，而只是引用一个内存地址，交换变量时，只是交换了引用的地址。
在 2、3 个值分配的时候是直接运用栈，在 3 个以上值分配的时候才是用了拆包的原理。

https://www.v2ex.com/t/483347   # 一些讨论
https://stackoverflow.com/questions/21047524/how-does-swapping-of-members-in-tuples-a-b-b-a-work-internally # 一行交换变量的两种原理
https://www.cnblogs.com/aydenwang/p/9398826.html    # 四种交换变量的方法
"""

import dis


def swap2(a, b):
    a, b = b, a  # ROT_TWO
    print(a, b)


def swap3(a, b, c):
    a, b, c = c, b, a  # ROT_THREE ROT_TWO
    print(a, b, c)


def swap4(a, b, c, d):
    a, b, c, d = d, c, b, a  # BUILD_TUPLE UNPACK_SEQUENCE
    print(a, b, c, d)


def swap5(a, b, c, d, e):
    a, b, c, d, e = e, d, c, b, a  # BUILD_TUPLE UNPACK_SEQUENCE
    print(a, b, c, d, e)


def swap55(a, b, c, d, e):
    a, b, c, d, e = d, e, a, c, b  # BUILD_TUPLE UNPACK_SEQUENCE
    print(a, b, c, d, e)


def swap():
    """交换变量,不涉及引用"""
    a, b, c, d, e = 10, 20, 30, 40, 50

    swap2(a, b)
    dis.dis(swap2)

    swap3(a, b, c)
    dis.dis(swap3)

    swap4(a, b, c, d)
    dis.dis(swap4)

    swap5(a, b, c, d, e)
    dis.dis(swap5)

    swap55(a, b, c, d, e)
    dis.dis(swap55)


"""
python3.8
ROT_TWO ROT_THREE ROT_FOUR 这样的指令可以直接交换两个变量,三个变量,四个变量,但是上面的例子中并没用到ROT_FOUR.

Python 将右侧表达式与左侧赋值分开。
首先计算右侧，结果存储在堆栈上，然后使用再次从堆栈中引用值的操作代码从左到右分配左侧名称。

对于包含 2 个或 3 个项目的元组分配，Python 仅直接使用堆栈.

"""


class Node(object):
    """单链表的结点"""

    def __init__(self, item):
        # item存放数据元素
        self.item = item
        # next是下一个节点的标识
        self.next = None

    # def __repr__(self):
    #     return "{} -> ".format(self.item)

    # def __getattr__(self, item):
    #     print('get')
    #     return super().__getattr__(item)
    #     # return self[item]

    # def __setattr__(self, key, value):
    #     print('set', key, value)
    #     super().__setattr__(key, value)


class SingleLinkList(object):
    """单链表"""

    def __init__(self):
        self._head = None
        self._end = None

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

    # 不考虑操作顺序反转必须要操作的步骤有:cur.next=last,last=cur,cur=cur.next,这样一共有6中操作
    def reverse1(self):
        """交换变量,3种正常:左侧cur都是在cur.next之后改的,遍历顺序不会断裂"""
        last, cur = None, self._head
        while cur:
            cur.next, cur, last = last, cur.next, cur  # 无中间变量交换,等式右边先计算,然后链式赋值从左到右.
            # cur.next, last, cur = last, cur, cur.next  # 同上
            # last, cur.next, cur = cur, last, cur.next  # 同上
        self._head = last

    """
    124          16 LOAD_FAST                1 (last)   # 从左到右,以此取值
                 18 LOAD_FAST                2 (cur)
                 20 LOAD_ATTR                1 (next)
                 22 LOAD_FAST                2 (cur)
                 24 ROT_THREE
                 26 ROT_TWO                             # 从左到右以此赋值
                 28 LOAD_FAST                2 (cur)    # 获取cur引用
                 30 STORE_ATTR               1 (next)   # 修改当前节点
                 32 STORE_FAST               2 (cur)    # 变更cur应用
                 34 STORE_FAST               1 (last)   
    """

    def reverse2(self):
        """交换变量,3种异常:左侧curl在curl.next前被赋值,导致遍历顺序断裂"""
        last, cur = None, self._head
        while cur:
            cur, cur.next, last = cur.next, last, cur
            # cur, last, cur.next = cur.next, cur, last
            # last, cur, cur.next = cur, cur.next, last
        self._head = last

    """
    146          16 LOAD_FAST                2 (cur)    # 从左到右,以此取值
                 18 LOAD_ATTR                1 (next)
                 20 LOAD_FAST                1 (last)
                 22 LOAD_FAST                2 (cur)
                 24 ROT_THREE
                 26 ROT_TWO                             # 从左到右以此赋值
                 28 STORE_FAST               2 (cur)    # 变更cur
                 30 LOAD_FAST                2 (cur)    # 获取最新cur引用
                 32 STORE_ATTR               1 (next)   # 变更最新cur的next
                 34 STORE_FAST               1 (last)
                 36 JUMP_ABSOLUTE           12
    """

    def reverse_swap(self):
        """异常:AttributeError: 'NoneType' object has no attribute 'next'"""
        last, cur = None, self._head
        while cur:
            print('前:', cur, cur.next, last)
            # 异常,cur值先被修改,导致cur.next取的值已经是被修改后的cur,导致链表断裂
            # cur, cur.next, last = cur.next, last, cur
            # cur, last, cur.next = cur.next, cur, last
            # last, cur, cur.next = cur, cur.next, last

            # 正常,cur.next先被修改,再把cur引用被覆盖并不会影响之前已经被修改的cur节点以及cur.next
            cur.next, cur, last = last, cur.next, cur  # 无中间变量交换,等式右边先计算,然后链式赋值从左到右.
            # cur.next, last, cur = last, cur, cur.next  # 同上
            # last, cur.next, cur = cur, last, cur.next  # 同上
            print('后:', cur, cur.next, last)
            # break
        self._head = last

    def reverse_swap2(self):  # 通过翻转单个note节点达到链表翻转
        """翻转链表"""
        # 非递归实现
        if not self._head or not self._head.next:
            return self._head
        last = None  # 指向上一个节点,以备后用
        cur = self._head  # 当前节点,也可以不定义变量直接参与循环,此处为了方便理解,单独定义变量
        while cur:  # 不会像上面那种有多种顺序,用这种零时变量的方式,顺序只有这一种.主要是因为链式交换等式的右侧已经入栈固定了在随后的网左侧赋值时不会改变.
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


line = SingleLinkList()
line.create(range(10))
print('-------------------1')
dis.dis(line.reverse1)
print('-------------------2')
dis.dis(line.reverse2)
# line.reverse_swap()
# line.print()
line.reverse_swap2()
line.print()

"""dis每一列的意思:
https://docs.python.org/zh-cn/3/library/dis.html?highlight=dis#module-dis

第一列：对应的源代码行数。
第二列：对应的内存字节码的索引位置。
第三列：内部机器代码的操作。
第四列：指令参数。
第五列：实际参数。

LOAD_FAST(var_num)
将指向局部对象 co_varnames[var_num] 的引用推入栈顶。

STORE_FAST(var_num)
将 TOS 存放到局部对象 co_varnames[var_num]。

BUILD_TUPLE(count)
创建一个使用了来自栈的 count 个项的元组，并将结果元组推入栈顶。

UNPACK_SEQUENCE(count)
将 TOS 解包为 count 个单独的值，它们将按从右至左的顺序被放入堆栈。

POP_TOP
删除堆栈顶部（TOS）项。

ROT_TWO
交换两个最顶层的堆栈项。

ROT_THREE
将第二个和第三个堆栈项向上提升一个位置，顶项移动到位置三。

ROT_FOUR
将第二个，第三个和第四个堆栈项向上提升一个位置，将顶项移动到第四个位置。
"""
