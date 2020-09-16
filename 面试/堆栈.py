class Stack(object):
    """堆栈"""

    def __init__(self, item=[]):
        self.item = []
        if len(item):
            for i in item:
                self.item.append(i)

    def push(self, item):
        self.item.append(item)

    def clear(self):
        del self.item

    def is_empty(self):
        return self.size() == 0

    def size(self):
        return len(self.item)

    def print(self):
        print(self.item)

    def top(self):
        return self.item[-1]

    def pop(self):
        data = self.top()
        self.item.pop()
        return data


print("创建堆栈")
stack = Stack([1, 2, 3])
stack.print()
print("向栈顶插入元素")
stack.push(4)
stack.print()
print("判断堆栈是否为空")
print(stack.is_empty())
print("返回堆栈中项的个数")
print(stack.size())
print("返回栈顶的项")
print(stack.top())
print("删除栈顶的项")
stack.pop()
stack.print()
print("清空堆栈")
print(stack.clear())


class Queue(object):
    """模拟队列"""

    def __init__(self, item=[]):
        self.item = []
        if len(item):
            for i in item:
                self.item.append(i)

    def enqueue(self, item):
        self.item.append(item)

    def dequeue(self):
        self.item.pop(0)

    def clear(self):
        del self.item

    def is_empty(self):
        return self.size() == 0

    def size(self):
        return len(self.item)

    def print(self):
        print(self.item)


print("创建队列")
queue = Queue([1, 2, 3])
queue.print()
print("向队列插入元素")
queue.enqueue(4)
queue.print()
print("从队列中删除元素")
queue.dequeue()
queue.print()
print("判断队列是否为空")
print(queue.is_empty())
print("返回队列中项的个数")
print(queue.size())
queue.print()
print("清空队列")
print(queue.clear())
