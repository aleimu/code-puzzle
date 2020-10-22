# -*- coding:utf-8 -*-
__doc__ = "反转链表"


class ListNode:
    def __init__(self, x, next):
        self.value = x
        self.next = next

    def __repr__(self):  # 递归打印链表串
        return "{} next:->{}".format(self.value, self.next)


a = ListNode('a', None)
b = ListNode('b', a)
c = ListNode('c', b)
d = ListNode('d', c)
e = ListNode('e', d)
f = ListNode('f', e)

print("before:", f)  # before: f next:->e next:->d next:->c next:->b next:->a next:->None


def reverseList(head: ListNode) -> ListNode:
    pre, cur = None, head
    while cur:
        cur.next, pre, cur = pre, cur, cur.next  # 无中间变量交换
    return pre


def reverseListNoRec(head):
    # 非递归实现
    if head is None:
        return head
    last = None  # 指向上一个节点
    while head:
        # 先用tmp保存head的下一个节点的信息，保证单链表不会因为失去head节点的next而就此断裂
        tmp = head.next
        # 保存完next，就可以让head的next指向last了
        head.next = last
        # 让last，head依次向后移动一个节点，继续下一次的指针反转
        last = head
        head = tmp
    return last


print("after:", reverseListNoRec(f))  # after: a next:->b next:->c next:->d next:->e next:->f next:->None


def ReverseListRec(head):
    # 递归实现
    if not head or not head.next:
        return head
    else:
        newHead = ReverseListRec(head.next)
        head.next.next = head
        head.next = None
        return newHead


print("after and after:", ReverseListRec(a))
# after and after: f next:->e next:->d next:->c next:->b next:->a next:->None
