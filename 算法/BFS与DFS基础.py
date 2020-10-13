__doc__ = '网上常用的python实现示例'


# 图算法 -- 深度优先搜搜 -- DFS -- 栈（先进后出）
# 1.利用栈实现
# 2.从源节点开始把节点按照深度放入栈，然后弹出
# 3.每弹出一个点，把该节点下一个没有进过栈的邻接点放入栈
# 4.直到栈变空
def DFS(graph, start):
    stack = [start]
    visited = set()
    step = 0  # 记录扩散的步数
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            for w in graph[vertex]:
                if w not in visited:
                    stack.append(w)
                    step += 1
            print(vertex)
    print(step)


# 图算法 -- 广度优先搜搜 -- BFS -- 队列（先进先出）
# 1.利用队列实现
# 2.从源节点开始依次按照宽度进队列，然后弹出
# 3.每弹出一个节点，就把该节点所有没有进过队列的邻接点放入队列
# 4.直到队列变空
def BFS(graph, start):
    queue = []  # 核心数据结构,模拟队列
    queue.append(start)  # 将起点加入队列
    visited = set()  # 避免走回头路
    visited.add(start)
    step = 0  # 记录扩散的步数
    while len(queue) > 0:
        vertex = queue.pop(0)
        nodes = graph[vertex]
        for w in nodes:
            if w not in visited:
                queue.append(w)
                visited.add(w)
                step += 1
        print(vertex)
    print(step)


graph = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D", "E"],
    "D": ["B", "C", "E", "F"],
    "E": ["C", "D"],
    "F": ["D"]
}
print("-----DFS-----")
DFS(graph, "A")
print("-----BFS-----")
BFS(graph, "A")
